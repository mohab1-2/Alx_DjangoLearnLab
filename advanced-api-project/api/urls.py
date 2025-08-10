from rest_framework import routers
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import path, include
 
router = routers.DefaultRouter()
router.register(r'books', ListView)
router.register(r'books/<int:pk>', DetailView, basename='book-detail')
router.register(r'books/create', CreateView, basename='book-create')
router.register(r'books/<int:pk>/update', UpdateView, basename='book-update')
router.register(r'books/<int:pk>/delete', DeleteView, basename='book-delete')
router.register(r'authors', AuthorView, basename='User')

urlpatterns = [
    path('', include(router.urls)),
]
