import os
import google.generativeai as genai
from dotenv import load_dotenv

def list_models():
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        return

    genai.configure(api_key=api_key)
    
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
                print(f"Display Name: {m.display_name}")
                print("-" * 20)
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_models()
