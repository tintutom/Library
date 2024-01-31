from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Author,Genre,Book
from .serializers import GenreSerializer,BookSerializer,AuthorSerializer

# author signup view
class AuthorSignupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        city = request.data.get('city')
        profile_image = request.data.get('profile_image')

        if not (username and password and email and city):
            return Response({"error": "Username, password, email, and city are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Generate author_id
            author_id = f'AR{city[:3].upper()}{Author.objects.filter(city=city).count() + 1:04d}'

            # Create the user and author objects together
            user = User.objects.create_user(username=username, password=password, email=email)
            author = Author.objects.create(user=user, city=city, profile_image=profile_image, author_id=author_id)
            
            serializer = AuthorSerializer(author)
            return Response({"message": "Author created successfully.", "author": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create author. {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# Author and Admin login
class AuthorLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
# Admin Genre Adding View
class GenreCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Check if the user making the request is an admin
        if not request.user.is_staff:
            return Response({"error": "Only admins can create genres."}, status=status.HTTP_403_FORBIDDEN)

        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Genre created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Created Genre Deletion   
class GenreDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        if not request.user.is_staff:
            return Response({"error":"Only admin can delete genres."},status=status.HTTP_403_FORBIDDEN)
        try:
            genre = Genre.objects.get(pk=id)
        except Genre.DoesNotExist:
            return Response({"error":"Genre does not exist."},status=status.HTTP_404_NOT_FOUND)
        genre.delete()
        return Response({"message":"Genre deleted successfully."},status=status.HTTP_204_NO_CONTENT)

# Adminside  Entire Authors Listout View
class AuthorListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
# Admin can listout a specific author entire details
class AuthorDetailAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = 'author_id'

# admin can listout a specific author entire books by author name
class AuthorBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_name = self.kwargs.get('author_name')
        try:
            author = Author.objects.get(user__username=author_name)
            return Book.objects.filter(author=author)
        except Author.DoesNotExist:
            return Book.objects.none()

    def list(self, request, *args, **kwargs):
        author_name = self.kwargs.get('author_name')
        if not author_name:
            return Response({"error": "Author name parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# Author book creating view

class AuthorBookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id):
        try:
            author = Author.objects.get(author_id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the author or an admin
        if request.user != author.user and not request.user.is_staff:
            return Response({"error": "You are not authorized to create books for this author."}, status=status.HTTP_403_FORBIDDEN)

        # Extract genre name from request data
        genre_name = request.data.get('genre')

        # Check if the genre exists
        try:
            genre = Genre.objects.get(name=genre_name)
        except Genre.DoesNotExist:
            return Response({"error": f"Genre '{genre_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Add the genre instance to request data
        request.data['genre'] = genre.id

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response({"message": "Book created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Author book edit view

class AuthorBookEditAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, author_id, book_id):
        try:
            author = Author.objects.get(author_id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            book = Book.objects.get(pk=book_id, author=author)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the author or an admin
        if request.user != author.user and not request.user.is_staff:
            return Response({"error": "You are not authorized to edit this book."}, status=status.HTTP_403_FORBIDDEN)

        # Extract genre name from request data
        genre_name = request.data.get('genre')

        # Check if the genre exists
        try:
            genre = Genre.objects.get(name=genre_name)
        except Genre.DoesNotExist:
            return Response({"error": f"Genre '{genre_name}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Update book details
        request.data['genre'] = genre.id
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated successfully."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


