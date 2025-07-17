FROM python:3.11-slim

WORKDIR /app

# 必要なファイルをコピー
COPY pyproject.toml uv.lock ./

# uvをインストール
RUN pip install --no-cache-dir uv

# 依存関係をインストール
RUN uv pip install --system --no-cache-dir -r pyproject.toml

# アプリケーションファイルをコピー
COPY main.py ./
COPY static ./static
COPY templates ./templates

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]