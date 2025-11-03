# テスト戦略とE2E自動化

## 概要

このドキュメントでは、AI Workflow Engine（n8n & Dify）のテスト戦略と自動化アプローチについて説明します。

## テストピラミッド

```
        /\
       /  \      E2E Tests (Playwright)
      /____\     - ブラウザ自動化
     /      \    - ワークフロー作成・実行
    /        \
   /   統合   \  Integration Tests (pytest)
  /____________\ - サービス間連携
 /              \
/    API Tests   \ API Level Tests (pytest + curl)
/________________\- ヘルスチェック
                  - エンドポイント確認
```

## 1. API Level Tests（最優先）

### 目的
- 各サービスが正常に起動しているか確認
- APIエンドポイントが応答するか確認
- 高速で安定したテストを実現

### ツール
- **pytest**: Pythonテストフレームワーク
- **httpx**: 非同期HTTP クライアント
- **curl**: コマンドライン HTTPクライアント

### テストケース

#### 1. ヘルスチェック（`tests/api/test_health.py`）

```python
@pytest.mark.api
@pytest.mark.smoke
def test_n8n_health(sync_http_client, n8n_url):
    """n8nが正常に起動しているか確認"""
    response = sync_http_client.get(n8n_url)
    assert response.status_code in [200, 401]

@pytest.mark.api
@pytest.mark.smoke
def test_weaviate_health(sync_http_client, weaviate_url):
    """Weaviateベクトルデータベースが準備完了か確認"""
    response = sync_http_client.get(f"{weaviate_url}/v1/.well-known/ready")
    assert response.status_code == 200
```

#### 2. データベース接続確認

```python
@pytest.mark.api
@pytest.mark.smoke
def test_postgres_connection(postgres_config):
    """PostgreSQLに接続できるか確認"""
    conn = psycopg2.connect(**postgres_config)
    conn.close()

@pytest.mark.api
@pytest.mark.smoke
def test_redis_connection(redis_config):
    """Redisに接続できるか確認"""
    r = redis.Redis(**redis_config)
    r.ping()
```

### 実行方法

```bash
# スモークテストのみ（高速）
pytest -m smoke

# すべてのAPIテスト
pytest tests/api/

# 詳細出力
pytest -v tests/api/test_health.py
```

## 2. Integration Tests

### 目的
- n8nとDifyの連携動作を確認
- ワークフローが正常に実行されるか確認
- データの流れを検証

### テストケース例

```python
@pytest.mark.integration
async def test_n8n_to_dify_workflow():
    """n8nからDifyへのデータ連携をテスト"""
    # 1. n8nでワークフローを起動
    # 2. DifyのAPIを呼び出し
    # 3. レスポンスを確認
    pass
```

## 3. E2E Tests（Playwright）

### 目的
- 実際のユーザー操作をシミュレート
- UIからのワークフロー作成を自動化
- エンドツーエンドの動作を保証

### Playwrightのセットアップ

```bash
# Playwrightのインストール
pip install playwright
playwright install

# ブラウザのインストール確認
playwright install chromium
```

### E2Eテスト例（将来実装予定）

```python
@pytest.mark.e2e
async def test_create_workflow_ui(page):
    """n8n UIからワークフローを作成"""
    # n8nにログイン
    await page.goto("http://localhost:5678")
    
    # 新しいワークフローを作成
    await page.click('text="New Workflow"')
    
    # ノードを追加
    await page.click('text="Add Node"')
    
    # 実行して結果を確認
    await page.click('text="Execute Workflow"')
    
    # 成功メッセージを確認
    assert await page.locator('text="Success"').is_visible()
```

## ヘルスチェックスクリプト

### scripts/health_check.sh

シンプルで高速なヘルスチェックスクリプトです。

```bash
#!/bin/bash
# すべてのサービスの稼働状態を確認

./scripts/health_check.sh
```

**チェック対象:**
- ✅ n8n (port 5678)
- ✅ Dify Web (port 3000)
- ✅ Dify API (port 5001)
- ✅ Weaviate (port 8080)

## CI/CD統合

### GitHub Actions設定例

```yaml
name: Test Workflow

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Compose
      run: docker compose up -d
    
    - name: Wait for services to be ready
      run: |
        sleep 30
        ./scripts/health_check.sh
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    
    - name: Run smoke tests
      run: |
        source venv/bin/activate
        pytest -m smoke --cov=. --cov-report=xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## ベストプラクティス

### 1. テストの独立性
- 各テストは他のテストに依存しない
- テストの実行順序に依存しない
- テストデータのクリーンアップを忘れない

### 2. テストの速度
- スモークテストは30秒以内
- API テストは1分以内
- E2Eテストは5分以内を目標

### 3. テストの保守性
- テストコードも本番コードと同様に管理
- 重複を避けるためにフィクスチャを活用
- わかりやすいテスト名とドキュメント

### 4. エラーハンドリング
- タイムアウトを適切に設定
- リトライロジックを実装
- 失敗時の詳細なログ出力

## トラブルシューティング

### テストが失敗する場合

#### 1. サービスが起動していない

```bash
# コンテナの状態を確認
docker compose ps

# すべてのサービスを再起動
docker compose restart
```

#### 2. ポートが競合している

```bash
# 使用中のポートを確認
sudo lsof -i :5678
sudo lsof -i :3000

# docker-compose.ymlでポートを変更
ports:
  - "15678:5678"  # n8n
  - "13000:3000"  # Dify
```

#### 3. データベース接続エラー

```bash
# PostgreSQLログを確認
docker compose logs postgres

# Redisログを確認
docker compose logs redis

# 接続をテスト
docker compose exec postgres pg_isready
docker compose exec redis redis-cli ping
```

### Playwrightのデバッグ

```bash
# ヘッドフルモードで実行（ブラウザを表示）
pytest tests/e2e/ --headed

# スローモーションで実行
pytest tests/e2e/ --slowmo=1000

# デバッグモード
PWDEBUG=1 pytest tests/e2e/
```

## 今後の拡張

### 短期的な目標
- [ ] n8n API経由でのワークフロー作成テスト
- [ ] Dify API経由でのアプリ作成テスト
- [ ] ワークフロー実行結果の検証

### 中期的な目標
- [ ] Playwrightによる完全なE2Eテスト
- [ ] パフォーマンステスト
- [ ] 負荷テスト

### 長期的な目標
- [ ] ビジュアルリグレッションテスト
- [ ] セキュリティテスト
- [ ] カオスエンジニアリング

## 参考リソース

- [pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/python/)
- [httpx Documentation](https://www.python-httpx.org/)
- [Docker Compose Testing Best Practices](https://docs.docker.com/compose/testing/)

---

**更新日**: 2025-11-02  
**作成者**: @0xchoux1
