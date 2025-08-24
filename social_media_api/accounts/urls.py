# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Existing authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    
    # Follow management URLs
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.user_following, name='user_following'),
    path('following/<int:user_id>/', views.user_following, name='user_following_by_id'),
    path('followers/', views.user_followers, name='user_followers'),
    path('followers/<int:user_id>/', views.user_followers, name='user_followers_by_id'),
]
