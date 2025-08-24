from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('token/', views.get_token, name='get_token'),
]
