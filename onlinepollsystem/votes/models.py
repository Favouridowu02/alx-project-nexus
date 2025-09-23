import uuid
from django.db import models



# Create your models here.
class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll_id = models.ForeignKey('polls.Poll', on_delete=models.CASCADE, null=False)
    option_id = models.ForeignKey('polls.Option', on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll_id', 'user_id')  # Ensure a user can vote only once per poll

    def __str__(self):
        return f"Vote by {self.user_id} for {self.option_id} in {self.poll_id}"