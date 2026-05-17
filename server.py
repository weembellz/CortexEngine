import json, subprocess, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()
STATE_FILE = "/home/weemb/cortex/world_state.json"
HTML_FILE = "/home/weemb/cortex/web/index.html"

class VoteRequest(BaseModel):
    voto_index: str

@app.get("/")
def read_index():
    return FileResponse(HTML_FILE)

@app.get("/api/v1/state")
def get_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/v1/simulation/vote")
def post_vote(req: VoteRequest):
    subprocess.run(["python3", "/home/weemb/cortex/event_engine.py", req.voto_index], check=True)
    return {"status": "success", "action_processed": req.voto_index}

@app.websocket("/ws/v1/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        pass
