# フロントエンド ドキュメント

## 概要

フロントエンドは HTML / CSS / JavaScript で構成されている。  
現時点では UI の静的なレイアウトが実装済みで、タイマーのインタラクティブなロジックは未実装である。

---

## ファイル構成

| ファイル | 状態 | 説明 |
|---|---|---|
| `templates/index.html` | 実装済み | メイン画面 HTML テンプレート |
| `static/css/styles.css` | 実装済み | スタイルシート |
| `static/js/app.js` | スタブ | JavaScript エントリポイント（ロジック未実装） |

---

## HTML テンプレート（index.html）

### 主要な要素

| 要素 ID / クラス | 説明 |
|---|---|
| `.timer-card` | タイマー全体を包むカードコンポーネント |
| `.session-label` | 現在のセッションモード表示（例: 作業中） |
| `#timer-ring` | 円形プログレスリング（`role="img"` で ARIA 対応） |
| `#timer-text` | 残り時間表示（形式: `mm:ss`） |
| `#start-button` | 開始ボタン（クラス: `btn btn-primary`） |
| `#reset-button` | リセットボタン（クラス: `btn btn-secondary`） |
| `#daily-progress` | 今日の進捗パネル（完了回数・集中時間） |

### 構造

```html
<main class="screen">
  <section class="timer-card">
    <header class="card-header">
      <h1>ポモドーロタイマー</h1>
    </header>
    <p class="session-label">作業中</p>
    <div id="timer-ring" class="timer-ring">
      <div class="timer-ring-inner">
        <p id="timer-text" class="timer-text">25:00</p>
      </div>
    </div>
    <div class="action-row">
      <button id="start-button" class="btn btn-primary">開始</button>
      <button id="reset-button" class="btn btn-secondary">リセット</button>
    </div>
    <section id="daily-progress" class="progress-panel">
      <!-- 完了回数・集中時間 -->
    </section>
  </section>
</main>
```

---

## スタイルシート（styles.css）

### CSS カスタムプロパティ（カラーパレット）

| 変数名 | 値 | 用途 |
|---|---|---|
| `--bg-start` | `#6f67cf` | 背景グラデーション上端 |
| `--bg-end` | `#5951bb` | 背景グラデーション下端 |
| `--card-bg` | `#ededf2` | カード背景色 |
| `--panel-bg` | `#d8d9e7` | 進捗パネル背景色 |
| `--primary` | `#6a74e6` | プライマリカラー（ボタン・リング） |
| `--text-main` | `#2e2f36` | メインテキスト色 |
| `--text-sub` | `#62657b` | サブテキスト色 |
| `--ring-track` | `#dcdde2` | リングのトラック（未完了部分）色 |

### 円形プログレスリング

`.timer-ring` は `conic-gradient` と CSS 変数 `--progress` を組み合わせて実装されている。

```css
.timer-ring {
  --progress: 0.72;   /* 0.0 〜 1.0 の進捗値 */
  background: conic-gradient(
    var(--primary) calc(var(--progress) * 1turn),
    var(--ring-track) 0
  );
}
```

進捗を変更するには `--progress` の値を JavaScript から更新する。

### レスポンシブ対応

`@media (max-width: 520px)` でモバイル向けの調整を適用している。

| 変更内容 | デスクトップ | モバイル |
|---|---|---|
| タイマーリング幅 | `clamp(220px, 56vw, 280px)` | `min(74vw, 250px)` |
| タイマーテキストサイズ | `clamp(2.8rem, 8vw, 4rem)` | `clamp(2rem, 12vw, 2.8rem)` |
| ボタンフォントサイズ | `1.9rem` | `1.2rem` |

---

## JavaScript（app.js）

現在の実装はブートストラップログ出力のみ。

```javascript
console.log("Pomodoro app bootstrap loaded.");
```

### 未実装の予定機能

設計ドキュメントに基づき、以下のモジュールの実装が計画されている。

| モジュール（予定） | 責務 |
|---|---|
| `timer/timer_state.js` | タイマーの状態定義（Idle / Running / Paused / Finished） |
| `timer/timer_machine.js` | 状態遷移ステートマシン |
| `timer/timer_service.js` | タイマーサービス（終了予定時刻ベースの残り時間計算） |
| `ui/renderer.js` | DOM 更新・描画 |
| `ui/controls.js` | ボタンイベントバインド |
| `storage/settings_repository.js` | 設定の永続化（LocalStorage 等） |
| `storage/progress_repository.js` | 進捗の永続化（LocalStorage 等） |

### タイマー状態（設計目標）

| 状態 | 説明 |
|---|---|
| `Idle` | 初期状態・リセット後 |
| `Running` | カウントダウン中 |
| `Paused` | 一時停止中 |
| `Finished` | セッション完了 |

### セッションモード（設計目標）

| モード | 説明 |
|---|---|
| `Work` | 作業セッション（デフォルト 25 分） |
| `ShortBreak` | 短休憩（デフォルト 5 分） |
| `LongBreak` | 長休憩（デフォルト 15 分、4 セッションごとに挿入） |
