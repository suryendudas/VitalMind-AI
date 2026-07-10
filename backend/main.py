import json
from fastapi import UploadFile, File
import shutil
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from health_analyzer import analyze
from granite import generate_response

app = FastAPI(title="VitalMind AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://vital-mind-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_prompt(summary: dict) -> str:
    formatted = json.dumps(summary, indent=2)

    return f"""
You are VitalMind AI.

You analyze wearable health data.

Never diagnose diseases or provide medical diagnoses.

Keep your answer under 180 words.

Do NOT repeat or copy the health summary.
Do NOT include JSON in your response.
Do NOT mention the input data directly.

Write exactly in this format:

Overall Wellness:
...

Recovery:
...

Sleep:
...

Heart Rate:
...

Recommendations:
- ...
- ...
- ...
- ...
- ...

Health Summary (for analysis only, never repeat this back):
{formatted}
"""


@app.get("/")
def root():
    return {"message": "VitalMind AI Backend Running"}


@app.get("/analyze")
def analyze_health():
    try:
        summary = analyze()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    prompt = _build_prompt(summary)

    try:
        ai_summary = generate_response(prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI response failed: {exc}")

    return {
        "health_summary": summary,
        "ai_summary": ai_summary,
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        upload_dir = "sample_data"

        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, "health_data.csv")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "CSV uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))