from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/')
    author_id = models.CharField(max_length=10, unique=True, editable=False)  

    def generate_author_id(self):
        city_code = self.city[:3].upper()
        author_count = Author.objects.filter(city=self.city).count() + 1
        author_id = f'AR{city_code}{author_count:04d}'
        return author_id

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    pages = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/')

    @property
    def author_name(self):
        return self.author.user.username

    @property
    def genre_name(self):
        return self.genre.name

