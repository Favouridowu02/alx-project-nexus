from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User Registration Serializer
    
    Creates a new user account with complete profile information.
    Validates password strength and ensures unique email/username.
    
    Example request:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!"
    }
    ```
    
    Example response:
    ```json
    {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com", 
        "username": "johndoe"
    }
    ```
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )

    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'username', 'password', 'password_confirm')
        read_only_fields = ('user_id',)
        extra_kwargs = {
            'email': {'help_text': 'Valid email address for account verification'},
            'username': {'help_text': 'Unique username for login'},
            'first_name': {'help_text': 'Your first name'},
            'last_name': {'help_text': 'Your last name'},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """
        Validate that both passwords match
        
        Args:
            attrs (dict): Dictionary containing validated field data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If passwords don't match
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with hashed password
        
        Args:
            validated_data (dict): Validated user data
            
        Returns:
            User: Created user instance
        """
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            username=validated_data.get('username')
        )
        user.set_password(password)  # This properly hashes the password
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    """
    User Login Serializer
    
    Authenticates user with email and password.
    Returns user data for successful authentication.
    
    Example request:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "SecurePass123!"
    }
    ```
    
    Example response (handled in view):
    ```json
    {
        "message": "Login successful",
        "user": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@example.com",
            "username": "johndoe"
        },
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    }
    ```
    """
    email = serializers.EmailField(
        help_text="Your registered email address",
        required=True,
        error_messages={
            'required': 'Email address is required',
            'invalid': 'Enter a valid email address'
        }
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Your account password",
        required=True,
        write_only=True,
        error_messages={
            'required': 'Password is required'
        }
    )

    def validate(self, attrs):
        """
        Authenticate user with provided credentials
        
        Args:
            attrs (dict): Dictionary containing email and password
            
        Returns:
            dict: Validated data including user object
            
        Raises:
            ValidationError: If credentials are invalid or user is inactive
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email, is_active=True)
                if user.check_password(password):
                    attrs['user'] = user
                    return attrs
                else:
                    raise serializers.ValidationError(
                        "Invalid credentials or inactive user."
                    )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Invalid credentials or inactive user."
                )
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'."
            )
        
class UserSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer
    
    Serializes user profile data for display purposes.
    Includes computed fields like full_name.
    
    Example response:
    ```json
    {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "date_joined": "2023-01-15T10:30:00Z",
        "updated_at": "2023-01-20T14:45:00Z"
    }
    ```
    """
    full_name = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ("user_id", "first_name", "last_name", "full_name", "email", "username", "date_joined", "updated_at")
        read_only_fields = ("user_id", "date_joined", "updated_at")
        extra_kwargs = {
            'user_id': {'help_text': 'Unique user identifier (UUID)'},
            'first_name': {'help_text': 'User\'s first name'},
            'last_name': {'help_text': 'User\'s last name'},
            'email': {'help_text': 'User\'s email address'},
            'username': {'help_text': 'User\'s unique username'},
            'date_joined': {'help_text': 'Account creation timestamp'},
            'updated_at': {'help_text': 'Last profile update timestamp'},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    User Profile Update Serializer
    
    Updates user profile information.
    Validates email uniqueness and ownership permissions.
    
    Example request:
    ```json
    {
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "email": "john.updated@example.com",
        "username": "johndoe_updated"
    }
    ```
    
    Example response (handled in view):
    ```json
    {
        "message": "Profile updated successfully",
        "user": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "first_name": "John Updated",
            "last_name": "Doe Updated",
            "email": "john.updated@example.com",
            "username": "johndoe_updated"
        }
    }
    ```
    """
    email = serializers.EmailField(
        required=False,
        help_text="New email address (must be unique)"
    )
    username = serializers.CharField(
        required=False,
        min_length=3,
        max_length=50,
        help_text="New username (must be unique, 3-50 characters)"
    )
    first_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=255,
        help_text="Updated first name (2-255 characters)"
    )
    last_name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=255,
        help_text="Updated last name (2-255 characters)"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def validate_email(self, value):
        """
        Validate email uniqueness (excluding current user)
        
        Args:
            value (str): Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If email is already in use by another user
        """
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already registered to another account"
            )
        return value
    
    def validate_username(self, value):
        """
        Validate username uniqueness (excluding current user)
        
        Args:
            value (str): Username to validate
            
        Returns:
            str: Validated username
            
        Raises:
            ValidationError: If username is already taken
        """
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken"
            )
        return value

    def validate(self, attrs):
        """
        Validate that user can only update their own profile
        
        Args:
            attrs (dict): Dictionary containing update data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If user tries to update another user's profile
        """
        request_user = self.context.get('request').user
        if request_user != self.instance:
            raise serializers.ValidationError({
                'non_field_errors': ['You can only update your own profile']
            })
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    """
    Password Change Serializer
    
    Validates and processes password changes for authenticated users.
    Requires old password verification and new password confirmation.
    
    Example request:
    ```json
    {
        "old_password": "OldSecurePass123!",
        "new_password": "NewSecurePass456!",
        "confirm_password": "NewSecurePass456!"
    }
    ```
    
    Example response (handled in view):
    ```json
    {
        "message": "Password changed successfully"
    }
    ```
    """
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Your current password",
        required=True,
        write_only=True,
        error_messages={
            'required': 'Current password is required'
        }
    )
    new_password = serializers.CharField(
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Your new password (must meet security requirements)",
        required=True,
        write_only=True,
        min_length=8,
        max_length=128,
        error_messages={
            'required': 'New password is required'
        }
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Confirm your new password",
        required=True,
        write_only=True,
        error_messages={
            'required': 'Password confirmation is required'
        }
    )

    def validate_old_password(self, value):
        """
        Verify that the old password is correct
        
        Args:
            value (str): Old password provided by user
            
        Returns:
            str: Validated old password
            
        Raises:
            ValidationError: If old password is incorrect
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Current password is incorrect"
            )
        return value
    
    def validate(self, attrs):
        """
        Validate that new passwords match
        
        Args:
            attrs (dict): Dictionary containing password data
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If new passwords don't match
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "New passwords don't match"
            })
        return attrs
    
    def save(self):
        """
        Save the new password to the user account
        
        Returns:
            User: Updated user instance
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password', 'updated_at'])
        return user


# Response serializers for Swagger documentation
class UserRegistrationResponseSerializer(serializers.Serializer):
    """Response serializer for user registration endpoint"""
    message = serializers.CharField(help_text="Success message")
    user = UserSerializer(help_text="Created user data")
    token = serializers.CharField(help_text="Authentication token")


class UserLoginResponseSerializer(serializers.Serializer):
    """Response serializer for user login endpoint"""
    message = serializers.CharField(help_text="Success message")
    user = UserSerializer(help_text="Authenticated user data")
    token = serializers.CharField(help_text="Authentication token")


class UserProfileUpdateResponseSerializer(serializers.Serializer):
    """Response serializer for profile update endpoint"""
    message = serializers.CharField(help_text="Success message")
    user = UserSerializer(help_text="Updated user data")


class PasswordChangeResponseSerializer(serializers.Serializer):
    """Response serializer for password change endpoint"""
    message = serializers.CharField(help_text="Success message")


class ErrorResponseSerializer(serializers.Serializer):
    """Generic error response serializer"""
    error = serializers.CharField(help_text="Error message")
    details = serializers.DictField(
        help_text="Detailed error information",
        required=False
    )
    
