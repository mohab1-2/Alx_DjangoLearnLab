# # your_app/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.login_view, name='home'),
#     path('register/', views.register_view, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('profile/', views.profile_view, name='profile'),
#     # NEW: These are the ones you add in Step 4
#     path('profile/edit/', views.edit_profile_view, name='edit_profile'),
#     path('profile/change-password/', views.change_password_view, name='change_password'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # List view - display all blog posts
    path('', views.ListView.as_view(), name='list'),
    
    # Detail view - show individual blog post
    path('post/<int:pk>/', views.DetailView.as_view(), name='detail'),
    
    # Create view - allow authenticated users to create new posts
    path('post/new/', views.CreateView.as_view(), name='create'),
    
    # Update view - let post authors edit their posts
    path('post/<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    
    # Delete view - let authors delete their posts
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]
