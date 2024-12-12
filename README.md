# morphling-bio-assignment
Assignment: Building a Scalable Backend Service  Objective  Design and implement a backend service that provides API endpoints

# FastAPI User Profile API
This is a simple FastAPI application for creating, retrieving, and managing user profiles. The application includes JWT-based authentication, SQLite database integration, and Docker containerization for easy deployment.


## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Run the Application Locally](#run-the-application-locally)
- [Docker Setup](#docker-setup)
- [Testing the Application](#testing-the-application)
- [Endpoints](#endpoints)

## Prerequisites

- Python 3.8 or later
- Docker (for containerization)
- Docker Compose (for managing multi-container apps)

## Installation and Setup

1. **Clone the repository:**

   Clone this repository to your local machine using the following command:

   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Create a virtual environment and activate it:**

   ```bash
    python3 -m venv venv
    source venv/bin/activate

   ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Set up the database:**
    # Add this line to create tables - database.py
    Base.metadata.create_all(bind=engine)

    # Run the code once:
    python main.py - run

5. **Start the development server:**
    uvicorn main:app --reload

6. **Access the Swagger UI documentation:**
    Open your web browser and navigate to http://localhost:8000/docs.

7. **Test the API endpoints** using tools like Postman or cURL.
    <!-- Test User Creation (POST /users): You can use a tool like Postman or curl to test the user creation API. The body should look like: -->

    # json data:

    {
    "name": "Krishna Kumar",
    "email": "kk@gmail.com",
    "role": "developer",
    "password": "********"
    }

    # Request:
    curl -X 'POST' \
    'http://127.0.0.1:8000/users' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "Krishna Kumar",
    "email": "kk@gmail.com",
    "role": "developer",
    "password": "********"
    }'

    <!-- Test Token Generation (POST /token): After creating a user, you can obtain a JWT token by passing the username and password: -->

    # json to pass
    {
    "username": "admin",
    "password": "password"
    }
    # Request:
    curl -X 'POST' \
    'http://127.0.0.1:8000/token' \
    -H 'Content-Type: application/json' \
    -d '{
        "username": "admin",
        "password": "password"
    }'

    <!-- The response will contain the JWT token: -->
    {
    "access_token": "<jwt-token>",
    "token_type": "bearer"
    }
    <!-- Access Protected Route (GET /secure-data): Use the token obtained in the previous step to access the protected route: -->

    # Request:
    curl -X 'GET' \
    'http://127.0.0.1:8000/secure-data' \
    -H 'Authorization: Bearer <your-jwt-token>'

8. **End points:**
    <!-- Endpoints: -->
    POST /users: Create a user profile
    GET /users: Retrieve user profiles based on search criteria (email/role)
    POST /token: Obtain a JWT token for authentication
    GET /secure-data: Access secure data (requires token)

9. **Docker Setup**
    # Build the Docker image:
    docker build -t fastapi-user-profile-api .

    # Run the Docker container:
    docker run -p 8000:8000 fastapi-user-profile-api

    Access the Swagger UI documentation at http://localhost:8000/docs.

10. **Docker compose**
    # Build the Docker image:
    docker-compose build

    # Run the Docker container:
    docker-compose up
11. **Run Tests**
    pytest tests/test_main.py
