# posts/views.py (add this to your existing views)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer

User = get_user_model()

class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    """
    Generate personalized feed based on users the current user follows
    """
    # Get users that the current user follows
    following_users = User.objects.filter(user_followers__follower=request.user)
    
    # Get posts from followed users, ordered by creation date (most recent first)
    feed_posts = Post.objects.filter(
        author__in=following_users
    ).select_related('author').prefetch_related('comments').order_by('-created_at')
    
    # If user doesn't follow anyone, show their own posts or empty feed
    if not feed_posts.exists():
        feed_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    # Apply pagination
    paginator = FeedPagination()
    paginated_posts = paginator.paginate_queryset(feed_posts, request)
    
    # Serialize the posts
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    # Return paginated response
    return paginator.get_paginated_response({
        'message': 'Feed retrieved successfully',
        'posts': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def discover_posts(request):
    """
    Show recent posts from all users (discovery feed)
    """
    all_posts = Post.objects.all().select_related('author').prefetch_related('comments').order_by('-created_at')
    
    # Apply pagination
    paginator = FeedPagination()
    paginated_posts = paginator.paginate_queryset(all_posts, request)
    
    # Serialize the posts
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    # Return paginated response
    return paginator.get_paginated_response({
        'message': 'Discover feed retrieved successfully',
        'posts': serializer.data
    })
