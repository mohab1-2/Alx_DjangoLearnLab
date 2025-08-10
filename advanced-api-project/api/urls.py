from django.urls import path
from .views import (
    BookGenericAPIView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('', BookGenericAPIView.as_view(), name='book-generic-api'),
    path('books/list/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
]








# from rest_framework import routers
# from .views import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.urls import path, include
 
# router = routers.DefaultRouter()
# router.register(r'books', ListView)
# router.register(r'books/<int:pk>', DetailView, basename='book-detail')
# router.register(r'books/create', CreateView, basename='book-create')
# router.register(r'books/<int:pk>/update', UpdateView, basename='book-update')
# router.register(r'books/<int:pk>/delete', DeleteView, basename='book-delete')
# router.register(r'authors', AuthorView, basename='User')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

