from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .model_utils import predictor
from .schemas import PredictionResponse
import os
import logging

app = FastAPI(title="Face Achievement Diagnosis API")

# フロントエンドからのリクエストを許可 (開発環境に合わせて調整してください)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Face Achievement Diagnosis API is running. Use /docs for documentation."}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # 画像ファイルかチェック
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")

    try:
        contents = await file.read()
        result = predictor.predict(contents)
        return result
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

def get_static_path():
    paths = ["/frontend", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

path = get_static_path()
if path:
    app.mount("/", StaticFiles(directory=path, html=True), name="static")

# 起動コマンド: uvicorn app.main:app --host 0.0.0.0 --port 7860