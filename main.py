from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class JobRequest(BaseModel):
    job_text: str

@app.post("/analyze")
def analyze_job(data: JobRequest):
    text = data.job_text.lower()
    reasons = []
    scam_score = 0

    if "free visa" in text or "free ticket" in text:
        reasons.append("Promises of free visa (usually scam)")
        scam_score += 20

    if re.search(r"\b(gmail\.com|yahoo\.com|hotmail\.com)\b", text):
        reasons.append("Uses personal email (Gmail/Yahoo) instead of company domain")
        scam_score += 20

    if "whatsapp" in text or "telegram" in text:
        reasons.append("Contact via WhatsApp/Telegram only")
        scam_score += 15

    if "no experience" in text or "anyone can apply" in text:
        reasons.append("Unrealistic requirements (no experience needed)")
        scam_score += 10

    if "salary" in text and "aed" in text:
        reasons.append("Unusually high salary for vague role")
        scam_score += 15

    if not re.search(r"\b(company|llc|ltd|inc)\b", text):
        reasons.append("No proper company name mentioned")
        scam_score += 20

    scam_score = min(scam_score, 100)
    verdict = "Likely a Scam" if scam_score >= 60 else "Looks Genuine"
    recommendation = "We strongly recommend avoiding this job offer." if verdict == "Likely a Scam" else "Seems safe, but always double-check."

    return {
        "verdict": verdict,
        "scam_probability": scam_score,
        "reasons": reasons,
        "recommendation": recommendation
    }
