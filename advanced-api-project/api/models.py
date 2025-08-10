from django.db import models

# the author class in python defines a model with name attribute and string  representation
#method 
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    published_year = models.IntegerField()
