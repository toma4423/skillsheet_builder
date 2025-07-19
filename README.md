# SkillSheet Builder

ITエンジニア向けスキルシート作成Webアプリケーション

## 概要

SkillSheet Builderは、ITエンジニアがスキルシートを簡単に作成するためのWebアプリケーションです。必要な情報を入力するだけで、プロフェッショナルなスキルシートをJSON形式で出力できます。

**主な特徴:**

*   **直感的なUI/UX**: スキルシートの各項目を迷わず入力できる、分かりやすいインターフェースを提供します。
*   **効率的な作成**: 必要な情報を入力するだけで、すぐにプロフェッショナルなスキルシートが完成します。
*   **高い互換性**: JSON形式で出力されるため、様々なツールで閲覧・編集が可能です。
*   **再利用性**: 過去に作成したJSONファイルを取り込むことで、前回の入力を基に簡単に更新・再作成が可能です。
*   **安心安全**: 入力されたデータはサーバー側に保存されず、セッション終了時に完全に破棄されます。安心してご利用いただけます。

## 機能

*   基本情報（氏名、性別、年齢など）の入力
*   対応可能業務の選択
*   職務経歴の追加・編集
*   プレビュー表示
*   JSON形式でのファイル出力
*   既存のJSONファイルからのデータ読み込み

## 技術スタック

*   バックエンド: FastAPI (Python 3.11)
*   フロントエンド: HTML, CSS, TypeScript
*   パッケージ管理: uv
*   コンテナ化: Docker
*   デプロイ: GCP Cloud Run (予定)

## セットアップ方法

### 前提条件

*   Python 3.11以上
*   uv (推奨) または pip
*   Docker (オプション)

### ローカル環境での実行

1.  リポジトリをクローン

    ```bash
    git clone https://github.com/yourusername/skillsheet-builder.git
    cd skillsheet-builder
    ```

2.  uvのインストール (もしインストールされていない場合)

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # インストール後、uvコマンドが利用できるようにPATHを設定してください。
    # 例: export PATH="$HOME/.cargo/bin:$PATH" を .bashrc や .zshrc に追加
    ```

3.  依存パッケージのインストール

    ```bash
    uv sync --dev
    ```

4.  アプリケーションの起動

    ```bash
    uvicorn main:app --reload
    ```

5.  ブラウザで [http://localhost:8000](http://localhost:8000) にアクセス

### Dockerでの実行

Dockerを使用してアプリケーションを起動する方法は、開発環境と本番環境で異なります。

#### 開発環境での実行

開発中は、ソースコードの変更が即座に反映されるように、ボリュームマウントを使用してコンテナを起動します。

1.  Dockerイメージのビルド

    ```bash
    docker build -t skillsheet-builder .
    ```

2.  Dockerコンテナの起動 (開発モード)

    ```bash
    docker run -p 8000:8000 -v .:/app skillsheet-builder uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

    *   `-p 8000:8000`: ホストの8000番ポートをコンテナの8000番ポートにマッピングします。
    *   `-v .:/app`: 現在のディレクトリをコンテナ内の `/app` にマウントし、コードの変更がリアルタイムで反映されるようにします。
    *   `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`: Uvicornサーバーをリロードモードで起動します。

3.  ブラウザで [http://localhost:8000](http://localhost:8000) にアクセス

#### 本番環境での実行

本番環境では、最適化されたイメージを使用し、リロードなしでアプリケーションを起動します。

1.  Dockerイメージのビルド

    ```bash
    docker build -t skillsheet-builder .
    ```

2.  Dockerコンテナの起動 (本番モード)

    ```bash
    docker run -p 8000:8000 skillsheet-builder uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    *   `-p 8000:8000`: ホストの8000番ポートをコンテナの8000番ポートにマッピングします。
    *   `uvicorn main:app --host 0.0.0.0 --port 8000`: Uvicornサーバーを通常モードで起動します。

3.  ブラウザで [http://localhost:8000](http://localhost:8000) にアクセス

## 使用方法

1.  トップページから「新規作成」または「ファイルから読み込み」を選択
2.  スキルシート編集ページで必要な情報を入力
    *   基本情報（氏名、ふりがな、性別、年齢、最寄駅、実務経験、自己PR、主要技術、保有資格）
    *   対応可能業務（各項目に対して「o」または「-」を選択）
    *   職務経歴（「経歴追加」ボタンで複数の経歴を追加可能）
3.  「プレビュー表示」ボタンをクリックしてプレビューを確認
4.  プレビューページで「JSON出力」ボタンをクリックしてファイルをダウンロード

## テスト

テストを実行するには、以下のコマンドを実行します：

```bash
pytest
```

カバレッジレポートを生成するには：

```bash
pytest --cov=.
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

バグ報告や機能リクエストは、GitHubのIssueで受け付けています。プルリクエストも歓迎します。# skillsheet_builder
