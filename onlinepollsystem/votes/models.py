import uuid
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey('polls.Poll', on_delete=models.CASCADE, null=False, related_name='votes')
    option = models.ForeignKey('polls.Option', on_delete=models.CASCADE, null=False, related_name='votes')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')
        ordering = ['-timestamp']

    def __str__(self):
        return f"Vote by {self.user.username} with email {self.user.email} for {self.option} in {self.poll}"
    
    def clean(self):
        """
        Ensure that the option belongs to the poll.
        """
        if self.option.poll != self.poll:
            raise ValidationError("The selected option does not belong to the poll.")