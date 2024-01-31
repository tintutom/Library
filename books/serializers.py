from rest_framework import serializers
from .models import Genre,Book,Author

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.user.username', read_only=True)
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'genre', 'genre_name', 'pages', 'cover_image']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['user', 'city', 'profile_image', 'author_id', 'books']