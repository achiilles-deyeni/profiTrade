from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import random
import asyncio
import datetime
from app.crypto_api import crypto_api

app = FastAPI()

# Set up templates and static files
template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

templates = Jinja2Templates(directory=template_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ChatRequest(BaseModel):
    query: str

def format_price(price: float) -> str:
    """Format price with appropriate decimals"""
    if price >= 1:
        return f"${price:,.2f}"
    else:
        return f"${price:.6f}"

def format_percentage(percentage: float) -> str:
    """Format percentage with color indicators"""
    if percentage > 0:
        return f"📈 +{percentage:.2f}%"
    else:
        return f"📉 {percentage:.2f}%"

async def generate_crypto_response(query: str) -> str:
    """Generate intelligent responses with real-time data"""
    
    query_lower = query.lower()
    
    # Get real-time data
    try:
        prices = await crypto_api.get_crypto_prices()
        market_data = await crypto_api.get_market_data()
        trending = await crypto_api.get_trending_coins()
    except Exception as e:
        print(f"API Error: {e}")
        prices = {}
        market_data = {}
        trending = []
    
    # Price queries
    if any(word in query_lower for word in ['price', 'cost', 'worth', 'value']):
        if 'bitcoin' in query_lower or 'btc' in query_lower:
            btc_data = prices.get('bitcoin', {})
            if btc_data:
                price = btc_data.get('usd', 0)
                change = btc_data.get('usd_24h_change', 0)
                mcap = btc_data.get('usd_market_cap', 0)
                
                return f"""₿ Bitcoin (BTC) Live Data:

💰 Current Price: {format_price(price)}
📊 24h Change: {format_percentage(change)}
🏪 Market Cap: ${mcap:,.0f}

Analysis: Bitcoin is {'showing strength' if change > 0 else 'experiencing volatility'}. 
{'Good buying opportunity for long-term holders.' if change < -5 else 'Consider taking some profits if heavily invested.' if change > 10 else 'Normal market movement.'}

⚡ Data updated in real-time"""
        
        elif 'ethereum' in query_lower or 'eth' in query_lower:
            eth_data = prices.get('ethereum', {})
            if eth_data:
                price = eth_data.get('usd', 0)
                change = eth_data.get('usd_24h_change', 0)
                mcap = eth_data.get('usd_market_cap', 0)
                
                return f"""🔷 **Ethereum (ETH) Live Data:**

💰 Current Price: {format_price(price)}
📊 24h Change: {format_percentage(change)}
🏪 Market Cap: ${mcap:,.0f}

Analysis: Ethereum is {'bullish with strong momentum' if change > 5 else 'bearish, consider waiting' if change < -5 else 'stable, good for DCA'}.
The ETH 2.0 upgrade continues to drive long-term value.

⚡ Live market data"""
    
    # Market overview
    elif any(word in query_lower for word in ['market', 'overview', 'sentiment', 'overall']):
        if market_data and 'data' in market_data:
            global_data = market_data['data']
            total_mcap = global_data.get('total_market_cap', {}).get('usd', 0)
            btc_dominance = global_data.get('market_cap_percentage', {}).get('btc', 0)
            
            # Get top coin performances
            top_movers = []
            for coin, data in list(prices.items())[:5]:
                change = data.get('usd_24h_change', 0)
                top_movers.append((coin.title(), change))
            
            return f"""📊 Live Crypto Market Overview:

🌍 Total Market Cap: ${total_mcap:,.0f}
₿ Bitcoin Dominance: {btc_dominance:.1f}%

📈 Top Movers (24h):
{chr(10).join([f'• {coin}: {format_percentage(change)}' for coin, change in sorted(top_movers, key=lambda x: x[1], reverse=True)[:3]])}

Market Sentiment: {'🟢 Bullish - Good time for entries' if btc_dominance > 45 else '🔴 Altcoin season - High volatility' if btc_dominance < 40 else '🟡 Neutral - Sideways movement'}

⚡ Updated every 5 minutes"""
    
    # Trending coins
    elif any(word in query_lower for word in ['trending', 'hot', 'popular', 'what\'s up']):
        if trending:
            trending_list = []
            for i, coin in enumerate(trending[:5], 1):
                name = coin['item']['name']
                symbol = coin['item']['symbol']
                rank = coin['item']['market_cap_rank'] or 'N/A'
                trending_list.append(f"{i}. **{name} ({symbol})** - Rank #{rank}")
            
            return f"""🔥 Trending Cryptocurrencies Right Now:

{chr(10).join(trending_list)}

What's driving the trends:
• Social media mentions increasing
• Trading volume spikes
• News and announcements

💡 Remember: Trending doesn't always mean good investment. Do your research!

⚡ Live trending data"""

    # Long-term investment with current data
    elif any(word in query_lower for word in ['long-term', 'hold', 'invest', 'buy']):
        btc_price = prices.get('bitcoin', {}).get('usd', 0)
        eth_price = prices.get('ethereum', {}).get('usd', 0)
        
        return f"""🚀 **Long-Term Investment Strategy (Live Data):**

Tier 1 - Safe Bets:
• Bitcoin (BTC) - Current: {format_price(btc_price) if btc_price else 'Loading...'}
• Ethereum (ETH) - Current: {format_price(eth_price) if eth_price else 'Loading...'}

Tier 2 - Growth Plays:
{chr(10).join([f'• {coin.title()} - {format_price(data.get("usd", 0))} ({format_percentage(data.get("usd_24h_change", 0))})' for coin, data in list(prices.items())[2:5]])}

Strategy:
1. Dollar-cost average weekly
2. 60% BTC/ETH, 40% altcoins
3. Hold through volatility
4. Take profits at 2x, 5x, 10x

⚠️ Current market conditions: {'Favorable for accumulation' if btc_price and any(data.get('usd_24h_change', 0) < 0 for data in prices.values()) else 'Consider waiting for dips'}

⚡ Prices updated in real-time"""
    
    # Default response with live data
    else:
        btc_change = prices.get('bitcoin', {}).get('usd_24h_change', 0)
        market_mood = '🟢 Bullish' if btc_change > 2 else '🔴 Bearish' if btc_change < -2 else '🟡 Neutral'
        
        return f"""💰 ProfiTrade Live Market Dashboard:

Current Market Mood: {market_mood}
Bitcoin 24h: {format_percentage(btc_change)}

I can help you with:
🔍 "Bitcoin price" - Live BTC data & analysis
📊 "Market overview" - Total market sentiment
🔥 "What's trending" - Hot coins right now
💡 "Investment advice" - Strategies with current prices
🎯 "Should I buy [coin]" - Specific coin analysis

**Quick Commands:**
• "Show me Bitcoin" → Live BTC analysis
• "Market sentiment" → Overall crypto market
• "Best coins to buy" → Top recommendations

⚡ *All data updates every 5 minutes*

What would you like to explore?"""

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat/ask")
async def chat_endpoint(chat_request: ChatRequest):
    # Generate intelligent response with real-time data
    response = await generate_crypto_response(chat_request.query)
    return {"response": response}

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}