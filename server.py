#!/usr/bin/env python3
import json, subprocess, sys
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
app = FastAPI()
STATE = "/home/weemb/cortex/world_state.json"
INDEX = "/home/weemb/cortex/web/index.html"
class VoteReq(BaseModel): vote_index: str
@app.get("/")
def read_root(): return FileResponse(INDEX)
@app.get("/api/v1/state")
def get_state():
    with open(STATE, "r", encoding="utf-8") as f: return json.load(f)
@app.post("/api/v1/simulation/vote")
def post_vote(req: VoteReq):
    subprocess.run(["python3", "/home/weemb/cortex/event_engine.py", req.vote_index], check=True)
    return {"status": "success"}