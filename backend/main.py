from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str
    language: str


@app.post("/explain")
def explain_code(request: CodeRequest):

    prompt = f"""
You are an expert programming tutor.
Explain the following {request.language} code briefly in 3-4 lines.
Keep the explanation simple and short.

Code:
{request.code}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False
            }
        )

        print("Status Code:", response.status_code)
        print("Raw Response:", response.text)

        if response.status_code != 200:
            return {"explanation": "Model error occurred."}

        data = response.json()
        explanation = data.get("response")

        if not explanation:
            explanation = "No explanation returned from model."

        return {"explanation": explanation}

    except Exception as e:
        return {"explanation": f"Server Error: {str(e)}"}
