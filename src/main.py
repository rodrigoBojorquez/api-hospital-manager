from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import public, doctors, users, admin

app = FastAPI(title="Medical appointment manager")

# ROUTERS
app.include_router(public.router)
app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(admin.router)

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
                <p>This API serves as an appointments manager for hospitals.</p>
                <p>Check out the documentation to get started with the API.</p>
                <p>Documentation: <a href="/docs">Documentation</a></p>
            </body>
        </html>
    '''

    return HTMLResponse(content=welcome, status_code=200)