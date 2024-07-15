import sys
import threading
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QProgressBar, QLineEdit, QLabel, QListWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
import pygame

class DownloadThread(QThread):
    progresso = pyqtSignal(int)
    status_message = pyqtSignal(str)

    def __init__(self, urls, output_path, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.urls = urls
        self.output_path = output_path

    def run(self):
        total = len(self.urls)
        for i, url in enumerate(self.urls):
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            self.status_message.emit(f"Baixando: {yt.title}")
            video.download(self.output_path)
            self.progresso.emit(int((i + 1) / total * 100))
        self.status_message.emit("Download Concluído")
        time.sleep(2)  # Espera 2 segundos com a barra cheia
        self.progresso.emit(0)  # Reseta a barra de progresso

class ConverterThread(QThread):
    progresso = pyqtSignal(int)
    status_message = pyqtSignal(str)

    def __init__(self, input_path, output_path, parent=None):
        super(ConverterThread, self).__init__(parent)
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        videos = [f for f in os.listdir(self.input_path) if f.endswith('.mp4')]
        total = len(videos)
        for i, video in enumerate(videos):
            video_path = os.path.join(self.input_path, video)
            audio_path = os.path.join(self.output_path, os.path.splitext(video)[0] + '.mp3')
            self.status_message.emit(f"Convertendo: {video}")
            audio_clip = AudioFileClip(video_path)
            audio_clip.write_audiofile(audio_path)
            os.remove(video_path)
            self.progresso.emit(int((i + 1) / total * 100))
        self.status_message.emit("Conversão Concluída")
        time.sleep(2)  # Espera 2 segundos com a barra cheia
        self.progresso.emit(0)  # Reseta a barra de progresso

class Player(QThread):
    progress_update = pyqtSignal(int)
    status_message = pyqtSignal(str)

    def __init__(self, audio_path):
        super(Player, self).__init__()
        self.audio_path = audio_path
        pygame.mixer.init()
        self.current_file = None
        self.total_length = 0

    def play_audio(self, audio_file):
        audio_path = os.path.join(self.audio_path, audio_file)
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        self.current_file = audio_file
        self.total_length = AudioFileClip(audio_path).duration
        self.status_message.emit(f"Tocando: {audio_file}")
        self.start()

    def pause_audio(self):
        pygame.mixer.music.pause()
        self.status_message.emit("Pausado")

    def unpause_audio(self):
        pygame.mixer.music.unpause()
        self.status_message.emit("Continuando")

    def run(self):
        while pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() // 1000
            self.progress_update.emit(int((pos / self.total_length) * 100))
            time.sleep(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciador de Downloads')
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        self.download_thread = None
        self.converter_thread = None
        self.player = None

        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Insira a URL do vídeo...')
        layout.addWidget(self.url_input)

        self.add_url_button = QPushButton('Adicionar URL', self)
        self.add_url_button.clicked.connect(self.add_url)
        layout.addWidget(self.add_url_button)

        self.url_list = QListWidget(self)
        layout.addWidget(self.url_list)

        self.download_button = QPushButton('Baixar Vídeos', self)
        self.download_button.clicked.connect(self.download_videos)
        layout.addWidget(self.download_button)

        self.download_progress = QProgressBar(self)
        layout.addWidget(self.download_progress)

        self.download_status = QLabel(self)
        layout.addWidget(self.download_status)

        self.convert_button = QPushButton('Converter para MP3', self)
        self.convert_button.clicked.connect(self.convert_videos)
        layout.addWidget(self.convert_button)

        self.convert_progress = QProgressBar(self)
        layout.addWidget(self.convert_progress)

        self.convert_status = QLabel(self)
        layout.addWidget(self.convert_status)

        self.audio_list = QListWidget(self)
        layout.addWidget(self.audio_list)

        self.play_button = QPushButton('Reproduzir', self)
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton('Pausar', self)
        self.pause_button.clicked.connect(self.pause_audio)
        layout.addWidget(self.pause_button)

        self.unpause_button = QPushButton('Continuar', self)
        self.unpause_button.clicked.connect(self.unpause_audio)
        layout.addWidget(self.unpause_button)

        self.play_progress = QProgressBar(self)
        self.play_progress.setStyleSheet("QProgressBar { text-align: center; } QProgressBar::chunk { background-color: #05B8CC; }")
        layout.addWidget(self.play_progress)

        self.play_status = QLabel(self)
        layout.addWidget(self.play_status)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.init_directories()
        self.load_audio_files()

    def init_directories(self):
        projeto_path = os.path.dirname(os.path.abspath(__file__))
        self.saida_path = os.path.join(projeto_path, "saida")
        self.video_path = os.path.join(self.saida_path, "Vídeo")
        self.audio_path = os.path.join(self.saida_path, "Áudio")

        os.makedirs(self.video_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)

    def add_url(self):
        url = self.url_input.text()
        if url:
            self.url_list.addItem(url)
            self.url_input.clear()

    def download_videos(self):
        urls = [self.url_list.item(i).text() for i in range(self.url_list.count())]
        if urls:
            self.download_thread = DownloadThread(urls, self.video_path)
            self.download_thread.progresso.connect(self.update_download_progress)
            self.download_thread.status_message.connect(self.update_download_status)
            self.download_thread.finished.connect(self.clear_url_list)
            self.download_thread.start()

    def clear_url_list(self):
        self.url_list.clear()

    def update_download_progress(self, value):
        self.download_progress.setValue(value)

    def update_download_status(self, message):
        self.download_status.setText(message)
        if message == "Download Concluído":
            self.load_audio_files()

    def convert_videos(self):
        self.converter_thread = ConverterThread(self.video_path, self.audio_path)
        self.converter_thread.progresso.connect(self.update_convert_progress)
        self.converter_thread.status_message.connect(self.update_convert_status)
        self.converter_thread.start()

    def update_convert_progress(self, value):
        self.convert_progress.setValue(value)

    def update_convert_status(self, message):
        self.convert_status.setText(message)
        if message == "Conversão Concluída":
            self.load_audio_files()

    def load_audio_files(self):
        if self.audio_path:
            self.audio_list.clear()
            audios = [f for f in os.listdir(self.audio_path) if f.endswith('.mp3')]
            for audio in audios:
                self.audio_list.addItem(audio)
            self.player = Player(self.audio_path)
            self.player.progress_update.connect(self.update_play_progress)
            self.player.status_message.connect(self.update_play_status)

    def play_audio(self):
        if self.audio_list.currentItem():
            audio_file = self.audio_list.currentItem().text()
            self.player.play_audio(audio_file)

    def pause_audio(self):
        if self.player:
            self.player.pause_audio()

    def unpause_audio(self):
        if self.player:
            self.player.unpause_audio()

    def update_play_progress(self, value):
        self.play_progress.setValue(value)

    def update_play_status(self, message):
        self.play_status.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
