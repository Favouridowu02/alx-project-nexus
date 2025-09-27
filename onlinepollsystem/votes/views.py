from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vote
from .serializers import VoteSerializer

class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user's votes"""
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user).select_related('poll', 'option', 'user')