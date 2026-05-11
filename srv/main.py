import json, os, uvicorn, threading, random, time
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Estado global del juego
game = {
    "h_index": 2.44,
    "crisis": 78,
    "gold": 2355.4,
    "btc": 64100.0,
    "muscle": {"temp": 0, "load": 0, "status": "offline"},
    "events": [],
    "chat_log": [],
    "tattoos": []   # diseños generados
}

# Simular actualización del oráculo cada 10 segundos (también se lee de state.json)
def update_from_oracle():
    while True:
        try:
            with open("data/state.json", "r") as f:
                data = json.load(f)
            game["h_index"] = data.get("world", {}).get("h_index", 2.44)
            game["crisis"] = data.get("world", {}).get("crisis_level", 78)
            game["gold"] = data.get("economy", {}).get("gold", 2355.4)
            game["btc"] = data.get("economy", {}).get("btc", 64100.0)
        except:
            pass
        time.sleep(5)

threading.Thread(target=update_from_oracle, daemon=True).start()

@app.post("/api/muscle/update")
async def muscle_update(req: Request):
    data = await req.json()
    game["muscle"] = data
    return {"status": "ok"}

@app.post("/api/game/action")
async def game_action(req: Request):
    data = await req.json()
    action = data.get("action")
    param = data.get("param", "")
    if action == "incise":
        # Intenta reducir crisis o generar tattoo
        if random.random() > 0.3:
            game["crisis"] = max(0, game["crisis"] - random.randint(5, 15))
            game["chat_log"].append(f"[SISTEMA] Incisión exitosa: crisis baja a {game['crisis']}%")
            # Generar diseño en cola para RTX 3060
            game["tattoos"].append({"prompt": param, "pending": True})
            return {"success": True, "msg": "Crisis reducida. Diseño en cola."}
        else:
            game["crisis"] = min(100, game["crisis"] + random.randint(5, 10))
            game["chat_log"].append(f"[SISTEMA] Incisión fallida: crisis sube a {game['crisis']}%")
            return {"success": False, "msg": "La incisión empeoró la situación."}
    elif action == "promote":
        # Campaña de propaganda: sube el H-INDEX artificialmente
        game["h_index"] = min(5.0, game["h_index"] + 0.2)
        game["chat_log"].append(f"[SISTEMA] Propaganda efectiva: H-INDEX sube a {game['h_index']:.2f}")
        return {"success": True, "msg": "La desinformación funciona."}
    elif action == "invest":
        # Invertir en tecnología: baja H-INDEX pero sube economía
        game["h_index"] = max(1.0, game["h_index"] - 0.3)
        game["gold"] += 100
        game["chat_log"].append(f"[SISTEMA] Inversión tecnológica: H-INDEX baja, oro +100")
        return {"success": True, "msg": "El PIB mejora ligeramente."}
    else:
        return {"success": False, "msg": "Acción desconocida"}

@app.post("/api/chat/send")
async def chat_send(req: Request):
    data = await req.json()
    user_msg = data.get("message", "")
    game["chat_log"].append(f"[TÚ] {user_msg}")
    # Respuesta automática del enjambre (simulada)
    resp = f"[IA] Procesando '{user_msg}'. El H-INDEX actual es {game['h_index']:.2f}."
    game["chat_log"].append(resp)
    return {"response": resp}

@app.get("/api/game/state")
async def game_state():
    return {
        "h_index": game["h_index"],
        "crisis": game["crisis"],
        "gold": game["gold"],
        "btc": game["btc"],
        "muscle": game["muscle"],
        "events": game["events"][-5:],
        "chat": game["chat_log"][-20:],
        "tattoos": game["tattoos"]
    }

@app.get("/")
def index():
    return FileResponse("web/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5005)
