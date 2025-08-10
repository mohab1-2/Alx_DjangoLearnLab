from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        def validate_published_year(self, value):
            if value > 2025:
                raise serializers.ValidationError("Published year cannot be in the future")
            return value