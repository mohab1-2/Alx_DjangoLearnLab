from bookshelf.models import book

book_to_delete = Book.objects.get(title="Animal Farm")
book_to_delete.delete()
