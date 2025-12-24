import os
from google import genai
from dotenv import load_dotenv

load_dotenv('.env')

api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

try:
    for model in client.models.list():
        print(f"{model.name}")
except Exception as e:
    print(e)
