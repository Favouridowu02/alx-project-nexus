from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Poll, Option
from .serializers import (
    PollSerializer,
    PollCreateSerializer,
    OptionSerializer,
    AddOptionSerializer,
    CastVoteSerializer
)
from votes.models import Vote

class IsPollOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a poll to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions are only allowed to the owner of the poll.
        return obj.created_by == request.user

class PollViewSet(viewsets.ModelViewSet):
    """
    ## Poll Management System
    
    Complete CRUD operations for managing polls in the online polling system.
    
    ### Features:
    - Create polls with multiple options
    - View all polls or specific polls
    - Update/Delete polls (owner only)
    - Vote on polls
    - View poll results
    - Manage poll options
    
    ### Permissions:
    - **List/Retrieve/Results**: Public access (no authentication required)
    - **Create**: Authenticated users only
    - **Update/Delete**: Poll owner only
    - **Vote**: Authenticated users only
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Poll.objects.all().select_related('created_by').prefetch_related('options')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PollCreateSerializer
        return PollSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        operation_id="list_polls",
        operation_summary="List All Polls",
        operation_description="""
        Retrieve a paginated list of all polls in the system.
        
        **Returns:**
        - All polls with basic information
        - Creator details for each poll
        - Current vote counts and totals
        - Poll status (active/expired)
        
        **Public Endpoint:**
        - No authentication required
        - Supports pagination
        - Includes both active and expired polls
        """,
        responses={
            200: openapi.Response(
                description="Polls retrieved successfully",
                examples={
                    "application/json": {
                        "count": 25,
                        "next": "http://api.example.com/polls/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                                "title": "Best Programming Language 2025",
                                "question": "Which language will dominate in 2025?",
                                "description": "Annual community survey on programming languages",
                                "created_by": {
                                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                    "username": "techguru",
                                    "first_name": "Jane",
                                    "last_name": "Doe",
                                    "email": "jane@example.com",
                                    "full_name": "Jane Doe"
                                },
                                "created_at": "2025-09-15T12:00:00Z",
                                "updated_at": "2025-09-20T08:30:00Z",
                                "expires_at": "2025-12-31T23:59:59Z",
                                "options": [
                                    {
                                        "option_id": "opt-001",
                                        "option_text": "Python",
                                        "vote_count": 127,
                                        "created_at": "2025-09-15T12:00:00Z"
                                    },
                                    {
                                        "option_id": "opt-002",
                                        "option_text": "JavaScript",
                                        "vote_count": 98,
                                        "created_at": "2025-09-15T12:00:00Z"
                                    }
                                ],
                                "total_votes": 225,
                                "is_active": True
                            }
                        ]
                    }
                }
            )
        },
        tags=['Polls - CRUD Operations']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="retrieve_poll",
        operation_summary="Get Poll Details",
        operation_description="""
        Retrieve detailed information about a specific poll.
        
        **Returns:**
        - Complete poll information
        - All options with current vote counts
        - Creator information
        - Total vote count
        - Poll status (active/expired)
        
        **Public Endpoint:**
        - No authentication required
        - Available to all users
        """,
        responses={
            200: openapi.Response(
                description="Poll details retrieved successfully",
                schema=PollSerializer,
                examples={
                    "application/json": {
                        "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Best Frontend Framework 2025",
                        "question": "Which frontend framework would you recommend for new projects?",
                        "description": "Community poll to determine trending frontend technologies",
                        "created_by": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "techexpert",
                            "first_name": "Sarah",
                            "last_name": "Wilson",
                            "email": "sarah@example.com",
                            "full_name": "Sarah Wilson"
                        },
                        "created_at": "2025-09-20T14:30:00Z",
                        "updated_at": "2025-09-25T10:15:00Z",
                        "expires_at": "2025-10-31T23:59:59Z",
                        "options": [
                            {
                                "option_id": "opt-101",
                                "option_text": "React",
                                "vote_count": 45,
                                "created_at": "2025-09-20T14:30:00Z"
                            },
                            {
                                "option_id": "opt-102",
                                "option_text": "Vue.js",
                                "vote_count": 32,
                                "created_at": "2025-09-20T14:30:00Z"
                            },
                            {
                                "option_id": "opt-103",
                                "option_text": "Angular",
                                "vote_count": 18,
                                "created_at": "2025-09-20T14:30:00Z"
                            }
                        ],
                        "total_votes": 95,
                        "is_active": True
                    }
                }
            ),
            404: openapi.Response(
                description="Poll not found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            )
        },
        tags=['Polls - CRUD Operations']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_id="create_poll",
        operation_summary="Create New Poll",
        operation_description="""
        Create a new poll with multiple options.
        
        **Requirements:**
        - Must be authenticated
        - Title and question are required
        - Minimum 2 options required
        - Each option must have option_text
        
        **Optional Fields:**
        - description: Additional poll description
        - expires_at: Poll expiration date (ISO format)
        
        **Process:**
        1. Validates poll data
        2. Creates poll with authenticated user as owner
        3. Creates all provided options
        4. Returns complete poll data with options
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'question', 'options'],
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Poll title (max 200 characters)',
                    example='Favorite Programming Language'
                ),
                'question': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Main poll question',
                    example='Which programming language do you prefer for web development?'
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Optional poll description',
                    example='A poll to determine the most popular programming language among developers'
                ),
                'expires_at': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    description='Poll expiration date (ISO 8601 format)',
                    example='2025-12-31T23:59:59Z'
                ),
                'options': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='List of poll options (minimum 2)',
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['option_text'],
                        properties={
                            'option_text': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Option text (max 255 characters)',
                                example='Python'
                            )
                        }
                    ),
                    example=[
                        {'option_text': 'Python'},
                        {'option_text': 'JavaScript'},
                        {'option_text': 'Java'},
                        {'option_text': 'Go'}
                    ]
                )
            },
        ),
        responses={
            201: openapi.Response(
                description="Poll created successfully",
                schema=PollSerializer,
                examples={
                    "application/json": {
                        "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Favorite Programming Language",
                        "question": "Which programming language do you prefer for web development?",
                        "description": "A poll to determine the most popular programming language",
                        "created_by": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "johndoe",
                            "first_name": "John",
                            "last_name": "Doe",
                            "email": "john@example.com",
                            "full_name": "John Doe"
                        },
                        "created_at": "2025-09-26T10:30:00Z",
                        "updated_at": "2025-09-26T10:30:00Z",
                        "expires_at": "2025-12-31T23:59:59Z",
                        "options": [
                            {
                                "option_id": "opt-001",
                                "option_text": "Python",
                                "vote_count": 0,
                                "created_at": "2025-09-26T10:30:00Z"
                            },
                            {
                                "option_id": "opt-002",
                                "option_text": "JavaScript",
                                "vote_count": 0,
                                "created_at": "2025-09-26T10:30:00Z"
                            }
                        ],
                        "total_votes": 0,
                        "is_active": True
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "options": ["Ensure this field has at least 2 items."]
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Polls - CRUD Operations']
    )
    def create(self, request, *args, **kwargs):
        """Create poll and return full poll data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poll = serializer.save(created_by=self.request.user)
        
        response_serializer = PollSerializer(poll, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['list', 'retrieve', 'results']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsPollOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    @swagger_auto_schema(
        operation_id="poll_results",
        operation_summary="Get Poll Results",
        operation_description="""
        View the current results of a specific poll.
        
        **Returns:**
        - Poll basic information
        - All options with vote counts and percentages
        - Total number of votes
        - Voting statistics
        
        **Public Endpoint:**
        - No authentication required
        - Real-time vote counts
        - Percentage calculations included
        """,
        responses={
            200: openapi.Response(
                description="Poll results retrieved successfully",
                examples={
                    "application/json": {
                        "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Best Frontend Framework 2025",
                        "total_votes": 127,
                        "results": [
                            {
                                "option_id": "opt-101",
                                "option_text": "React",
                                "votes": 58,
                                "percentage": 45.67
                            },
                            {
                                "option_id": "opt-102", 
                                "option_text": "Vue.js",
                                "votes": 41,
                                "percentage": 32.28
                            },
                            {
                                "option_id": "opt-103",
                                "option_text": "Angular", 
                                "votes": 28,
                                "percentage": 22.05
                            }
                        ]
                    }
                }
            ),
            404: openapi.Response(
                description="Poll not found",
                examples={
                    "application/json": {
                        "detail": "Poll not found."
                    }
                }
            )
        },
        tags=['Polls - Results & Analytics']
    )
    def results(self, request, pk=None):
        """Get poll results"""
        poll = self.get_object()
        options_data = []
        
        for option in poll.options.all():
            options_data.append({
                'option_id': option.option_id,
                'option_text': option.option_text,
                'votes': option.vote_count,
                'percentage': (option.vote_count / poll.total_votes * 100) if poll.total_votes > 0 else 0
            })
        
        return Response({
            'poll_id': poll.poll_id,
            'title': poll.title,
            'total_votes': poll.total_votes,
            'results': options_data
        })
    
    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_id="cast_vote",
        operation_summary="Cast Vote on Poll",
        operation_description="""
        Cast your vote on a specific poll option.
        
        **Requirements:**
        - Must be authenticated
        - Poll must be active (not expired)
        - User can only vote once per poll
        - Option must exist in the poll
        
        **Process:**
        1. Validates poll is active and option exists
        2. Checks if user has already voted
        3. Creates vote record
        4. Updates vote counts
        5. Returns confirmation with updated totals
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['option_id'],
            properties={
                'option_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='ID of the option to vote for',
                    example='opt-102'
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Vote cast successfully",
                examples={
                    "application/json": {
                        "message": "Vote cast successfully",
                        "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                        "option_voted": {
                            "option_id": "opt-102",
                            "option_text": "Vue.js",
                            "vote_count": 42
                        },
                        "total_votes": 128,
                        "vote_timestamp": "2025-09-26T15:30:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error or poll inactive",
                examples={
                    "application/json": {
                        "detail": "This poll is no longer active"
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Poll or option not found",
                examples={
                    "application/json": {
                        "detail": "Option not found in this poll."
                    }
                }
            ),
            409: openapi.Response(
                description="User has already voted",
                examples={
                    "application/json": {
                        "detail": "You have already voted on this poll."
                    }
                }
            )
        },
        tags=['Polls - Voting']
    )
    def vote(self, request, pk=None):
        """Cast vote on poll"""
        poll = self.get_object()
        
        if not poll.is_active:
            return Response({'error': 'This poll has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Vote.objects.filter(poll=poll, user=request.user).exists():
            return Response({'error': 'You have already voted on this poll'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CastVoteSerializer(data=request.data, context={'poll': poll})
        if serializer.is_valid():
            option = serializer.validated_data['option_id']
            Vote.objects.create(poll=poll, option=option, user=request.user)
            return Response({'message': 'Vote cast successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    @swagger_auto_schema(
        operation_id="poll_options",
        operation_summary="Get Poll Options",
        operation_description="""
        Retrieve all available options for a specific poll.
        
        **Returns:**
        - List of all poll options
        - Option IDs and text
        - Current vote counts for each option
        - Creation timestamps
        
        **Public Endpoint:**
        - No authentication required
        - Useful for displaying voting choices
        """,
        responses={
            200: openapi.Response(
                description="Poll options retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "option_id": "opt-101",
                            "option_text": "React",
                            "vote_count": 58,
                            "created_at": "2025-09-20T14:30:00Z",
                            "poll": "550e8400-e29b-41d4-a716-446655440000"
                        },
                        {
                            "option_id": "opt-102",
                            "option_text": "Vue.js", 
                            "vote_count": 42,
                            "created_at": "2025-09-20T14:30:00Z",
                            "poll": "550e8400-e29b-41d4-a716-446655440000"
                        },
                        {
                            "option_id": "opt-103",
                            "option_text": "Angular",
                            "vote_count": 28,
                            "created_at": "2025-09-20T14:30:00Z", 
                            "poll": "550e8400-e29b-41d4-a716-446655440000"
                        }
                    ]
                }
            ),
            404: openapi.Response(
                description="Poll not found",
                examples={
                    "application/json": {
                        "detail": "Poll not found."
                    }
                }
            )
        },
        tags=['Polls - Options Management']
    )
    def options(self, request, pk=None):
        """Get poll options"""
        poll = self.get_object()
        serializer = OptionSerializer(poll.options.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_id="add_poll_option",
        operation_summary="Add New Option to Poll",
        operation_description="""
        Add a new option to an existing poll.
        
        **Requirements:**
        - Must be authenticated
        - Only poll owner can add options
        - Poll must be active (not expired)
        - Option text must be unique within the poll
        
        **Process:**
        1. Validates user is poll owner
        2. Checks poll is still active
        3. Validates option text is unique
        4. Creates new option with zero votes
        5. Returns created option data
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['option_text'],
            properties={
                'option_text': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Text for the new option (max 255 characters)',
                    example='Svelte'
                )
            },
        ),
        responses={
            201: openapi.Response(
                description="Option added successfully",
                examples={
                    "application/json": {
                        "option_id": "opt-104",
                        "option_text": "Svelte",
                        "vote_count": 0,
                        "created_at": "2025-09-26T16:45:00Z",
                        "poll": "550e8400-e29b-41d4-a716-446655440000",
                        "message": "Option added successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "option_text": ["This field is required."]
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied - not poll owner",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            404: openapi.Response(
                description="Poll not found",
                examples={
                    "application/json": {
                        "detail": "Poll not found."
                    }
                }
            )
        },
        tags=['Polls - Options Management']
    )
    def add_option(self, request, pk=None):
        """Add option to poll (owner only)"""
        poll = self.get_object()
        
        if poll.created_by != request.user:
            return Response({'error': 'Only poll owner can add options'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AddOptionSerializer(data=request.data, context={'poll': poll})
        if serializer.is_valid():
            Option.objects.create(
                poll=poll,
                option_text=serializer.validated_data['option_text']
            )
            return Response({'message': 'Option added successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_id="my_polls",
        operation_summary="Get My Polls",
        operation_description="""
        Retrieve all polls created by the authenticated user.
        
        **Returns:**
        - List of polls owned by current user
        - Complete poll information including options
        - Vote counts and statistics
        - Creation and expiration dates
        
        **Authentication Required:**
        - Only authenticated users can access
        - Returns only polls created by the requesting user
        """,
        responses={
            200: openapi.Response(
                description="User's polls retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "Team Lunch Preference",
                            "question": "What type of cuisine should we order for team lunch?",
                            "description": "Weekly team lunch poll",
                            "created_by": {
                                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                                "username": "teamlead",
                                "first_name": "Sarah",
                                "last_name": "Johnson",
                                "email": "sarah@company.com",
                                "full_name": "Sarah Johnson"
                            },
                            "created_at": "2025-09-25T09:00:00Z",
                            "updated_at": "2025-09-25T09:00:00Z",
                            "expires_at": "2025-09-27T18:00:00Z",
                            "options": [
                                {
                                    "option_id": "opt-201",
                                    "option_text": "Italian",
                                    "vote_count": 5,
                                    "created_at": "2025-09-25T09:00:00Z"
                                },
                                {
                                    "option_id": "opt-202",
                                    "option_text": "Chinese",
                                    "vote_count": 3,
                                    "created_at": "2025-09-25T09:00:00Z"
                                }
                            ],
                            "total_votes": 8,
                            "is_active": True
                        }
                    ]
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Polls - User Collections']
    )
    def my_polls(self, request):
        """Get current user's polls"""
        polls = Poll.objects.filter(created_by=request.user)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_id="active_polls",
        operation_summary="Get Active Polls",
        operation_description="""
        Retrieve all currently active polls across the platform.
        
        **Returns:**
        - List of all active (non-expired) polls
        - Public polls available for voting
        - Complete poll information with options
        - Real-time vote counts
        
        **Filtering:**
        - Only returns polls that haven't expired
        - Includes polls from all users
        - Ordered by creation date (newest first)
        
        **Public Endpoint:**
        - No authentication required
        - Perfect for browse/discovery functionality
        """,
        responses={
            200: openapi.Response(
                description="Active polls retrieved successfully", 
                examples={
                    "application/json": [
                        {
                            "poll_id": "550e8400-e29b-41d4-a716-446655440000",
                            "title": "Best Frontend Framework 2025",
                            "question": "Which frontend framework would you recommend?",
                            "description": "Community poll for trending technologies",
                            "created_by": {
                                "user_id": "456e7890-e89b-12d3-a456-426614174001",
                                "username": "developer_pro",
                                "first_name": "Alex",
                                "last_name": "Chen",
                                "email": "alex@example.com",
                                "full_name": "Alex Chen"
                            },
                            "created_at": "2025-09-20T14:30:00Z",
                            "updated_at": "2025-09-25T10:15:00Z",
                            "expires_at": "2025-10-31T23:59:59Z",
                            "options": [
                                {
                                    "option_id": "opt-101",
                                    "option_text": "React",
                                    "vote_count": 58,
                                    "created_at": "2025-09-20T14:30:00Z"
                                },
                                {
                                    "option_id": "opt-102",
                                    "option_text": "Vue.js",
                                    "vote_count": 42,
                                    "created_at": "2025-09-20T14:30:00Z"
                                }
                            ],
                            "total_votes": 100,
                            "is_active": True
                        }
                    ]
                }
            ),
            500: openapi.Response(
                description="Server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error"
                    }
                }
            )
        },
        tags=['Polls - User Collections']
    )
    def active_polls(self, request):
        """Get all active polls"""
        from django.utils import timezone
        active_polls = Poll.objects.filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=timezone.now())
        )
        serializer = PollSerializer(active_polls, many=True)
        return Response(serializer.data)

class OptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing poll options.
    
    **Functionality:**
    - **List Options**: Get all options or filter by poll
    - **Create Option**: Add new option to a poll (owner only)
    - **Retrieve Option**: Get specific option details
    - **Update Option**: Modify option text (owner only)
    - **Delete Option**: Remove option from poll (owner only)
    
    **Permissions:**
    - **List/Retrieve**: Authenticated users only
    - **Create/Update/Delete**: Poll owner only
    
    **Query Parameters:**
    - `poll`: Filter options by poll ID
    """
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Option.objects.all()
        poll_id = self.request.query_params.get('poll', None)
        if poll_id:
            queryset = queryset.filter(poll_id=poll_id)
        return queryset
    
    def perform_create(self, serializer):
        poll = serializer.validated_data['poll']
        if poll.created_by != self.request.user:
            raise serializers.ValidationError("You can only add options to your own polls")
        serializer.save()

    @swagger_auto_schema(
        operation_id="list_options",
        operation_summary="List Poll Options",
        operation_description="""
        Retrieve all poll options, optionally filtered by poll.
        
        **Query Parameters:**
        - `poll`: UUID of poll to filter options by
        
        **Returns:**
        - List of options with vote counts
        - Option IDs and text content
        - Associated poll information
        - Creation timestamps
        
        **Authentication Required:**
        - Only authenticated users can access
        """,
        manual_parameters=[
            openapi.Parameter(
                'poll',
                openapi.IN_QUERY,
                description="Filter options by poll UUID",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            )
        ],
        responses={
            200: openapi.Response(
                description="Options retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "option_id": "opt-101",
                            "option_text": "React",
                            "vote_count": 45,
                            "poll": "550e8400-e29b-41d4-a716-446655440000",
                            "created_at": "2025-09-20T14:30:00Z"
                        },
                        {
                            "option_id": "opt-102",
                            "option_text": "Vue.js",
                            "vote_count": 32,
                            "poll": "550e8400-e29b-41d4-a716-446655440000",
                            "created_at": "2025-09-20T14:30:00Z"
                        }
                    ]
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Options - Management']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="create_option",
        operation_summary="Create Poll Option",
        operation_description="""
        Create a new option for a specific poll.
        
        **Requirements:**
        - Must be authenticated
        - Must be the poll owner
        - Poll must exist and be active
        - Option text must be unique within the poll
        
        **Process:**
        1. Validates user owns the specified poll
        2. Checks option text uniqueness
        3. Creates option with zero votes
        4. Returns created option data
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['option_text', 'poll'],
            properties={
                'option_text': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Text content for the option (max 255 characters)',
                    example='TypeScript'
                ),
                'poll': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_UUID,
                    description='UUID of the poll this option belongs to',
                    example='550e8400-e29b-41d4-a716-446655440000'
                )
            },
        ),
        responses={
            201: openapi.Response(
                description="Option created successfully",
                examples={
                    "application/json": {
                        "option_id": "opt-105",
                        "option_text": "TypeScript",
                        "vote_count": 0,
                        "poll": "550e8400-e29b-41d4-a716-446655440000",
                        "created_at": "2025-09-26T17:00:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "detail": "You can only add options to your own polls"
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Poll not found",
                examples={
                    "application/json": {
                        "detail": "Poll not found."
                    }
                }
            )
        },
        tags=['Options - Management']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)