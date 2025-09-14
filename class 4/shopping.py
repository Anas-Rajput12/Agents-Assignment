from agents import Agent, Runner
from connection import config
import requests
import random

API_URL = "https://hackathon-apis.vercel.app/api/products"
def fetch_products(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def filter_products_by_category(products_list, category_name):
    filtered = [p for p in products_list if category_name.lower() in p['category']['name'].lower()]
    return filtered if filtered else products_list[:5]


def format_products(products_list):
    formatted = ""
    for p in products_list[:5]:  
        formatted += f"- **{p['name']}** (${p['price']}): {p['description']}\n"
    return formatted


def run_shopping_agent():
    products = fetch_products(API_URL)

    agent1 = Agent(
        name="welcome_agent",
        instructions="Welcome the user warmly in one short, catchy sentence."
    )
    result1 = Runner.run_sync(agent1, "user arrived at store", run_config=config)
    print("\n(Welcome):", result1.final_output)

    agent2 = Agent(
        name="query_agent",
        instructions="Ask the user professionally: 'What type of product are you interested in today?'"
    )
    result2 = Runner.run_sync(agent2, "", run_config=config)
    print("(Query):", result2.final_output)

    user_category = input("\nYou: ")

    filtered_products = filter_products_by_category(products, user_category)
    agent3 = Agent(
        name="product_agent",
        instructions=(
            f"Present these products in a professional and catchy way for user query: '{user_category}'.\n"
            f"Products:\n{format_products(filtered_products)}"
        )
    )
    result3 = Runner.run_sync(agent3, user_category, run_config=config)
    print("\n(Products):", result3.final_output)

    buy_input = input("\nDo you want to buy any product? (yes/no): ").strip().lower()
    if buy_input in ["yes", "y"]:
        payment_options = {
            "1": "Credit Card",
            "2": "Debit Card",
            "3": "PayPal",
            "4": "Cash on Delivery"
        }

        print("\nPlease select a payment method:")
        for key, value in payment_options.items():
            print(f"{key}. {value}")

        choice = input("\nEnter option number (1-4): ").strip()
        selected_method = payment_options.get(choice, "Invalid choice")

        if selected_method != "Invalid choice":
            agent4 = Agent(
                name="payment_agent",
                instructions=f"You have selected **{selected_method}** as your payment method. Confirm purchase in a professional and catchy way."
            )
            result4 = Runner.run_sync(agent4, "user selected payment", run_config=config)
            print("\n(Payment):", result4.final_output)

            order_id = f"ORD{random.randint(1000,9999)}"
            delivery_days = random.choice([3, 5, 7])
            agent5 = Agent(
                name="confirmation_agent",
                instructions=f"Confirm the order with ID {order_id} and expected delivery in {delivery_days} days. Make it sound professional and friendly."
            )
            result5 = Runner.run_sync(agent5, "confirm order", run_config=config)
            print("\n(Confirmation):", result5.final_output)

    agent6 = Agent(
        name="thanks_agent",
        instructions="Thank the user warmly and professionally for visiting/shopping."
    )
    result6 = Runner.run_sync(agent6, "end of interaction", run_config=config)
    print("\n(Thanks):", result6.final_output)


if __name__ == "__main__":
    run_shopping_agent()
