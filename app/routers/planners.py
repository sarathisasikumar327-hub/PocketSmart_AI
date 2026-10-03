import json, uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, RecommendationHistory
from ..dependencies import get_current_user
from ..services.recommendation_service import make_recommendation

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_history(db, user, planner, payload, result):
    h = RecommendationHistory(user_id=user.id, planner_type=planner, budget=float(payload["budget"]),
                               query_json=json.dumps(payload), result_json=json.dumps(result))
    db.add(h); db.commit()

@router.get("/planner/{planner}")
def planner_page(planner: str, request: Request):
    if planner not in {"home", "party", "jewelry"}:
        return HTMLResponse("Planner not found", status_code=404)
    return request.app.state.templates.TemplateResponse(f"{planner}_planner.html", {"request": request, "planner": planner})

@router.post("/generate-home")
def generate_home(request: Request, budget: float = Form(...), room: str = Form(...), style: str = Form(...),
                  lights: int = Form(2), fans: int = Form(1), tables: int = Form(1), extra: str = Form(""),
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    payload = {"budget": budget, "room": room, "style": style, "lights": lights, "fans": fans, "tables": tables, "extra": extra}
    result = make_recommendation("home", payload)
    save_history(db, user, "home", payload, result)
    return request.app.state.templates.TemplateResponse("recommendations.html", {"request": request, "result": result, "title": "Home Interior Recommendations"})

@router.post("/generate-party")
def generate_party(request: Request, budget: float = Form(...), event_type: str = Form(...), guests: int = Form(...),
                   venue: str = Form(...), food_preference: str = Form(...), extra: str = Form(""),
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    payload = {"budget": budget, "event_type": event_type, "guests": guests, "venue": venue, "food_preference": food_preference, "extra": extra}
    result = make_recommendation("party", payload)
    save_history(db, user, "party", payload, result)
    return request.app.state.templates.TemplateResponse("recommendations.html", {"request": request, "result": result, "title": "Party Budget Recommendations"})

@router.post("/generate-jewelry")
async def generate_jewelry(request: Request, budget: float = Form(...), occasion: str = Form(...), style: str = Form(...),
                           metal: str = Form(...), outfit_color: str = Form(""), extra: str = Form(""),
                           outfit_image: UploadFile | None = File(None), user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    image_path = None
    image_name = ""
    if outfit_image and outfit_image.filename:
        ext = Path(outfit_image.filename).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            return HTMLResponse("Only JPG, JPEG, PNG and WEBP images are supported.", status_code=400)
        image_name = f"{uuid.uuid4().hex}{ext}"
        image_path = str(UPLOAD_DIR / image_name)
        content = await outfit_image.read()
        if len(content) > 5 * 1024 * 1024:
            return HTMLResponse("Image must be 5 MB or smaller.", status_code=400)
        Path(image_path).write_bytes(content)

    payload = {"budget": budget, "occasion": occasion, "style": style, "metal": metal, "outfit_color": outfit_color, "extra": extra}
    result = make_recommendation("jewelry", payload, image_path)
    save_history(db, user, "jewelry", payload, result)
    return request.app.state.templates.TemplateResponse("recommendations.html", {"request": request, "result": result, "title": "Jewelry Recommendations"})
