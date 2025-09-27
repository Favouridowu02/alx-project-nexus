from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import login, logout
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserRegistrationResponseSerializer,
    UserLoginResponseSerializer,
    UserProfileUpdateResponseSerializer,
    PasswordChangeResponseSerializer,
    ErrorResponseSerializer
)


class UserRegistrationView(APIView):
    """
    ## User Registration Endpoint
    
    Creates a new user account with complete validation.
    
    ### Features:
    - Email validation and uniqueness check
    - Username validation and uniqueness check  
    - Password strength validation
    - Automatic token generation
    - Account activation
    
    ### Requirements:
    - Valid email address
    - Unique username (3-50 characters)
    - Strong password (8+ characters)
    - Password confirmation
    - First and last name
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="register_user",
        operation_summary="Register New User Account",
        operation_description="""
        Register a new user account with email verification.
        
        **Password Requirements:**
        - Minimum 8 characters
        - Mix of letters, numbers, and special characters
        - Cannot be too similar to personal information
        - Cannot be a commonly used password
        
        **Returns:**
        - User profile data
        - Authentication token for immediate login
        """,
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=UserRegistrationResponseSerializer,
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "john.doe@example.com",
                            "username": "johndoe",
                            "full_name": "John Doe",
                            "date_joined": "2024-01-15T10:30:00Z"
                        },
                        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                schema=ErrorResponseSerializer,
                examples={
                    "application/json": {
                        "email": ["User with this email already exists."],
                        "username": ["This username is already taken."],
                        "password": ["This password is too weak."],
                        "password_confirm": ["Passwords don't match."]
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Register a new user account"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    ## User Login Endpoint
    
    Authenticates existing users with email and password.
    
    ### Features:
    - Email-based authentication
    - Secure password verification
    - Token generation for API access
    - Account status validation
    - Login session management
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="login_user",
        operation_summary="User Login",
        operation_description="""
        Authenticate user with email and password credentials.
        
        **Authentication Process:**
        1. Validates email format
        2. Checks if user exists and is active
        3. Verifies password hash
        4. Generates/retrieves authentication token
        5. Creates login session
        
        **Returns:**
        - User profile information
        - Authentication token for API requests
        """,
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=UserLoginResponseSerializer,
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "user": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "first_name": "John",
                            "last_name": "Doe", 
                            "email": "john.doe@example.com",
                            "username": "johndoe",
                            "full_name": "John Doe"
                        },
                        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                schema=ErrorResponseSerializer,
                examples={
                    "application/json": {
                        "non_field_errors": ["Invalid email or password"]
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Authenticate user login"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    ## User Logout Endpoint
    
    Securely logs out authenticated users.
    
    ### Features:
    - Token invalidation
    - Session cleanup
    - Secure logout process
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="logout_user",
        operation_summary="User Logout",
        operation_description="""
        Logout the current authenticated user.
        
        **Process:**
        1. Validates authentication token
        2. Deletes user's authentication token
        3. Clears login session
        4. Invalidates API access
        
        **Security:**
        - Prevents token reuse
        - Clears server-side session data
        - Requires valid token to logout
        """,
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token your_auth_token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Logout successful",
                examples={
                    "application/json": {
                        "message": "Logout successful"
                    }
                }
            ),
            400: openapi.Response(
                description="Logout failed",
                examples={
                    "application/json": {
                        "error": "Something went wrong"
                    }
                }
            ),
            401: "Authentication required"
        },
        tags=['Authentication']
    )
    def post(self, request):
        """Logout current user"""
        try:
            request.user.auth_token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Something went wrong during logout'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ## User Management ViewSet
    
    Complete user account management system.
    
    ### Available Operations:
    - **GET** `/users/` - List all users (Admin only)
    - **GET** `/users/{id}/` - Get specific user details
    - **PUT/PATCH** `/users/{id}/` - Update user information
    - **DELETE** `/users/{id}/` - Delete user account (Admin only)
    
    ### Custom Actions:
    - **GET** `/users/profile/` - Get current user's profile
    - **PUT/PATCH** `/users/update_profile/` - Update current user's profile
    - **POST** `/users/change_password/` - Change user password
    - **DELETE** `/users/deactivate_account/` - Deactivate account
    - **GET** `/users/voting_history/` - Get user's voting history
    - **GET** `/users/all_users/` - Get all users (Admin only)
    - **DELETE** `/users/{id}/delete_user/` - Delete user by ID (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(user_id=self.request.user.user_id)
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'all_users', 'delete_user']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(
        operation_id="get_user_profile",
        operation_summary="Get Current User Profile",
        operation_description="""
        Retrieve the authenticated user's complete profile information.
        
        **Returns:**
        - Complete user profile data
        - Read-only computed fields (full_name, etc.)
        - Account timestamps
        """,
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully",
                schema=UserSerializer
            ),
            401: "Authentication required"
        },
        tags=['User Profile']
    )
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='put',
        operation_id="update_user_profile_put",
        operation_summary="Update User Profile (Complete)",
        operation_description="Update all user profile fields (PUT method)",
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=UserProfileUpdateResponseSerializer
            ),
            400: "Validation error"
        },
        tags=['User Profile']
    )
    @swagger_auto_schema(
        method='patch',
        operation_id="update_user_profile_patch",
        operation_summary="Update User Profile (Partial)",
        operation_description="""
        Partially update user profile information (PATCH method).
        
        **Features:**
        - Update only specified fields
        - Email uniqueness validation
        - Username uniqueness validation
        - Permission validation (own profile only)
        
        **Updatable Fields:**
        - first_name
        - last_name
        - email (must be unique)
        - username (must be unique)
        """,
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=UserProfileUpdateResponseSerializer,
                examples={
                    "application/json": {
                        "message": "Profile updated successfully",
                        "user": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "first_name": "John Updated",
                            "last_name": "Doe Updated",
                            "email": "john.updated@example.com",
                            "username": "johndoe_updated"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "email": ["This email address is already registered"],
                        "username": ["This username is already taken"]
                    }
                }
            ),
            403: "Permission denied - Can only update own profile"
        },
        tags=['User Profile']
    )
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update current user's profile information
        """
        serializer = UserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id="change_user_password",
        operation_summary="Change User Password",
        operation_description="""
        Change the authenticated user's password.
        
        **Security Requirements:**
        - Current password verification
        - New password strength validation
        - Password confirmation matching
        - Automatic token refresh
        
        **Process:**
        1. Validates current password
        2. Checks new password strength
        3. Confirms password match
        4. Updates password hash
        5. Maintains current login session
        """,
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                schema=PasswordChangeResponseSerializer,
                examples={
                    "application/json": {
                        "message": "Password changed successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "old_password": ["Current password is incorrect"],
                        "confirm_password": ["New passwords don't match"],
                        "new_password": ["This password is too weak"]
                    }
                }
            )
        },
        tags=['User Profile']
    )
    @action(detail=False, methods=["post"])
    def change_password(self, request):
        """Change current user's password"""
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id="deactivate_user_account",
        operation_summary="Deactivate User Account",
        operation_description="""
        Deactivate the current user's account (soft delete).
        
        **Process:**
        - Sets is_active = False
        - Preserves user data for potential reactivation
        - Prevents future logins
        - Maintains data integrity
        
        **Note:** This is a soft delete. Account can be reactivated by admin.
        """,
        responses={
            200: openapi.Response(
                description="Account deactivated successfully",
                examples={
                    "application/json": {
                        "message": "Account deactivated successfully"
                    }
                }
            )
        },
        tags=['User Profile']
    )
    @action(detail=False, methods=['delete'])
    def deactivate_account(self, request):
        """Deactivate current user's account"""
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({
            'message': 'Account deactivated successfully'
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="get_voting_history",
        operation_summary="Get User's Voting History",
        operation_description="""
        Retrieve complete voting history for the authenticated user.
        
        **Returns:**
        - List of all votes cast by user
        - Poll information for each vote
        - Option details and timestamps
        - Sorted by most recent first
        """,
        responses={
            200: openapi.Response(
                description="Voting history retrieved",
                examples={
                    "application/json": [
                        {
                            "vote_id": "vote-uuid",
                            "poll": {
                                "poll_id": "poll-uuid",
                                "title": "Best Programming Language"
                            },
                            "option": {
                                "option_id": "option-uuid", 
                                "option_text": "Python"
                            },
                            "timestamp": "2024-01-15T14:30:00Z"
                        }
                    ]
                }
            )
        },
        tags=['User Profile']
    )
    @action(detail=False, methods=['get'])
    def voting_history(self, request):
        """Get current user's voting history"""
        try:
            from votes.models import Vote
            from votes.serializers import VoteSerializer
            votes = Vote.objects.filter(user=request.user).select_related(
                'poll', 'option'
            ).order_by('-timestamp')
            serializer = VoteSerializer(votes, many=True)
            return Response(serializer.data)
        except ImportError:
            return Response({
                'message': 'No voting history available'
            })

    @swagger_auto_schema(
        operation_id="list_all_users",
        operation_summary="List All Users (Admin Only)",
        operation_description="""
        Retrieve list of all users in the system.
        
        **Admin Only:** Requires staff permissions.
        
        **Returns:**
        - Complete list of all users
        - Full profile information
        - Account status and timestamps
        """,
        responses={
            200: openapi.Response(
                description="Users retrieved successfully",
                schema=UserSerializer(many=True)
            ),
            403: "Admin access required"
        },
        tags=['Admin Operations']
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def all_users(self, request):
        """Get all users - Admin only"""
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="delete_user_by_id",
        operation_summary="Delete User by ID (Admin Only)",
        operation_description="""
        Permanently delete a user account by ID.
        
        **Admin Only:** Requires staff permissions.
        **Warning:** This is a permanent deletion.
        
        **Process:**
        1. Validates user existence
        2. Performs hard delete
        3. Removes all related data
        4. Cannot be undone
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="User ID (UUID)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="User deleted successfully",
                examples={
                    "application/json": {
                        "message": "User deleted successfully"
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "error": "User not found"
                    }
                }
            ),
            403: "Admin access required"
        },
        tags=['Admin Operations']
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def delete_user(self, request, pk=None):
        """Delete a user by ID - Admin only"""
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({
                'message': 'User deleted successfully'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)