import json
from helpers import get_all_chunks_embeddings 

# load all_chunks.json into dict
with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

embeddings_map = get_all_chunks_embeddings(all_chunks_map)

with open('embeddings_map.json', 'w') as f:
  json.dump(embeddings_map, f)