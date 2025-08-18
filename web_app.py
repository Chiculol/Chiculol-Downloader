# web_app.py (versão com filtros de codec para compatibilidade)
from flask import Flask, render_template, request
from downloader import obter_formatos, iniciar_download

app = Flask(__name__)


@app.route('/')
def pagina_inicial():
    return render_template('index.html')


@app.route('/analisar', methods=['POST'])
def analisar_url():
    url = request.form['url']
    try:
        video_titulo, formatos = obter_formatos(url)
        return render_template('analise.html',
                               video_titulo=video_titulo,
                               formatos=formatos,
                               url_original=url)
    except Exception as e:
        return f"<h1>Ocorreu um erro ao analisar o link.</h1><p>Erro: {e}</p><a href='/'>Tentar novamente</a>"


@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    formato_yt_dlp = ''
    is_audio_only = False

    # Verifica qual botão ou campo foi enviado
    if 'qualidade' in request.form:
        # Botões de VÍDEO + ÁUDIO com filtro de codec para máxima compatibilidade
        qualidade = request.form['qualidade']
        if qualidade == 'baixa':
            # Melhor vídeo MP4 (codec AVC) + melhor áudio M4A (codec AAC) até 480p
            formato_yt_dlp = 'bestvideo[height<=480][ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]'
        elif qualidade == 'media':
            # Melhor vídeo MP4 (codec AVC) + melhor áudio M4A (codec AAC) até 720p
            formato_yt_dlp = 'bestvideo[height<=720][ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]'
        elif qualidade == 'alta':
            # Melhor vídeo MP4 (codec AVC) + melhor áudio M4A (codec AAC) até 1080p
            formato_yt_dlp = 'bestvideo[height<=1080][ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]'
        elif qualidade == 'extrema':
            # Melhor vídeo MP4 + melhor áudio M4A. Prioriza o container MP4 que geralmente tem codecs compatíveis.
            formato_yt_dlp = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    elif 'qualidade_audio' in request.form:
        # Botões de APENAS ÁUDIO
        is_audio_only = True
        qualidade = request.form['qualidade_audio']
        if qualidade == 'baixa':
            formato_yt_dlp = 'worstaudio'
        elif qualidade == 'media':
            formato_yt_dlp = 'bestaudio[abr<=128]'
        elif qualidade == 'alta':
            formato_yt_dlp = 'bestaudio/best'

    elif request.form.get('format_id'):
        # Campo de ID customizado
        formato_yt_dlp = request.form['format_id'].strip()

    if not formato_yt_dlp:
        return "<h1>Erro: Nenhuma opção de qualidade foi selecionada.</h1><a href='/'>Voltar</a>"

    try:
        iniciar_download(url, formato_yt_dlp, is_audio_only=is_audio_only)
        return render_template('download_completo.html')
    except Exception as e:
        return f"<h1>Ocorreu um erro durante o download.</h1><p>Erro: {e}</p><a href='/'>Tentar novamente</a>"


if __name__ == '__main__':
    app.run(debug=True)
