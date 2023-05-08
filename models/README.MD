This database is designed for a discussion platform similar to Reddit. It has several entities, such as Users, Communities, Posts, Comments, and several relationship tables to capture many-to-many relationships like Community Subscriptions, Post Likes, and Saved Posts.

# **Entities**

## **User**

The `User` entity represents registered users on the platform. Each user has a unique ID, a username, an email, a password, an authentication status, and a code.

Fields:
- `user_id` (int): primary key
- `username` (str): username
- `password` (str): password
- `email` (str): email
- `is_authenticated` (bool): is authenticated
- `code` (str): code

## **Community**

The `Community` entity represents the different communities (or groups) created by users on the platform. Each community has a unique ID, a user ID (creator), a community name, and a description.

Fields:
- `community_id` (int): primary key
- `user_id` (int): foreign key to `User`'s table
- `community_name` (str): community name
- `description` (str): community description

## **Post**

The `Post` entity represents the posts created by users in different communities. Each post has a unique ID, a user ID (author), a community ID, a post name, a description, and a creation timestamp.

Fields:
- `post_id` (int): primary key
- `user_id` (int): foreign key to `User`'s table
- `community_id` (int): foreign key to `Community`'s table
- `post_name` (str): name of the post
- `description` (str): description of the post
- `create_dttm` (datetime): date and time of creation

## **Comment**

The `Comment` entity represents the comments made by users on various posts. Each comment has a unique ID, a post ID, a user ID (author), a comment text, and a creation timestamp.

Fields:
- `comment_id` (int): primary key
- `post_id` (int): foreign key to `Post`'s table
- `user_id` (int): foreign key to `User`'s table
- `comment` (str): comment
- `create_dttm` (datetime): date and time of creation

# **Relationship Tables**

## **CommunitySubscribe**

The `CommunitySubscribe` table captures the many-to-many relationship between `User` and `Community`, representing which users are subscribed to which communities.

Fields:
- `community_subscribe_id` (int): primary key
- `community_id` (int): foreign key to `Community`'s table
- `user_id` (int): foreign key to `User`'s table

## **LikePost**

The `LikePost` table captures the many-to-many relationship between `User` and `Post`, representing which users have liked which posts.

Fields:
- `like_post_id` (int): primary key
- `post_id` (int): foreign key to `Post`'s table
- `user_id` (int): foreign key to `User`'s table

## **SavePost**

The `SavePost` table captures the many-to-many relationship between `User` and `Post`, representing which users have saved which posts.

Fields:
- `save_post_id` (int): primary key
- `post_id` (int): foreign key to `Post`'s table
- `user_id` (int): foreign key to `User`'s table

# **Relationships**

1. A `User` can create multiple `Community` entities, but each `Community` is created by only one `User`.
2. A `User` can create multiple `Post` entities, but each `Post` is created by only one `User`.
3. A `User` can create multiple `Comment` entities