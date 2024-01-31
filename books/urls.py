from django.urls import path
from .views import AuthorSignupAPIView ,AuthorLoginAPIView,GenreCreateAPIView,GenreDeleteAPIView,AuthorListAPIView,AuthorBookCreateAPIView,AuthorBookEditAPIView,AuthorDetailAPIView,AuthorBooksAPIView

urlpatterns = [
# Admin side urls
    path('signup/', AuthorSignupAPIView.as_view(), name='author-signup'),
    path('login/', AuthorLoginAPIView.as_view(), name='author-login'),
    path('add-genre/', GenreCreateAPIView.as_view(), name='genre-adding'),
    path('delete-genre/<int:id>/', GenreDeleteAPIView.as_view(), name='genre-deleting'),
    path('authers/', AuthorListAPIView.as_view(), name='book-create'),
    path('authors/<str:author_id>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('author-books/<str:author_name>/', AuthorBooksAPIView.as_view(), name='author-books'),
    
# Author side urls
    path('create/<str:author_id>/', AuthorBookCreateAPIView.as_view(), name='author-book-create'),
    path('book/<str:author_id>/<int:book_id>/', AuthorBookEditAPIView.as_view(), name='author-book-edit'),
]