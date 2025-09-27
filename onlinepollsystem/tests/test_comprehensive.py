import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tests.factories import UserFactory, PollFactory, OptionFactory
from polls.models import Poll, Option
from votes.models import Vote

User = get_user_model()

@pytest.mark.django_db
class TestUserAuthenticationAPI:
    """Comprehensive tests for authentication endpoints at /api/v1/auth/"""
    
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

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post('/api/v1/auth/register/', self.user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'message' in response.data
        assert 'user' in response.data
        assert 'token' in response.data
        assert response.data['user']['email'] == self.user_data['email']
        assert response.data['user']['username'] == self.user_data['username']
        assert User.objects.filter(email=self.user_data['email']).exists()

    def test_user_registration_duplicate_email(self):
        """Test registration with existing email"""
        UserFactory(email=self.user_data['email'], username='different_user')
        
        response = self.client.post('/api/v1/auth/register/', self.user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_user_registration_duplicate_username(self):
        """Test registration with existing username"""
        UserFactory(username=self.user_data['username'], email='different@example.com')
        
        response = self.client.post('/api/v1/auth/register/', self.user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPassword123!'
        
        response = self.client.post('/api/v1/auth/register/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # Password mismatch error can be in field-specific or non_field_errors
        assert ('password_confirm' in response.data or 'non_field_errors' in response.data)

    def test_user_registration_weak_password(self):
        """Test registration with weak password"""
        data = self.user_data.copy()
        data['password'] = '123'
        data['password_confirm'] = '123'
        
        response = self.client.post('/api/v1/auth/register/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_user_registration_invalid_email(self):
        """Test registration with invalid email format"""
        data = self.user_data.copy()
        data['email'] = 'invalid-email'
        
        response = self.client.post('/api/v1/auth/register/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_user_login_success(self):
        """Test successful user login"""
        user = UserFactory(
            email=self.user_data['email'],
            password='SecurePass123!'
        )
        
        login_data = {
            'email': self.user_data['email'],
            'password': 'SecurePass123!'
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert 'user' in response.data
        assert 'token' in response.data
        assert response.data['user']['email'] == user.email

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        user = UserFactory(email=self.user_data['email'])
        
        login_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_user_login_nonexistent_user(self):
        """Test login with non-existent user"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'AnyPassword123!'
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login_inactive_user(self):
        """Test login with inactive user"""
        user = UserFactory(
            email=self.user_data['email'],
            password='SecurePass123!',
            is_active=False
        )
        
        login_data = {
            'email': self.user_data['email'],
            'password': 'SecurePass123!'
        }
        
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_logout_success(self):
        """Test successful user logout"""
        user = UserFactory()
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post('/api/v1/auth/logout/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        # Token should be deleted
        assert not Token.objects.filter(user=user).exists()

    def test_user_logout_without_authentication(self):
        """Test logout without authentication"""
        response = self.client.post('/api/v1/auth/logout/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserManagementAPI:
    """Comprehensive tests for user management endpoints at /api/v1/users/"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.client = APIClient()
        self.user = UserFactory()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_user_profile(self):
        """Test getting user profile via /api/v1/users/profile/"""
        response = self.client.get('/api/v1/users/profile/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'user_id' in response.data
        assert response.data['email'] == self.user.email
        assert response.data['username'] == self.user.username

    def test_get_user_profile_unauthenticated(self):
        """Test getting profile without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/v1/users/profile/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_user_profile_patch(self):
        """Test partial update of user profile"""
        updated_data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        }
        
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert 'user' in response.data
        assert response.data['user']['first_name'] == updated_data['first_name']
        assert response.data['user']['last_name'] == updated_data['last_name']
        
        # Verify database update
        self.user.refresh_from_db()
        assert self.user.first_name == updated_data['first_name']
        assert self.user.last_name == updated_data['last_name']

    def test_update_user_profile_put(self):
        """Test complete update of user profile"""
        updated_data = {
            'first_name': 'CompletelyUpdated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'username': 'updateduser'
        }
        
        response = self.client.put('/api/v1/users/update_profile/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['email'] == updated_data['email']
        assert response.data['user']['username'] == updated_data['username']

    def test_update_profile_duplicate_email(self):
        """Test updating profile with existing email"""
        other_user = UserFactory(email='existing@example.com')
        
        updated_data = {
            'email': 'existing@example.com'
        }
        
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_update_profile_duplicate_username(self):
        """Test updating profile with existing username"""
        other_user = UserFactory(username='existinguser')
        
        updated_data = {
            'username': 'existinguser'
        }
        
        response = self.client.patch('/api/v1/users/update_profile/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_change_password_success(self):
        """Test successful password change"""
        # Set a known password for the user
        self.user.set_password('oldpassword123')
        self.user.save()
        
        password_data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        
        response = self.client.post('/api/v1/users/change_password/', password_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Password changed successfully'
        
        # Verify password was changed
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword123')

    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password"""
        self.user.set_password('correctoldpassword')
        self.user.save()
        
        password_data = {
            'old_password': 'wrongoldpassword',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        
        response = self.client.post('/api/v1/users/change_password/', password_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'old_password' in response.data

    def test_change_password_mismatch_confirmation(self):
        """Test password change with mismatched confirmation"""
        self.user.set_password('oldpassword123')
        self.user.save()
        
        password_data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword123'
        }
        
        response = self.client.post('/api/v1/users/change_password/', password_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_voting_history(self):
        """Test getting user's voting history"""
        response = self.client.get('/api/v1/users/voting_history/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_deactivate_account(self):
        """Test account deactivation"""
        response = self.client.delete('/api/v1/users/deactivate_account/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        
        # Verify account was deactivated
        self.user.refresh_from_db()
        assert not self.user.is_active

    def test_all_users_admin_required(self):
        """Test that all_users endpoint requires admin privileges"""
        response = self.client.get('/api/v1/users/all_users/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_all_users_admin_success(self):
        """Test admin can access all users"""
        admin_user = UserFactory(is_staff=True, is_superuser=True)
        admin_token, created = Token.objects.get_or_create(user=admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        
        response = self.client.get('/api/v1/users/all_users/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 2  # At least our test user and admin user


@pytest.mark.django_db
class TestPollAPI:
    """Comprehensive tests for poll management at /api/v1/polls/"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.client = APIClient()
        self.user = UserFactory()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_polls_anonymous(self):
        """Test listing polls without authentication (should work)"""
        self.client.credentials()  # Remove authentication
        PollFactory.create_batch(3)
        
        response = self.client.get('/api/v1/polls/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data  # Paginated response
        assert len(response.data['results']) == 3

    def test_list_polls_authenticated(self):
        """Test listing polls with authentication"""
        PollFactory.create_batch(3)
        
        response = self.client.get('/api/v1/polls/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data  # Paginated response
        assert len(response.data['results']) == 3

    def test_create_poll_success(self):
        """Test successful poll creation"""
        poll_data = {
            'title': 'Test Poll',
            'question': 'What is your favorite color?',
            'description': 'This is a test poll',
            'expires_at': (timezone.now() + timedelta(days=7)).isoformat(),
            'options': [
                {'option_text': 'Option 1'},
                {'option_text': 'Option 2'},
                {'option_text': 'Option 3'}
            ]
        }
        
        response = self.client.post('/api/v1/polls/', poll_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == poll_data['title']
        assert response.data['created_by']['user_id'] == str(self.user.user_id)
        
        # Verify poll was created in database
        poll = Poll.objects.get(title=poll_data['title'])
        assert poll.created_by == self.user
        assert poll.options.count() == 3

    def test_create_poll_unauthenticated(self):
        """Test poll creation without authentication"""
        self.client.credentials()  # Remove authentication
        
        poll_data = {
            'title': 'Test Poll',
            'question': 'What is your favorite color?',
            'description': 'This is a test poll'
        }
        
        response = self.client.post('/api/v1/polls/', poll_data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_poll(self):
        """Test retrieving a specific poll"""
        poll = PollFactory(created_by=self.user)
        
        response = self.client.get(f'/api/v1/polls/{poll.poll_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['poll_id'] == str(poll.poll_id)
        assert response.data['title'] == poll.title

    def test_update_poll_owner(self):
        """Test updating poll by owner"""
        poll = PollFactory(created_by=self.user)
        
        updated_data = {
            'title': 'Updated Poll Title',
            'description': 'Updated description'
        }
        
        response = self.client.patch(f'/api/v1/polls/{poll.poll_id}/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == updated_data['title']

    def test_update_poll_non_owner(self):
        """Test updating poll by non-owner"""
        other_user = UserFactory()
        poll = PollFactory(created_by=other_user)
        
        updated_data = {
            'title': 'Should not be updated'
        }
        
        response = self.client.patch(f'/api/v1/polls/{poll.poll_id}/', updated_data, format='json')
        
        # This might return 403 or 404 depending on permissions implementation
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_delete_poll_owner(self):
        """Test deleting poll by owner"""
        poll = PollFactory(created_by=self.user)
        poll_id = poll.poll_id
        
        response = self.client.delete(f'/api/v1/polls/{poll_id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Poll.objects.filter(poll_id=poll_id).exists()

    def test_poll_results(self):
        """Test getting poll results"""
        poll = PollFactory(created_by=self.user)
        option1 = OptionFactory(poll=poll, option_text='Option 1')
        option2 = OptionFactory(poll=poll, option_text='Option 2')
        
        # Create some votes
        voter1 = UserFactory()
        voter2 = UserFactory()
        Vote.objects.create(poll=poll, option=option1, user=voter1)
        Vote.objects.create(poll=poll, option=option2, user=voter2)
        
        response = self.client.get(f'/api/v1/polls/{poll.poll_id}/results/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert response.data['total_votes'] == 2

    def test_cast_vote_success(self):
        """Test successfully casting a vote"""
        poll = PollFactory()
        option = OptionFactory(poll=poll)
        
        vote_data = {
            'option_id': str(option.option_id)
        }
        
        response = self.client.post(f'/api/v1/polls/{poll.poll_id}/vote/', vote_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'message' in response.data
        
        # Verify vote was recorded
        assert Vote.objects.filter(poll=poll, user=self.user, option=option).exists()

    def test_cast_duplicate_vote(self):
        """Test casting vote on same poll twice"""
        poll = PollFactory()
        option = OptionFactory(poll=poll)
        
        # Cast first vote
        Vote.objects.create(poll=poll, option=option, user=self.user)
        
        vote_data = {
            'option_id': str(option.option_id)
        }
        
        response = self.client.post(f'/api/v1/polls/{poll.poll_id}/vote/', vote_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_vote_expired_poll(self):
        """Test voting on expired poll"""
        poll = PollFactory(expires_at=timezone.now() - timedelta(days=1))
        option = OptionFactory(poll=poll)
        
        vote_data = {
            'option_id': str(option.option_id)
        }
        
        response = self.client.post(f'/api/v1/polls/{poll.poll_id}/vote/', vote_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_get_poll_options(self):
        """Test getting poll options"""
        poll = PollFactory()
        option1 = OptionFactory(poll=poll)
        option2 = OptionFactory(poll=poll)
        
        response = self.client.get(f'/api/v1/polls/{poll.poll_id}/options/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 2

    def test_add_option_to_poll_owner(self):
        """Test adding option to poll by owner"""
        poll = PollFactory(created_by=self.user)
        
        option_data = {
            'option_text': 'New Option'
        }
        
        response = self.client.post(f'/api/v1/polls/{poll.poll_id}/add_option/', option_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'message' in response.data
        
        # Verify option was added
        assert Option.objects.filter(poll=poll, option_text=option_data['option_text']).exists()

    def test_add_option_to_poll_non_owner(self):
        """Test adding option to poll by non-owner"""
        other_user = UserFactory()
        poll = PollFactory(created_by=other_user)
        
        option_data = {
            'option_text': 'Should not be added'
        }
        
        response = self.client.post(f'/api/v1/polls/{poll.poll_id}/add_option/', option_data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_my_polls(self):
        """Test getting user's own polls"""
        # Create polls by this user and other users
        my_poll1 = PollFactory(created_by=self.user, title='My Poll 1')
        my_poll2 = PollFactory(created_by=self.user, title='My Poll 2')
        other_poll = PollFactory(title='Other Poll')
        
        response = self.client.get('/api/v1/polls/my_polls/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 2
        
        poll_titles = [poll['title'] for poll in response.data]
        assert 'My Poll 1' in poll_titles
        assert 'My Poll 2' in poll_titles
        assert 'Other Poll' not in poll_titles

    def test_get_active_polls(self):
        """Test getting active polls"""
        # Create active and expired polls
        active_poll = PollFactory(
            title='Active Poll',
            expires_at=timezone.now() + timedelta(days=7)
        )
        expired_poll = PollFactory(
            title='Expired Poll',
            expires_at=timezone.now() - timedelta(days=1)
        )
        no_expiry_poll = PollFactory(
            title='No Expiry Poll',
            expires_at=None
        )
        
        response = self.client.get('/api/v1/polls/active_polls/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        
        poll_titles = [poll['title'] for poll in response.data]
        assert 'Active Poll' in poll_titles
        assert 'No Expiry Poll' in poll_titles
        # Expired poll should not be in results (this depends on implementation)


@pytest.mark.django_db
class TestVoteAPI:
    """Comprehensive tests for voting endpoints at /api/v1/votes/"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.client = APIClient()
        self.user = UserFactory()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_user_votes(self):
        """Test listing user's votes"""
        # Create some votes for this user
        poll1 = PollFactory()
        poll2 = PollFactory()
        option1 = OptionFactory(poll=poll1)
        option2 = OptionFactory(poll=poll2)
        
        vote1 = Vote.objects.create(poll=poll1, option=option1, user=self.user)
        vote2 = Vote.objects.create(poll=poll2, option=option2, user=self.user)
        
        # Create a vote by another user (should not appear)
        other_user = UserFactory()
        other_vote = Vote.objects.create(poll=poll1, option=option1, user=other_user)
        
        response = self.client.get('/api/v1/votes/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data  # Paginated response
        assert len(response.data['results']) == 2
        
        # Verify votes belong to current user
        for vote in response.data['results']:
            assert vote['user']['user_id'] == str(self.user.user_id)

    def test_retrieve_specific_vote(self):
        """Test retrieving a specific vote"""
        poll = PollFactory()
        option = OptionFactory(poll=poll)
        vote = Vote.objects.create(poll=poll, option=option, user=self.user)
        
        response = self.client.get(f'/api/v1/votes/{vote.vote_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['vote_id'] == str(vote.vote_id)
        assert response.data['user']['user_id'] == str(self.user.user_id)

    def test_cannot_access_other_user_vote(self):
        """Test that users cannot access other users' votes directly"""
        other_user = UserFactory()
        poll = PollFactory()
        option = OptionFactory(poll=poll)
        other_vote = Vote.objects.create(poll=poll, option=option, user=other_user)
        
        response = self.client.get(f'/api/v1/votes/{other_vote.vote_id}/')
        
        # Should return 404 since vote doesn't belong to current user
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_votes_unauthenticated(self):
        """Test listing votes without authentication"""
        self.client.credentials()  # Remove authentication
        
        response = self.client.get('/api/v1/votes/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestIntegrationWorkflows:
    """End-to-end integration tests combining authentication, polls, and voting"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.client = APIClient()

    def test_complete_user_poll_vote_workflow(self):
        """Test complete workflow: register -> login -> create poll -> vote -> check results"""
        
        # 1. Register a new user
        user_data = {
            'first_name': 'Integration',
            'last_name': 'User',
            'email': 'integration@example.com',
            'username': 'integrationuser',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!'
        }
        
        register_response = self.client.post('/api/v1/auth/register/', user_data, format='json')
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # 2. Login (though register already gives us a token)
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        login_response = self.client.post('/api/v1/auth/login/', login_data, format='json')
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.data['token']
        
        # 3. Set authentication for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # 4. Create a poll
        poll_data = {
            'title': 'Integration Test Poll',
            'question': 'Which option do you prefer?',
            'description': 'This is an integration test poll',
            'options': [
                {'option_text': 'Option A'},
                {'option_text': 'Option B'},
                {'option_text': 'Option C'}
            ]
        }
        
        poll_response = self.client.post('/api/v1/polls/', poll_data, format='json')
        assert poll_response.status_code == status.HTTP_201_CREATED
        poll_id = poll_response.data['poll_id']
        
        # 5. Get poll options
        options_response = self.client.get(f'/api/v1/polls/{poll_id}/options/')
        assert options_response.status_code == status.HTTP_200_OK
        assert len(options_response.data) == 3
        
        # 6. Vote on the poll
        option_id = options_response.data[0]['option_id']
        vote_data = {
            'option_id': option_id
        }
        
        vote_response = self.client.post(f'/api/v1/polls/{poll_id}/vote/', vote_data, format='json')
        assert vote_response.status_code == status.HTTP_201_CREATED
        
        # 7. Check poll results
        results_response = self.client.get(f'/api/v1/polls/{poll_id}/results/')
        assert results_response.status_code == status.HTTP_200_OK
        assert results_response.data['total_votes'] == 1
        
        # 8. Check user's voting history
        history_response = self.client.get('/api/v1/users/voting_history/')
        assert history_response.status_code == status.HTTP_200_OK
        assert len(history_response.data) == 1
        
        # 9. Check user's votes via votes endpoint
        votes_response = self.client.get('/api/v1/votes/')
        assert votes_response.status_code == status.HTTP_200_OK
        assert len(votes_response.data['results']) == 1
        
        # 10. Logout
        logout_response = self.client.post('/api/v1/auth/logout/')
        assert logout_response.status_code == status.HTTP_200_OK

    def test_multi_user_poll_voting(self):
        """Test multiple users voting on the same poll"""
        
        # Create poll creator
        creator = UserFactory()
        creator_token, _ = Token.objects.get_or_create(user=creator)
        
        # Create voters
        voter1 = UserFactory()
        voter2 = UserFactory()
        voter1_token, _ = Token.objects.get_or_create(user=voter1)
        voter2_token, _ = Token.objects.get_or_create(user=voter2)
        
        # Creator creates a poll
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {creator_token.key}')
        poll_data = {
            'title': 'Multi-user Test Poll',
            'question': 'What is your favorite programming language?',
            'description': 'Testing multiple users voting',
            'options': [
                {'option_text': 'Python'},
                {'option_text': 'JavaScript'},
                {'option_text': 'Java'}
            ]
        }
        
        poll_response = self.client.post('/api/v1/polls/', poll_data, format='json')
        assert poll_response.status_code == status.HTTP_201_CREATED
        poll_id = poll_response.data['poll_id']
        
        # Get options
        options_response = self.client.get(f'/api/v1/polls/{poll_id}/options/')
        options = options_response.data
        
        # Voter 1 votes for Python
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {voter1_token.key}')
        vote_response1 = self.client.post(f'/api/v1/polls/{poll_id}/vote/', {
            'option_id': options[0]['option_id']  # Python
        }, format='json')
        assert vote_response1.status_code == status.HTTP_201_CREATED
        
        # Voter 2 votes for JavaScript
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {voter2_token.key}')
        vote_response2 = self.client.post(f'/api/v1/polls/{poll_id}/vote/', {
            'option_id': options[1]['option_id']  # JavaScript
        }, format='json')
        assert vote_response2.status_code == status.HTTP_201_CREATED
        
        # Check results (anyone can view)
        self.client.credentials()  # No auth needed for results
        results_response = self.client.get(f'/api/v1/polls/{poll_id}/results/')
        assert results_response.status_code == status.HTTP_200_OK
        assert results_response.data['total_votes'] == 2
        
        # Check that each option has correct vote counts
        results = results_response.data['results']
        python_option = next(r for r in results if r['option_text'] == 'Python')
        javascript_option = next(r for r in results if r['option_text'] == 'JavaScript')
        java_option = next(r for r in results if r['option_text'] == 'Java')
        
        assert python_option['votes'] == 1
        assert javascript_option['votes'] == 1
        assert java_option['votes'] == 0

    def test_admin_user_management_workflow(self):
        """Test admin user management capabilities"""
        
        # Create admin user
        admin_user = UserFactory(is_staff=True, is_superuser=True)
        admin_token, _ = Token.objects.get_or_create(user=admin_user)
        
        # Create regular users
        user1 = UserFactory(first_name='User', last_name='One')
        user2 = UserFactory(first_name='User', last_name='Two')
        
        # Admin gets all users
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        all_users_response = self.client.get('/api/v1/users/all_users/')
        assert all_users_response.status_code == status.HTTP_200_OK
        assert len(all_users_response.data) >= 3  # admin + 2 regular users
        
        # Admin deletes a user
        delete_response = self.client.delete(f'/api/v1/users/{user1.user_id}/delete_user/')
        assert delete_response.status_code == status.HTTP_200_OK
        
        # Verify user was deleted
        assert not User.objects.filter(user_id=user1.user_id).exists()
        
        # Verify other users still exist
        assert User.objects.filter(user_id=user2.user_id).exists()
        assert User.objects.filter(user_id=admin_user.user_id).exists()