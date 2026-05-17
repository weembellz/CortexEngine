#!/usr/bin/env python3
import asyncio, json, os, sys, subprocess
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE = Path("/home/weemb/cortex")
sys.path.append(str(BASE))
from core.chat_ollama import OllamaClient

STATE_PATH = BASE / "core/world_state.json"
INDEX_PATH = BASE / "web/index.html"
GEN_PATH = BASE / "bin/generator_asset_forge.py"

app = FastAPI(title="CORTEX VOICE MASTER ENGINE")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class VotePayload(BaseModel): vote_index: int
class ChatPayload(BaseModel): text: str

def load_state():
    with open(STATE_PATH, "r", encoding="utf-8") as f: return json.load(f)
def save_state(s):
    with open(STATE_PATH, "w", encoding="utf-8") as f: json.dump(s, f, indent=2)
def run_generator():
    if GEN_PATH.exists(): subprocess.run(["python3", str(GEN_PATH)], capture_output=True)

clients = []

@app.websocket("/api/v1/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept(); clients.append(ws)
    try:
        while True:
            msg = await ws.receive_text(); data = json.loads(msg)
            if data.get("type") == "voice_transcription":
                s = load_state(); client = OllamaClient(); reply = client.get_directive(data["text"], s)
                s.setdefault("simulation", {}).setdefault("chat_log", []).append({"sender": "Operador_Voz", "message": data["text"]})
                s["simulation"]["chat_log"].append({"sender": "Cortex_OS", "message": reply}); save_state(s)
                await ws.send_json({"type": "voice_reply", "text": reply})
    except WebSocketDisconnect: clients.remove(ws)

async def broadcaster():
    while True:
        await asyncio.sleep(2)
        try:
            s = load_state()
            if "system" not in s: s["system"] = {}
            s["system"]["timestamp"] = datetime.now().isoformat()
            for c in clients[:]:
                try: await c.send_json({"type": "state_update", "data": s})
                except: pass
        except: pass

@app.on_event("startup")
async def startup(): asyncio.create_task(broadcaster())

@app.get("/")
async def root(): return FileResponse(INDEX_PATH)

@app.get("/api/v1/state")
async def get_state(): return load_state()

@app.post("/api/v1/simulation/vote")
async def vote(v: VotePayload, bg: BackgroundTasks):
    s = load_state(); debt = s["simulation"].get("deuda_publica_pct", 113.2)
    if v.vote_index == 0: s["simulation"]["deuda_publica_pct"] = max(0.0, debt - 10.0)
    elif v.vote_index == 1: s["simulation"]["deuda_publica_pct"] = max(0.0, debt - 8.5)
    save_state(s); bg.add_task(run_generator); return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("srv.server:app", host="0.0.0.0", port=5005, reload=False)
