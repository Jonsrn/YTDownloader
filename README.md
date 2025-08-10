# Music Downloader v2.0 🎵

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt-5-green?style=for-the-badge&logo=qt)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

Uma aplicação de desktop moderna e intuitiva para baixar vídeos do YouTube, convertê-los para MP3 e gerenciar sua biblioteca de músicas, tudo em um só lugar.

---

## 🚀 Sobre o Projeto

Sabe quando você só quer baixar umas músicas para ouvir offline, sem complicação? Foi com essa ideia que o Music Downloader nasceu. O que começou como um projeto pessoal para resolver uma necessidade simples, evoluiu para uma ferramenta completa, com uma interface que dá gosto de usar.

O objetivo é simples: colar o link, baixar, converter e ouvir. Sem abas de navegador, sem anúncios, sem distrações. Apenas você e suas músicas.

### ✨ Principais Funcionalidades

* **Download Simples:** Cole uma ou várias URLs do YouTube e baixe os vídeos em alta resolução.
* **Conversão para MP3:** Converta automaticamente os vídeos baixados para o formato MP3, limpando os arquivos de vídeo para economizar espaço.
* **Player Integrado:** Um player de música completo para você ouvir sua biblioteca. Com controles de play/pause, avançar, retroceder e uma barra de progresso interativa.
* **Interface Moderna:** Um design escuro, limpo e organizado em abas para uma experiência de uso agradável.

---

## 🌱 A Evolução: Da v1.0 para a v2.0

Este projeto passou por uma transformação completa. A versão 1.0 era funcional, mas... digamos que ela tinha um charme dos anos 2010. A v2.0 é uma reconstrução total, focada na experiência do usuário.

### **Versão 1.0 - O Início *

A primeira versão fazia o trabalho, mas a interface era uma lista única de botões e barras de progresso. Era um pouco confusa e visualmente datada.

<img width="603" height="650" alt="Captura de tela 2025-08-10 041423" src="https://github.com/user-attachments/assets/6a76a8c3-1ccc-4569-adc1-898be2df2437" />


### **Versão 2.0 - Uma Reforma Completa ✨**

A nova versão foi repensada do zero, com uma abordagem totalmente diferente:

* **UI/UX Moderna:** A interface agora é escura, elegante e organizada em duas abas principais: **Downloader** e **Player**. Tudo o que você precisa está a um clique de distância, de forma intuitiva.
* **Ícones e Clareza Visual:** Todos os botões agora têm ícones, tornando as ações instantaneamente reconhecíveis. O uso de cores e espaçamento foi aprimorado para não cansar a vista.
* **Player Robusto:** O player de música deixou de ser básico e agora conta com uma playlist, botões de "próximo/anterior" e uma barra de progresso que você pode arrastar para avançar ou retroceder na música.
* **Feedback ao Usuário:** As mensagens de status são mais claras e o fluxo de trabalho (baixar -> converter -> ouvir) é muito mais natural.

<img width="848" height="581" alt="image" src="https://github.com/user-attachments/assets/3c4fc72e-b227-477a-83ec-acfb4b28eaee" />

<img width="698" height="582" alt="image" src="https://github.com/user-attachments/assets/e25a9287-0f52-42b9-9d53-b9dd805aa722" />

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias:

* **Python:** A linguagem principal por trás de toda a lógica.
* **PyQt5:** Para a construção da interface gráfica de desktop.
* **Pytubefix:** A biblioteca que lida com os downloads do YouTube.
* **MoviePy:** Utilizada para a conversão de MP4 para MP3.
* **Pygame:** Para a funcionalidade do player de áudio.
* **Qtawesome:** Para os ícones incríveis que dão vida à interface.

---

## ⚙️ Instalação e Uso

Para rodar este projeto localmente, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv .venv
    # No Windows
    .venv\Scripts\activate
    # No macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    (Crie um arquivo `requirements.txt` com o conteúdo abaixo e rode o comando)
    ```bash
    pip install -r requirements.txt
    ```

    **Conteúdo para `requirements.txt`:**
    ```
    PyQt5
    pytubefix
    moviepy
    pygame
    qtawesome
    ```

4.  **Execute a aplicação:**
    ```bash
    python seu_arquivo_principal.py
    ```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---


