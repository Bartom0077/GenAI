from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# === FRONT ===
# serwuj katalog "static" pod /static (np. /static/app.css)
app.mount("/static", StaticFiles(directory="static"), name="static")

# serwuj stronę główną (GET /) -> static/index.html
@app.get("/")
def root():
    return FileResponse("static/index.html")

# === API ===
class AnalyzeReq(BaseModel):
    message: str
    loc: dict | None = None

@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat()}

@app.post("/analyze")
def analyze(req: AnalyzeReq):
    text = (req.message or "").lower()
    trigger = any(k in text for k in ["sos", "pomocy", "ratunku"])
    if trigger:
        return {
            "risk": "HIGH",
            "actions": [
                {"type": "NOTIFY_CONTACT", "message": "Możliwe zagrożenie. Sprawdź lokalizację."},
                {"type": "GUIDE_USER", "text": "Wejdź do jasnego miejsca i zadzwoń na 112."}
            ],
            "reason": "Frazy alarmowe wykryte"
        }
    return {"risk": "LOW", "actions": [{"type": "NO_ACTION"}], "reason": "Brak fraz alarmowych"}
