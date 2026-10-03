from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.get("/register")
def register_page(request: Request):
    return request.app.state.templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    email = email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        return RedirectResponse("/register?error=Email+already+registered", status_code=303)
    user = User(name=name.strip(), email=email, password_hash=hash_password(password))
    db.add(user); db.commit(); db.refresh(user)
    token = create_access_token(user.id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return response

@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        return RedirectResponse("/login?error=Invalid+email+or+password", status_code=303)
    token = create_access_token(user.id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=86400)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
