import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, PollFactory, OptionFactory
from users.models import User
from polls.models import Poll, Option

@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_user_registration(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        response = self.client.post('/api/v1/auth/register/', user_data, format='json')
        
        # assert response.status_code == status.HTTP_201_CREATED
        # assert 'user' in response.data
        # assert response.data['user']['email'] == user_data['email']

    def test_user_login(self):
        user = UserFactory()
        user.set_password('password123')
        user.save()
        
        login_data = {
            'email': user.email,
            'password': 'password123'
        }
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        # assert response.status_code == status.HTTP_200_OK
        # assert 'token' in response.data

    def test_get_user_profile(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/v1/users/profile/')
        
        # assert response.status_code == status.HTTP_200_OK
        # assert response.data['email'] == user.email

@pytest.mark.django_db  
class TestPollAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_create_poll(self):
        self.client.force_authenticate(user=self.user)
        
        poll_data = {
            'title': 'Test Poll',
            'description': 'Test Description',
            'options': ['Option 1', 'Option 2', 'Option 3']
        }
        response = self.client.post('/api/v1/polls/', poll_data, format='json')
        
        # assert response.status_code == status.HTTP_201_CREATED
        # assert response.data['title'] == poll_data['title']

    def test_list_polls(self):
        poll = PollFactory(created_by=self.user)
        
        response = self.client.get('/api/v1/polls/')
        
        # assert response.status_code == status.HTTP_200_OK
        # assert len(response.data) >= 1

    def test_get_poll_detail(self):
        poll = PollFactory(created_by=self.user)
        
        response = self.client.get(f'/api/v1/polls/{poll.poll_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == poll.title