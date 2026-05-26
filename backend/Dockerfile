FROM python:3.10-slim

# 必要なシステムパッケージのインストール（画像の処理などに必要）
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードと学習済みモデルのコピー
COPY ./app ./app
COPY ./create_model/src ./create_model/src
COPY ./create_model/models ./create_model/models

# Gunicornを使用して起動（Uvicornワーカーを利用）
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]