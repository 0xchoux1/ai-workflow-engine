"""
Pytest configuration and shared fixtures
"""
import os
import pytest
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Service URLs
N8N_URL = os.getenv("N8N_URL", "http://localhost:5678")
DIFY_WEB_URL = os.getenv("DIFY_WEB_URL", "http://localhost:3000")
DIFY_API_URL = os.getenv("DIFY_API_URL", "http://localhost:5001")
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


@pytest.fixture(scope="session")
def n8n_url():
    """n8n service URL"""
    return N8N_URL


@pytest.fixture(scope="session")
def dify_web_url():
    """Dify web interface URL"""
    return DIFY_WEB_URL


@pytest.fixture(scope="session")
def dify_api_url():
    """Dify API URL"""
    return DIFY_API_URL


@pytest.fixture(scope="session")
def weaviate_url():
    """Weaviate vector database URL"""
    return WEAVIATE_URL


@pytest.fixture(scope="session")
def postgres_config():
    """PostgreSQL connection config"""
    return {
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "difyai123456"),
        "database": os.getenv("POSTGRES_DB", "dify"),
    }


@pytest.fixture(scope="session")
def redis_config():
    """Redis connection config"""
    return {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "password": os.getenv("REDIS_PASSWORD", "difyai123456"),
    }


@pytest.fixture
async def http_client():
    """Async HTTP client for testing"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client


@pytest.fixture
def sync_http_client():
    """Synchronous HTTP client for testing"""
    with httpx.Client(timeout=30.0) as client:
        yield client
