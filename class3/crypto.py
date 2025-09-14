from agents import Agent, Runner
from connection import config
import requests

def get_crypto_price(symbol: str) -> str:
    """
    Fetch current price of a cryptocurrency from CoinGecko API.
    :param symbol: e.g., 'bitcoin', 'ethereum', 'dogecoin'
    :return: Price string
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if symbol.lower() in data:
            price = data[symbol.lower()]["usd"]
            return f"The current price of {symbol.capitalize()} is ${price} USD."
        else:
            return f"Cryptocurrency '{symbol}' not found."
    except Exception as e:
        return f"Error fetching price: {e}"

user_input = input("Enter your crypto query (e.g., 'Price of Bitcoin'): ")

crypto_keywords = ['bitcoin', 'ethereum', 'dogecoin', 'litecoin', 'ripple', 'cardano']

detected_crypto = next((c for c in crypto_keywords if c in user_input.lower()), None)

if detected_crypto:
    price_info = get_crypto_price(detected_crypto)
    print(price_info)  
    instructions = (
        f"You are a cryptocurrency assistant. Always use this price for {detected_crypto}: "
        f"{price_info} Answer the user's question in English based on this exact price."
    )
else:
    instructions = (
        "You are a cryptocurrency assistant. Answer crypto-related questions accurately in English."
    )

agent = Agent(
    name="crypto_agent",
    instructions=instructions
)

# Run AI Agent synchronously
result = Runner.run_sync(
    agent,
    user_input,
    run_config=config
)

print("Crypto Agent Response:", result.final_output)
