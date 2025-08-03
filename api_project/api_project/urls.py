from django.urls import path
from api.views import BookListCreateAPIView

urlpatterns = [
    path("api/books", BookListCreateAPIView.as_view(), name="book_list_create"),
]