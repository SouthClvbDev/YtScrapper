import yt_dlp
import json
import time
from datetime import timezone
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup


# Agregamos los canales
channels = {
    "Vorterix": "https://www.youtube.com/@VorterixOficial",
    "Olga": "https://www.youtube.com/@olgaenvivo_",
    "Luzu": "https://www.youtube.com/@luzutv"
}

def get_live_video_url(channel_url):
    response = requests.get(channel_url + "/live")
    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup.find_all("link", {"rel": "canonical"}):
        href = tag.get("href")
        if "watch?v=" in href:
            return href
    return None

def get_live_viewers(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        if info.get('is_live'):
            return {
                'title': info.get('title'),
                'channel': info.get('channel'),
                'viewers': info.get('concurrent_view_count'),
                'time': datetime.now(timezone.utc).isoformat()
            }
    return None

def save_data(channel_name, data):
    # Ignoramos si falta viewers o channel
    if data.get("viewers") is None or data.get("channel") is None:
        print(f"❌ Datos inválidos para {channel_name}, no se guardan.")
        return

    filename = f"{channel_name.replace(' ', '_')}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            history = json.load(f)
    else:
        history = []

    history.append(data)

    with open(filename, 'w') as f:
        json.dump(history, f, indent=2)

def main_loop():
    while True:
        print(f"🕒 Check @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for name, url in channels.items():
            video_url = get_live_video_url(url)
            if video_url:
                data = get_live_viewers(video_url)
                if data:
                    print(f"✅ {name}: {data['viewers']} viewers - {data['title']}")
                    save_data(name, data)
                else:
                    print(f"⚠️ {name}: no se pudo obtener viewers")
            else:
                print(f"⛔ {name}: no hay stream en vivo")
        time.sleep(30)  # 5 minutos

if __name__ == "__main__":
    from bs4 import BeautifulSoup  # por si no está arriba
    main_loop()
