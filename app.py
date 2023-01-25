import json
from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware
from helpers import answer_query_with_context
import time
import sys
from loguru import logger

# API config
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# log config
logger.add("logs/log.json", format="Log {level} at {time} has message: {message}", serialize=True)
logger.add(sys.stdout, format="Log {level} at {time} has message: {message} (Extra data below) \n{extra}", serialize=False) 

with open('embeddings_map.json', 'r') as f:
  embeddings_map = json.load(f)

with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

@app.post("/")
def query(params: dict):
  try:
    shouldRunReal = False 

    if shouldRunReal:
      question = params['question']
      answer = answer_query_with_context(question, all_chunks_map, embeddings_map, False)

    else:
      question = params['question']
      answer = "This is a sample answer."
      time.sleep(2)

      # TODO: need to add user info
    logger.info("QA Executed", extra={"question": question, "answer": answer})
    return {"status_code":200, "answer": answer} 
  except Exception as e:
    logger.error("Exception raised", extra={"question": params['question'], "error": e})
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def feedback(params: dict):
  try:
    logger.info("Feedback logged", extra={"feedback": params['feedback']})
    return {"status_code": 200} 
  except Exception as e:
    logger.error("Exception raised", extra={"feedback": params['feedback'], "error": e})
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def read_test():
    return {"Hello": "World"}