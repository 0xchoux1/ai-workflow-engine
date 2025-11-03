# 🚀 クイックスタート: n8n × Google Drive 自動アップロード

このガイドは、最短時間でn8nとGoogle Driveの連携を体験するための簡易版です。  
詳細な設定は [SETUP_GOOGLEDRIVE.md](./SETUP_GOOGLEDRIVE.md) を参照してください。

---

## ⏱️ 所要時間: 約15分

---

## 📋 準備するもの

- [ ] Googleアカウント
- [ ] Docker Desktop（起動済み）
- [ ] インターネット接続

---

## 🎯 手順

### ステップ1: Google Cloud Platformの設定（5分）

#### 1.1 プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 「新しいプロジェクト」を作成
   - プロジェクト名: `n8n-googledrive-test`

#### 1.2 Google Drive APIの有効化

1. 左メニュー → 「APIとサービス」 → 「ライブラリ」
2. 「Google Drive API」を検索して有効化

#### 1.3 OAuth認証情報の作成

**同意画面:**
1. 「APIとサービス」 → 「OAuth 同意画面」
2. ユーザータイプ: **外部** → 「作成」
3. アプリ名: `n8n Test`
4. サポートメール: あなたのGmail
5. デベロッパー連絡先: あなたのGmail
6. 「保存して次へ」（スコープはスキップ）
7. テストユーザー: あなたのGmailを追加

**OAuth クライアント ID:**
1. 「認証情報」 → 「認証情報を作成」 → 「OAuth クライアント ID」
2. アプリケーションの種類: **ウェブ アプリケーション**
3. 名前: `n8n Client`
4. 承認済みのリダイレクトURI: `http://localhost:5678/rest/oauth2-credential/callback`
5. 「作成」をクリック

**📝 メモ:** クライアントIDとシークレットをコピーしておく

---

### ステップ2: n8nの起動（2分）

```bash
# プロジェクトディレクトリに移動
cd /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine

# n8nを起動
docker-compose up -d n8n

# 起動確認（数秒待つ）
docker-compose logs n8n | grep "n8n ready"
```

ブラウザで http://localhost:5678 を開く

---

### ステップ3: Google Drive認証情報の設定（3分）

#### 3.1 n8nで認証情報を追加

1. n8n UI → 左メニュー「Credentials」
2. 「Add Credential」→ 「Google Drive OAuth2 API」を検索
3. 以下を入力:
   - Credential name: `Google Drive - My Account`
   - Client ID: ステップ1でコピーしたID
   - Client Secret: ステップ1でコピーしたシークレット
4. 「Connect my account」をクリック
5. Googleアカウントでログイン → アクセスを許可
6. 「Save」をクリック

✅ **認証完了！**

---

### ステップ4: ワークフローのインポート（2分）

#### 4.1 ワークフローファイルをインポート

1. n8n UI → 左メニュー「Workflows」
2. 右上「Add workflow」 → 「Import from File」
3. ファイルを選択: `n8n_workflows/google-drive-upload-workflow.json`
4. インポート完了後、ワークフローエディタが開く

#### 4.2 認証情報の関連付け

各Google Driveノードで認証情報を設定：

1. **「Google Drive - Create Folder」** ノードをクリック
2. 「Credential to connect with」で `Google Drive - My Account` を選択
3. 同様に **「Google Drive - Upload File」** ノードも設定
4. 右上「Save」をクリック

#### 4.3 ファイルパスの確認

**「Read Binary File」ノードを確認：**

1. 「Read Binary File」ノードをクリック
2. 「File Path」が `/tmp/upload/sample.txt` になっていることを確認
3. もし `.pdf` になっている場合は `.txt` に変更
4. 「Save」をクリック

---

### ステップ5: テストファイルの準備（1分）

```bash
# プロジェクトディレクトリで実行
cd /home/choux1/dev/github.com/0xchoux1/ai-workflow-engine

# テストファイルがあることを確認
ls -la upload/

# 出力例:
# sample.txt
# sample.png
```

既にサンプルファイルが用意されています！

---

### ステップ6: ワークフローの実行（2分）

#### 6.1 実行

1. n8nのワークフローエディタで「Execute Workflow」をクリック
2. 各ノードが順番に実行される（緑のチェックマークが表示）

#### 6.2 結果確認

**n8nで確認:**
- 各ノードをクリックして出力を確認
- 「Google Drive - Create Folder」ノード → フォルダIDが表示される
- 「Google Drive - Upload File」ノード → ファイルIDが表示される

**Google Driveで確認:**
1. [Google Drive](https://drive.google.com) にアクセス
2. マイドライブに `2025-11-02_upload` のようなフォルダがある
3. フォルダ内にファイルがアップロードされている

✅ **成功！**

---

## 🎉 完了！

おめでとうございます！n8nとGoogle Driveの連携が動作しました。

---

## 📚 次のステップ

### 1. ファイル名やフォルダ名をカスタマイズ

**フォルダ名の変更:**
- 「Google Drive - Create Folder」ノードの `Folder Name` を編集
- 例: `=Backup_{{ $now.format('yyyy-MM-dd') }}`
- ⚠️ **重要**: 先頭に `=` を付けて変数として評価させる

**ファイル名の変更:**
- 「Google Drive - Upload File」ノードの `File Name` を編集
- 例: `=report_{{ $now.format('yyyyMMdd') }}.pdf`
- ⚠️ **重要**: 先頭に `=` を付けて変数として評価させる

### 2. 定期実行の設定

スケジュール実行版のワークフローをインポート：

```bash
# ファイル: n8n_workflows/google-drive-scheduled-upload.json
```

1. n8n UI → 「Import from File」
2. 「Schedule Trigger」ノードで実行時刻を設定
   - デフォルト: 毎日午前2時
   - カスタマイズ: Cron式で柔軟に設定可能

### 3. 複数ファイルのアップロード

`upload/` ディレクトリに複数のファイルを配置：

```bash
cp /path/to/file1.pdf upload/
cp /path/to/file2.jpg upload/
```

スケジュール実行版のワークフローを使用すると、全ファイルが一括アップロードされます。

### 4. Slack通知を追加

ワークフローの最後に「Slack」ノードを追加して、アップロード完了を通知できます。

---

## ❓ トラブルシューティング

### 変数が展開されない（{{ }} がそのまま表示される）

**症状:**
- ファイル名が `uploaded_{{ $now.format(...) }}.txt` のままになる
- フォルダがルートにアップロードされる

**原因:**
- n8nの式には先頭に `=` が必要

**解決方法:**
1. 「Google Drive - Upload File」ノードをクリック
2. 「File Name」フィールドを確認
3. 先頭に `=` を追加:
   - 変更前: `uploaded_{{ $now.format('yyyyMMdd_HHmmss') }}.txt`
   - 変更後: `=uploaded_{{ $now.format('yyyyMMdd_HHmmss') }}.txt`
4. 「Parent Folder」も確認:
   - `={{ $node["Google Drive - Create Folder"].json["id"] }}`
5. 「Save」→ 再実行

### ファイルがフォルダ外にアップロードされる

**症状:**
- ファイルがマイドライブのルートに作成される
- フォルダ内にファイルがない

**原因:**
- Parent Folderの設定が「From list」のまま、または正しく設定されていない

**解決方法:**
1. 「Google Drive - Upload File」ノードをクリック
2. 「Parent Folder」セクションを確認
3. 左側のドロップダウンを **「By ID」** または **「Expression」** に変更
4. 入力欄に式を入力: `{{ $node["Google Drive - Create Folder"].json.id }}`
5. フォルダIDが表示される（例: `1oXaNfVRGfkRg678QmRkRgotq0lB-l4cC`）
6. 「Save」→ 再実行

**重要なポイント:**
- 「From list」モードでは前のノードの結果を参照できません
- 必ず「By ID」または「Expression」モードに切り替えてください

### 認証エラーが出る

→ [SETUP_GOOGLEDRIVE.md - 問題1](./SETUP_GOOGLEDRIVE.md#問題1-認証エラー401-unauthorized) を参照

### ファイルが見つからない

→ [SETUP_GOOGLEDRIVE.md - 問題2](./SETUP_GOOGLEDRIVE.md#問題2-ファイルが見つからないenoent) を参照

### その他の問題

→ [SETUP_GOOGLEDRIVE.md](./SETUP_GOOGLEDRIVE.md) の「7. トラブルシューティング」セクションを参照

---

## 📖 詳細ガイド

より詳しい情報は以下を参照：

- **セットアップガイド**: [SETUP_GOOGLEDRIVE.md](./SETUP_GOOGLEDRIVE.md)
- **ブログ記事**: [BLOG_N8N_GOOGLEDRIVE.md](./BLOG_N8N_GOOGLEDRIVE.md)
- **プロジェクトREADME**: [README.md](./README.md)

---

**Happy Automation! 🚀**

