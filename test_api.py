
from google import genai

# Direct initialization bypassing local file paths completely
client = genai.Client(
    vertexai=True,
    project="the-slate-494421-c8",
    location="us-central1"
)

print("Attempting connection directly via project ID...")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! Confirming live connection.",
)
print("\n=== Success! ===")
print("API Response:", response.text)

