import json
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Header  
from fastapi.middleware.cors import CORSMiddleware
from auth_bearer import JWTBearer
from auth_handler import decodeJWT, signJWT
from helpers import answer_query_with_context
import time
import sys
from loguru import logger
from oauth import Oauth

# API config
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOW_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# log config
logger.add("logs/log.json", format="Log {level} at {time} has message: {message}", serialize=True)
logger.add(sys.stdout, format="Log {level} at {time} has message: {message} (Extra data below) \n{extra}", serialize=False) 

load_dotenv()
GUILD_ID_1729="900827411917201418"
discord_oauth = Oauth(
  os.getenv("CLIENT_ID"),
  os.getenv("CLIENT_SECRET"),
  os.getenv("REDIRECT_URL"),
  scope="identify guilds"
)

with open('embeddings_map.json', 'r') as f:
  embeddings_map = json.load(f)

with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

@app.post("/", dependencies=[Depends(JWTBearer())])
def query(params: dict, authorization = Header(None)):
  bearer, token = authorization.split(" ")
  jwt_data = decodeJWT(token)

  try:
    shouldRunReal = False 

    if shouldRunReal:
      question = params['question']
      answer = answer_query_with_context(question, all_chunks_map, embeddings_map, False)
    else:
      question = params['question']
      answer = "This is a sample answer."
      time.sleep(2)

    logger.info("QA Executed", extra={"question": question, "answer": answer, "discord_username": jwt_data['discord_username']})
    return {"status_code":200, "answer": answer} 
  except Exception as e:
    logger.error("Exception raised", extra={"question": params['question'], "error": e, "discord_username": jwt_data['discord_username']})
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback", dependencies=[Depends(JWTBearer())])
def feedback(params: dict, authorization = Header(None)):
  bearer, token = authorization.split(" ")
  jwt_data = decodeJWT(token)

  try:
    logger.info("Feedback logged", extra={"feedback": params['feedback'], "discord_username": jwt_data['discord_username']})
    return {"status_code": 200} 
  except Exception as e:
    logger.error("Exception raised", extra={"feedback": params['feedback'], "error": e, "discord_username": jwt_data['discord_username']})
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/check_jwt", dependencies=[Depends(JWTBearer())])
def check_jwt():
  return {"status_code": 200}

@app.post("/discord")
def auth(params: dict):
  try:
    # Get discord tokens using code from authentication and check if access token is available 
    tokens = discord_oauth.get_access_token(code=params['code'])
    if (not ("access_token" in tokens)):
        raise HTTPException(status_code=500, detail="No access token found with the discord code that was sent after authentication.")

    # Use tokens to get discord data including guilds
    discord_data = discord_oauth.get_user(access_token=tokens["access_token"])
    guilds = discord_oauth.get_guilds(access_token=tokens["access_token"])

    # Check if user is in 1729 guild
    if not any([guild["id"] == GUILD_ID_1729 for guild in guilds]):
        raise HTTPException(status_code=500, detail="This user does not have the 1729 guild in their guilds list: " + discord_data["username"])

    JWTToken = signJWT(discord_data['id'], discord_data['username'])
    return {"status_code": 200, "detail": "User authenticated", "jwt_access_token": JWTToken}
  except Exception as e:
    logger.error("Error in /discord endpoint", extra={"error": e})
    return {"status_code": 500}

@app.get("/test")
def read_test():
    return {"Hello": "World"}