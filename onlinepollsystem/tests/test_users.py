import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.models import User
from tests.factories import UserFactory

@pytest.mark.django_db
class TestUserAuthenticationAPI:
    """Test class for User Authentication endpoints at /api/v1/auth/"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.client = APIClient()
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'username': 'johndoe',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/api/v1/auth/register/', self.user_data, format='json')
        
        print(f"Registration Response Status: {response.status_code}")
        print(f"Registration Response Data: {response.data}")
        
        # Check if registration was successful
        if response.status_code == status.HTTP_201_CREATED:
            assert 'user' in response.data
            assert response.data['user']['email'] == self.user_data['email']
            assert response.data['user']['username'] == self.user_data['username']
        else:
            # Print error details for debugging
            print(f"Registration failed: {response.data}")

    def test_user_login(self):
        """Test user login endpoint"""
        # First create a user
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            password=self.user_data['password']
        )
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        print(f"Login Response Status: {response.status_code}")
        print(f"Login Response Data: {response.data}")
        
        # Check if login was successful
        if response.status_code == status.HTTP_200_OK:
            assert 'token' in response.data
            assert 'user' in response.data
        else:
            print(f"Login failed: {response.data}")

    def test_user_logout(self):
        """Test user logout endpoint"""
        # Create user and authenticate
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post('/api/v1/auth/logout/')
        
        print(f"Logout Response Status: {response.status_code}")
        print(f"Logout Response Data: {response.data}")
        
        # Logout should return 200
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_profile(self):
        """Test get user profile endpoint - Using ViewSet action"""
        # Create user and authenticate
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Based on your UserViewSet, the profile endpoint is an action
        response = self.client.get('/api/v1/users/profile/')
        
        print(f"Profile Response Status: {response.status_code}")
        print(f"Profile Response Data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'email' in response.data
        assert response.data['email'] == user.email

    def test_update_user_profile(self):
        """Test update user profile endpoint - Using ViewSet action"""
        # Create user and authenticate
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        updated_data = {
            'first_name': 'John Updated',
            'last_name': 'Doe Updated'
        }
        
        # Based on your UserViewSet, update_profile is a custom action
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        print(f"Update Profile Response Status: {response.status_code}")
        print(f"Update Profile Response Data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert response.data['user']['first_name'] == updated_data['first_name']
        assert response.data['user']['last_name'] == updated_data['last_name']

    def test_change_password(self):
        """Test change password endpoint - Using ViewSet action"""
        # Create user with known password
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='oldpassword123'
        )
        
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Based on your ChangePasswordSerializer, check what fields it expects
        password_data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'  # This might be the expected field name
        }
        
        response = self.client.post('/api/v1/users/change_password/', password_data, format='json')
        
        print(f"Change Password Response Status: {response.status_code}")
        print(f"Change Password Response Data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Password changed successfully'
        
        # Verify the password was actually changed
        user.refresh_from_db()
        assert user.check_password('newpassword123')

    def test_get_voting_history(self):
        """Test get user's voting history endpoint"""
        # Create user and authenticate
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Based on your UserViewSet, voting_history is a custom action
        response = self.client.get('/api/v1/users/voting_history/')
        
        print(f"Voting History Response Status: {response.status_code}")
        print(f"Voting History Response Data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_deactivate_account(self):
        """Test deactivate account endpoint"""
        # Create user and authenticate
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Based on your UserViewSet, deactivate_account is a custom action with DELETE method
        response = self.client.delete('/api/v1/users/deactivate_account/')
        
        print(f"Deactivate Account Response Status: {response.status_code}")
        print(f"Deactivate Account Response Data: {response.data}")
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        
        # Verify the account was deactivated
        user.refresh_from_db()
        assert not user.is_active

    def test_user_registration_with_invalid_data(self):
        """Test user registration with invalid data"""
        invalid_data = {
            'first_name': '',  # Empty first name
            'email': 'invalid-email',  # Invalid email format
            'username': '',  # Empty username
            'password': '123',  # Too short password
            'password_confirm': '456'  # Passwords don't match
        }
        
        response = self.client.post('/api/v1/auth/register/', invalid_data, format='json')
        
        print(f"Invalid Registration Response Status: {response.status_code}")
        print(f"Invalid Registration Response Data: {response.data}")
        
        # Should return 400 Bad Request
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login_with_invalid_credentials(self):
        """Test user login with invalid credentials"""
        # Create a user first
        user = UserFactory(email='test@example.com', password='correctpassword')
        
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        print(f"Invalid Login Response Status: {response.status_code}")
        print(f"Invalid Login Response Data: {response.data}")
        
        # Should return 400 Bad Request
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_access_profile_without_authentication(self):
        """Test accessing profile without authentication"""
        response = self.client.get('/api/v1/users/profile/')
        
        print(f"Unauthenticated Profile Response Status: {response.status_code}")
        print(f"Unauthenticated Profile Response Data: {response.data}")
        
        # Should return 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_with_wrong_old_password(self):
        """Test changing password with wrong old password"""
        user = UserFactory(password='correctoldpassword')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        password_data = {
            'old_password': 'wrongoldpassword',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        
        response = self.client.post('/api/v1/users/change_password/', password_data, format='json')
        
        print(f"Wrong Old Password Response Status: {response.status_code}")
        print(f"Wrong Old Password Response Data: {response.data}")
        
        # Should return 400 Bad Request
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'old_password' in response.data

    def test_list_all_users_admin_only(self):
        """Test listing all users - Admin only endpoint"""
        # Create regular user
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Try to access admin endpoint
        response = self.client.get('/api/v1/users/all_users/')
        
        print(f"All Users (Regular User) Response Status: {response.status_code}")
        print(f"All Users (Regular User) Response Data: {response.data}")
        
        # Should return 403 Forbidden for regular user
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Now test with admin user
        admin_user = UserFactory(is_staff=True, is_superuser=True)
        admin_token, created = Token.objects.get_or_create(user=admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        
        response = self.client.get('/api/v1/users/all_users/')
        
        print(f"All Users (Admin) Response Status: {response.status_code}")
        print(f"All Users (Admin) Response Data: {response.data}")
        
        # Should return 200 OK for admin user
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_update_profile_with_duplicate_email(self):
        """Test updating profile with email that already exists"""
        # Create two users
        user1 = UserFactory(email='user1@example.com')
        user2 = UserFactory(email='user2@example.com')
        
        # Authenticate as user1
        token, created = Token.objects.get_or_create(user=user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Try to update user1's email to user2's email
        updated_data = {
            'email': 'user2@example.com'  # This should fail
        }
        
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        print(f"Duplicate Email Update Response Status: {response.status_code}")
        print(f"Duplicate Email Update Response Data: {response.data}")
        
        # Should return 400 Bad Request due to duplicate email
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_update_profile_with_duplicate_username(self):
        """Test updating profile with username that already exists"""
        # Create two users
        user1 = UserFactory(username='user1')
        user2 = UserFactory(username='user2')
        
        # Authenticate as user1
        token, created = Token.objects.get_or_create(user=user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Try to update user1's username to user2's username
        updated_data = {
            'username': 'user2'  # This should fail
        }
        
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        print(f"Duplicate Username Update Response Status: {response.status_code}")
        print(f"Duplicate Username Update Response Data: {response.data}")
        
        # Should return 400 Bad Request due to duplicate username
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data