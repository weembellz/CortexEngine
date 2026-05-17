#!/usr/bin/env python3
import json, os, subprocess
from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE = "/home/weemb/cortex"
BRIDGE = f"{BASE}/var/world/params.json"
INDEX  = f"{BASE}/web/index.html"

app = FastAPI(title="Cortex Core", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class VoteReq(BaseModel):
    voto_index: str

def read_bridge() -> dict:
    if not os.path.exists(BRIDGE):
        raise HTTPException(status_code=503, detail="Bridge no disponible")
    with open(BRIDGE, "r") as f:
        return json.load(f)

@app.get("/")
def root():
    if not os.path.exists(INDEX):
        raise HTTPException(status_code=404, detail="Interfaz no encontrada")
    return FileResponse(INDEX)

@app.get("/api/v1/state")
def get_state():
    data = read_bridge()
    data["server_ts"] = datetime.now(timezone.utc).isoformat()
    return {"success": True, "world_state": data}

@app.post("/api/v1/simulation/vote")
def vote(req: VoteReq):
    engine = f"{BASE}/core/event_engine.py"
    if not os.path.exists(engine):
        raise HTTPException(status_code=503, detail="Motor no disponible")
    subprocess.Popen(
        ["python3", engine, req.voto_index],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return {"status": "queued", "action": req.voto_index}

@app.websocket("/ws/v1/voice")
async def voice_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            await websocket.send_bytes(data)
    except Exception:
        pass
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5005, reload=False)
