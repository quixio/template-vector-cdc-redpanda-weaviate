# Weaviate Quickstart Guide
# This script guides you through the basics of Weaviate, based on the quickstart guide.
# Full documentation is available at https://weaviate.io/developers/weaviate/quickstart

# Ensure you have the Weaviate Python client installed. Install it using pip if necessary:
# !pip install -U weaviate-client

# Import necessary libraries
import weaviate
from weaviate.embedded import EmbeddedOptions
import requests
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

# Or, for using Embedded Weaviate which spins up an instance in the background:
# client = weaviate.Client(
#     embedded_options=EmbeddedOptions(),
#     additional_headers={
#         "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
#     }
# )

# Create a class
if client.schema.exists("Question"):
    client.schema.delete_class("Question")

if client.schema.exists("QuestionV"):
    client.schema.delete_class("QuestionV")

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  # Use `generative-openai` module for generative queries
    }
}

class_vobj = {
    "class": "QuestionV",
    "vectorizer": "none",
    "moduleConfig": {
        "generative-openai": {}  # Use `generative-openai` module for generative queries
    }
}

client.schema.create_class(class_vobj)
client.schema.create_class(class_obj)

# Add objects to Weaviate instance using a batch import process
# Load data
url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Batch import all Questions
with client.batch(batch_size=100) as batch:
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        client.batch.add_data_object(properties, "Question")


###### START PREGENERATED VECTORS PROCEDURE
# # Load data
import requests
fname = "jeopardy_tiny_with_vectors_all-OpenAI-ada-002.json"  # This file includes pre-generated vectors
url = f'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/{fname}'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch(
    batch_size=100
) as batch:
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        custom_vector = d["vector"]
        client.batch.add_data_object(
            properties,
            "QuestionV",
            vector=custom_vector) # Add custom vector

###### END PREGENERATED VECTORS PROCEDURE

# Example of a semantic search using nearText search for quiz objects similar to "biology"
nearText = {"concepts": ["biology"]}
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)
print(json.dumps(response, indent=4))

# Semantic search with a filter for objects with a "category" value of "ANIMALS"
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_where({
        "path": ["category"],
        "operator": "Equal",
        "valueText": "ANIMALS"
    })
    .with_limit(2)
    .do()
)
print(json.dumps(response, indent=4))

# Generative search with a single prompt
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_generate(single_prompt="Explain {answer} as you might to a five-year-old.")
    .with_limit(2)
    .do()
)
print(json.dumps(response, indent=4))

# Generative search with a grouped task
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_generate(grouped_task="Write a tweet with emojis about these facts.")
    .with_limit(2)
    .do()
)
print(response["data"]["Get"]["Question"][0]["_additional"]["generate"]["groupedResult"])

# Note: For full functionality, uncomment and adjust the necessary parts of this script according to your Weaviate instance details and data.
uuid = client.data_object.create(
    class_name="QuestionV",
    data_object={
        "answer": "cat",
        "category": "ANIMAL",
        "question": "A four legged thing that goes meow meow",
    },
    vector = [0.12345] * 1536
)

print(uuid)  # the return value is the object's UUID