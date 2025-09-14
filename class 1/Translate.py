from agents import Agent, Runner
from connection import config

languages = {
    "en": "English",
    "ur": "Urdu",
    "sd": "Sindhi",
    "roman": "Roman Urdu",
    "zh": "Chinese"
}

text = input("Enter text to translate: ")
print("Supported languages:", ', '.join(f"{code} ({name})" for code, name in languages.items()))

user_input = input("Enter target language code or name: ").lower()

if user_input in languages:
    target_lang = user_input
else:
    matched = [code for code, name in languages.items() if name.lower() == user_input]
    if matched:
        target_lang = matched[0]
    else:
        print("Language not supported. Defaulting to English.")
        target_lang = "en"

agent = Agent(
    name="translator",
    instructions=f"You are a translation assistant. Translate all input into {languages[target_lang]}."
)

result = Runner.run_sync(
    agent,
    text,
    run_config=config
)

print(f"Translated Text ({languages[target_lang]}): {result.final_output.encode('utf-8').decode('utf-8')}")

