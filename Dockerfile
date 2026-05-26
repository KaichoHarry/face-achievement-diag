FROM python:3.10-slim

# Hugging FaceはUID 1000のユーザーで実行されることを推奨しています
RUN useradd -m -u 1000 user

# 必要なシステムパッケージのインストール（画像の処理などに必要）
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存関係のインストール
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードと学習済みモデルのコピー
COPY backend/app ./app
COPY backend/create_model/src ./create_model/src
COPY backend/create_model/models ./create_model/models
# フロントエンドのコードもコピー
COPY --chown=user:user frontend /frontend

USER user

# メモリ節約のためGunicornを介さずUvicornを直接起動
# Hugging Face Spaces は 7860 ポートを期待します
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]