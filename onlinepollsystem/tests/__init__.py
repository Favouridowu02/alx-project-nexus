from django.contrib.auth import get_user_model
import pytest

@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(username='john', email='john@example.com', password='password123')
    return user