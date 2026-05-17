#!/usr/bin/env python3
import json, urllib.request
class OllamaClient:
    def __init__(self, model="tinyllama", host="http://localhost:11434"):
        self.model = model
        self.url = f"{host}/api/generate"
    def get_directive(self, prompt: str, state: dict = None) -> str:
        ctx = "Tàrrega/Ciutadilla. RGC (801.85 EUR). XMR. RTX 3060."
        data = {"model": self.model, "prompt": f"Contexto: {ctx}. Operador Anna Armengol: {prompt}", "stream": False}
        try:
            req = urllib.request.Request(self.url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())["response"].strip()
        except: return "Inferencia local activa en background."
