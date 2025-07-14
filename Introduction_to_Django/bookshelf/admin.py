from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year', 'author')
    fields = ('title', 'author', 'publication_year', 'pages', 'description')
    list_per_page = 25
    ordering = ['-publication_year', 'title']