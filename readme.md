# 🎬 **Chiculol-Downloader V2 (Versão Web)**

Este é um aplicativo **web** desenvolvido em **Python (Flask)**.  
Ele fornece uma interface gráfica amigável no navegador para baixar vídeos e áudios do YouTube, oferecendo tanto opções de **download rápido** com qualidades pré-definidas quanto **opções avançadas** para usuários que necessitam de formatos específicos.

---

## 🚀 **Funcionalidades**
- **Interface Web Intuitiva**: Uma interface limpa e moderna com design de *Glassmorphism*.
- **Download por Presets**: Botões de um clique para baixar vídeos em:
  - 📺 Baixa (480p)  
  - 📺 Média (720p)  
  - 📺 Alta (1080p)  
  - 📺 Extrema (1440p / 4K)  
- **Extração de Áudio**: Conversão para MP3 em diferentes qualidades.
- **Controle Avançado**: Lista completa de formatos disponíveis + opção de download via **ID específico**.
- **Organização Automática**: Downloads salvos na pasta `downloads` dentro do projeto.
- **Amplo Suporte a Sites**: Compatível com **centenas de sites além do YouTube**, graças ao motor [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

---

## 🛠️ **Pré-requisitos**
Antes de executar este projeto, certifique-se de que tem os seguintes softwares instalados:

- **Python** → versão 3.9 ou superior (recomendado)  
- **FFmpeg** → usado para juntar (*mux*) arquivos de vídeo e áudio, além de conversão de áudio para MP3.  

📥 **Download FFmpeg**: [FFmpeg Official Builds](https://ffmpeg.org/download.html)  
⚠️ É **crucial** que o `ffmpeg` esteja no **PATH do sistema**.
