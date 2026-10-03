import os, json, re
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types

def get_client():
    key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=key) if key else None

def _extract_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return None
    return None

def generate_recommendations(planner: str, payload: dict, catalog: list, image_path: Optional[str] = None):
    client = get_client()
    if not client:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = f"""
You are PocketSmart AI, a budget-aware recommendation assistant.
Planner: {planner}
User input:
{json.dumps(payload, indent=2)}

Candidate catalog:
{json.dumps(catalog, indent=2)}

Create practical recommendations that stay within the user's total budget.
Return ONLY valid JSON with this exact structure:
{{
  "summary": "short summary",
  "budget_allocation": [
    {{"category": "name", "amount": 0, "reason": "short reason"}}
  ],
  "recommendations": [
    {{
      "name": "item",
      "category": "category",
      "estimated_price": 0,
      "platform": "platform",
      "reason": "why it fits",
      "search_query": "search phrase"
    }}
  ],
  "tips": ["tip 1", "tip 2"]
}}
Use only realistic estimates. Do not claim live availability. Keep the total estimated recommendation spend within the budget.
"""
    contents = [prompt]
    if image_path and Path(image_path).exists():
        data = Path(image_path).read_bytes()
        mime = "image/jpeg"
        if image_path.lower().endswith(".png"):
            mime = "image/png"
        contents.append(types.Part.from_bytes(data=data, mime_type=mime))
        contents.append("Analyze the outfit image only for broad color/style coordination. Do not identify the person.")

    try:
        response = client.models.generate_content(model=model, contents=contents)
        return _extract_json(response.text or "")
    except Exception:
        return None
