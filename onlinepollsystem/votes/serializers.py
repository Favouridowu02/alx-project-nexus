from rest_framework import serializers
from .models import Vote
from polls.serializers import PollSerializer, OptionSerializer
from users.serializers import UserSerializer

class VoteSerializer(serializers.ModelSerializer):
    poll = PollSerializer(read_only=True)
    option = OptionSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    # Add convenience fields that extract data from related objects
    poll_title = serializers.CharField(source='poll.title', read_only=True)
    option_text = serializers.CharField(source='option.option_text', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Vote
        fields = ['vote_id', 'poll', 'poll_title', 'option', 'option_text', 
                 'user', 'user_username', 'timestamp']
        read_only_fields = ['vote_id', 'timestamp']