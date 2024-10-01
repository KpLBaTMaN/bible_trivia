# Bible Trivia Frontend

A mobile-friendly frontend for the Bible Trivia website built with FastAPI and Bootstrap.

## Features

- Responsive Design using Bootstrap
- User Authentication (Register, Login, Logout)
- Dashboard displaying user progress and available trivia sections
- Trivia sections with multiple-choice questions
- Global and Section-specific Leaderboards
- Accessible and Intuitive UI

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/bible_trivia_frontend.git
    cd bible_trivia_frontend
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**

    ```bash
    uvicorn app.main:app --reload
    ```

5. **Access the Website**

    Open your browser and navigate to `http://localhost:8000`.

## Customization

- **Branding**: Update colors and logos in `app/static/css/styles.css` and `app/static/images/`.
- **API Base URL**: Adjust the `API_BASE_URL` in `app/utils.py` if your backend is hosted elsewhere.
- **Templates**: Modify HTML templates in `app/templates/` to fit your design preferences.

## Deployment

For production deployment, consider using a production-ready server like **Gunicorn** with **Uvicorn Workers** and setting up SSL for secure connections.

Example using Gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
