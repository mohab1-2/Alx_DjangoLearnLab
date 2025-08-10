from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter  # Ensure SearchFilter and OrderingFilter are correctly imported
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework


filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]  # Correct usage of filters.OrderingFilter and filters.SearchFilter
filterset_fields = ['title', 'author', 'publication_year']  # Filtering fields
search_fields = ['title', 'author']  # Search fields
ordering_fields = ['title', 'publication_year']  # Ordering fields

class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
  


class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
# Create your views here.



