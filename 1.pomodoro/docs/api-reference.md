# API リファレンス

## 概要

本ドキュメントは、Pomodoro Timer Web アプリのバックエンド API を記述する。  
現在の実装は Flask で構成されており、以下のエンドポイントが提供されている。

---

## エンドポイント一覧

### GET /

**概要**: メイン画面（HTML）を返却する。

**レスポンス**

| ステータスコード | 内容 |
|---|---|
| `200 OK` | `index.html` テンプレートをレンダリングした HTML |

**例**

```http
GET / HTTP/1.1
Host: localhost:5000
```

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang="ja">
...
```

---

### GET /health

**概要**: アプリケーションの死活監視用エンドポイント。

**レスポンス**

| ステータスコード | 内容 |
|---|---|
| `200 OK` | JSON 形式のステータス情報 |

**レスポンスボディ**

```json
{
  "status": "ok"
}
```

**例**

```http
GET /health HTTP/1.1
Host: localhost:5000
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"status": "ok"}
```

---

## 未実装エンドポイント（計画中）

以下のエンドポイントは設計ドキュメントに記載されているが、現時点では実装されていない。

| メソッド | パス | 概要 |
|---|---|---|
| `GET` | `/api/settings` | タイマー設定取得 |
| `PUT` | `/api/settings` | タイマー設定更新 |
| `GET` | `/api/progress/today` | 当日の進捗取得 |
| `POST` | `/api/progress/session-completed` | セッション完了の記録 |
