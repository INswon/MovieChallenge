# FlowCompass (MVP)　優先度スコアで「次にやるべきこと」を整理するタスク管理アプリ

## 1. アプリ概要
### What
FlowCompass は、タスクを「主観」で選ぶのではなく、
貢献度 × 期限 から計算した 優先度スコア（0.0〜1.0） を使って自動で並び替えるタスク管理システムです。

### Why
急ぎのタスクに引っ張られて、本当に大事な作業が後回しになる問題を避けるために、
**客観的に見て今やるべき順番** が分かる仕組みを作りました。

**初期のMVPでは、以下のプロセスで開発を進めました。**
- 優先度スコアの計算ロジック
- タスクのCRUD操作
- 認証（ログイン）
- 基本的なテスト


## 2. 主な機能一覧
| 機能カテゴリ | 機能名             | 概要                                           | 認証        |
|:------------:|--------------------|-----------------------------------------------|:-----------:|
| コアロジック | 優先度スコア自動計算 | 貢献度と締切度合いから優先度スコアを自動算出（アプリの核） | 不要        |
| Read         | 一覧・詳細表示      | スコア順にソートされたタスクを閲覧          | 不要 |
| Write        | 作成 / 更新 / 削除  | 認証済みユーザーのみがタスクを操作可能      | 必須        |


## 3. セットアップ手順
```bash
# 1. リポジトリをクローン
git clone https://github.com/your-name/FlowCompass.git
cd FlowCompass

# 2. 仮想環境を作成（任意）
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. 依存パッケージをインストール
pip install -r requirements.txt

# 4. マイグレーションを適用
python manage.py migrate

# 5. 開発サーバーを起動
python manage.py runserver
```

## 4. テストの実行方法
```bash
python manage.py test
```



## 4. 利用技術（Tech Stack）
- バックエンド: Python (3.11.6), Django (5.2.8)
- データベース: SQLite3 (開発用)
- フロントエンド: HTML, CSS (最小限)
- 認証: Django標準の認証システム (LoginRequiredMixinを使用)


