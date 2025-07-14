# Import the model
from bookshelf.models import Book

# CREATE
$book = Book(title="1984", author="George Orwell", publication_year=1949)
$book.save()


# RETRIEVE
all_books = Book.objects.all()
print(all_books)

for book in all_books:
    print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# UPDATE
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")

# DELETE
book_to_delete = Book.objects.get(title="Animal Farm")
book_to_delete.delete()
