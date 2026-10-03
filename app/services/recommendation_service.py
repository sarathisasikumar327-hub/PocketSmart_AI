import json
from .catalog_service import get_catalog, search_url
from .gemini_service import generate_recommendations

def fallback(planner, payload):
    budget = float(payload["budget"])
    catalog = get_catalog(planner)
    if planner == "home":
        weights = {"Lighting": .15, "Fan": .15, "Furniture": .40, "Decor": .15, "Storage": .15}
        desired = {"Lighting": payload.get("lights", 1), "Fan": payload.get("fans", 1), "Furniture": payload.get("tables", 1), "Decor": 1, "Storage": 1}
    elif planner == "party":
        weights = {"Food": .45, "Decoration": .20, "Entertainment": .15, "Accommodation": .20}
        desired = {"Food": payload.get("guests", 1), "Decoration": 1, "Entertainment": 1, "Accommodation": 1}
    else:
        weights = {"Necklace": .35, "Earrings": .20, "Bracelet": .20, "Ring": .15}
        desired = {"Necklace": 1, "Earrings": 1, "Bracelet": 1, "Ring": 1}

    allocations = [{"category": k, "amount": round(budget*v), "reason": f"Planned share for {k}."} for k,v in weights.items()]
    recs = []
    for item in catalog:
        cat = item["category"]
        if cat not in weights:
            continue
        qty = desired.get(cat, 1)
        price = item["base_price"] * (qty if item.get("unit") == "guest" else 1)
        if price <= budget * 0.75 or len(recs) < 3:
            recs.append({
                "name": item["name"], "category": cat, "estimated_price": round(price),
                "platform": item["platform"],
                "reason": f"Fits the {cat.lower()} portion of your plan.",
                "search_query": item["name"]
            })
        if len(recs) >= 6:
            break
    return {
        "summary": f"A fallback {planner} plan was created for a budget of ₹{budget:,.0f}.",
        "budget_allocation": allocations,
        "recommendations": recs,
        "tips": ["Compare final prices before purchase.", "Use the platform links to verify current availability and delivery charges."]
    }

def make_recommendation(planner, payload, image_path=None):
    catalog = get_catalog(planner)
    ai = generate_recommendations(planner, payload, catalog, image_path)
    result = ai if isinstance(ai, dict) else fallback(planner, payload)
    for r in result.get("recommendations", []):
        r["link"] = search_url(r.get("platform", ""), r.get("search_query") or r.get("name", ""))
    result["planner"] = planner
    return result
