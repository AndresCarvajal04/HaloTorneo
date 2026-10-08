from flask import Flask, render_template, request, jsonify
from rcon import send_halo_command
import random
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "tournament_data.json"
GAMETYPES_FILE = Path(__file__).parent / "gametypes.json"

MAP_POOL = [
    {"id": "beavercreek", "name": "Battle Creek", "mode": "team_slayer"},
    {"id": "bloodgulch",  "name": "Blood Gulch",  "mode": "team_slayer"},
    {"id": "damnation",   "name": "Damnation",    "mode": "team_slayer"},
    {"id": "prisoner",    "name": "Prisoner",     "mode": "team_slayer"},
    {"id": "chillout",    "name": "Chill Out",    "mode": "team_slayer"},
    {"id": "hangemhigh",  "name": "Hang 'Em High","mode": "team_slayer"},
    {"id": "wizard",      "name": "Wizard",       "mode": "team_slayer"},
    {"id": "sidewinder",  "name": "Sidewinder",   "mode": "team_slayer"}
]

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "current_match": "Semifinal 1",
        "team_red": {"name": "Equipo Alpha"},
        "team_blue": {"name": "Equipo Bravo"},
        "bracket": {
            "semi1_t1": "Equipo Alpha",
            "semi1_t2": "Equipo Bravo",
            "semi2_t1": "Equipo Charlie",
            "semi2_t2": "Equipo Delta",
            "final_t1": "",
            "final_t2": "",
            "champion": "Por Definir"
        },
        "stats": []
    }

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/map", methods=["POST"])
def set_map():
    data = request.json or {}
    map_id = data.get("map_id", "beavercreek")
    gametype = data.get("gametype", "team_slayer")
    res = send_halo_command(f"sv_map {map_id} {gametype}")
    return jsonify({"success": True, "response": res})

@app.route("/api/roulette", methods=["POST"])
def trigger_roulette():
    chosen = random.choice(MAP_POOL)
    send_halo_command(f'say * "[RULETA] Mapa seleccionado: {chosen["name"]} ({chosen["mode"]})"')
    send_halo_command(f'sv_map {chosen["id"]} {chosen["mode"]}')
    return jsonify({"success": True, "selected": chosen})

@app.route("/api/vote/<action>", methods=["POST"])
def handle_vote(action):
    if action == "start":
        res = send_halo_command("startvote")
    elif action == "end":
        res = send_halo_command("endvote")
    else:
        return jsonify({"error": "Unknown vote action"}), 400
    return jsonify({"success": True, "response": res})

@app.route("/api/command", methods=["POST"])
def manual_command():
    cmd = (request.json or {}).get("command", "")
    res = send_halo_command(cmd)
    return jsonify({"response": res})

@app.route("/api/bracket", methods=["GET", "POST"])
def handle_bracket():
    t_data = load_data()
    if request.method == "POST":
        new_bracket = request.json or {}
        t_data["bracket"] = new_bracket
        save_data(t_data)
        return jsonify({"success": True, "bracket": t_data["bracket"]})
    return jsonify(t_data.get("bracket", {}))

@app.route("/api/stats", methods=["GET", "POST"])
def handle_stats():
    t_data = load_data()
    if request.method == "POST":
        new_stat = request.json or {}
        # Append or update player
        existing = False
        for s in t_data["stats"]:
            if s.get("name", "").lower() == new_stat.get("name", "").lower():
                s["k"] = new_stat.get("k", s["k"])
                s["d"] = new_stat.get("d", s["d"])
                s["a"] = new_stat.get("a", s["a"])
                s["team"] = new_stat.get("team", s["team"])
                existing = True
                break
        if not existing and new_stat.get("name"):
            t_data["stats"].append(new_stat)
        save_data(t_data)
        return jsonify({"success": True, "stats": t_data["stats"]})
    return jsonify({"stats": t_data.get("stats", [])})

@app.route("/api/gametypes", methods=["GET", "POST"])
def handle_gametypes():
    if request.method == "POST":
        data = request.json or {}
        gametypes = []
        if GAMETYPES_FILE.exists():
            try:
                gametypes = json.loads(GAMETYPES_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        gametypes.append(data)
        GAMETYPES_FILE.write_text(json.dumps(gametypes, indent=2), encoding="utf-8")
        return jsonify({"success": True, "saved": data})
    else:
        if GAMETYPES_FILE.exists():
            return GAMETYPES_FILE.read_text(encoding="utf-8")
        return jsonify([])

@app.route("/api/update_teams", methods=["POST"])
def update_teams():
    t_data = load_data()
    data = request.json or {}
    t_data["team_red"]["name"] = data.get("team_red", t_data["team_red"]["name"])
    t_data["team_blue"]["name"] = data.get("team_blue", t_data["team_blue"]["name"])
    t_data["current_match"] = data.get("current_match", t_data["current_match"])
    save_data(t_data)
    
    send_halo_command(f'say * "[MATCH] En juego: {t_data["team_red"]["name"]} VS {t_data["team_blue"]["name"]}"')
    return jsonify({"success": True, "state": t_data})

if __name__ == "__main__":
    print("Forerunner Tournament Web Admin en ejecucion en http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
