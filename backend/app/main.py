from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .model_utils import predictor
from .schemas import PredictionResponse

app = FastAPI(title="Face Achievement Diagnosis API")

# フロントエンドからのリクエストを許可 (開発環境に合わせて調整してください)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=500, detail=str(e))

# 起動コマンド: uvicorn app.main:app --reload