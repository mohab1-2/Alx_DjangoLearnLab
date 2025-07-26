from library_books.models import Book

---
# Create a book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()


# <Book:1948>
"Book.objects.create"