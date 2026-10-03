# PocketSmart AI — Smart Budget & Recommendation Assistant

PocketSmart AI is a FastAPI + Jinja2 + Gemini-powered budget recommendation assistant based on the supplied project documentation.

## Features
- User registration, login, logout and JWT authentication
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image upload
- Gemini-powered recommendation generation
- Budget-aware allocation
- Platform-aware links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO
- Recommendation history
- User dashboard
- Responsive HTML/CSS/JavaScript UI
- Local SQLite database
- Graceful fallback recommendations when Gemini is unavailable

## Project structure
```text
PocketSmart_AI/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── planners.py
│   │   └── dashboard.py
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── recommendation_service.py
│   │   └── catalog_service.py
│   ├── templates/
│   └── static/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 1. Install Python
Use Python 3.10+.

## 2. Create a virtual environment
Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies
```powershell
pip install -r requirements.txt
```

## 4. Configure Gemini
Create `.env` from `.env.example`:
```powershell
copy .env.example .env
```
Then put your Gemini API key into `GEMINI_API_KEY`.

The model is configurable using `GEMINI_MODEL`. If `gemini-1.5-flash-pro` is available in your environment and you specifically need the model named in the documentation, set:
```text
GEMINI_MODEL=gemini-1.5-flash-pro
```
Otherwise use a currently available Gemini Flash model.

## 5. Run
```powershell
uvicorn app.main:app --reload
```

Open:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

## 6. Demo account
Register a new account from the UI. Passwords are hashed before storage.

## How recommendations work
1. User enters budget and preferences.
2. FastAPI validates the request.
3. The recommendation service creates a structured budget plan.
4. Gemini receives a domain-specific prompt.
5. The AI response is parsed into recommendation cards.
6. If Gemini is unavailable or returns invalid output, deterministic fallback recommendations are returned.
7. The result is saved in recommendation history.

## Product/service links
The supplied documentation mentions third-party sources such as Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO. This implementation uses safe search links and a local catalog rather than scraping those sites. This avoids hard-coded fake prices and avoids depending on private APIs.

## Important security notes
- Never commit `.env`.
- Replace `SECRET_KEY` before deployment.
- For production, use HTTPS, a production database, secure cookies, rate limiting, and a proper secret manager.
- Uploaded images are stored locally in `app/static/uploads/` for this demo.

## Testing
```powershell
pytest -q
```
