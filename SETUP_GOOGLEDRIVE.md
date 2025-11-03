# Google Drive自動アップロード - セットアップ手順書

本書は、n8nとGoogle Driveを連携させて、ファイルを自動的にアップロードするワークフローの設定手順を説明します。

---

## 📋 目次

1. [前提条件](#1-前提条件)
2. [Google Cloud Platformの設定](#2-google-cloud-platformの設定)
3. [n8nの起動](#3-n8nの起動)
4. [n8nでの認証情報設定](#4-n8nでの認証情報設定)
5. [ワークフローのインポート](#5-ワークフローのインポート)
6. [動作確認](#6-動作確認)
7. [トラブルシューティング](#7-トラブルシューティング)

---

## 1. 前提条件

### 必要な環境

- ✅ Docker Desktop（または Docker + Docker Compose）
  - バージョン: Docker 20.10以上、Docker Compose 2.0以上
- ✅ Googleアカウント
- ✅ 最低8GBのメモリ（推奨16GB）
- ✅ インターネット接続

### 推奨スキル

- 基本的なコマンドライン操作
- Dockerの基礎知識（任意、あれば望ましい）

---

## 2. Google Cloud Platformの設定

### 2.1 GCPプロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 右上の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名を入力
   ```
   プロジェクト名: n8n-googledrive-automation
   ```
4. 「作成」をクリック

### 2.2 Google Drive APIの有効化

1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 検索バーに `Google Drive API` と入力
3. 「Google Drive API」を選択
4. 「有効にする」をクリック

### 2.3 OAuth 2.0認証情報の作成

#### ステップ1: OAuth同意画面の設定

1. 「APIとサービス」→「OAuth 同意画面」を選択
2. ユーザータイプ: **外部** を選択
3. 「作成」をクリック

**アプリ情報の入力:**

| 項目 | 値 |
|------|-----|
| アプリ名 | `n8n Google Drive Integration` |
| ユーザーサポートメール | あなたのGmailアドレス |
| アプリのロゴ | （任意） |
| アプリのホームページ | （任意） |
| アプリのプライバシーポリシー | （任意） |
| アプリの利用規約 | （任意） |
| 承認済みドメイン | （空欄） |
| デベロッパーの連絡先情報 | あなたのGmailアドレス |

4. 「保存して次へ」をクリック

**スコープの設定:**

5. 「スコープを追加または削除」をクリック
6. 以下のスコープを検索して追加（推奨）:
   - `.../auth/drive` （フルアクセス）
   - または `.../auth/drive.file` （アプリが作成したファイルのみ）
7. 「更新」→「保存して次へ」

**テストユーザーの追加:**

8. 「ADD USERS」をクリック
9. あなたのGmailアドレスを追加
10. 「保存して次へ」→「ダッシュボードに戻る」

#### ステップ2: OAuth クライアント IDの作成

1. 「APIとサービス」→「認証情報」を選択
2. 「認証情報を作成」→「OAuth クライアント ID」を選択
3. アプリケーションの種類: **ウェブ アプリケーション**
4. 以下を入力:

| 項目 | 値 |
|------|-----|
| 名前 | `n8n OAuth Client` |
| 承認済みの JavaScript 生成元 | `http://localhost:5678` |
| 承認済みのリダイレクト URI | `http://localhost:5678/rest/oauth2-credential/callback` |

⚠️ **注意:** n8nがリモートサーバーで動作する場合は、`localhost` を該当のドメインまたはIPアドレスに置き換えてください。

5. 「作成」をクリック

#### ステップ3: クライアントIDとシークレットの保存

作成が完了すると、以下の情報が表示されます：

```
クライアント ID: 123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
クライアント シークレット: GOCSPX-Abc123Def456Ghi789Jkl012
```

**🔒 重要:** この情報は後で使用するので、安全な場所にコピーして保管してください。

---

## 3. n8nの起動

### 3.1 プロジェクトのセットアップ

```bash
# プロジェクトディレクトリに移動
cd /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine

# アップロード用ディレクトリの作成
mkdir -p upload

# テスト用ファイルの作成
echo "This is a test file for Google Drive upload" > upload/test.txt
```

### 3.2 docker-compose.ymlの確認

`docker-compose.yml` に以下のボリュームマウントが設定されているか確認します：

```yaml
services:
  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
    volumes:
      - n8n_data:/home/node/.n8n
      - ./upload:/tmp/upload  # ← この行を確認/追加
```

### 3.3 n8nの起動

```bash
# n8nコンテナの起動
docker-compose up -d n8n

# 起動確認
docker-compose ps

# ログの確認
docker-compose logs -f n8n
```

起動が成功すると、以下のような出力が表示されます：

```
n8n    | n8n ready on 0.0.0.0, port 5678
n8n    | Version: 1.x.x
```

### 3.4 n8nへのアクセス

1. ブラウザで http://localhost:5678 を開く
2. 初回の場合、管理者アカウントを作成
   - メールアドレス: あなたのメールアドレス
   - パスワード: 強力なパスワードを設定

---

## 4. n8nでの認証情報設定

### 4.1 Credentialsページへ移動

1. n8nのメインメニュー（左側）から **「Credentials」** をクリック
2. 右上の **「Add Credential」** ボタンをクリック
3. 検索バーに `Google Drive` と入力
4. **「Google Drive OAuth2 API」** を選択

### 4.2 認証情報の入力

以下の情報を入力します：

| 項目 | 値 |
|------|-----|
| **Credential name** | `Google Drive - My Account` |
| **Client ID** | GCPで取得したクライアントID |
| **Client Secret** | GCPで取得したクライアントシークレット |

### 4.3 Googleアカウントの連携

1. **「Connect my account」** ボタンをクリック
2. Googleのログイン画面が開く（既にログイン済みの場合はスキップ）
3. n8nがGoogle Driveへのアクセスを要求する画面が表示される
4. **「続行」** をクリック
5. 必要な権限を確認して **「許可」** をクリック
6. 成功すると、n8nのCredentialsページに戻る
7. **「Save」** をクリックして保存

✅ **認証完了！** n8nからGoogle Driveにアクセスできるようになりました。

---

## 5. ワークフローのインポート

### 5.1 ワークフローファイルの確認

本プロジェクトには、2つのワークフローテンプレートが含まれています：

```
n8n_workflows/
├── google-drive-upload-workflow.json       # 基本版（手動実行）
└── google-drive-scheduled-upload.json      # スケジュール実行版（自動バックアップ）
```

### 5.2 基本ワークフローのインポート

#### ステップ1: ワークフローページへ移動

1. n8nのメインメニューから **「Workflows」** をクリック
2. 右上の **「Add workflow」** → **「Import from File」** を選択

#### ステップ2: ファイルのインポート

1. `n8n_workflows/google-drive-upload-workflow.json` を選択
2. インポートが完了すると、ワークフローエディタが開く

#### ステップ3: 認証情報の関連付け

インポート後、各Google Driveノードで認証情報を設定する必要があります：

1. **「Google Drive - Create Folder」** ノードをクリック
2. 「Credential to connect with」の横にある **ドロップダウン** をクリック
3. 先ほど作成した `Google Drive - My Account` を選択
4. 同様に **「Google Drive - Upload File」** ノードにも認証情報を設定

#### ステップ4: ワークフローの保存

1. 右上の **「Save」** ボタンをクリック
2. ワークフロー名を確認（デフォルト: `Google Drive Auto Upload`）

---

## 6. 動作確認

### 6.1 テストファイルの準備

```bash
# プロジェクトディレクトリで実行
cd /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine

# テスト用ファイルの作成
echo "Hello from n8n! This is a test file." > upload/sample.txt

# または画像ファイルをコピー
# cp /path/to/your/image.jpg upload/sample.jpg

# ファイルの確認
ls -lh upload/
```

### 6.2 ワークフローの実行

#### ステップ1: ワークフローエディタで実行

1. n8nのワークフローエディタを開く（`Google Drive Auto Upload`）
2. 左上の **「Execute Workflow」** ボタンをクリック
3. 各ノードが順番に実行される（緑のチェックマークが表示される）

#### ステップ2: 実行結果の確認

各ノードをクリックして、出力を確認します：

**ノード: Manual Trigger**
- 実行されたことを確認

**ノード: Google Drive - Create Folder**
- フォルダが作成されたことを確認
- 出力例:
  ```json
  {
    "kind": "drive#file",
    "id": "1a2b3c4d5e6f7g8h9i0j",
    "name": "2025-11-02_upload",
    "mimeType": "application/vnd.google-apps.folder"
  }
  ```

**ノード: Read Binary File**
- ファイルが読み込まれたことを確認

**ノード: Google Drive - Upload File**
- ファイルがアップロードされたことを確認
- 出力例:
  ```json
  {
    "kind": "drive#file",
    "id": "9j8i7h6g5f4e3d2c1b0a",
    "name": "uploaded_20251102_143025.pdf",
    "mimeType": "application/pdf"
  }
  ```

### 6.3 Google Driveでの確認

1. [Google Drive](https://drive.google.com) にアクセス
2. マイドライブのルートに `2025-11-02_upload` のようなフォルダが作成されていることを確認
3. フォルダを開き、アップロードされたファイルがあることを確認
4. ファイルをクリックして、内容が正しいか確認

✅ **動作確認完了！** ファイルが正常にアップロードされました。

---

## 7. トラブルシューティング

### 問題1: 認証エラー（401 Unauthorized）

**症状:**
```
ERROR: Unauthorized - Please check your OAuth credentials
```

**原因:**
- クライアントIDまたはクライアントシークレットが間違っている
- OAuth同意画面でアプリが承認されていない

**解決方法:**
1. GCPコンソールで認証情報を再確認
2. n8nのCredentialsページで認証情報を再入力
3. 「Reconnect」をクリックして再認証

---

### 問題2: ファイルが見つからない（ENOENT）

**症状:**
```
ERROR: ENOENT: no such file or directory, open '/tmp/upload/sample.txt'
```

**原因:**
- 指定したファイルパスにファイルが存在しない
- Dockerボリュームマウントが正しく設定されていない

**解決方法:**

1. **ホスト側でファイルが存在するか確認:**
   ```bash
   ls -la /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine/upload/
   ```

2. **コンテナ内でファイルが見えるか確認:**
   ```bash
   docker-compose exec n8n ls -la /tmp/upload/
   ```

3. **ボリュームマウントの確認:**
   `docker-compose.yml` の以下の行を確認:
   ```yaml
   volumes:
     - ./upload:/tmp/upload
   ```

4. **n8nを再起動:**
   ```bash
   docker-compose restart n8n
   ```

---

### 問題3: フォルダIDが取得できない

**症状:**
```
ERROR: Cannot read property 'id' of undefined
```

**原因:**
- 前のノード（Create Folder）の実行に失敗している
- ノード名が一致していない

**解決方法:**

1. **ノード名の確認:**
   - 「Google Drive - Upload File」ノードの設定で、`Parent Folder ID` の式を確認
   - 式: `{{ $node["Google Drive - Create Folder"].json["id"] }}`
   - ノード名が完全に一致しているか確認（スペースや大文字小文字も含む）

2. **前のノードの出力を確認:**
   - 「Google Drive - Create Folder」ノードをクリック
   - 「Output」タブで `id` フィールドが存在するか確認

---

### 問題4: ポート5678が既に使用されている

**症状:**
```
ERROR: Bind for 0.0.0.0:5678 failed: port is already allocated
```

**原因:**
- 別のアプリケーションがポート5678を使用している

**解決方法:**

1. **ポートを変更:**
   `docker-compose.yml` を編集:
   ```yaml
   ports:
     - "15678:5678"  # ホスト側のポートを15678に変更
   ```

2. **n8nを再起動:**
   ```bash
   docker-compose up -d n8n
   ```

3. **新しいURLでアクセス:**
   ```
   http://localhost:15678
   ```

4. **GCPのリダイレクトURIも更新:**
   ```
   http://localhost:15678/rest/oauth2-credential/callback
   ```

---

### 問題5: APIクォータ超過

**症状:**
```
ERROR: Rate Limit Exceeded. Please try again later.
```

**原因:**
- Google Drive APIの利用制限（1分間に100リクエストなど）に達した

**解決方法:**

1. **一時的に待機:**
   - 通常、100秒ほど待つとリセットされます

2. **ワークフローに遅延を追加:**
   - 大量のファイルをアップロードする場合、「Wait」ノードを追加
   - 各アップロード間に1〜2秒の遅延を設定

3. **GCPのクォータを確認:**
   - GCPコンソール → 「APIとサービス」 → 「ダッシュボード」
   - 使用状況を確認

---

## 🎉 セットアップ完了！

これで、n8nとGoogle Driveの連携が完了しました。

### 次のステップ

1. **スケジュール実行版を試す**
   - `google-drive-scheduled-upload.json` をインポート
   - 毎日自動的にバックアップを実行

2. **カスタマイズ**
   - フォルダ名やファイル名を業務に合わせて変更
   - 条件分岐やエラーハンドリングを追加

3. **他サービスとの連携**
   - Slackへの通知を追加
   - Notionにログを記録

### サポート

問題が解決しない場合は、以下を確認してください：

- [n8n公式ドキュメント](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [Google Drive API ドキュメント](https://developers.google.com/drive/api/v3/about-sdk)

---

**Happy Automation! 🚀**

