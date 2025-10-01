import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CryptoAPIService:
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_duration = 300  # 5 minutes
        
    async def _make_request(self, url: str, headers: dict = None) -> dict:
        """Make async HTTP request with error handling"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache_timestamps:
            return False
        return datetime.now() - self.cache_timestamps[key] < timedelta(seconds=self.cache_duration)
    
    async def get_crypto_prices(self, symbols: List[str] = None) -> Dict:
        """Get current crypto prices from CoinGecko"""
        if symbols is None:
            symbols = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polygon']
        
        cache_key = f"prices_{'-'.join(symbols)}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        symbols_str = ','.join(symbols)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbols_str}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
        
        data = await self._make_request(url)
        if data:
            self.cache[cache_key] = data
            self.cache_timestamps[cache_key] = datetime.now()
            return data
        
        return {}
    
    async def get_market_data(self) -> Dict:
        """Get overall market data"""
        cache_key = "market_data"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        url = "https://api.coingecko.com/api/v3/global"
        data = await self._make_request(url)
        
        if data:
            self.cache[cache_key] = data
            self.cache_timestamps[cache_key] = datetime.now()
            return data
        
        return {}
    
    async def get_trending_coins(self) -> List:
        """Get trending cryptocurrencies"""
        cache_key = "trending"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        url = "https://api.coingecko.com/api/v3/search/trending"
        data = await self._make_request(url)
        
        if data and 'coins' in data:
            trending = data['coins']
            self.cache[cache_key] = trending
            self.cache_timestamps[cache_key] = datetime.now()
            return trending
        
        return []
    
    async def get_coin_details(self, coin_id: str) -> Dict:
        """Get detailed information about a specific coin"""
        cache_key = f"coin_{coin_id}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&community_data=false&developer_data=false"
        data = await self._make_request(url)
        
        if data:
            self.cache[cache_key] = data
            self.cache_timestamps[cache_key] = datetime.now()
            return data
        
        return {}

# Global instance
crypto_api = CryptoAPIService()