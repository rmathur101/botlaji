from helpers import answer_query_with_context
import os
import json

with open('embeddings_map.json', 'r') as f:
  embeddings_map = json.load(f)

with open('all_chunks_map.json', 'r') as f:
  all_chunks_map = json.load(f)

# query = "Can you give me some specific examples of what countries are doing today that are preventing innovation from happening?"
# query = "What are the steps to create a network state?"
# query = "Why do we need network states?"
# query = "What is a startup society and how do you found one?"
# query = "what are the steps to founding a startup society?"
# query = "Can you give me an example of a startup society and how it was founded?"
# query = "What do you see the future looking like in the next 10 or 20 year?"
# query = "What kind of new technologies or ways of living will be possible in a network state?"
# query = "How do you organize a group capable of collective action? Can you give me an example?"
# query = "Can you give me an example of a network union?"
# query = "What does the future of media look like? How will network states change the future of media?"
# query = "What are your thoughts about the new york times?"
# query = "Can you give me an example of how the NYT started a war?"
# query = "How can I get involved in the network state movement?"
# query = "What role does crypto and blockchain play in the creation of network states?"
# query = "What are your thoughts about China and the future of China?"
# query = "What are the most important and contrarian ideas in the book?"
# query = "What is the concept of the ledger of record and why is it important?"
# query = "What is an example of how the ledger of record will be used to build network states?"
# query = "What are the different ways that liberals, convservatives, and libertarians view the world and will impact the future?"
# query = "What technologies will be most important in the future?"
# query = "What color are coco beans?"
# query = "What is the book about?"
query = "What is wrong with the current society?"

answer = answer_query_with_context(query, all_chunks_map, embeddings_map, show_prompt=True)
print(answer)
