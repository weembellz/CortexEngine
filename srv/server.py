#!/usr/bin/env python3
import asyncio, json, subprocess
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE = Path.home() / "cortex"
STATE = BASE / "core/world_state.json"
INDEX = BASE / "web/index.html"
ENGINE = BASE / "core/engine.py"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class VotePayload(BaseModel): vote_index: int
class TelemetryPayload(BaseModel): gpu_load: float; ue_fps: float; terrarium_temp: float; terrarium_hum: float
class ChatPayload(BaseModel): text: str

def load():
    with open(STATE) as f: return json.load(f)
def save(s):
    with open(STATE, "w") as f: json.dump(s, f, indent=2)

clients = []

@app.websocket("/api/v1/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: clients.remove(ws)

async def broadcaster():
    while True:
        await asyncio.sleep(2)
        try:
            s = load()
            s["system"]["timestamp"] = datetime.now().isoformat()
            for c in clients[:]:
                try: await c.send_json(s)
                except: pass
        except: pass

@app.on_event("startup")
async def start(): asyncio.create_task(broadcaster())

@app.get("/")
async def root(): return FileResponse(INDEX)

@app.get("/api/v1/state")
async def get_state(): return load()

@app.post("/api/v1/simulation/vote")
async def vote(v: VotePayload, bg: BackgroundTasks):
    action = "subir_iva" if v.vote_index == 0 else ("recortar_sanidad" if v.vote_index == 1 else "ejecutar_golpe")
    def run(): subprocess.run(["python3", str(ENGINE), action], capture_output=True)
    bg.add_task(run)
    return {"success": True}

@app.post("/api/v1/nodes/muscle/telemetry")
async def telemetry(d: TelemetryPayload):
    s = load()
    s["infrastructure"]["gpu_load_pct"] = d.gpu_load
    s["infrastructure"]["ue_fps"] = d.ue_fps
    s["infrastructure"]["terrarium_temperature_celsius"] = d.terrarium_temp
    s["infrastructure"]["terrarium_humidity_percentage"] = d.terrarium_hum
    s["infrastructure"]["node_muscle_status"] = "ONLINE"
    save(s)
    return {"success": True}

@app.post("/api/v1/enjambre/chat")
async def chat(p: ChatPayload):
    # Simulación simple (puedes conectar Ollama después)
    return {"respuesta": f"Recibido: {p.text}. Ollama no está configurado aún, pero el sistema funciona."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("srv.server:app", host="0.0.0.0", port=5005, reload=False)
