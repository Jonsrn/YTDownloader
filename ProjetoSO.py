import threading
import os
from tqdm import tqdm
from pytube import YouTube
import time
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import shutil
from pathlib import Path
import pygame


link_semaphore = threading.Semaphore()


download_semaphore = threading.Semaphore()


alternancia_semaphore = threading.Semaphore(1)  


def baixar_video(url, pasta_saida):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(pasta_saida)
    return 1


def baixar_videos(urls, pasta_saida, total_videos, progress_bar):
    total_baixados = 0
    metade = len(urls) // 2

    for url in urls[:metade]:
        with download_semaphore:
            total_baixados += baixar_video(url, pasta_saida)
            progress_bar.update(1)

    for url in urls[metade:]:

        alternancia_semaphore.acquire()
        with download_semaphore:
            total_baixados += baixar_video(url, pasta_saida)
            progress_bar.update(1)
        alternancia_semaphore.release()


def baixando_videos():
    print("Bem-vindo ao assistente de download de vídeos")
    num_videos = int(input("Quantos vídeos você deseja baixar? "))
    urls = []

    for i in range(num_videos):
        url = input(f"Insira o URL do vídeo {i + 1}: ")
        urls.append(url)

    projeto_path = os.path.dirname(os.path.abspath(__file__))
    saida_path = os.path.join(projeto_path, "saida")
    if not os.path.exists(saida_path):
        os.makedirs(saida_path)

    video_path = os.path.join(saida_path, "Vídeo")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    with link_semaphore:

        with tqdm(total=num_videos, desc="Downloads concluídos", unit="video") as progress_bar:
            baixar_videos(urls, video_path, num_videos, progress_bar)

    print("Todos os downloads foram concluídos!")
    time.sleep(3)


def baixar_musica(url, pasta_saida):
    yt = YouTube(url)
    musica = yt.streams.filter(only_audio=True).first()
    musica.download(pasta_saida)
    return 1


def baixar_musicas(urls, pasta_saida, total_musicas, progress_bar):
    total_baixados = 0
    metade = len(urls) // 2

    for url in urls[:metade]:
        with download_semaphore:
            total_baixados += baixar_musica(url, pasta_saida)
            progress_bar.update(1)

    for url in urls[metade:]:
        alternancia_semaphore.acquire()
        with download_semaphore:
            total_baixados += baixar_musica(url, pasta_saida)
            progress_bar.update(1)
        alternancia_semaphore.release()


def baixando_musicas():
    print("Bem-vindo ao assistente de download de músicas")
    num_musicas = int(input("Quantas músicas você deseja baixar? "))
    urls = []

    for i in range(num_musicas):
        url = input(f"Insira o URL da música {i + 1}: ")
        urls.append(url)

    projeto_path = os.path.dirname(os.path.abspath(__file__))
    saida_path = os.path.join(projeto_path, "saida")
    if not os.path.exists(saida_path):
        os.makedirs(saida_path)

    musica_path = os.path.join(saida_path, "Música")
    if not os.path.exists(musica_path):
        os.makedirs(musica_path)

    with link_semaphore:

        with tqdm(total=num_musicas, desc="Downloads concluídos", unit="música", postfix="") as progress_bar:
            baixar_musicas(urls, musica_path, num_musicas, progress_bar)

    print("Todos os downloads foram concluídos!")

    time.sleep(3)


conversao_semaphore = threading.Semaphore()


def converter_musica(nome_arquivo_mp4, pasta_saida):
    nome_arquivo_mp3 = os.path.splitext(nome_arquivo_mp4)[0] + ".mp3"
    audio_clip = AudioFileClip(nome_arquivo_mp4)
    audio_clip.write_audiofile(nome_arquivo_mp3)

    return nome_arquivo_mp3


def converter_musicas(pasta_entrada, pasta_saida, total_musicas, progress_bar):
    total_convertidos = 0

    for nome_arquivo_mp4 in os.listdir(pasta_entrada):
        if nome_arquivo_mp4.endswith(".mp4"):
            nome_arquivo_mp4 = os.path.join(pasta_entrada, nome_arquivo_mp4)
            conversao_semaphore.acquire()
            nome_arquivo_mp3 = converter_musica(nome_arquivo_mp4, pasta_saida)
            total_convertidos += 1
            progress_bar.update(1)
            conversao_semaphore.release()
            shutil.move(nome_arquivo_mp3, os.path.join(pasta_saida, os.path.basename(nome_arquivo_mp3)))

    return total_convertidos


def converter_musicas_e_reproduzir():
    print("Convertendo e reproduzindo músicas...")
    pasta_entrada = "saida/Música"
    pasta_saida = "saida/Musicas_Convertidas"

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    num_musicas = len([nome_arquivo for nome_arquivo in os.listdir(pasta_entrada) if nome_arquivo.endswith(".mp4")])
    with tqdm(total=num_musicas, desc="Conversões concluídas", unit="música") as progress_bar:
        total_convertidos = converter_musicas(pasta_entrada, pasta_saida, num_musicas, progress_bar)

    print(f"Todas as {total_convertidos} músicas foram convertidas e salvas em '{pasta_saida}'")

    resposta = input("Deseja apagar os arquivos pré-convertidos? (s/n): ").strip().lower()
    if resposta == "s":
        for arquivo in os.listdir(pasta_entrada):
            arquivo_caminho = os.path.join(pasta_entrada, arquivo)
            if arquivo.endswith(".mp4"):
                os.remove(arquivo_caminho)
        print("Arquivos pré-convertidos removidos com sucesso!")


reproducao_semaphore = threading.Semaphore()

def reproduzir_musica(musica_path, progress_bar):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            progress_bar.update(1)
            time.sleep(1)
        pygame.mixer.quit()
    except pygame.error as e:
        print(f"Erro ao reproduzir música: {e}")

def selecionar_musica():
    projeto_path = os.path.dirname(os.path.abspath(__file__))
    musicas_convertidas_path = os.path.join(projeto_path, "saida", "Musicas_Convertidas")

    if not os.path.exists(musicas_convertidas_path):
        print("A pasta de músicas convertidas não existe.")
        return

    musicas = list(Path(musicas_convertidas_path).glob("*.mp3"))

    if not musicas:
        print("Não há músicas convertidas disponíveis.")
        return

    print("Músicas disponíveis para reprodução:")
    for i, musica in enumerate(musicas):
        print(f"{i + 1}. {musica.stem}")

    while True:
        try:
            escolha = int(input("Digite o número da música que deseja reproduzir (0 para sair): "))
            if escolha == 0:
                print("Saindo da reprodução de músicas.")
                return
            elif 0 < escolha <= len(musicas):
                musica_escolhida = musicas[escolha - 1]

                pygame.mixer.init()
                pygame.mixer.music.load(str(musica_escolhida))
                duracao = pygame.mixer.Sound(str(musica_escolhida)).get_length()
                progress_bar = tqdm(total=duracao, desc="Reproduzindo", unit="s", leave=False)

                with reproducao_semaphore:
                    reproduzir_musica(str(musica_escolhida), progress_bar)
                break
            else:
                print("Escolha inválida. Por favor, digite o número correspondente à música desejada.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro correspondente à música desejada.")

def converter_video_para_mp3(nome_arquivo_mp4, pasta_saida):
    try:

        video_clip = VideoFileClip(nome_arquivo_mp4)

        audio_clip = video_clip.audio

        novo_nome_arquivo = os.path.splitext(os.path.basename(nome_arquivo_mp4))[0] + ".mp3"

        novo_caminho_arquivo = os.path.join(pasta_saida, novo_nome_arquivo)
        audio_clip.write_audiofile(novo_caminho_arquivo)
        audio_clip.close()
        video_clip.close()
        return novo_caminho_arquivo
    except Exception as e:
        print(f"Erro ao converter vídeo para MP3: {e}")
        return None

def converter_videos_para_mp3(videos, pasta_saida, progress_bar):
    total_convertidos = 0
    for nome_arquivo_mp4 in videos:
        conversao_semaphore.acquire()
        novo_nome_arquivo = converter_video_para_mp3(nome_arquivo_mp4, pasta_saida)
        if novo_nome_arquivo:
            total_convertidos += 1
            progress_bar.update(1)
        conversao_semaphore.release()
    return total_convertidos

def converter_videos_e_reproduzir():
    print("Convertendo e reproduzindo vídeos...")
    pasta_entrada = "saida/Vídeo"
    pasta_saida = "saida/Musicas_Convertidas"

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)


    videos = [os.path.join(pasta_entrada, nome_arquivo) for nome_arquivo in os.listdir(pasta_entrada) if nome_arquivo.endswith(".mp4")]

    metade = len(videos) // 2
    videos_thread1 = videos[:metade]
    videos_thread2 = videos[metade:]

    num_videos = len(videos)
    with tqdm(total=num_videos, desc="Conversões concluídas", unit="vídeo") as progress_bar:
        thread1 = threading.Thread(target=converter_videos_para_mp3, args=(videos_thread1, pasta_saida, progress_bar))
        thread2 = threading.Thread(target=converter_videos_para_mp3, args=(videos_thread2, pasta_saida, progress_bar))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    print(f"Todos os {num_videos} vídeos foram convertidos para MP3 e salvos em '{pasta_saida}'")

def excluir_video():
    pasta_video = "saida/Vídeo"

    videos = [os.path.join(pasta_video, nome_arquivo) for nome_arquivo in os.listdir(pasta_video) if nome_arquivo.endswith(".mp4")]

    if not videos:
        print("Não há vídeos disponíveis para excluir.")
        time.sleep(2)
        return

    print("Vídeos disponíveis para exclusão:")
    for i, video in enumerate(videos):
        print(f"{i + 1}. {os.path.basename(video)}")

    while True:
        try:
            escolha = int(input("Digite o número do vídeo que deseja excluir (0 para cancelar): "))
            if escolha == 0:
                print("Operação de exclusão cancelada.")
                time.sleep(2)
                return
            elif 0 < escolha <= len(videos):
                video_escolhido = videos[escolha - 1]

                try:
                    os.remove(video_escolhido)
                    print("Vídeo excluído com sucesso!")
                    time.sleep(2)
                except Exception as e:
                    print(f"Não foi possível excluir o arquivo desejado, pois o mesmo está atualmente aberto em outra instância.")
                    time.sleep(3)
                break
            else:
                print("Escolha inválida. Por favor, digite o número correspondente ao vídeo desejado.")
                time.sleep(2)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro correspondente ao vídeo desejado.")
            time.sleep(2)




def menuPrincipal():
    print("\n=============MENU===========")
    print("Bem vindo ao Programa de Download e conversão de vídeos")
    print("[1] Iniciar")
    print("[2] Sobre")
    print("[0] Encerrar Programa")
    print("============================")


def Sobre():
    print("\n=============SOBRE===========")
    print("Trabalho realizado por:")
    print("Jonathan dos Santos")
    print("João Batista")
    print("Matheus Rikelmy")
    print("Henrique dos Santos")
    print("============================")


def subMenu():
    print("\n=============MENU===========")
    print("Selecione a categoria que deseja trabalhar")
    print("[1] Vídeo")
    print("[2] Audio")
    print("[0] Retornar ao Menu Principal")
    print("============================")


def menuVideo():
    print("\n=============VÍDEO===========")
    print("Selecione a operação que deseja realizar")
    print("[1] Baixar Vídeo do Youtube")
    print("[2] Conversão de Formato")
    print("[3] Excluir Vídeo")
    print("[0] Retornar ao Menu Anterior")
    print("============================")


def menuAudio():
    print("\n=============AUDIO===========")
    print("Selecione a operação que deseja realizar")
    print("[1] Baixar Audio do Youtube")
    print("[2] Converter Músicas Baixadas para Reproduzir")
    print("[3] Reproduzir Música")
    print("[0] Retornar ao Menu Anterior")
    print("============================")




while True:
    try:
        menuPrincipal()
        escolha = int(input("Sua Escolha: "))
        if (escolha == 1):
            while True:
                try:
                    subMenu()
                    escolha1 = int(input("Sua escolha: "))
                    if (escolha1 == 1):
                        while True:
                            try:
                                menuVideo()
                                escolha2 = int(input("Sua escolha: "))

                                if (escolha2 == 1):
                                    # Baixar video do yt
                                    baixando_videos()

                                if (escolha2 == 2):
                                    # Conversão de formato
                                    converter_videos_e_reproduzir()

                                if (escolha2 == 3):
                                    #excluir video
                                    excluir_video()
                                if (escolha2 == 0):
                                    print("Retornando...")
                                    break
                            except:
                                print("Entrada inválida, tente novamente")
                    if (escolha1 == 2):
                        while True:
                            try:
                                menuAudio()
                                escolha3 = int(input("Sua escolha: "))

                                if (escolha3 == 1):
                                    # Baixar Audio do Youtube
                                    baixando_musicas()

                                if (escolha3 == 2):
                                    # Converter Músicas Baixadas para Reproduzir
                                    converter_musicas_e_reproduzir()

                                if (escolha3 == 3):
                                    selecionar_musica()

                                if (escolha3 == 0):
                                    print("Retornando...")
                                    break
                            except:
                                print("Entrada inválida, tente novamente")

                    if (escolha1 == 0):
                        print("Retornando ao Menu Principal")
                        break
                except:
                    print("Entrada inválida, tente novamente")
                    time.sleep(2)
        if (escolha == 2):
            Sobre()
            time.sleep(3)
        if (escolha == 0):
            print("Encerrando Programa")
            time.sleep(1)
            break

    except:
        print("Entrada inválida, tente novamente")