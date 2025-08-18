import yt_dlp
import re

def formatar_tamanho(b):
    """Função auxiliar para mostrar o tamanho do arquivo de forma legível (KB, MB, GB)."""
    if b is None:
        return "N/A"
    if b < 1024**2:
        return f"{b/1024:.2f} KB"
    if b < 1024**3:
        return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

print("--- Bem-vindo ao baixador de vídeos do Chiculol ^^ (Versão de Linha de Comando) ---")
link_do_video = input("Por favor, cole o link do vídeo: ")

titulo_limpo = 'video_baixado'

try:
    # Opção para ignorar playlists e usar cookies se necessário
    ydl_opts_info = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'youtube-cookies.txt' # Tenta usar cookies se o arquivo existir
    }
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(link_do_video, download=False)
        titulo = info.get('title', 'video_sem_titulo')
        titulo_limpo = re.sub(r'[\\/*?:"<>|]', "", titulo)

        print(f"\nAnalisando o vídeo: '{titulo}'")
        print("\n--- Formatos de vídeo e áudio disponíveis ---")

        for f in info.get('formats', []):
            if f.get('vcodec') != 'none' or f.get('acodec') != 'none':
                resolucao = f.get('resolution', 'Áudio')
                extensao = f.get('ext')
                tamanho = formatar_tamanho(f.get('filesize') or f.get('filesize_approx'))
                print(f"ID: {f['format_id']:<5} | Ext: {extensao:<5} | Resolução: {resolucao:<15} | Tamanho: ~{tamanho:<10}")

except Exception as e:
    print(f"\nOps! Não foi possível obter os detalhes do vídeo. Erro: {e}")
    exit()

print("\n--- Como Escolher ---")
print("1. Para a melhor qualidade, escolha um ID de vídeo e um ID de áudio (ex: 137+140).")
print("2. Para um arquivo único com vídeo e áudio (qualidade até 720p), digite um ID (ex: 22).")
print("3. Para apenas o áudio, escolha um ID que tenha 'Áudio' na resolução.")
print("4. Para deixar o programa escolher a melhor qualidade, apenas pressione ENTER.")

escolha = input("\nDigite o(s) ID(s) desejado(s): ").strip()

if not escolha:
    print("\nNenhuma seleção feita. Baixando a melhor qualidade padrão...")
    formato_selecionado = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
else:
    print(f"\nVocê escolheu o formato: {escolha}")
    formato_selecionado = escolha

ydl_opts_download = {
    'format': formato_selecionado,
    'outtmpl': f'{titulo_limpo}.%(ext)s',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'cookiefile': 'youtube-cookies.txt'
}

try:
    print("\nIniciando o download... Isso pode demorar.")
    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([link_do_video])
    print("\n--- Download concluído com sucesso! ---")
    print(f"O arquivo foi salvo na pasta do projeto.")

except Exception as e:
    print(f"\nOps! Ocorreu um erro durante o download: {e}")
    print("Verifique se os IDs estão corretos e se o FFmpeg está instalado.")