# Upload ディレクトリ

このディレクトリは、n8nワークフローでGoogle Driveにアップロードするファイルを格納するための場所です。

## 📁 用途

- n8nのワークフローがこのディレクトリ内のファイルを読み込みます
- Dockerコンテナ内では `/tmp/upload` としてマウントされます
- テスト用のサンプルファイルが含まれています

## 📄 サンプルファイル

- `sample.txt` - テキストファイルのサンプル
- `sample.png` - 画像ファイルのサンプル

## 🚀 使い方

### 1. ファイルを配置

アップロードしたいファイルをこのディレクトリに配置します：

```bash
# ファイルをコピー
cp /path/to/your/file.pdf upload/

# または新規作成
echo "Test content" > upload/myfile.txt
```

### 2. n8nワークフローで指定

n8nの「Read Binary File」ノードで以下のようにパスを指定：

```
/tmp/upload/sample.txt
```

複数ファイルの場合：

```
/tmp/upload/*
```

### 3. Google Driveへアップロード

ワークフローを実行すると、このディレクトリ内のファイルがGoogle Driveにアップロードされます。

## ⚠️ 注意事項

- このディレクトリ内のファイルはGit管理外です（`.gitignore`に含まれています）
- 機密情報を含むファイルを配置しても、リポジトリにはコミットされません
- Dockerコンテナを再起動しても、ファイルは保持されます

## 🔄 定期バックアップの設定

スケジュール実行ワークフロー（`google-drive-scheduled-upload.json`）を使用すると、
このディレクトリ内のファイルを定期的にGoogle Driveにバックアップできます。

詳細は `SETUP_GOOGLEDRIVE.md` を参照してください。

