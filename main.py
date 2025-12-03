from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

# Load API Key
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# ---------- Tool Function ----------
def calculator(a: float, b: float, operator: str):
    if operator == "+": return a + b
    if operator == "-": return a - b
    if operator == "*": return a * b
    if operator == "/": return a / b if b != 0 else "Error: Division by zero"
    return "Invalid operator"


tools = [
    {
        "function_declarations": [
            {
                "name": "calculator",
                "description": "Performs arithmetic operations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"},
                        "operator": {
                            "type": "string",
                            "enum": ["+", "-", "*", "/"]
                        }
                    },
                    "required": ["a", "b", "operator"]
                }
            }
        ]
    }
]

# ---------- Model ----------
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-pro",
    tools=tools,
    system_instruction=(
        "You are a helpful AI assistant. "
        "You answer any general question normally. "
        "Use the calculator tool ONLY when user asks to compute, calculate, solve, or evaluate math expressions."
    )
)

chat = model.start_chat(history=[])

print("\nGemini Bot Ready! Type `exit` to quit.\n")

# ---------- Chat Loop ----------
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye")
        break

    response = chat.send_message(user_input, stream=True)

    print("Bot:", end=" ", flush=True)
    function_call = None

    # ---- Stream first model reply ----
    for chunk in response:
        for part in chunk.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                for char in part.text:
                    print(char, end="", flush=True)
                    time.sleep(0.03)

            if hasattr(part, "function_call") and part.function_call:
                function_call = part.function_call

    print() 

    # ---- If tool call required ----
    if function_call:
        print(f"\n🔧 Tool call detected → {function_call.name}()")

        args = dict(function_call.args)
        result = calculator(**args)

        followup = chat.send_message({
            "function_response": {
                "name": function_call.name,
                "response": {"result": result}
            }
        }, stream=True)

        print("Bot:", end=" ", flush=True)

        for chunk in followup:
            for part in chunk.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    for char in part.text:
                        print(char, end="", flush=True)
                        time.sleep(0.03)

        print("\n")  
