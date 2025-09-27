import uuid
from django.db import models
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    """
        Poll model representing a poll with a question and multiple options.
    """
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    question = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['-created_at']
    
    @property
    def is_active(self):
        if self.expires_at:
            return timezone.now() < self.expires_at
        return True
    
    @property
    def total_votes(self):
        return sum(option.vote_count for option in self.options.all())
    
    def __str__(self):
        return self.title

    

class Option(models.Model):
    """
        Option model representing an option for a poll.
    """
    option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options', null=False)
    option_text = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('poll', 'option_text')


    @property
    def vote_count(self):
        return self.votes.count()

    def __str__(self):
        return f'{self.option_text} - {self.poll.title}'