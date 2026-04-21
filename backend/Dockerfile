# Python 3.11のスリム版を使用
FROM python:3.11-slim

# コンテナ内の作業ディレクトリ
WORKDIR /app

# 必要なOSライブラリ（OpenCVやPostgreSQL用）をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# FastAPIを起動（ホットリロード有効）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]