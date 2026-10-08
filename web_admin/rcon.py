import time
from pathlib import Path

# Ubicación del directorio del servidor de Halo
SERVER_DIR = Path(__file__).resolve().parent.parent / "server"
QUEUE_FILE = SERVER_DIR / "command_queue.txt"
RESP_FILE = SERVER_DIR / "command_response.txt"

def send_halo_command(cmd: str, server_ip="127.0.0.1", port=2302, password="admin123") -> str:
    """
    Envía comandos directamente al servidor de Halo CE a través del puente de SAPP Lua.
    Esto garantiza ejecución inmediata sin problemas de socket UDP.
    """
    cmd = cmd.strip()
    if not cmd:
        return "Comando vacío."

    try:
        SERVER_DIR.mkdir(parents=True, exist_ok=True)
        
        # Eliminar respuesta anterior si existe
        if RESP_FILE.exists():
            try:
                RESP_FILE.unlink()
            except Exception:
                pass

        # Escribir comando en la cola
        with open(QUEUE_FILE, "a", encoding="utf-8") as f:
            f.write(cmd + "\n")

        # Esperar brevemente confirmación de SAPP (hasta 0.6s)
        start_time = time.time()
        while time.time() - start_time < 0.6:
            if RESP_FILE.exists():
                try:
                    resp_text = RESP_FILE.read_text(encoding="utf-8").strip()
                    RESP_FILE.unlink(missing_ok=True)
                    return resp_text
                except Exception:
                    pass
            time.sleep(0.05)

        return f"Comando encolado con éxito: {cmd}"
    except Exception as e:
        return f"Error enviando comando: {e}"
