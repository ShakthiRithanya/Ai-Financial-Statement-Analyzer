import google.generativeai as genai
import sys

def list_models(api_key):
    try:
        genai.configure(api_key=api_key)
        print("--- Available Models ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}, Display: {m.display_name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnose_models.py YOUR_API_KEY")
    else:
        list_models(sys.argv[1])
