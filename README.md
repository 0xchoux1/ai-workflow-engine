# AI Workflow Engine - n8n & Dify セルフホスト環境

n8nとDifyをDockerでセルフホストし、AI駆動のワークフロー自動化環境を構築するプロジェクトです。

## 📋 目次

- [プロジェクト概要](#プロジェクト概要)
- [n8nとDifyの比較](#n8nとdifyの比較)
- [なぜ両方のツールを導入するのか](#なぜ両方のツールを導入するのか)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [テスト](#テスト)
- [実践ガイド](#実践ガイド)
- [トラブルシューティング](#トラブルシューティング)

## プロジェクト概要

このリポジトリは、2つの強力なワークフロー自動化ツールをDocker環境でセルフホストするための設定を提供します：

- **n8n**: 汎用ワークフロー自動化プラットフォーム
- **Dify**: LLM特化型ワークフロー・AIアプリ開発プラットフォーム

両ツールともオープンソースであり、公式のDocker環境が提供されているため、セルフホストが容易です。

## n8nとDifyの比較

### n8n（エヌエイトエヌ）

**特徴:**
- **汎用的なワークフロー自動化**: 1000以上の統合ノードで多様なSaaS、API、データベースと連携可能
- **ポジショニング**: Zapier、Makeのオープンソース代替
- **得意領域**: 
  - SaaS間のデータ連携
  - ETL（データ抽出・変換・ロード）
  - バックオフィス業務の自動化
  - Webhookベースの統合
- **ライセンス**: Sustainable Use License（フェアコード）
- **想定ユーザー**: エンジニア、データ担当者、テクニカルチーム

**強み:**
- 豊富な外部サービス連携（Slack, GitHub, Google Workspace, Notion等）
- ビジュアルなワークフローエディタ
- JavaScriptによるカスタムロジック記述
- 条件分岐、ループ、エラーハンドリングの充実

### Dify

**特徴:**
- **LLM特化型プラットフォーム**: AIアプリケーション開発・運用に最適化
- **ポジショニング**: LLMOps（LLM Operations）プラットフォーム
- **得意領域**:
  - Prompt Orchestration（プロンプト管理）
  - RAG（Retrieval-Augmented Generation）パイプライン
  - Autonomous Agent（自律型エージェント）
  - AIアプリのストア配信
- **ライセンス**: Apache 2.0
- **想定ユーザー**: AIプロダクト開発者、プロンプトエンジニア、MLOpsチーム

**強み:**
- LLMプロバイダーの一元管理（OpenAI, Anthropic, Azure OpenAI等）
- ベクトルデータベース統合によるRAG構築
- プロンプトのバージョン管理とA/Bテスト
- エージェント実行のログ・モニタリング機能
- ノーコードでAIチャットボット・アプリを公開可能

## なぜ両方のツールを導入するのか

### 補完的な役割

n8nとDifyは互いに補完し合う関係にあり、併用することで以下のメリットがあります：

#### 1. **ワークフローの役割分担**

```
┌─────────────────────────────────────────────────┐
│                   n8n                           │
│  - 外部SaaSとのデータ連携                       │
│  - トリガー管理（Webhook、スケジュール）        │
│  - データ前処理・後処理                         │
│  - 通知・レポート配信                           │
└──────────────┬──────────────────────────────────┘
               │ API連携
┌──────────────▼──────────────────────────────────┐
│                   Dify                          │
│  - LLMによる自然言語処理                        │
│  - RAGによる知識ベース検索                      │
│  - エージェント実行                             │
│  - プロンプト最適化                             │
└─────────────────────────────────────────────────┘
```

#### 2. **具体的なユースケース例**

**ケース1: カスタマーサポート自動化**
- n8n: Slackからの問い合わせを受信 → 前処理
- Dify: RAGで社内ナレッジベースを検索 → LLMで回答生成
- n8n: 回答をSlackに返信 + Notionに記録

**ケース2: コンテンツ生成パイプライン**
- n8n: Google Sheetsからトピックリストを取得
- Dify: 各トピックについてLLMで記事生成
- n8n: 生成コンテンツをWordPressに投稿 + チームに通知

**ケース3: データ分析レポート**
- n8n: 定期的にデータベースからデータ抽出
- Dify: LLMでデータ分析と洞察生成
- n8n: レポートをメール送信 + ダッシュボード更新

#### 3. **選択基準**

| タスク | 推奨ツール | 理由 |
|--------|------------|------|
| SaaS連携が中心 | n8n | 豊富な統合ノード |
| LLM処理が中心 | Dify | プロンプト管理、RAG機能 |
| 複雑な条件分岐 | n8n | ワークフロー制御が得意 |
| 自然言語理解が必要 | Dify | LLMに特化 |
| エージェント的振る舞い | Dify | Autonomous Agent機能 |
| 定期実行・Webhook | n8n | トリガー機能が充実 |

### セルフホストのメリット

両ツールをセルフホストすることで：

- **コスト管理**: クラウド版の従量課金を回避
- **データプライバシー**: 機密情報を自社環境で管理
- **カスタマイズ性**: 環境変数、ネットワーク、統合の自由度
- **スケーラビリティ**: 必要に応じてリソースを調整可能

## セットアップ

### 前提条件

- Docker 20.10以上
- Docker Compose 2.0以上
- 8GB以上のメモリ推奨

### インストール手順

1. **リポジトリのクローン**

```bash
git clone https://github.com/0xchoux1/ai-workflow-engine.git
cd ai-workflow-engine
```

2. **環境変数の設定**

```bash
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

3. **Docker環境の起動**

```bash
docker-compose up -d
```

4. **アクセス確認**

- n8n: http://localhost:5678
- Dify: http://localhost:3000

### 初回セットアップ

#### n8n
1. ブラウザで http://localhost:5678 にアクセス
2. 管理者アカウントを作成
3. ワークフローの作成を開始

#### Dify
1. ブラウザで http://localhost:3000 にアクセス
2. 管理者アカウントを作成
3. LLMプロバイダーのAPI キーを設定

## 使用方法

### n8nでワークフローを作成

```bash
# n8nコンテナのログを確認
docker-compose logs -f n8n
```

### DifyでAIアプリを構築

```bash
# Difyコンテナのログを確認
docker-compose logs -f dify-api
```

### データのバックアップ

```bash
# n8nデータ
docker-compose exec n8n sh -c "cd /home/node/.n8n && tar czf - ." > n8n-backup.tar.gz

# Difyデータベース
docker-compose exec postgres pg_dump -U postgres dify > dify-backup.sql
```

## テスト

### テスト戦略

このプロジェクトは3層のテスト戦略を採用しています：

```
1. API Level Tests (最優先)
   - 各サービスのヘルスチェック
   - エンドポイントの接続確認
   - 高速で安定

2. Integration Tests
   - サービス間の連携確認
   - Docker Composeによる統合テスト

3. E2E Tests (必要に応じて)
   - Playwrightによるブラウザ自動化
   - ワークフロー作成から実行まで
```

### クイックテスト

#### シェルスクリプトによるヘルスチェック

```bash
# すべてのサービスの稼働状態を確認
./scripts/health_check.sh
```

**出力例:**
```
=== Service Health Check ===

Checking n8n... ✓ HTTP 200
Checking Dify Web... ✓ HTTP 200
Checking Dify API... ✓ HTTP 200
Checking Weaviate Ready... ✓ HTTP 200
Checking Weaviate Meta... ✓ HTTP 200

All services are healthy!
```

### Pytestによる自動テスト

#### セットアップ

```bash
# Python仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

#### テストの実行

```bash
# すべてのテストを実行
pytest

# スモークテストのみ実行（高速）
pytest -m smoke

# 詳細な出力付きで実行
pytest -v

# カバレッジレポート付きで実行
pytest --cov=. --cov-report=html
```

#### テストの種類

**スモークテスト** (`-m smoke`):
- n8n接続確認
- Dify Web接続確認
- Dify API接続確認
- Weaviate接続確認
- PostgreSQL接続確認
- Redis接続確認

**統合テスト** (`-m integration`):
- サービス間の連携確認
- ワークフロー実行テスト

**E2Eテスト** (`-m e2e`):
- ブラウザ自動化テスト（Playwright使用）
- UIからのワークフロー作成・実行

### CI/CDでの利用

```yaml
# .github/workflows/test.yml の例
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start services
        run: docker compose up -d
      - name: Wait for services
        run: sleep 30
      - name: Run health check
        run: ./scripts/health_check.sh
      - name: Run pytest
        run: |
          python3 -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          pytest -m smoke
```

### テストのカスタマイズ

環境変数でテスト対象のURLを変更できます：

```bash
# .envファイルに追加
N8N_URL=http://localhost:5678
DIFY_WEB_URL=http://localhost:3000
DIFY_API_URL=http://localhost:5001
WEAVIATE_URL=http://localhost:8080
```

## 実践ガイド

### 🚀 n8n + Google Drive 自動アップロード

n8nとGoogle Driveを連携させて、ローカルファイルを自動的にアップロードするワークフローを構築できます。

#### 📖 詳細ガイド

**セットアップ手順:**  
[SETUP_GOOGLEDRIVE.md](./SETUP_GOOGLEDRIVE.md) - Google Drive API設定からワークフロー作成まで完全ガイド

**クイックスタート:**  
[QUICKSTART_GOOGLEDRIVE.md](./QUICKSTART_GOOGLEDRIVE.md) - 15分で試せる簡易ガイド

#### ⚡ クイックスタート

```bash
# 1. アップロード用ディレクトリの準備
mkdir -p upload
echo "Test file" > upload/sample.txt

# 2. n8nの起動
docker-compose up -d n8n

# 3. ワークフローのインポート
# n8n UI (http://localhost:5678) でワークフローをインポート
# ファイル: n8n_workflows/google-drive-upload-workflow.json
```

#### 📁 提供されるワークフロー

1. **基本版** - `google-drive-upload-workflow.json`
   - 手動実行でファイルをアップロード
   - フォルダの自動作成
   - 日時情報の埋め込み

2. **スケジュール実行版** - `google-drive-scheduled-upload.json`
   - 定期的な自動バックアップ
   - 複数ファイルの一括アップロード
   - 実行結果の通知

#### 🎯 主な機能

✅ Google Driveにフォルダを自動作成  
✅ ローカルファイルの自動アップロード  
✅ ファイル名に日時情報を埋め込み  
✅ スケジュール実行による定期バックアップ  
✅ 複数ファイルの一括処理  

---

## トラブルシューティング

### ポート競合

既にポート5678や3000が使用されている場合：

```bash
# docker-compose.ymlのportsセクションを編集
# 例: "5678:5678" -> "15678:5678"
```

### メモリ不足

```bash
# Dockerのメモリ制限を確認
docker stats

# docker-compose.ymlにリソース制限を追加
```

## 参考リソース

- [n8n公式ドキュメント](https://docs.n8n.io/)
- [Dify公式ドキュメント](https://docs.dify.ai/)
- [n8n GitHub](https://github.com/n8n-io/n8n)
- [Dify GitHub](https://github.com/langgenius/dify)

## ライセンス

このリポジトリの設定ファイルはMITライセンスの下で公開されています。
各ツール（n8n、Dify）は独自のライセンスに従います。

## 貢献

Issue、Pull Requestを歓迎します！

---

作成者: [@0xchoux1](https://github.com/0xchoux1)
