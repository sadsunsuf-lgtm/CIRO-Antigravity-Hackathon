
import os
import sys
from google import genai

# Use your working, authenticated project credentials
client = genai.Client(
    vertexai=True, 
    project="the-slate-494421-c8", 
    location="us-central1"
)

# Initialize a stateful multi-turn chat session using Gemini
chat = client.chats.create(model="gemini-2.5-flash")

print("\n====================================================")
print("?? UNLIMITED HACKATHON CHAT AGENT INITIALIZED")
print("====================================================")
print("Type your coding or design prompts below.")
print("Type \"exit\" or \"quit\" to close the session.\n")

while True:
    try:
        user_input = input("You ??: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("\nExiting chat. Good luck with the build!")
            break
            
        if not user_input.strip():
            continue
            
        print("\nGemini ??: Thinking...")
        response = chat.send_message(user_input)
        
        # Clear the "Thinking..." line and print the real response
        sys.stdout.write("\033[F\033[K") 
        print(f"Gemini ??:\n{response.text}\n")
        print("-" * 52)
        
    except KeyboardInterrupt:
        print("\nSession ended via keyboard interrupt.")
        break
    except Exception as e:
        print(f"\nError: {e}\n")

