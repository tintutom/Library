
API Documentation : https://documenter.getpostman.com/view/29389936/2s9YytfzwQ


1. Models
Author: Represents an author with fields like username, email, city, profile image, and author ID.
Genre: Represents a genre with a name field.
Book: Represents a book with fields like title, author (ForeignKey to Author), genre (ForeignKey to Genre), number of pages, and cover image.

2. Common Login and Signup API
Login API: Allows both authors and admins to log in using their credentials.
Signup for Author: Allows authors to sign up by providing necessary details like username, password, email, city, and profile image.

3. Admin APIs
Add Genre: Allows the admin to add a new genre.
Get All Authors: Retrieves details of all authors, including their books.
Get Details of a Specific Author: Retrieves details of a specific author, including their books.
Get Books of a Specific Author: Retrieves books of a specific author.
Delete Genre: Allows the admin to delete a genre.

4. Author APIs
Add Book: Allows authors to add a new book with details like title, genre, number of pages, and cover image.
Edit Book: Allows authors to edit details of an existing book.

5. Export Book Data API
Export Books by Genre: Allows the admin to export all book data for a specific genre in a structured format (CSV or JSON).
Includes details such as book name, author name, number of pages, and any other relevant information.
Ensures that the export functionality is efficient and handles large datasets gracefully.
