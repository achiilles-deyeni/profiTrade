from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import random

app = FastAPI()

# Set up templates and static files
template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

templates = Jinja2Templates(directory=template_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ChatRequest(BaseModel):
    query: str

def generate_crypto_response(query: str) -> str:
    """Generate intelligent responses based on query content"""
    
    query_lower = query.lower()
    
    # Long-term investment advice
    if any(word in query_lower for word in ['long-term', 'long term', 'hold', 'hodl', 'years']):
        responses = [
            """🚀 **For Long-Term Growth (3-5+ years):**

**Top Tier (Lower Risk):**
• **Bitcoin (BTC)** - Digital gold, store of value, institutional adoption
• **Ethereum (ETH)** - Smart contracts, DeFi ecosystem, ETH 2.0 upgrades

**High Potential (Higher Risk):**
• **Solana (SOL)** - Fast, scalable blockchain for DApps
• **Cardano (ADA)** - Academic approach, sustainable blockchain
• **Polygon (MATIC)** - Ethereum scaling solution

⚠️ **Remember:** Never invest more than you can afford to lose. Do your own research (DYOR)!""",
            
            """💡 **Long-term Crypto Strategy:**

**Core Holdings (60-70%):**
• Bitcoin & Ethereum - The safest bets in crypto

**Growth Plays (20-30%):**
• Layer 1 blockchains: Solana, Avalanche, Algorand
• DeFi tokens: Chainlink, Uniswap, Aave

**Moonshots (5-10%):**
• Emerging projects with strong fundamentals

📈 **Strategy:** Dollar-cost average (DCA) monthly, hold through volatility, take profits gradually."""
        ]
        
    # Short-term trading
    elif any(word in query_lower for word in ['short-term', 'trading', 'quick', 'fast']):
        responses = [
            """⚡ **Short-Term Trading Tips:**

**Technical Analysis Focus:**
• Watch Bitcoin dominance & market sentiment
• Use RSI, MACD, moving averages
• Set stop-losses (5-10% max loss)

**Hot Sectors:**
• AI tokens: FET, OCEAN, AGIX
• Gaming: IMX, SAND, MANA
• DeFi: UNI, SUSHI, COMP

⚠️ **Risk Warning:** Short-term trading is highly risky. 90% of traders lose money."""
        ]
        
    # Specific coin questions
    elif 'bitcoin' in query_lower or 'btc' in query_lower:
        responses = [
            """₿ **Bitcoin Analysis:**

**Bullish Factors:**
• Institutional adoption (Tesla, MicroStrategy, ETFs)
• Limited supply (21M max)
• Store of value narrative
• Lightning Network growth

**Price Targets:**
• Conservative: $80K-$100K this cycle
• Optimistic: $150K-$200K

**Strategy:** DCA weekly, hold long-term, never sell everything."""
        ]
        
    elif 'ethereum' in query_lower or 'eth' in query_lower:
        responses = [
            """🔷 **Ethereum Analysis:**

**Bullish Factors:**
• Ethereum 2.0 and staking rewards
• DeFi & NFT ecosystem leader  
• Layer 2 solutions scaling
• Deflationary tokenomics (EIP-1559)

**Risks:**
• High gas fees during congestion
• Competition from other smart contract platforms

**Target:** $8K-$15K potential this cycle."""
        ]
        
    # Market analysis
    elif any(word in query_lower for word in ['market', 'analysis', 'outlook', 'prediction']):
        responses = [
            """📊 **Current Market Analysis:**

**Bull Market Indicators:**
• Bitcoin halving cycle (2024)
• Institutional adoption increasing
• Regulatory clarity improving
• Spot Bitcoin ETFs approved

**Key Levels to Watch:**
• BTC: Support at $35K, resistance at $50K
• ETH: Support at $2K, resistance at $3K

**Timeline:** Potential peak in late 2024 - early 2025."""
        ]
        
    # Risk management
    elif any(word in query_lower for word in ['risk', 'safe', 'strategy', 'portfolio']):
        responses = [
            """🛡️ **Risk Management Strategy:**

**Portfolio Allocation:**
• 40% Bitcoin (safest crypto bet)
• 30% Ethereum (smart contract leader)  
• 20% Top altcoins (SOL, ADA, DOT)
• 10% High-risk/high-reward plays

**Rules:**
• Never invest borrowed money
• Take profits on the way up (20%, 50%, 80% gains)
• Set stop-losses for trading positions
• Keep 6 months expenses in traditional savings"""
        ]
        
    # General advice
    else:
        responses = [
            """💰 **General Crypto Investment Advice:**

**Golden Rules:**
1. Only invest what you can afford to lose
2. Do your own research (DYOR)
3. Dollar-cost average into positions
4. Think long-term (3-5+ years)
5. Diversify across different projects

**Red Flags:**
❌ Promises of guaranteed returns
❌ "Get rich quick" schemes  
❌ Anonymous teams
❌ No real use case or utility

Ask me about specific coins, strategies, or market analysis!""",
            
            """🎯 **How Can I Help You Today?**

I can assist with:
• **Coin Analysis** - BTC, ETH, altcoins
• **Market Trends** - Bull/bear signals
• **Trading Strategies** - DCA, swing trading  
• **Portfolio Advice** - Risk management
• **DeFi Projects** - Yield farming, staking

**Popular Questions:**
"Should I buy Bitcoin now?"
"Best altcoins for 2024?"
"How to start crypto investing?"

What specific aspect interests you most?"""
        ]
    
    return random.choice(responses)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat/ask")
async def chat_endpoint(chat_request: ChatRequest):
    # Generate intelligent response instead of just echoing
    response = generate_crypto_response(chat_request.query)
    return {"response": response}