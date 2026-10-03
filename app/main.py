from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .database import Base, engine
from .routers import auth, planners, dashboard

BASE_DIR = Path(__file__).resolve().parent
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PocketSmart AI", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.state.templates = templates

app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(dashboard.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs-info")
def docs_info():
    return {"message": "PocketSmart AI API", "docs": "/docs"}

@app.get("/startup")
def startup():
    return {"status": "ready", "service": "PocketSmart AI"}

@app.get("/session-info")
def session_info(request: Request):
    return {"logged_in": bool(request.cookies.get("access_token"))}

@app.get("/session-data")
def session_data(request: Request):
    return {"logged_in": bool(request.cookies.get("access_token"))}
