import os
import urllib.request
from pathlib import Path

# Destino de las imágenes locales para el panel web
DEST_DIR = Path(__file__).resolve().parent / "static" / "maps"
DEST_DIR.mkdir(parents=True, exist_ok=True)

# Enlaces directos a capturas oficiales de mapas clásicos de Halo CE
MAP_IMAGES = {
    "beavercreek": "https://halo.wiki.gallery/images/thumb/7/7b/Battle_creek.jpg/600px-Battle_creek.jpg",
    "bloodgulch": "https://halo.wiki.gallery/images/thumb/e/e0/Blood_gulch.jpg/600px-Blood_gulch.jpg",
    "damnation": "https://halo.wiki.gallery/images/thumb/d/d4/Damnation.jpg/600px-Damnation.jpg",
    "prisoner": "https://halo.wiki.gallery/images/thumb/7/76/Prisoner.jpg/600px-Prisoner.jpg",
    "chillout": "https://halo.wiki.gallery/images/thumb/b/b3/Chill_out.jpg/600px-Chill_out.jpg",
    "hangemhigh": "https://halo.wiki.gallery/images/thumb/0/05/Hang_%27Em_High.jpg/600px-Hang_%27Em_High.jpg",
    "wizard": "https://halo.wiki.gallery/images/thumb/0/07/Wizard.jpg/600px-Wizard.jpg",
    "sidewinder": "https://halo.wiki.gallery/images/thumb/1/1b/Sidewinder.jpg/600px-Sidewinder.jpg"
}

def download_maps():
    print("====================================================")
    print(" Descargador de Vistas Previas de Mapas (Halo CE)   ")
    print("====================================================")
    print(f"Guardando imágenes en: {DEST_DIR}\n")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for map_id, url in MAP_IMAGES.items():
        dest_file = DEST_DIR / f"{map_id}.jpg"
        print(f"[*] Descargando vista previa para '{map_id}'...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp, open(dest_file, "wb") as out:
                out.write(resp.read())
            print(f"  [OK] Guardado: {dest_file.name}")
        except Exception as e:
            print(f"  [!] No se pudo descargar desde el servidor remoto ({e}).")

    print("\n[LISTO] Vistas previas preparadas para el panel web.")

if __name__ == "__main__":
    download_maps()
