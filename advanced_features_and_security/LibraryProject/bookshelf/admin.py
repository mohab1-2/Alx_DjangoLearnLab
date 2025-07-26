from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'pages')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
    # Remove any reference to 'created_at' if it exists