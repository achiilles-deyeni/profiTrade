from app.data.crypto_db import crypto_db

def get_most_sustainable():
    return max(crypto_db, key=lambda x: crypto_db[x]["sustainability_score"])

def get_trending():
    return [coin for coin, data in crypto_db.items() if data["price_trend"] == "rising"]

def get_profitable():
    return [coin for coin, data in crypto_db.items() if data["price_trend"] == "rising" and data["market_cap"] == "high"]

def advise(user_query: str):
    query = user_query.lower()
    if "sustainable" in query:
        coin = get_most_sustainable()
        return f"{coin} is the most sustainable choice!"
    elif "trending" in query or "up" in query:
        return f"Trending coins: {', '.join(get_trending())}"
    elif "profitable" in query or "investment" in query:
        picks = get_profitable()
        return f"Profitable pick: {picks[0]}" if picks else "No profitable picks right now."
    else:
        return "I’m not sure. Try asking about 'sustainable', 'trending', or 'profitable'."
