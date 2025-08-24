# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Existing post URLs
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
    
    # Feed URLs
    path('feed/', views.user_feed, name='user_feed'),
    path('discover/', views.discover_posts, name='discover_posts'),
]
