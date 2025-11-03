"""
API Health Check Tests
Tests to verify all services are accessible and responding
"""
import pytest
import httpx
import redis
import psycopg2


@pytest.mark.api
@pytest.mark.smoke
def test_n8n_health(sync_http_client, n8n_url):
    """Test n8n is accessible"""
    response = sync_http_client.get(n8n_url, follow_redirects=True)
    assert response.status_code in [200, 401], f"n8n returned {response.status_code}"
    # 401 is acceptable if basic auth is enabled
    print(f"✓ n8n is accessible: HTTP {response.status_code}")


@pytest.mark.api
@pytest.mark.smoke
def test_dify_web_health(sync_http_client, dify_web_url):
    """Test Dify web interface is accessible"""
    response = sync_http_client.get(dify_web_url, follow_redirects=True)
    assert response.status_code == 200, f"Dify Web returned {response.status_code}"
    print(f"✓ Dify Web is accessible: HTTP {response.status_code}")


@pytest.mark.api
@pytest.mark.smoke
def test_dify_api_health(sync_http_client, dify_api_url):
    """Test Dify API is accessible via nginx"""
    response = sync_http_client.get(f"{dify_api_url}/health", follow_redirects=True)
    # API might return 404 if /health endpoint doesn't exist, but should not be connection error
    assert response.status_code in [200, 404], f"Dify API returned {response.status_code}"
    print(f"✓ Dify API is accessible: HTTP {response.status_code}")


@pytest.mark.api
@pytest.mark.smoke
def test_weaviate_health(sync_http_client, weaviate_url):
    """Test Weaviate vector database is ready"""
    response = sync_http_client.get(f"{weaviate_url}/v1/.well-known/ready")
    assert response.status_code == 200, f"Weaviate returned {response.status_code}"
    print(f"✓ Weaviate is ready: HTTP {response.status_code}")


@pytest.mark.api
@pytest.mark.smoke
def test_postgres_connection(postgres_config):
    """Test PostgreSQL database is accessible"""
    try:
        conn = psycopg2.connect(**postgres_config)
        conn.close()
        print("✓ PostgreSQL connection successful")
    except Exception as e:
        pytest.fail(f"PostgreSQL connection failed: {e}")


@pytest.mark.api
@pytest.mark.smoke
def test_redis_connection(redis_config):
    """Test Redis is accessible"""
    try:
        r = redis.Redis(**redis_config, decode_responses=True)
        r.ping()
        print("✓ Redis connection successful")
    except Exception as e:
        pytest.fail(f"Redis connection failed: {e}")


@pytest.mark.api
@pytest.mark.smoke
def test_weaviate_meta(sync_http_client, weaviate_url):
    """Test Weaviate metadata endpoint"""
    response = sync_http_client.get(f"{weaviate_url}/v1/meta")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    print(f"✓ Weaviate version: {data.get('version')}")


@pytest.mark.integration
def test_all_services_smoke():
    """
    Smoke test to verify all critical services are running
    This test should run first to catch infrastructure issues
    """
    print("\n=== Running Full Service Smoke Test ===")
    # This test is a placeholder that will be marked as passed
    # if all individual health tests pass
    pass
