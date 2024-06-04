# FastAPI Authentication and User Management

This project provides a basic user authentication and management system using FastAPI. Users can register, log in, log out, and delete their accounts. Additionally, all requests during these operations are logged and stored in a database.

## Setup

### Requirements

- Python 3.12+
- SQLite (or another supported database)
- Virtualenv (optional but recommended)

### Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/sakiphan/FastAPI-python.git
    cd FastAPI-python
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate  # Windows
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Start the FastAPI application:
    ```bash
    python run.py
    ```

5. To run the HTML file through a server:
    ```bash
    python -m http.server 8000
    ```

## Usage

### Home Page

Open your browser and go to `http://127.0.0.1:8001`. Here you can register and log in.

### Register

1. Click on the `Register` button.
2. Enter the username, email, full name, and password.
3. Click the `Register` button.
4. After successful registration, you will be redirected to the login page.

### Login

1. Click on the `Login` button.
2. Enter the username and password.
3. Click the `Login` button.
4. After successful login, you will be redirected to the user actions page.

### Logout

1. Click the `Logout` button.
2. After successful logout, you will be redirected back to the login page.

### Delete Account

1. Click the `Delete Account` button.
2. After successfully deleting your account, you will be redirected to the registration page.

## Project Structure

- `main.py`: The main file for the FastAPI application.
- `auth.py`: Handles authentication and JWT token operations.
- `crud.py`: Database operations (CRUD operations).
- `database.py`: Database connection and session management.
- `logs.py`: Logging database operations.
- `schemas.py`: Pydantic models for request and response validation.
- `middleware.py`: Middleware for logging requests.
- `run.py`: Script to start the FastAPI application.
- `index.html`: HTML file for testing the registration, login, logout, and account deletion.

## Example HTML File

The HTML file `index.html` provides a simple interface to test the API. It includes forms for registration, login, logout, and account deletion, with a basic CSS style.

## Notes

- Make sure the FastAPI server is running on `http://127.0.0.1:8001` as the HTML file makes requests to this address.
- Ensure email validation is enforced to include an `@` symbol as required.