from google import genai
import api

client = genai.Client(api_key=api.API_KEY)
models = client.models.list()
for model in models:
    print(f"Name: {model.name}")