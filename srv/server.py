import json, subprocess, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()
STATE_FILE = "/home/weemb/cortex/core/world_state.json"
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
    subprocess.run(["python3", "/home/weemb/cortex/core/engine.py", req.voto_index], check=True)
    return {"status": "success", "action_processed": req.voto_index}

@app.websocket("/ws/v1/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[VOICE] Canal de voz Cortex conectado.")
    try:
        while True:
            # Recibir chunks de Opus/WebM en ráfagas de 100ms
            audio_chunk = await websocket.receive_bytes()
            
            # PIPELINE DE TRABAJO REAL FUTURO:
            # 1. texto = whisper_stt(audio_chunk)
            # 2. respuesta_texto = llm_query(texto, STATE_FILE)
            # 3. audio_out = piper_tts(respuesta_texto)
            # await websocket.send_bytes(audio_out)
            
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        print("[VOICE] Canal de voz Cortex desconectado.")
