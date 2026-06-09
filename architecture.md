# Pomodoro Timer Webアプリ アーキテクチャ案

## 1. 目的

本ドキュメントは、Flask + HTML/CSS/JavaScript で実装するポモドーロタイマーWebアプリのアーキテクチャ方針を定義する。

設計上の最重要ポイントは以下とする。

- モックに忠実なUIを実現しやすいこと
- MVPを素早く構築できること
- 将来の機能追加に耐えられること
- ユニットテストしやすいこと

## 2. 全体方針

初期フェーズでは「サーバーは薄く、タイマー制御はフロントエンド中心」で実装する。

- Flask
  - 画面配信
  - 設定/進捗のAPI提供
- フロントエンド(JavaScript)
  - タイマー状態管理
  - カウントダウン制御
  - モード遷移
  - DOM更新
- HTML/CSS
  - モック準拠のレイアウト
  - 円形プログレス表示
  - レスポンシブ対応

## 3. レイヤード構成

### 3.1 レイヤー責務

- Presentation Layer
  - Flaskのルーティング
  - HTMLテンプレート
  - CSS/JSの配信
- Application Layer
  - ユースケースのオーケストレーション
  - 例: 設定更新、セッション完了処理
- Domain Layer
  - ポモドーロ状態遷移ルール
  - 日次進捗集計ルール
  - 時間計算ルール
- Infrastructure Layer
  - 設定/進捗の保存
  - 初期はローカル保存、後続でSQLite等に差し替え可能

### 3.2 推奨ディレクトリ案

実装時は以下のように責務分離する。

- 1.pomodoro/
  - app.py
  - templates/
    - index.html
  - static/
    - css/
      - styles.css
    - js/
      - timer/
        - timer_state.js
        - timer_machine.js
        - timer_service.js
      - ui/
        - renderer.js
        - controls.js
      - storage/
        - settings_repository.js
        - progress_repository.js
      - app.js
  - domain/
    - pomodoro_rules.py
    - progress.py
    - clock.py
  - application/
    - use_cases.py
  - infrastructure/
    - repository.py
    - local_store.py

補足:

- 現在は最小構成のため app.py だけで開始してよい。
- 機能増加に応じて上記へ段階的に分離する。

## 4. フロントエンド設計

### 4.1 状態モデル

- TimerStatus
  - Idle
  - Running
  - Paused
  - Finished
- SessionMode
  - Work
  - ShortBreak
  - LongBreak

### 4.2 イベント駆動

主要イベント:

- START
- PAUSE
- RESUME
- RESET
- TICK
- SESSION_COMPLETED
- MODE_SWITCHED

状態遷移は「ステートマシン」で明示し、イベントごとの遷移先を固定する。

### 4.3 時刻計算の原則

タイマー精度を担保するため、1秒減算方式ではなく「終了予定時刻との差分」で残り時間を計算する。

- 背景タブ復帰時のズレを抑える
- スリープ復帰後も正しく再計算できる

## 5. API設計(MVP)

### 5.1 ルート

- GET /
  - UI配信

### 5.2 設定

- GET /api/settings
  - 作業時間、休憩時間、長休憩設定を返却
- PUT /api/settings
  - 設定更新

### 5.3 進捗

- GET /api/progress/today
  - 今日の完了回数/集中時間を返却
- POST /api/progress/session-completed
  - セッション完了を記録

### 5.4 運用

- GET /health
  - ヘルスチェック

## 6. データモデル

### 6.1 Settings

- work_minutes
- short_break_minutes
- long_break_minutes
- long_break_interval

### 6.2 DailyProgress

- date(YYYY-MM-DD)
- completed_sessions
- focus_minutes

日付キーで管理し、日付変更時は当日データを新規作成する。

## 7. テスト容易性を高める設計

### 7.1 純粋関数化

タイマー遷移ロジックを純粋関数化する。

- Input: 現在状態、イベント、現在時刻
- Output: 次状態、残り秒数、ドメインイベント

副作用を分離することで、ユニットテストが高速かつ安定する。

### 7.2 Clock抽象化

時刻依存を抽象化する。

- Clockインターフェース
- 本番: SystemClock
- テスト: FakeClock

これにより日跨ぎや復帰時補正を再現しやすくなる。

### 7.3 Repository境界

永続化をインターフェースで分離する。

- SettingsRepository
- ProgressRepository

テスト時はインメモリ実装を使い、I/O依存を除去する。

### 7.4 DOM操作分離

ドメインとDOM操作を分離する。

- ドメイン: 状態遷移と計算のみ
- UI層: 描画とイベントバインドのみ

ブラウザ依存を減らし、ロジック単体テストを容易にする。

### 7.5 API薄層化

Flaskルートは以下に限定する。

- 入力検証
- ユースケース呼び出し
- レスポンス整形

ロジックをルートから排除し、APIテストとユースケーステストの責務を明確化する。

## 8. 推奨テスト戦略

### 8.1 ドメインテスト(最優先)

- 状態遷移
- 残り時間計算
- 長休憩挿入ルール
- 日次リセット

### 8.2 アプリケーション層テスト

- セッション完了時の進捗更新
- 設定変更の反映

### 8.3 APIテスト

- 正常系
- バリデーションエラー
- 日付境界

### 8.4 UIテスト(最小限)

- 開始/停止/リセットの連携
- 画面再読み込み後の復元

## 9. 開発フェーズ

### Phase 1: MVP

- 単一画面のUI
- フロント中心タイマー
- ローカル保存

### Phase 2: サーバー拡張

- 設定/進捗APIの安定化
- 永続化層の抽象化

### Phase 3: 体験向上

- 通知音
- キーボード操作
- ユーザー別データ管理(必要時)

## 10. 非機能要件

- タイマー誤差は実運用で体感差が出ないレベルに抑える
- UIはモバイル/デスクトップ双方で破綻しない
- エラー時は状態を壊さず、再読込で復元可能にする

## 11. 既存コードとの整合

現状のエントリポイントは 1.pomodoro/app.py である。

初期実装はこのファイルから開始し、機能拡張時に以下の順で分離する。

1. static/js にタイマーロジックを分離
2. APIを追加
3. Python側のドメイン/インフラを分離

以上の方針で、短期実装と中長期保守性を両立する。