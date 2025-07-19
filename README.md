# SkillSheet Builder

ITエンジニア向けスキルシート作成Webアプリケーション

## 概要

SkillSheet Builderは、ITエンジニアがスキルシートを簡単に作成するためのWebアプリケーションです。必要な情報を入力するだけで、プロフェッショナルなスキルシートをXLSX形式で出力できます。

主な機能：
- 基本情報（氏名、性別、年齢など）の入力
- 対応可能業務の選択
- 職務経歴の追加・編集
- プレビュー表示
- XLSX形式でのファイル出力
- 既存のXLSXファイルからのデータ読み込み

## 技術スタック

- バックエンド: FastAPI (Python 3.11)
- フロントエンド: HTML, CSS, JavaScript
- Excel操作: openpyxl
- コンテナ化: Docker
- デプロイ: GCP Cloud Run (予定)

## セットアップ方法

### 前提条件

- Python 3.11以上
- Docker (オプション)

### ローカル環境での実行

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/skillsheet-builder.git
cd skillsheet-builder
```

2. 仮想環境を作成して有効化

```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
# または
.venv\Scripts\activate  # Windowsの場合
```

3. 依存パッケージのインストール

```bash
pip install -e .
```

4. アプリケーションの起動

```bash
uvicorn main:app --reload
```

5. ブラウザで http://localhost:8000 にアクセス

### Dockerでの実行

1. Dockerイメージのビルド

```bash
docker build -t skillsheet-builder .
```

2. Dockerコンテナの起動

```bash
docker run -p 8000:8000 skillsheet-builder
```

   開発中にソースコードの変更を即座に反映させたい場合は、以下のコマンドでコンテナを起動します。

```bash
docker run -p 8000:8000 -v .:/app skillsheet-builder
```

3. ブラウザで http://localhost:8000 にアクセス

## 使用方法

1. トップページから「新規作成」または「ファイルから読み込み」を選択
2. スキルシート編集ページで必要な情報を入力
   - 基本情報（氏名、ふりがな、性別、年齢、最寄駅、実務経験、自己PR、主要技術、保有資格）
   - 対応可能業務（各項目に対して「o」または「-」を選択）
   - 職務経歴（「経歴追加」ボタンで複数の経歴を追加可能）
3. 「プレビュー表示」ボタンをクリックしてプレビューを確認
4. プレビューページで「XLSX出力」ボタンをクリックしてファイルをダウンロード

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
