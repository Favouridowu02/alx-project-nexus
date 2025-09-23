import uuid
from django.db import models

# Create your models here.

class User(models.Model):
    """
    Custom User model

    Methods:
        - __str__: Returns the string representation of the user (email).
        - full_name: Property that returns the full name of the user.
        - get_short_name: Returns the short name (username) of the user.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.username