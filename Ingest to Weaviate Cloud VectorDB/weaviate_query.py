import weaviate
import json
import os

os.environ["WEAVIATE_API KEY"] = "bPrhnrliwPMjhNAmwy9rez5WAU9BYAyEPKcG"

# Initialize the Weaviate client. Replace the placeholder values with your actual Weaviate instance details.
client = weaviate.Client(
    url="https://quix-template-viv8pz43.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ["WEAVIATE_API KEY"]),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]
    }
)
some_objects = client.data_object.get()
print(json.dumps(some_objects))