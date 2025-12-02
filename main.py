from dotenv import load_dotenv
import os
import google.generativeai as genai


load_dotenv()

# --- CONFIG ---
api_key=os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-pro")

print("Gemini Chatbot Ready! Type 'exit' to quit.\n")

chat = model.start_chat(history=[])

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = chat.send_message(user_input)
    print("Bot:", response.text)

#Tool 
# Streaming 

"""

# Print chat history
for msg in chat.history:
    role = msg.role.capitalize()
    text = msg.parts[0].text
    print(f"{role}: {text}")

"""

