from rest_framework.test import APITestCase, APIClient
from django.urls import path, include
from django.contrib.auth.models import User
from .models import Book
from rest_framework import status

class BookAPITestCase(APITestCase):
        def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='password')
        self.cllint =APIClient()
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2024
        }
        self.book = Book.objects.create(**self.book_data)
        self.url_list = '/api/books/'
        self.url_detail = f'/api/books/{self.book.id}/'
        self.client.login(username='testuser', password='password')




