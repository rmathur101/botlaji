import json
from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from helpers import answer_query_with_context
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('embeddings_map.json', 'r') as f:
  embeddings_map = json.load(f)

with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

@app.post("/")
def read_root(params: dict):
  # question = params['question']
  # answer = answer_query_with_context(question, all_chunks_map, embeddings_map, False)
  answer = "This is a sample answer."
  time.sleep(5)
  return {"answer": answer} 

@app.get("/test")
def read_test():
    return {"Hello": "World"}