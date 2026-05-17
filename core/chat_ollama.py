import json, urllib.request, urllib.error
class OllamaClient:
    def __init__(self, model="tinyllama", host="http://localhost:11434"):
        self.model = model
        self.url = f"{host}/api/generate"
    def get_directive(self, prompt: str, state=None) -> str:
        data = {"model":self.model, "prompt":prompt, "stream":False}
        try:
            req = urllib.request.Request(self.url, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())["response"].strip()
        except:
            return "Ollama offline. Ejecuta 'ollama serve'."
