import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, RecommendationHistory
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard")
def dashboard(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).limit(10).all()
    return request.app.state.templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "history": history})

@router.get("/history")
def history(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(RecommendationHistory).filter_by(user_id=user.id).order_by(RecommendationHistory.created_at.desc()).all()
    parsed = []
    for h in items:
        parsed.append({"id": h.id, "planner_type": h.planner_type, "budget": h.budget, "created_at": h.created_at, "query": json.loads(h.query_json), "result": json.loads(h.result_json)})
    return request.app.state.templates.TemplateResponse("history.html", {"request": request, "user": user, "items": parsed})
