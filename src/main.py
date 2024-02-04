from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


@app.get('/')
def home():
    welcome = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Hospital Manager</title>
            </head>
            <body>
                <h1>Welcome to Hospital Manager API</h1>
                <p>This API serves as a appointments manager for hospitals.</p>
                <p>Check out the documentation to get started with the API.</p>
                <p>Documentation: <a href="https://{os.getenv("API_URL")}/docs">Documentation</a></p>
            </body>
        </html>
    '''

    return HTMLResponse(content=welcome, status_code=200)