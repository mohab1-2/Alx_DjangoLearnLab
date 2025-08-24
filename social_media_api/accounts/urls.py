from django.urls import path
from .views import RegisterView, LoginView, ProfileView

# You can also import the function-based views if you prefer:
# from .views import register_user, login_user, user_profile

urlpatterns = [
    # Class-based views
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    
    # Alternative: Function-based views (uncomment if you prefer these)
    # path('register/', register_user, name='user-register'),
    # path('login/', login_user, name='user-login'),
    # path('profile/', user_profile, name='user-profile'),
]
