MAX_LEN = 20000  # per https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
"""
MODEL NAME              TOKENIZER	   MAX INPUT TOKENS  OUTPUT DIMENSIONS
text-embedding-ada-002  cl100k_base  8191              1536
"""

for i in range(len(issues)):
  while len(repr(issues[i])) > MAX_LEN: # maximum embedding size
    if issues[i]['comments']:
      del issues[i]['comments'][0] # jettison earliest comments to get small
      continue
    issues[i]['body'] = issues[i]['body'][  # truncate body to fit
        :len(issues[i]['body']) - (len(repr(issues[i])) - MAX_LEN)]  # trim excess

# Prepare for Chroma database loading and embedding

docs     = []
ids      = []
metadata = []
for issue in issues:
  docs.append(repr(issue))          # documents are text of json dicts
  ids.append(str(issue['number']))  # doc id is issue number
  md = {'state': issue['state']}    # put issue state (open/closed)
  for label in issue['labels']:     # ...and each label in
    md[label] = 'yes'               # ...metadata, as "Label: yes"
  metadata.append(md)


print(len(json.dumps(issues, indent=2)))

!pip install openai
!pip install chromadb

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from time import sleep

embed_fn = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY,
              model_name="text-embedding-ada-002") 

client = PersistentClient(path="chroma-db")

vectordb = client.get_collection("react-issues",  # was .get_or_create_collection to make
                                 embedding_function=embed_fn)

def load_db(batch=1):  #necessary because of OpenAI API rate limiting
  batch_size = 10
  while (batch - 1) * batch_size < len(docs):
    start_index = (batch - 1) * batch_size
    end_index = min(batch * batch_size, len(docs))
    vectordb.add(documents=docs[start_index:end_index],
                 metadatas=metadata[start_index:end_index],
                 ids=ids[start_index:end_index])
    print('*** Batch', batch, 'of', len(issues) // batch_size + 1, 'complete')
    batch += 1
    sleep(2)  

#OpenAI rate limiting: https://platform.openai.com/account/rate-limits
#text-embedding-ada-002: 1,000,000 tokens/minute, 3,000 requests/minute

#load_db(batch=183)  # *** Batch 757 of 757 complete

vectordb.count()
