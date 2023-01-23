from helpers import answer_query_with_context
import os
import json
import sys

with open('embeddings_map.json', 'r') as f:
  embeddings_map = json.load(f)

with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

query = sys.argv[1] 
show_prompt = False
if (len(sys.argv) > 2):
  show_prompt =  sys.argv[2] == 'True'

answer = answer_query_with_context(query, all_chunks_map, embeddings_map, show_prompt)
print('-'*20)
print(answer)
