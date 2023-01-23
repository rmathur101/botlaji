import os
import numpy as np
import openai
from dotenv import load_dotenv
import tiktoken
from transformers import GPT2TokenizerFast

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# two model pipeline will be used here. the embedding model will be used to generate embeddings for the book chunks and the query (so that we can calculate the similarity between the two), and the completion model will be used to generate the answer to the question when given a query and a book chunk.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
COMPLETIONS_MODEL = os.getenv("COMPLETIONS_MODEL")
COMPLETIONS_MODEL_MAX_TOKENS = int(os.getenv("COMPLETIONS_MODEL_MAX_TOKENS"))
COMPLETIONS_MODEL_TEMP = float(os.getenv("COMPLETIONS_MODEL_TEMP"))

COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": COMPLETIONS_MODEL_TEMP,
    "max_tokens": COMPLETIONS_MODEL_MAX_TOKENS,
    "model": COMPLETIONS_MODEL,
    # "top_p": 1
}

# check would this work?
MAX_SECTION_LEN = int(os.getenv("MAX_SECTION_LEN")) 
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
  result = openai.Embedding.create(
    model=model,
    input=text
  )
  return result["data"][0]["embedding"]

def get_all_chunks_embeddings(all_chunks_map):
  embeddings_map = {}
  for index, value in all_chunks_map.items():
    # print(index)
    # print(value)
    embedding = get_embedding(value['document'], EMBEDDING_MODEL)
    embeddings_map[index] = embedding 
  return embeddings_map

def vector_similarity(x, y):
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    # print(x)
    # print('-'*20)
    # print(y)
    return np.dot(np.array(x), np.array(y))

def order_document_sections_by_query_similarity(query_embedding, embeddings_map): 
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in embeddings_map.items()
    ], reverse=True)
    
    return document_similarities

def construct_prompt(question, context_embeddings: dict, all_chunks_map) -> str:
    """
    Fetch relevant 
    """
    question_embedding = get_embedding(question, EMBEDDING_MODEL)
    most_relevant_document_sections = order_document_sections_by_query_similarity(question_embedding, context_embeddings)

    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []
     
    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.        
        document_section = all_chunks_map[section_index]['document']
        
        # chosen_sections_len += document_section.tokens + separator_len
        
        chosen_sections_len += len(tokenizer.encode(document_section)) + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break
            
        chosen_sections.append(SEPARATOR + document_section.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))
            
    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join(chosen_sections_indexes))
    
    # header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""
    # header = """Answer the question as truthfully as possible using the provided context. If you can't, give it your best guess and let us know that you are guessing. And if the answer is not contained within the text below, or you are not confident about making any guesses, say "I don't know."\n\nContext:\n"""
    header = """Answer the question using the provided context."\n\nContext:\n"""
    
    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"

def answer_query_with_context(query, all_chunks, embeddings_map, show_prompt: bool = False) -> str:
    prompt = construct_prompt(query, embeddings_map, all_chunks)
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(prompt=prompt, **COMPLETIONS_API_PARAMS)

    return response["choices"][0]["text"].strip(" \n")