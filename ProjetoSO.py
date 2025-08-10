import sys
import threading
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QProgressBar, QLineEdit, QLabel, QListWidget, 
                             QMessageBox, QHBoxLayout, QTabWidget, QSlider,
                             QStyleFactory)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
import pygame
import qtawesome as qta # Importa a biblioteca de ícones

# --- Threads (Lógica de Backend - Sem alteração) ---

class DownloadThread(QThread):
    progresso = pyqtSignal(int)
    status_message = pyqtSignal(str)
    download_completo = pyqtSignal()

    def __init__(self, urls, output_path, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.urls = urls
        self.output_path = output_path
        self.is_running = True

    def run(self):
        total = len(self.urls)
        for i, url in enumerate(self.urls):
            if not self.is_running:
                break
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()
                self.status_message.emit(f"Baixando: {yt.title[:40]}...")
                video.download(self.output_path)
                self.progresso.emit(int((i + 1) / total * 100))
            except Exception as e:
                self.status_message.emit(f"Erro ao baixar {url}: {e}")
        
        if self.is_running:
            self.status_message.emit("Download Concluído")
            self.download_completo.emit()
            time.sleep(2)
        
        self.progresso.emit(0)
        self.status_message.emit("Pronto")

    def stop(self):
        self.is_running = False

class ConverterThread(QThread):
    progresso = pyqtSignal(int)
    status_message = pyqtSignal(str)
    conversao_completa = pyqtSignal()

    def __init__(self, input_path, output_path, parent=None):
        super(ConverterThread, self).__init__(parent)
        self.input_path = input_path
        self.output_path = output_path
        self.is_running = True

    def run(self):
        videos = [f for f in os.listdir(self.input_path) if f.endswith('.mp4')]
        total = len(videos)
        if total == 0:
            self.status_message.emit("Nenhum vídeo para converter.")
            self.progresso.emit(0)
            return

        for i, video in enumerate(videos):
            if not self.is_running:
                break
            video_path = os.path.join(self.input_path, video)
            audio_path = os.path.join(self.output_path, os.path.splitext(video)[0] + '.mp3')
            try:
                self.status_message.emit(f"Convertendo: {video[:40]}...")
                with AudioFileClip(video_path) as audio_clip:
                    audio_clip.write_audiofile(audio_path, logger=None)
                os.remove(video_path)
                self.progresso.emit(int((i + 1) / total * 100))
            except Exception as e:
                self.status_message.emit(f"Erro ao converter {video}: {e}")

        if self.is_running:
            self.status_message.emit("Conversão Concluída")
            self.conversao_completa.emit()
            time.sleep(2)

        self.progresso.emit(0)
        self.status_message.emit("Pronto")

    def stop(self):
        self.is_running = False

class PlayerThread(QThread):
    progress_update = pyqtSignal(int)
    status_message = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, audio_path, parent=None):
        super(PlayerThread, self).__init__(parent)
        self.audio_file_path = audio_path
        self.total_length = 0
        self.is_playing = False
        self.is_paused = False
        self.seek_offset = 0.0 # CORREÇÃO: Adiciona um offset para o seek
        pygame.mixer.init()

    def play(self):
        try:
            pygame.mixer.music.load(self.audio_file_path)
            sound = pygame.mixer.Sound(self.audio_file_path)
            self.total_length = sound.get_length()
            self.seek_offset = 0.0 # CORREÇÃO: Reseta o offset para a nova música
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.start()
        except pygame.error as e:
            self.status_message.emit(f"Erro ao tocar: {e}")

    def run(self):
        while self.is_playing:
            if pygame.mixer.music.get_busy():
                # CORREÇÃO: Calcula a posição real somando o tempo de reprodução atual com o offset do seek
                pos_since_play = pygame.mixer.music.get_pos() / 1000.0
                current_pos = self.seek_offset + pos_since_play
                if self.total_length > 0:
                    progress = int((current_pos / self.total_length) * 100)
                    self.progress_update.emit(min(progress, 100))
            elif not self.is_paused:
                self.is_playing = False
                self.progress_update.emit(100)
                self.finished.emit()
            
            time.sleep(0.2)

    def toggle_pause(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.status_message.emit(f"Tocando: {os.path.basename(self.audio_file_path)}")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.status_message.emit("Pausado")

    def set_position(self, percentage):
        if self.is_playing and self.total_length > 0:
            # CORREÇÃO: Usa stop() e play(start=...) para um seek mais confiável
            target_seconds = (percentage / 100.0) * self.total_length
            self.seek_offset = target_seconds
            
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=self.seek_offset)
            
            if self.is_paused:
                pygame.mixer.music.pause()

    def stop(self):
        self.is_playing = False
        pygame.mixer.music.stop()
        self.progress_update.emit(0)


# --- Interface Gráfica (Totalmente Reformulada) ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Downloader')
        self.setGeometry(100, 100, 700, 550)
        
        # Threads e flags
        self.download_thread = None
        self.converter_thread = None
        self.player_thread = None
        self.is_paused = False
        self.is_seeking = False # Flag para controlar o arraste do slider

        self.init_directories()
        self.initUI()
        self.load_audio_files()

    def initUI(self):
        # Estilo da aplicação (QSS)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QMainWindow {
                border: 1px solid #34495e;
            }
            QTabWidget::pane {
                border-top: 2px solid #34495e;
            }
            QTabBar::tab {
                background: #34495e;
                color: #ecf0f1;
                padding: 10px;
                border: 1px solid #2c3e50;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #46627f;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #4a6987;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
            QLineEdit {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                padding: 8px;
                border-radius: 5px;
                color: #ecf0f1;
            }
            QListWidget {
                background-color: #34495e;
                alternate-background-color: #31445a;
                border: 1px solid #2c3e50;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QProgressBar {
                border: 1px solid #34495e;
                border-radius: 5px;
                text-align: center;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                border-radius: 4px;
            }
            QLabel {
                color: #bdc3c7;
            }
            QSlider::groove:horizontal {
                border: 1px solid #34495e;
                height: 4px;
                background: #34495e;
                margin: 2px 0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #3498db;
                width: 14px;
                margin: -6px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #27ae60;
                border: 1px solid #34495e;
                height: 4px;
                border-radius: 2px;
            }
        """)

        # Abas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Criar abas
        self.create_downloader_tab()
        self.create_player_tab()

    def create_downloader_tab(self):
        downloader_widget = QWidget()
        main_layout = QVBoxLayout(downloader_widget)

        # Seção de URL
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit(placeholderText='Insira a URL do vídeo do YouTube...')
        url_layout.addWidget(self.url_input)
        self.add_url_button = QPushButton(qta.icon('fa5s.plus', color='white'), ' Adicionar')
        self.add_url_button.clicked.connect(self.add_url)
        url_layout.addWidget(self.add_url_button)
        main_layout.addLayout(url_layout)

        # Lista de URLs
        self.url_list = QListWidget()
        self.url_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.url_list)

        # Seção de Download
        download_layout = QHBoxLayout()
        self.download_button = QPushButton(qta.icon('fa5s.download', color='white'), ' Baixar Vídeos')
        self.download_button.clicked.connect(self.download_videos)
        download_layout.addWidget(self.download_button)
        self.download_progress = QProgressBar()
        download_layout.addWidget(self.download_progress)
        main_layout.addLayout(download_layout)
        self.download_status = QLabel("Pronto para baixar.")
        main_layout.addWidget(self.download_status)

        # Seção de Conversão
        convert_layout = QHBoxLayout()
        self.convert_button = QPushButton(qta.icon('fa5s.cogs', color='white'), ' Converter para MP3')
        self.convert_button.clicked.connect(self.convert_videos)
        convert_layout.addWidget(self.convert_button)
        self.convert_progress = QProgressBar()
        convert_layout.addWidget(self.convert_progress)
        main_layout.addLayout(convert_layout)
        self.convert_status = QLabel("Pronto para converter.")
        main_layout.addWidget(self.convert_status)
        
        self.tabs.addTab(downloader_widget, qta.icon('fa5s.cloud-download-alt'), "Downloader")
        
    def create_player_tab(self):
        player_widget = QWidget()
        main_layout = QVBoxLayout(player_widget)
        
        # Lista de Músicas
        self.audio_list = QListWidget()
        self.audio_list.setAlternatingRowColors(True)
        self.audio_list.itemDoubleClicked.connect(self.play_selected_audio)
        main_layout.addWidget(self.audio_list)
        
        # Status da Música
        self.play_status = QLabel("Selecione uma música para tocar.")
        self.play_status.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.play_status)
        
        # Slider de Progresso
        self.play_slider = QSlider(Qt.Horizontal)
        self.play_slider.setEnabled(False) 
        self.play_slider.sliderPressed.connect(self.on_slider_pressed)
        self.play_slider.sliderReleased.connect(self.on_slider_released)
        main_layout.addWidget(self.play_slider)
        
        # Controles do Player
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()

        self.previous_button = QPushButton(qta.icon('fa5s.step-backward', color='white'), '')
        self.previous_button.setFixedSize(50, 50)
        self.previous_button.clicked.connect(self.play_previous)
        controls_layout.addWidget(self.previous_button)

        self.play_pause_button = QPushButton(qta.icon('fa5s.play', color='white'), '')
        self.play_pause_button.setFixedSize(60, 60)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        controls_layout.addWidget(self.play_pause_button)

        self.next_button = QPushButton(qta.icon('fa5s.step-forward', color='white'), '')
        self.next_button.setFixedSize(50, 50)
        self.next_button.clicked.connect(self.play_next)
        controls_layout.addWidget(self.next_button)
        
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)
        
        self.tabs.addTab(player_widget, qta.icon('fa5s.music'), "Player")

    def init_directories(self):
        if getattr(sys, 'frozen', False):
            projeto_path = os.path.dirname(sys.executable)
        else:
            projeto_path = os.path.dirname(os.path.abspath(__file__))
        
        self.saida_path = os.path.join(projeto_path, "saida")
        self.video_path = os.path.join(self.saida_path, "Vídeo")
        self.audio_path = os.path.join(self.saida_path, "Áudio")

        os.makedirs(self.video_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)

    # --- Lógica de Funções ---
    def add_url(self):
        url = self.url_input.text()
        if "http" in url:
            self.url_list.addItem(url)
            self.url_input.clear()
        else:
            QMessageBox.warning(self, "URL Inválida", "Por favor, insira uma URL válida.")

    def download_videos(self):
        urls = [self.url_list.item(i).text() for i in range(self.url_list.count())]
        if not urls:
            QMessageBox.information(self, "Nenhuma URL", "Adicione URLs à lista antes de baixar.")
            return
        
        self.download_button.setEnabled(False)
        self.download_thread = DownloadThread(urls, self.video_path)
        self.download_thread.progresso.connect(self.download_progress.setValue)
        self.download_thread.status_message.connect(self.download_status.setText)
        self.download_thread.download_completo.connect(self.on_download_finished)
        self.download_thread.finished.connect(lambda: self.download_button.setEnabled(True))
        self.download_thread.start()

    def on_download_finished(self):
        self.url_list.clear()
        QMessageBox.information(self, "Sucesso", "Download dos vídeos concluído!")

    def convert_videos(self):
        self.convert_button.setEnabled(False)
        self.converter_thread = ConverterThread(self.video_path, self.audio_path)
        self.converter_thread.progresso.connect(self.convert_progress.setValue)
        self.converter_thread.status_message.connect(self.convert_status.setText)
        self.converter_thread.conversao_completa.connect(self.on_conversion_finished)
        self.converter_thread.finished.connect(lambda: self.convert_button.setEnabled(True))
        self.converter_thread.start()

    def on_conversion_finished(self):
        QMessageBox.information(self, "Sucesso", "Conversão para MP3 concluída!")
        self.load_audio_files()
        self.tabs.setCurrentIndex(1)

    def load_audio_files(self):
        self.audio_list.clear()
        if os.path.exists(self.audio_path):
            audios = sorted([f for f in os.listdir(self.audio_path) if f.endswith('.mp3')])
            for audio in audios:
                self.audio_list.addItem(audio)

    def play_selected_audio(self):
        if not self.audio_list.currentItem():
            return
        
        self.stop_audio()
        
        audio_file = self.audio_list.currentItem().text()
        full_path = os.path.join(self.audio_path, audio_file)
        
        self.player_thread = PlayerThread(full_path)
        self.player_thread.progress_update.connect(self.update_play_slider)
        self.player_thread.status_message.connect(self.play_status.setText)
        self.player_thread.finished.connect(self.on_music_finished)
        
        self.play_status.setText(f"Tocando: {audio_file}")
        self.play_pause_button.setIcon(qta.icon('fa5s.pause', color='white'))
        self.is_paused = False
        self.play_slider.setEnabled(True)
        self.player_thread.play()

    def toggle_play_pause(self):
        if not self.player_thread or not self.player_thread.is_playing:
            self.play_selected_audio()
        else:
            self.player_thread.toggle_pause()
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.play_pause_button.setIcon(qta.icon('fa5s.play', color='white'))
            else:
                self.play_pause_button.setIcon(qta.icon('fa5s.pause', color='white'))
    
    def stop_audio(self):
        if self.player_thread:
            self.player_thread.stop()
        self.play_pause_button.setIcon(qta.icon('fa5s.play', color='white'))
        self.play_slider.setValue(0)
        self.play_slider.setEnabled(False)
        self.play_status.setText("Selecione uma música para tocar.")
        self.is_paused = False

    def on_music_finished(self):
        self.play_next()

    def play_next(self):
        if self.audio_list.count() == 0:
            return
        
        current_row = self.audio_list.currentRow()
        next_row = current_row + 1
        if next_row >= self.audio_list.count():
            next_row = 0
        
        self.audio_list.setCurrentRow(next_row)
        self.play_selected_audio()

    def play_previous(self):
        if self.audio_list.count() == 0:
            return

        current_row = self.audio_list.currentRow()
        prev_row = current_row - 1
        if prev_row < 0:
            prev_row = self.audio_list.count() - 1
            
        self.audio_list.setCurrentRow(prev_row)
        self.play_selected_audio()

    def on_slider_pressed(self):
        if self.player_thread and self.player_thread.is_playing:
            self.is_seeking = True

    def on_slider_released(self):
        if self.player_thread and self.player_thread.is_playing and self.is_seeking:
            self.player_thread.set_position(self.play_slider.value())
        self.is_seeking = False

    def update_play_slider(self, value):
        if not self.is_seeking:
            self.play_slider.setValue(value)

    def closeEvent(self, event):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            self.download_thread.wait()
        if self.converter_thread and self.converter_thread.isRunning():
            self.converter_thread.stop()
            self.converter_thread.wait()
        if self.player_thread and self.player_thread.isRunning():
            self.player_thread.stop()
            self.player_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
