FROM python:3.11-slim

WORKDIR /app

# 必要なファイルをコピー
COPY pyproject.toml uv.lock ./

# uvをインストール (公式推奨の方法)RUN apt-get update && apt-get install -y curl &&     curl -LsSf https://astral.sh/uv/install.sh | sh &&     chmod +x /root/.cargo/bin/uv &&     ln -s /root/.cargo/bin/uv /usr/local/bin/uv &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# 依存関係をインストール
RUN uv sync --no-dev

# アプリケーションファイルをコピー
COPY main.py ./
COPY static ./static
COPY templates ./templates

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]