# ✅ 動作検証チェックリスト: n8n × Google Drive

このチェックリストを使用して、n8nとGoogle Driveの連携が正しく動作しているか確認します。

---

## 📋 検証対象

- ✅ Google Cloud Platform (GCP) の設定
- ✅ n8nの起動と認証
- ✅ ワークフローのインポート
- ✅ 基本ワークフローの実行
- ✅ スケジュール実行ワークフローの動作
- ✅ エラーハンドリング

---

## 🔧 事前準備

### 環境確認

```bash
# Dockerの確認
docker --version
# 期待: Docker version 20.10以上

# Docker Composeの確認
docker-compose --version
# 期待: Docker Compose version 2.0以上

# プロジェクトディレクトリに移動
cd /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine

# ファイル構成の確認
ls -la
```

**期待される出力:**
```
docker-compose.yml
n8n_workflows/
upload/
README.md
SETUP_GOOGLEDRIVE.md
...
```

---

## ステップ1: Google Cloud Platform設定の検証

### 1.1 プロジェクトの確認

- [ ] GCPコンソールでプロジェクトが作成されている
- [ ] プロジェクト名: `n8n-googledrive-automation` (または任意の名前)

### 1.2 APIの有効化確認

1. GCPコンソール → 「APIとサービス」 → 「ダッシュボード」
2. 有効なAPIのリストに「Google Drive API」がある

- [ ] Google Drive APIが有効化されている

### 1.3 OAuth認証情報の確認

1. 「APIとサービス」 → 「認証情報」
2. OAuth 2.0 クライアントIDが存在する

- [ ] OAuth クライアントIDが作成されている
- [ ] クライアントIDとシークレットをメモしている
- [ ] リダイレクトURIが設定されている: `http://localhost:5678/rest/oauth2-credential/callback`

### 1.4 OAuth同意画面の確認

1. 「OAuth 同意画面」タブ
2. アプリが設定されている

- [ ] アプリ名が設定されている
- [ ] ユーザーサポートメールが設定されている
- [ ] テストユーザーが追加されている

**✅ ステップ1完了**

---

## ステップ2: n8nの起動確認

### 2.1 Dockerボリュームマウントの確認

```bash
# docker-compose.ymlの確認
grep -A 2 "volumes:" docker-compose.yml | grep -A 1 "n8n_data"
```

**期待される出力:**
```yaml
volumes:
  - n8n_data:/home/node/.n8n
  - ./upload:/tmp/upload
```

- [ ] `./upload:/tmp/upload` のマウント設定がある

### 2.2 n8nコンテナの起動

```bash
# n8nを起動
docker-compose up -d n8n

# 起動確認
docker-compose ps
```

**期待される出力:**
```
NAME    IMAGE            COMMAND    SERVICE   CREATED   STATUS    PORTS
n8n     n8nio/n8n:latest ...       n8n       ...       Up        0.0.0.0:5678->5678/tcp
```

- [ ] n8nコンテナが `Up` 状態
- [ ] ポート5678がマッピングされている

### 2.3 n8nログの確認

```bash
docker-compose logs n8n | tail -20
```

**期待される出力:**
```
n8n ready on 0.0.0.0, port 5678
Version: 1.x.x
```

- [ ] エラーログがない
- [ ] "n8n ready" メッセージが表示されている

### 2.4 n8n UIへのアクセス

ブラウザで http://localhost:5678 を開く

- [ ] n8nのログイン/ダッシュボード画面が表示される
- [ ] 初回の場合、アカウント作成画面が表示される

**✅ ステップ2完了**

---

## ステップ3: Google Drive認証の設定確認

### 3.1 認証情報の追加

1. n8n UI → 左メニュー「Credentials」
2. 「Add Credential」→ 「Google Drive OAuth2 API」

- [ ] Google Drive OAuth2 APIが選択できる

### 3.2 認証情報の入力

| 項目 | 状態 |
|------|------|
| Credential name | ✅ 入力済み |
| Client ID | ✅ 入力済み |
| Client Secret | ✅ 入力済み |

- [ ] すべての項目が入力されている

### 3.3 アカウント接続

1. 「Connect my account」をクリック
2. Googleログイン画面が開く

- [ ] Googleログイン画面が正常に開く
- [ ] ログイン後、権限許可画面が表示される

### 3.4 認証の完了

- [ ] 「許可」をクリック後、n8nに戻る
- [ ] 「Connected」状態になる
- [ ] 「Save」で保存できる

**✅ ステップ3完了**

---

## ステップ4: ワークフローのインポート確認

### 4.1 ワークフローファイルの存在確認

```bash
ls -la n8n_workflows/
```

**期待される出力:**
```
google-drive-upload-workflow.json
google-drive-scheduled-upload.json
```

- [ ] 2つのJSONファイルが存在する

### 4.2 基本ワークフローのインポート

1. n8n UI → 「Workflows」
2. 「Add workflow」 → 「Import from File」
3. `google-drive-upload-workflow.json` を選択

- [ ] インポートが成功する
- [ ] ワークフローエディタが開く
- [ ] 4つのノードが表示される
  - Manual Trigger
  - Google Drive - Create Folder
  - Read Binary File
  - Google Drive - Upload File

### 4.3 認証情報の関連付け

各Google Driveノードをクリック:

- [ ] 「Google Drive - Create Folder」ノードに認証情報を設定
- [ ] 「Google Drive - Upload File」ノードに認証情報を設定
- [ ] ワークフローを保存できる

**✅ ステップ4完了**

---

## ステップ5: サンプルファイルの確認

### 5.1 uploadディレクトリの確認

```bash
ls -la upload/
```

**期待される出力:**
```
README.md
sample.txt
sample.png
```

- [ ] サンプルファイルが存在する

### 5.2 コンテナ内からの確認

```bash
docker-compose exec n8n ls -la /tmp/upload
```

**期待される出力:**
```
README.md
sample.txt
sample.png
```

- [ ] コンテナ内からファイルが見える
- [ ] パーミッションエラーがない

**✅ ステップ5完了**

---

## ステップ6: 基本ワークフローの実行テスト

### 6.1 ワークフローの実行

1. n8nのワークフローエディタで `Google Drive Auto Upload` を開く
2. 「Execute Workflow」をクリック

- [ ] 実行が開始される
- [ ] すべてのノードが順番に実行される

### 6.2 各ノードの出力確認

#### Manual Trigger
- [ ] 緑のチェックマークが表示される

#### Google Drive - Create Folder
出力例:
```json
{
  "kind": "drive#file",
  "id": "1a2b3c4d5e6f7g8h9i0j",
  "name": "2025-11-02_upload",
  "mimeType": "application/vnd.google-apps.folder"
}
```

- [ ] フォルダIDが取得できている
- [ ] フォルダ名に日付が含まれている

#### Read Binary File
- [ ] バイナリデータが読み込まれている
- [ ] エラーが表示されていない

#### Google Drive - Upload File
出力例:
```json
{
  "kind": "drive#file",
  "id": "9j8i7h6g5f4e3d2c1b0a",
  "name": "uploaded_20251102_143025.pdf",
  "mimeType": "application/pdf"
}
```

- [ ] ファイルIDが取得できている
- [ ] ファイル名にタイムスタンプが含まれている

### 6.3 Google Driveでの確認

1. [Google Drive](https://drive.google.com) にアクセス
2. マイドライブを開く

- [ ] 日付入りフォルダ（例: `2025-11-02_upload`）が作成されている
- [ ] フォルダ内にファイルがアップロードされている
- [ ] ファイルをダウンロードして内容を確認できる

### 6.4 実行履歴の確認

1. n8n UI → 左メニュー「Executions」
2. 最新の実行を確認

- [ ] 実行履歴に成功（Success）と表示される
- [ ] 実行時刻が記録されている

**✅ ステップ6完了**

---

## ステップ7: スケジュール実行ワークフローのテスト

### 7.1 ワークフローのインポート

1. 「Import from File」
2. `google-drive-scheduled-upload.json` を選択

- [ ] インポートが成功する
- [ ] 6つのノードが表示される
  - Schedule Trigger
  - Google Drive - Create Folder
  - Read Binary Files
  - Split In Batches
  - Google Drive - Upload File
  - Set Notification

### 7.2 スケジュール設定の確認

「Schedule Trigger」ノードをクリック:

- [ ] Cron式が設定されている（デフォルト: `0 2 * * *`）
- [ ] 実行時刻を変更できる

### 7.3 手動でのテスト実行

1. ワークフローを「Active」にする
2. または「Execute Workflow」で手動実行

- [ ] 複数ファイルが処理される
- [ ] 各ファイルが順番にアップロードされる
- [ ] Google Driveでフォルダとファイルを確認できる

**✅ ステップ7完了**

---

## ステップ8: エラーハンドリングのテスト

### 8.1 ファイルが存在しない場合

1. ワークフローの「Read Binary File」ノードを編集
2. 存在しないファイルパスを指定: `/tmp/upload/nonexistent.txt`
3. 実行

**期待される動作:**
- [ ] エラーメッセージが表示される
- [ ] `ENOENT: no such file or directory` エラー

### 8.2 認証エラーのシミュレーション

1. 認証情報を一時的に削除
2. ワークフローを実行

**期待される動作:**
- [ ] 認証エラーが表示される
- [ ] Google Driveノードで失敗する

### 8.3 復旧確認

- [ ] 認証情報を再設定
- [ ] ファイルパスを正しいものに戻す
- [ ] ワークフローが正常に実行される

**✅ ステップ8完了**

---

## 📊 検証結果サマリー

### 成功した項目

- [ ] GCP設定
- [ ] n8n起動
- [ ] 認証設定
- [ ] ワークフローインポート
- [ ] 基本ワークフロー実行
- [ ] スケジュール実行
- [ ] エラーハンドリング

### 失敗した項目（該当する場合）

問題が発生した場合は、以下を確認：

1. [SETUP_GOOGLEDRIVE.md - トラブルシューティング](./SETUP_GOOGLEDRIVE.md#7-トラブルシューティング)
2. [QUICKSTART_GOOGLEDRIVE.md - トラブルシューティング](./QUICKSTART_GOOGLEDRIVE.md#-トラブルシューティング)

---

## 🎉 検証完了！

すべてのチェック項目が完了したら、n8nとGoogle Driveの連携が正常に動作しています。

### 次のステップ

1. **カスタマイズ**: ワークフローを業務に合わせて調整
2. **定期実行**: スケジュールトリガーを設定
3. **通知追加**: Slack、Discord、メールなどへの通知を追加
4. **モニタリング**: 実行履歴の定期確認

### ブログ執筆時の参考資料

この検証チェックリストは、ブログ記事の「動作検証」セクションの執筆に活用できます：

- スクリーンショットを撮る場所
- 読者が詰まりやすいポイント
- トラブルシューティング情報

---

**Happy Automation! 🚀**

