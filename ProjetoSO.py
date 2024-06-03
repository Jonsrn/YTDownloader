from pytube import YouTube
import os
import threading
import time

def baixar_video(url, pasta_saida):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(pasta_saida)
    print(f"Download do vídeo '{yt.title}' completo!")

def baixar_videos(urls, pasta_saida):
    metade = len(urls) // 2
    threads = []

    for url in urls[:metade]:
        thread = threading.Thread(target=baixar_video, args=(url, pasta_saida))
        threads.append(thread)
        thread.start()

    for url in urls[metade:]:
        thread = threading.Thread(target=baixar_video, args=(url, pasta_saida))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def baixando_videos():
    print("Bem-vindo ao assistente de download de vídeos")
    num_videos = int(input("Quantos vídeos você deseja baixar? "))
    urls = []

    for i in range(num_videos):
        url = input(f"Insira o URL do vídeo {i+1}: ")
        urls.append(url)

    projeto_path = os.path.dirname(os.path.abspath(__file__))
    saida_path = os.path.join(projeto_path, "saida")
    if not os.path.exists(saida_path):
        os.makedirs(saida_path)

    video_path = os.path.join(saida_path, "Vídeo")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    baixar_videos(urls, video_path)
    print("Todos os downloads foram concluídos!")

def baixar_musica(url, pasta_saida):
    yt = YouTube(url)
    musica = yt.streams.filter(only_audio=True).first()
    musica.download(pasta_saida)
    print(f"Download da música '{yt.title}' completo!")

def baixar_musicas():
    print("Bem-vindo ao assistente de download de músicas")
    num_musicas = int(input("Quantas músicas você deseja baixar? "))
    urls = []

    for i in range(num_musicas):
        url = input(f"Insira o URL da música {i+1}: ")
        urls.append(url)

    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_musica = os.path.join(pasta_atual, "saida", "Música")

    if not os.path.exists(pasta_musica):
        os.makedirs(pasta_musica)

    metade = len(urls) // 2
    threads = []

    for url in urls[:metade]:
        thread = threading.Thread(target=baixar_musica, args=(url, pasta_musica))
        threads.append(thread)
        thread.start()

    for url in urls[metade:]:
        thread = threading.Thread(target=baixar_musica, args=(url, pasta_musica))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


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
    print("Os outros")
    print("============================")

def subMenu():
    print("\n=============MENU===========")
    print("Selecione a categoria que deseja trabalhar")
    print("[1] Vídeo")
    print("[2] Audio")
    print("[3] Imagem")
    print("[0] Retornar ao Menu Principal")
    print("============================")

def menuVideo():
    print("\n=============VÍDEO===========")
    print("Selecione a operação que deseja realizar")
    print("[1] Baixar Vídeo do Youtube")
    print("[2] Conversão de Formato")
    print("[3] Renderizar Vídeo")
    print("[0] Retornar ao Menu Anterior")
    print("============================")

def menuAudio():
    print("\n=============AUDIO===========")
    print("Selecione a operação que deseja realizar")
    print("[1] Baixar Audio do Youtube")
    print("[2] Montar uma playlist")
    print("[3] Reproduzir Música")
    print("[0] Retornar ao Menu Anterior")
    print("============================")

def menuImagem():
    print("\n=============IMAGEM===========")
    print("Selecione a operação que deseja realizar")
    print("[1] Baixar Imagem Especifica do Google")
    print("[2] Procurar e Baixar Imagem")
    print("[3] Converter Formato de Imagem")
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
                              #Baixar video do yt
                              baixando_videos()
                              print("")
                           if (escolha2 == 2):
                              #Conversão de formato
                              print("")
                           if (escolha2 == 3):
                              #renderizar video
                              print("")
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
                               #Baixar Audio do Youtube
                               baixar_musicas()
                               print("")
                            if (escolha3 == 2):
                               #Montar Playlist
                               print("")
                            if (escolha3 == 3):
                               #Reproduzir Música
                               print("")
                            if (escolha3 == 0):
                                print("Retornando...")
                                break
                         except:
                             print("Entrada inválida, tente novamente")

                 if (escolha1 == 3):
                     while True:
                         try:
                             menuImagem()
                             escolha4 = int(input("Sua escolha: "))

                             if(escolha4 == 1):
                                 #baixar imagem especifica do google
                                 print("")
                             if (escolha4 == 2):
                                 #pesquisar imagem por tag
                                 print("")
                             if (escolha4 == 3):
                                 #Converter formato de Imagem
                                 print("")
                             if (escolha4 == 0):
                                 print("Retornando...")
                                 break
                         except:
                             print("Entrada inválida, tente novamente")

                 if (escolha1 == 0):
                     print("Retornando ao Menu Principal")
                     break
               except:
                   print("Entrada inválida, tente novamente")
       if (escolha == 2):
           Sobre()
           time.sleep(3)
       if (escolha == 0):
           print("Encerrando Programa")
           break;

    except:
        print("Entrada inválida, tente novamente")
