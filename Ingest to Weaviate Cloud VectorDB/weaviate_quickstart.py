import weaviate
import weaviate.classes as wvc
import os
import requests
import json

# # For using WCS
import weaviate
import json
import os

client = weaviate.Client(
    url = "https://some-endpoint.weaviate.network",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR-WEAVIATE-API-KEY"),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }


if client.schema.exists("Question"):
    client.schema.delete_class("Question")