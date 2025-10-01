import os
from decouple import config

# API Keys (get free keys from these services)
COINMARKETCAP_API_KEY = config('COINMARKETCAP_API_KEY', default='your_api_key_here')
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1'

# Cache settings
CACHE_DURATION = 300  # 5 minutes in seconds