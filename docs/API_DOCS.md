# API Documentation

## Base URL

```
http://localhost:5000
```

## Authentication

All protected routes require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### POST /signup

Creates a new user account.

Request:

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

Response:

```json
{
  "message": "User registered successfully",
  "status": 201
}
```

#### POST /login

Authenticates a user.

Request:

```json
{
  "email": "string",
  "password": "string"
}
```

Response:

```json
{
  "message": "Login successful",
  "token": "jwt_token",
  "status": 200
}
```

### Comments

#### GET /comments/{post_id}

Retrieves all comments for a post.

Response:

```json
{
  "comments": [
    {
      "_id": "string",
      "content": "string",
      "user_id": "string",
      "username": "string",
      "created_at": "string",
      "replies": []
    }
  ],
  "total_comments": "number",
  "status": 200
}
```

#### POST /comments

Creates a new comment.

Request:

```json
{
  "post_id": "string",
  "content": "string",
  "parent_id": "string" // optional
}
```

Response:

```json
{
  "message": "Comment added successfully",
  "comment_id": "string",
  "status": 201
}
```
