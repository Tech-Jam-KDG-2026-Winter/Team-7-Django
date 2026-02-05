# EVEZAP

## Architecture

- Python 3.12.3

- Django 6.0.1

- HTML

- SQlite

## Main features

- ログイン、ログアウト機能 (login/logout)

- ユーザーに最適化するための質問を行う機能 (Personalization questions)

- パーソナライズ化されたタスクの表示機能 (Personalized task display)

- タスクの達成度合いが分かるカレンダー表示

## Settings

```bash
#仮想環境の作成 (Create virtual environment.)
python3 -m venv venv

#仮想環境の適用 (Apply a virtual environment.)
source venv/bin/activate #macOS, Linux
venv\Scripts\activate #Windows

# Pythonパッケージのインストール (Install Python package.)
pip3 install -r requirements.txt

# マイグレーションの反映 (Apply database schema changes)
python3 manage.py migrate

# デモデータのインストール (Loads the data from initial_data.json into your database)
python3 manage.py loaddata initial_data.json

# デモデータのユーザーのパスワードを設定 (set user's password of test data)
python3 manage.py set_test_passwords

```

## Execute
```bash
python3 manage.py runserver
```