# Social Media API

A Django REST Framework API for social media functionality with custom user authentication.

## Features

- Custom User Model with bio, profile picture, and followers
- Token-based authentication
- User registration and login
- Profile management
- Follow/unfollow functionality

## Setup Instructions

### 1. Install Dependencies

```bash
pip install django djangorestframework pillow
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication Endpoints

- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/token/` - Get authentication token

### Profile Endpoints

- `GET /api/accounts/profile/` - Get current user profile
- `PUT /api/accounts/profile/` - Update current user profile
- `GET /api/accounts/user/{username}/` - Get user profile by username

### Social Endpoints

- `POST /api/accounts/follow/{username}/` - Follow/unfollow user

## Testing the API

### Using the Test Script

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Run the test script:
   ```bash
   python test_api.py
   ```

### Using Postman

1. **Register a new user:**
   - Method: POST
   - URL: `http://localhost:8000/api/accounts/register/`
   - Body (JSON):
   ```json
   {
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpass123",
       "password_confirm": "testpass123",
       "first_name": "Test",
       "last_name": "User",
       "bio": "This is a test user"
   }
   ```

2. **Login:**
   - Method: POST
   - URL: `http://localhost:8000/api/accounts/login/`
   - Body (JSON):
   ```json
   {
       "username": "testuser",
       "password": "testpass123"
   }
   ```

3. **Get Profile (with authentication):**
   - Method: GET
   - URL: `http://localhost:8000/api/accounts/profile/`
   - Headers: `Authorization: Token <your_token>`

## Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Token <your_token>
```

## Custom User Model

The project uses a custom user model (`CustomUser`) that extends Django's `AbstractUser` with:

- `bio`: Text field for user biography
- `profile_picture`: Image field for profile pictures
- `followers`: Many-to-many relationship for following functionality

## File Structure

```
social_media_api/
├── accounts/
│   ├── models.py          # Custom user model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── social_media_api/
│   ├── settings.py        # Project settings
│   └── urls.py            # Main URL configuration
├── manage.py
├── test_api.py            # Test script
└── README.md
```
