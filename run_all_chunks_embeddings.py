from dotenv import load_dotenv
import openai
import json 
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
  result = openai.Embedding.create(
    model=model,
    input=text
  )
  return result["data"][0]["embedding"]

def get_all_chunks_embeddings(all_chunks_map):
  embeddings_map = {}
  for index, chunk in all_chunks_map.items():
    embedding = get_embedding(chunk, EMBEDDING_MODEL)
    embeddings_map[index] = embedding 
  return embeddings_map

# load all_chunks.json into dict
with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

# TODO: this is a hack to only get the first 5 chunks for testing purposes.
embeddings_map = get_all_chunks_embeddings(dict(list(all_chunks_map.items())[:5]))

with open('embeddings_map.json', 'w') as f:
  json.dump(embeddings_map, f)

# TODO: note that we are actually using ADA not CURIE as far as I can tell which is why the dimensionality is coming to 1536. Should make a pull request to the docs to update this.