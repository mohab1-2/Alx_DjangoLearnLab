from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Option 1: Using class-based views (recommended)
urlpatterns = [
    # Post URLs
    path('', views.PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # Comment URLs - nested under posts
    path('<int:post_pk>/comments/', views.CommentListCreateView.as_view(), name='post-comments'),
    
    # Comment URLs - direct access
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]

# Option 2: Using function-based views (alternative)
# urlpatterns = [
#     path('', views.post_list_create, name='post-list-create'),
#     path('<int:pk>/', views.post_detail, name='post-detail'),
# ]

# Note: Make sure to include these URLs in your main urls.py:
# from django.urls import path, include
# 
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/accounts/', include('accounts.urls')),
#     path('api/posts/', include('posts.urls')),
# ]