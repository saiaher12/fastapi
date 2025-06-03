# FastAPI User Management Application

This project is a simple user management application built using FastAPI. It provides a RESTful API for managing users, including functionalities to create, read, update, and delete users. The application also serves a frontend interface using Jinja2 templates.

## Project Structure

```
fastapi
├── log.py               # FastAPI application code
├── templates            # Directory for HTML templates
│   └── index.html       # Main HTML template served by the application
├── .env                 # Environment variables for database connection
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/saiaher12/fastapi.git
   cd fastapi
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your database connection details:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=fastapi
   DB_PORT=3306
   ```

5. **Run the application:**
   ```
   uvicorn log:app --reload
   ```

## Usage

- Navigate to `http://localhost:8000` to access the frontend interface.
- Use the following API endpoints for user management:
  - `GET /users` - Retrieve all users
  - `POST /users` - Create a new user
  - `PUT /users/{id}` - Update an existing user
  - `DELETE /users/{id}` - Delete a user

## License

This project is licensed under the MIT License.