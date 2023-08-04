import pinecone
import json
import numpy as np
import itertools
from transformers import BertModel, BertTokenizer

def chunks(iterable, size=50):  # Reduce batch size here
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))

#calling file
with open('issues.json') as f:
    data = json.load(f)

# Choose the BERT model
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# This function returns the BERT embedding for a given text
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(axis=1).detach().numpy().flatten()  # Return numpy array

# Create dictionary to hold unique ID to title mapping
number_to_title = {item['number']: item['title'] for item in data}

embeddings = {item['number']: get_embedding(item['title']) for item in data}

pinecone.init(api_key='98bbd484-d97e-4d83-a941-fb846cb0162f', environment='us-west4-gcp-free')

index_name = "json-embedding-768"

index = pinecone.Index(index_name=index_name)

# Convert the embeddings dictionary to the expected format
vectors = [{"id": str(id), "values": vector.tolist()} for id, vector in embeddings.items()]

for vector_chunk in chunks(vectors):  # Call chunks with adjusted batch size
    index.upsert(list(vector_chunk))

print('ok')


################
# import json
# import numpy as np
# import itertools
# from transformers import BertModel, BertTokenizer
# from langchain.vectorstores import pinecone
# from langchain.embeddings.openai import OpenAIEmbeddings
# import pinecone

# def chunks(iterable, size=50):
#     iterator = iter(iterable)
#     for first in iterator:
#         yield itertools.chain([first], itertools.islice(iterator, size - 1))

# #calling file
# with open('issues.json') as f:
#     data = json.load(f)

# # Choose the OpenAI embedding model
# OPENAI_API_KEY = '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'  # replace this ASAP
# model = "text-embedding-ada-002"

# embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# # This function returns the OpenAI embedding for a given text
# def get_embedding(number):
#     item = data.get(number)
#     if item is not None:
#         text = str(item['title'])
#         embedding = model.embed(text)
#         return embedding.detach().numpy().flatten()
#     else:
#         return None

# # Create dictionary to hold unique ID to title mapping
# number_to_title = {item['number']: item['title'] for item in data}

# # Create embeddings dictionary
# embeddings = {int(item['number']): get_embedding(item['number']) for item in data}

# pinecone.init(api_key='98bbd484-d97e-4d83-a941-fb846cb0162f', environment='asia-southeast1')

# index_name = "index-2json"

# index = pinecone.Index(index_name=index_name)

# # Convert embeddings dictionary to the expected format
# vectors = [{"id": str(id), "values": vector.tolist()} for id, vector in embeddings.items()]

# # Upsert embeddings to Pinecone
# for vector_chunk in chunks(vectors):
#     index.upsert(vector_chunk)

# print('ok')
build_embedding_json.py
Displaying build_embedding_json.py.
