# GoInsightAdmin


## 開発環境

Visual Studio Code拡張機能Remote Containerでの開発を推奨

### 利用ツール

主要な開発ツール  
Remote Containerで開発環境を構築する場合自動的にインストールされる

| ツール      | 用途                 |
| ----------- | -------------------- |
| Python 3.11 | 開発言語             |
| Django 4.2  | フレームワーク       |
| PostgreSQL  | データベース         |
| make        | CLIユーティリティ    |
| git         | バージョン管理       |
| pre-commit  | 構文チェック自動実行 |
| flake8      | 構文チェック         |
| isort       | 構文チェック         |
| black       | 構文チェック         |
| mypy        | 静的型チェック       |

#### Remote Containerを利用しない場合

```bash
# Python依存ライブラリインストール
poetry install

# 各種サーバー起動
docker-compose -f .devcontainer/docker-compose.yml up -d

# 開発サーバーでコマンドを実行する方法
docker-compose -f .devcontainer/docker-compose.yml exec app <コマンド>
```

### 起動コンテナ

| サービス       | 説明                     | ブラウザアクセス              | 開放ポート  |
| -------------- | ------------------------ | ----------------------------- | ----------- |
| app            | アプリケーション実行環境 | localhost:8000 (`make run`時) | 8000        |
| aurora         | データベースサーバー     |                               | 5432        |
| s3             | Amazon S3モック          | localhost:19001               | 19000,19001 |
| dynamodb       | Amazon DynamoDBモック    |                               | 18000       |
| dynamodb-admin | Amazon DynamoDB管理画面  | localhost:18001               | 18001       |

* AWSモックログイン情報
    * goinsight-aws-user
    * goinsight-aws-password

### 開発環境内コマンド

詳細は[Django公式ドキュメント](https://docs.djangoproject.com/ja/4.2/ref/django-admin/)参照

#### ログインユーザー作成

```bash
python src/manage.py createsuperuser
```

#### アプリケーション起動

```bash
make run
```

#### Djangoアプリケーション作成

```bash
make app-<アプリ名>
```

#### マイグレーションファイル作成

```bash
make migrations
```

#### マイグレーション実行

```bash
make migrate
```
