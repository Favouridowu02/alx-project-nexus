from rest_framework import serializers
from .models import Poll, Option
from users.serializers import UserSerializer

class OptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Option
        fields = ('option_id', 'option_text', 'vote_count', 'created_at')
        read_only_fields = ('option_id', 'created_at')


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    total_votes = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Poll
        fields = ('poll_id', 'title', 'question', 'description', 'created_by', 'created_at', 
                 'updated_at', 'expires_at', 'options', 'total_votes', 'is_active')
        read_only_fields = ('poll_id', 'created_at', 'updated_at')

class PollCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(max_length=255)),
        write_only=True,
        min_length=2
    )
    
    class Meta:
        model = Poll
        fields = ('title', 'question', 'description', 'expires_at', 'options')
    
    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        
        # Create options
        for option_dict in options_data:
            option_text = option_dict.get('option_text', '')
            if option_text:
                Option.objects.create(poll=poll, option_text=option_text)
        
        return poll
    
class AddOptionSerializer(serializers.Serializer):
    option_text = serializers.CharField(max_length=255)
    
    def validate_option_text(self, value):
        poll = self.context['poll']
        if Option.objects.filter(poll=poll, option_text=value).exists():
            raise serializers.ValidationError("This option already exists for this poll.")
        return value
    
class CastVoteSerializer(serializers.Serializer):
    option_id = serializers.UUIDField()
    
    def validate_option_id(self, value):
        poll = self.context['poll']
        try:
            option = Option.objects.get(option_id=value, poll=poll)
            return option
        except Option.DoesNotExist:
            raise serializers.ValidationError("Invalid option for this poll.")