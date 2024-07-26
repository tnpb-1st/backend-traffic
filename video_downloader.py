import os
import json
import requests
import threading
from datetime import datetime
from moviepy.editor import VideoFileClip


# Função para obter o timestamp atual
def get_current_timestamp():
    return int(datetime.now().timestamp() * 1e9)


# Função para baixar um vídeo
def download_video(camera_info, group_id, timestamp, download_dir):
    video_url = f"{camera_info['url']}?time={timestamp}"
    video_filename = f"{group_id}_{camera_info['camera']}_{timestamp}.mp4"
    video_path = os.path.join(download_dir, video_filename)

    response = requests.get(video_url)

    if response.status_code == 200:
        with open(video_path, "wb") as video_file:
            video_file.write(response.content)
        return video_path
    else:
        print(f"Erro ao baixar vídeo de {camera_info['name']}")
        return None


# Função para processar um vídeo e cortar o último segundo se tiver mais de 9 segundos
def process_video(video_path):
    try:
        clip = VideoFileClip(video_path)
        if clip.duration > 8:
            clip = clip.subclip(0, clip.duration - 1)
            processed_path = video_path.replace(".mp4", "_processed.mp4")
            clip.write_videofile(
                processed_path, codec="libx264", audio_codec="aac", bitrate="5000k"
            )
            os.remove(video_path)
            os.rename(processed_path, video_path)
        clip.close()
    except Exception as e:
        print(f"Erro ao processar o vídeo {video_path}: {e}")


# Função para processar o download de vídeos de um grupo de câmeras
def process_camera_group(group_id, cameras, timestamp, download_dir, updated_cameras):
    for camera in cameras:
        video_path = download_video(camera, group_id, timestamp, download_dir)
        if video_path:
            process_video(video_path)
            camera["path"] = os.path.abspath(video_path)
        updated_cameras.append(camera)


# Função principal para gerenciar os downloads
def download_videos_pipeline():
    # Caminho para o arquivo JSON e diretório de download
    json_file_path = "./cameras.json"
    download_dir = "downloaded_videos"

    # Criar diretório de download se não existir
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Ler o arquivo JSON
    with open(json_file_path, "r") as json_file:
        camera_data = json.load(json_file)

    # Obter o timestamp atual
    timestamp = get_current_timestamp()

    # Lista para armazenar threads e dados atualizados das câmeras
    threads = []
    updated_camera_data = {}

    # Iniciar download de vídeos para cada grupo de câmeras
    for group_id, cameras in camera_data.items():
        updated_cameras = []
        updated_camera_data[group_id] = updated_cameras
        thread = threading.Thread(
            target=process_camera_group,
            args=(group_id, cameras, timestamp, download_dir, updated_cameras),
        )
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    print(updated_camera_data)
    return updated_camera_data


# test
if __name__ == "__main__":
    download_videos_pipeline()
