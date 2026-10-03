from urllib.parse import quote_plus

CATALOG = {
    "home": [
        {"name": "LED Ceiling Light", "platform": "Amazon", "base_price": 1299, "category": "Lighting"},
        {"name": "Modern Ceiling Fan", "platform": "Amazon", "base_price": 2499, "category": "Fan"},
        {"name": "Compact Dining Table", "platform": "IKEA", "base_price": 7999, "category": "Furniture"},
        {"name": "Wall Art Set", "platform": "IKEA", "base_price": 1499, "category": "Decor"},
        {"name": "Storage Cabinet", "platform": "Amazon", "base_price": 5499, "category": "Storage"},
        {"name": "Accent Chair", "platform": "IKEA", "base_price": 6999, "category": "Furniture"},
    ],
    "party": [
        {"name": "Party Catering Package", "platform": "Zomato", "base_price": 350, "category": "Food", "unit": "guest"},
        {"name": "Food Delivery Package", "platform": "Swiggy", "base_price": 300, "category": "Food", "unit": "guest"},
        {"name": "Party Decoration Kit", "platform": "Amazon", "base_price": 1499, "category": "Decoration"},
        {"name": "Event Stay Search", "platform": "OYO", "base_price": 2499, "category": "Accommodation", "unit": "room"},
        {"name": "Sound & Lighting Package", "platform": "Amazon", "base_price": 3999, "category": "Entertainment"},
    ],
    "jewelry": [
        {"name": "Minimal Pendant Necklace", "platform": "Amazon", "base_price": 1299, "category": "Necklace"},
        {"name": "Elegant Stud Earrings", "platform": "Amazon", "base_price": 899, "category": "Earrings"},
        {"name": "Fashion Bracelet", "platform": "Flipkart", "base_price": 999, "category": "Bracelet"},
        {"name": "Statement Necklace Set", "platform": "Flipkart", "base_price": 2499, "category": "Necklace"},
        {"name": "Occasion Ring", "platform": "Amazon", "base_price": 1599, "category": "Ring"},
    ],
}

def search_url(platform, query):
    domains = {
        "Amazon": "https://www.amazon.in/s?k=",
        "Flipkart": "https://www.flipkart.com/search?q=",
        "IKEA": "https://www.ikea.com/in/en/search/?q=",
        "Swiggy": "https://www.swiggy.com/search?query=",
        "Zomato": "https://www.zomato.com/search?q=",
        "OYO": "https://www.oyorooms.com/search?location=",
    }
    return domains.get(platform, "https://www.google.com/search?q=") + quote_plus(query)

def get_catalog(planner):
    return CATALOG.get(planner, [])
