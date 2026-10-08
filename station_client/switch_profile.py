import os
import sys
import shutil
import subprocess
from pathlib import Path

# Adjust path to your Halo CE installation if different
HALO_EXE = Path(r"C:\Program Files (x86)\Microsoft Games\Halo Custom Edition\halo.exe")
SAVEGAMES_DIR = Path.home() / "Documents" / "My Games" / "Halo CE" / "savegames"
STORED_PROFILES = Path(__file__).parent / "tournament_profiles"

def list_available_profiles():
    if not STORED_PROFILES.exists():
        STORED_PROFILES.mkdir(parents=True)
    return [f.name for f in STORED_PROFILES.iterdir() if f.is_dir()]

def swap_and_launch(profile_name: str, server_ip="127.0.0.1", port=2302):
    src = STORED_PROFILES / profile_name
    dest = SAVEGAMES_DIR / profile_name
    
    if not src.exists():
        print(f"[ERROR] Stored profile '{profile_name}' not found in {STORED_PROFILES}")
        return

    # Copy profile files to active savegames folder
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    print(f"[OK] Profile '{profile_name}' synced to Halo CE.")

    # Launch Halo CE connected to tournament server
    cmd = [str(HALO_EXE), "-console", "-profile", profile_name, "-connect", f"{server_ip}:{port}"]
    print(f"[OK] Launching Halo: {' '.join(cmd)}")
    subprocess.Popen(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python switch_profile.py <ProfileName> [Server_IP]")
        print("Available profiles:", list_available_profiles())
        sys.exit(1)
        
    p_name = sys.argv[1]
    s_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
    swap_and_launch(p_name, s_ip)
