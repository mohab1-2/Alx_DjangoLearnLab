from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Post CRUD operations
    - GET /posts/ - List all posts
    - POST /posts/ - Create a new post
    - GET /posts/{id}/ - Get post details
    - PUT /posts/{id}/ - Update post (author only)
    - DELETE /posts/{id}/ - Delete post (author only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a post"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Update the post"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Delete the post"""
        instance.delete()

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        """
        Custom action to handle comments for a specific post
        GET /posts/{id}/comments/ - List comments
        POST /posts/{id}/comments/ - Create comment
        """
        post = self.get_object()
        
        if request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Comment CRUD operations
    - GET /comments/ - List all comments
    - POST /comments/ - Create a new comment
    - GET /comments/{id}/ - Get comment details
    - PUT /comments/{id}/ - Update comment (author only)
    - DELETE /comments/{id}/ - Delete comment (author only)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'post']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Update the comment"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Delete the comment"""
        instance.delete()

# Alternative: Generic views (if you prefer, but ViewSets are recommended for REST APIs)
from rest_framework import generics

class PostListCreateView(generics.ListCreateAPIView):
    """
    List all posts or create a new post
    GET /posts/ - List all posts with pagination and filtering
    POST /posts/ - Create a new post (authenticated users only)
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post
    GET /posts/{id}/ - Get post details with comments
    PUT /posts/{id}/ - Update post (author only)
    DELETE /posts/{id}/ - Delete post (author only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    """
    List comments for a specific post or create a new comment
    GET /posts/{post_id}/comments/ - List all comments for a post
    POST /posts/{post_id}/comments/ - Create a new comment (authenticated users only)
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific comment
    GET /comments/{id}/ - Get comment details
    PUT /comments/{id}/ - Update comment (author only)
    DELETE /comments/{id}/ - Delete comment (author only)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
