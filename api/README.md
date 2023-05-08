This `api` directory contains the following Python files responsible for handling various aspects of the application:

1. `signup.py`
2. `login.py`
3. `community.py`
4. `post.py`
5. `comments.py`

Below is a brief description of each file's functionality and purpose.

# **APIs**
## 1. **Signup: `signup.py`**

`signup.py` is responsible for handling user registration. It defines a route `/signup` that accepts a `POST` request containing user details, such as `username`, `email`, and `password`. The module validates and processes the provided data, and if successful, creates a new user in the database.

## 2. **Log In: `login.py`**

`login.py` is responsible for handling user authentication. It defines a route `/login` that accepts a `POST` request containing a user's `email` and `password`. The module checks the provided credentials against the stored data in the database. If the credentials are valid, the module returns an access token, which the user can use for accessing protected routes.

## 3. **Community: `community.py`**

`community.py` is responsible for managing the community aspect of the application. This module includes the following routes:

- `/create_community`: Allows users to create a new community.
- `/join_community`: Allows users to join an existing community.
- `/leave_community`: Allows users to leave a community.
- `/get_my_communities`: Retrieves the communities that a user is part of.

## 4. **Post: `post.py`**

`post.py` is responsible for managing user posts. This module includes the following routes:

- `/create_post`: Allows users to create a new post in a community.
- `/get_post`: Retrieves a specific post.
- `/get_community_posts`: Retrieves all the posts in a community.
- `/delete_post`: Allows users to delete their own posts.

## 5. **Comments: `comments.py`**

`comments.py` is responsible for managing comments on posts. This module includes the following routes:

- `/new_comment`: Allows users to create a new comment on a post.
- `/all_comments`: Retrieves all the comments for a specific post.
- `/delete_comment`: Allows users to delete their own comments.

These routes are designed to work together, providing a seamless experience for users to interact with the application's various features.