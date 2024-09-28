from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="app/templates")

# Backend API URL (point this to your backend API)
API_BASE_URL = "http://192.168.4.39:8000"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the main HTML page.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Fetch all questions from the backend
            response = await client.get(f"{API_BASE_URL}/questions/")
            response.raise_for_status()  # Raise an exception if the status code is not 2xx
            questions = response.json()
    except httpx.HTTPError as e:
        # Log the error and provide a useful response
        print(f"HTTP Error occurred: {e}")
        return HTMLResponse("Failed to fetch questions.", status_code=500)

    # Pass the questions data to the template
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions})