from library_books.models import Book

all_books = Book.objects.all()
print(all_books)

for book in all_books:
    print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")