from dotenv import load_dotenv
import numpy as np
import openai
import pandas as pd
import pickle
import tiktoken
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

prompt = "Who won the 2020 Summer Olympics men's high jump?"

openai.Completion.create(
    prompt=prompt,
    temperature=0,
    max_tokens=300,
    model=COMPLETIONS_MODEL
)["choices"][0]["text"].strip(" \n")