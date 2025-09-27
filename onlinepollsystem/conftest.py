import os
import django
from django.conf import settings

# Configure Django settings before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinepollsystem.settings')
django.setup()

import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import User

@pytest.fixture(scope='session')
def django_db_setup():
    """Setup test database"""
    pass

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user():
    """Create a test user and return it"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        password='testpass123'
    )
    return user

@pytest.fixture
def authenticated_client(authenticated_user):
    """Return an authenticated API client"""
    client = APIClient()
    token, created = Token.objects.get_or_create(user=authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client, authenticated_user

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Allow database access for all tests"""
    pass