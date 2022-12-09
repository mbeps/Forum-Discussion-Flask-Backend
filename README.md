# Back-End System for Forum Site (Final Year Project)
- This is the back-end system for a forum site
- People can discuss about certain topics with other users in specific communities
- Each community has its own interests where specific types of discussions take place

## Features
### Authentication
- Sign up
- Log in

### Community
- Create communities
- Delete communities
- Subscribe to existing communities
- Unsubscribe from communities
- View all communities 
- View all subscribed communities

### Post
- Create posts
- Modify posts*
- Delete posts
- Comment on posts

### Comment
- Modify comments*
- Delete comments

## Requirements
- Poetry 1.2+
- Python 3.11+
- MySQL 8

# Instructions
**Set Up `.env` File**
- `.env.example` is provided 

**Installing Required Packages for Project**
```
poetry install
```

**Running Application**
```
poetry run python app.py 
```