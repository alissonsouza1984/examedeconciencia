from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def baixar_mp3(link):
    try:
        yt = YouTube(link)
        print(f"Baixando: {yt.title}")

        audio_stream = yt.streams.filter(only_audio=True).first()
        arquivo_temp = audio_stream.download(filename="temp_audio.mp4")

        nome_arquivo_mp3 = yt.title.replace(" ", "_").replace("/", "_") + ".mp3"
        clip = AudioFileClip(arquivo_temp)
        clip.write_audiofile(nome_arquivo_mp3)

        clip.close()
        os.remove(arquivo_temp)

        print(f"Download completo: {nome_arquivo_mp3}")
    except Exception as e:
        print(f"Erro ao baixar: {e}")

# 🟢 Pergunta o link
if __name__ == "__main__":
    link = input("Cole o link do vídeo do YouTube: ").strip()
    baixar_mp3(link)
