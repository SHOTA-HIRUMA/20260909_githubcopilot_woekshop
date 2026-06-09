# アーキテクチャ概要

## 現在の実装状態

本ドキュメントは、Pomodoro Timer Web アプリの **現在の実装** を記述する。  
設計上の目標アーキテクチャについては [`/architecture.md`](../../../architecture.md) を参照。

---

## ディレクトリ構成（実装済み）

```
1.pomodoro/
├── app.py                  # Flask アプリケーションファクトリ
├── requirements.txt        # 依存パッケージ
├── templates/
│   └── index.html          # メイン画面テンプレート
├── static/
│   ├── css/
│   │   └── styles.css      # スタイルシート
│   └── js/
│       └── app.js          # フロントエンド JavaScript (スタブ)
└── tests/
    └── test_app.py         # バックエンドテスト
```

---

## 各コンポーネントの概要

### app.py（Flask アプリケーション）

- `create_app()` 関数でアプリケーションインスタンスを生成するファクトリパターンを採用。
- 現在提供するルートは `GET /` と `GET /health` の 2 つのみ。
- デバッグモードで `python app.py` を実行すると `0.0.0.0:5000` で起動する。

```python
def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
```

### templates/index.html（HTML テンプレート）

- Jinja2 テンプレート。現時点では動的な変数を使用していない（静的 HTML）。
- `lang="ja"` で日本語コンテンツを提供。
- タイマー UI の骨格（タイマーリング、ボタン、今日の進捗パネル）が含まれる。

### static/css/styles.css（スタイルシート）

- CSS カスタムプロパティ（変数）でカラーパレットを管理。
- `conic-gradient` を用いた円形プログレスリング（`.timer-ring`）を実装。
- `@media (max-width: 520px)` によるモバイル向けレスポンシブ対応を含む。

### static/js/app.js（JavaScript）

- 現在は `console.log("Pomodoro app bootstrap loaded.")` のみのスタブ。
- タイマーロジック・DOM 操作はまだ実装されていない。

---

## 依存関係

| パッケージ | バージョン | 用途 |
|---|---|---|
| Flask | 3.1.3 | Web フレームワーク |
| pytest | 9.0.3 | テストフレームワーク |

---

## テスト

`tests/test_app.py` に以下の 2 つのテストが実装されている。

| テスト名 | 内容 |
|---|---|
| `test_index_route_returns_200` | `GET /` が 200 を返し、UI 要素を含むことを確認 |
| `test_health_route_returns_ok` | `GET /health` が `{"status": "ok"}` を返すことを確認 |

テスト実行コマンド:

```bash
pytest tests/
```

---

## 現状と設計目標のギャップ

設計ドキュメントでは多層アーキテクチャ（Domain / Application / Infrastructure レイヤー）と複数の API エンドポイントが定義されているが、現時点の実装は MVP の初期段階（Phase 1 開始直前）に相当する。

- バックエンドの API 層（`/api/*`）は未実装
- Python 側のドメイン・アプリケーション・インフラ層は未作成
- フロントエンドのタイマーロジックは未実装
