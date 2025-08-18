# downloader.py
import yt_dlp
import re
import os


def formatar_tamanho(b):
    """Função auxiliar para mostrar o tamanho do arquivo de forma legível (KB, MB, GB)."""
    if b is None: return "N/A"
    if b < 1024 ** 2: return f"{b / 1024:.2f} KB"
    if b < 1024 ** 3: return f"{b / 1024 ** 2:.2f} MB"
    return f"{b / 1024 ** 3:.2f} GB"


def obter_formatos(url):
    """
    Pega uma URL do YouTube, extrai as informações e retorna o título e uma lista de formatos.
    """
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'youtube-cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = info.get('title', 'Sem Título')

        formatos_disponiveis = []
        for f in info.get('formats', []):
            if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                # Determina qual codec exibir: vídeo se houver, senão áudio.
                vcodec = f.get('vcodec')
                acodec = f.get('acodec')
                codec_info = 'N/A'
                if vcodec and vcodec != 'none':
                    codec_info = vcodec.split('.')[0]  # Limpa o nome do codec (ex: avc1.4d401e -> avc1)
                elif acodec and acodec != 'none':
                    codec_info = acodec.split('.')[0]

                formatos_disponiveis.append({
                    'id': f.get('format_id'),
                    'ext': f.get('ext'),
                    'resolucao': f.get('resolution', 'Áudio'),
                    'tamanho': formatar_tamanho(f.get('filesize') or f.get('filesize_approx')),
                    'codec': codec_info  # Adiciona a informação do codec
                })
        return titulo, formatos_disponiveis


def iniciar_download(url, formato_selecionado, pasta_downloads='downloads', is_audio_only=False):
    """
    Inicia o download de uma URL com um formato específico, com opção para extrair apenas o áudio.
    """
    # Garante que a pasta de downloads exista
    if not os.path.exists(pasta_downloads):
        os.makedirs(pasta_downloads)

    ydl_opts = {
        'format': formato_selecionado,
        'noplaylist': True,
        'cookiefile': 'youtube-cookies.txt',
        'outtmpl': os.path.join(pasta_downloads, '%(title)s.%(ext)s'),
    }

    if is_audio_only:
        # Usa postprocessors para extrair e converter o áudio para MP3
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Qualidade padrão de 192kbps
        }]
    else:
        # Para vídeo, garante que o arquivo final seja MP4
        ydl_opts['merge_output_format'] = 'mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
