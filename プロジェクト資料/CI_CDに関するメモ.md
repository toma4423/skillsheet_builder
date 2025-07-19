# CI/CDに関するメモ

## GitHub Actions トラブルシューティング分析

今回のGitHub ActionsのCI/CD設定において、`pytest: command not found` エラーが繰り返し発生し、その解決に時間を要しました。以下に、その原因と最終的な解決策をまとめます。

### 発生した問題

1.  **`pytest: command not found` エラーの繰り返し**:
    *   当初、`uv sync --dev` で依存関係をインストールした後、`pytest` コマンドを直接実行していました。
    *   仮想環境をアクティベートするために `source .venv/bin/activate` を追加しましたが、GitHub Actionsの非対話型シェルではこのコマンドが `PATH` を正しく設定しないことが判明しました。
    *   `uv run pytest` を試みましたが、これも `pytest` 実行ファイルを見つけることができませんでした。
    *   `::add-path::` や `$GITHUB_PATH` を使って `.venv/bin` を `PATH` に追加しようとしましたが、GitHub Actionsのセキュリティ強化によりこれらの方法が非推奨・無効化されていたり、期待通りに機能しなかったりしました。
    *   最終的に、`.venv/bin/pytest` のようにフルパスで指定しても、なぜか実行ファイルが見つからないという状況に陥りました。これは、`uv` が仮想環境を構築する際の内部的な挙動や、GitHub Actionsの環境との相性によるものと考えられます。

2.  **`typescript` の依存関係の競合エラー**:
    *   `pyproject.toml` の `[project.optional-dependencies]` の `dev` セクションに `typescript>=5.0.0` が誤って記載されていました。
    *   `typescript` は主にNode.js/JavaScriptのプロジェクトで利用されるものであり、Pythonのパッケージ管理ツールである `uv` がPythonの依存関係として解決しようとした際に、利用可能な `typescript` パッケージのバージョンが古く、指定されたバージョン (`>=5.0.0`) を満たせないために依存関係の競合が発生しました。

### 最終的な解決策

上記の問題を解決するために、以下の変更を行いました。

1.  **Pythonパッケージ管理ツールの変更**:
    *   `uv` を使用したPython依存関係のインストールを中止し、GitHub Actionsの `setup-python` アクションと標準の `pip` を使用するように変更しました。
    *   これにより、`pytest` や `pytest-cov` などのPythonパッケージがGitHub Actionsの環境で確実にインストールされ、`PATH` も適切に設定されるようになりました。

    ```yaml
    - name: Install dependencies with pip
      run: |
        python -m pip install --upgrade pip
        pip install fastapi uvicorn jinja2 python-multipart pydantic
        pip install pytest httpx pytest-cov
    ```

2.  **`pytest` および `coverage` コマンドの直接呼び出し**:
    *   `pip` でインストールされた `pytest` および `coverage` は、GitHub Actionsの環境の `PATH` に自動的に追加されるため、仮想環境のアクティベーションやフルパスの指定なしに直接コマンドを呼び出すことができるようになりました。

    ```yaml
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=term-missing --cov-report=xml
        
    - name: Display coverage summary
      run: |
        coverage report --show-missing
    ```

3.  **`pyproject.toml` から `typescript` の削除**:
    *   `pyproject.toml` から `typescript` の依存関係を削除しました。これにより、Pythonの依存関係解決における競合が解消されました。

### まとめ

今回のトラブルシューティングから得られた教訓は以下の通りです。

*   **GitHub Actionsの環境特性の理解**: GitHub Actionsの `run` ステップは独立したシェルで実行されるため、ローカル環境での仮想環境のアクティベーション方法がそのまま適用できるとは限りません。環境変数や `PATH` の設定には、GitHub Actionsが提供する推奨される方法（例: `setup-python` アクション、`$GITHUB_ENV`）を優先的に使用すべきです。
*   **依存関係の適切な管理**: プロジェクトの依存関係は、使用する言語やエコシステム（Python/pip/uv, Node.js/npm/yarnなど）に応じて適切に管理する必要があります。異なるエコシステムのパッケージが混在する場合、それぞれの管理ツールで独立して管理することが重要です。
*   **デバッグの重要性**: エラーが発生した際には、`ls -la` や `echo $PATH` のようなデバッグコマンドをワークフローに一時的に追加することで、環境の状態を把握し、問題の根本原因を特定するのに役立ちます。

これらの修正により、CI/CDパイプラインが安定して動作するようになり、今後の開発効率向上に貢献できると考えています。
