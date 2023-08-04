#importing packages
import numpy as np
import pandas as pd
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import json
from time import sleep

print("working...")
sleep(.5)
print("Extracting data from Json File...")
sleep(.5)
print("Embedding file this will take a minute...")
sleep(.5)
print("Please hold while I work...")
# Define the model we want to use (it'll download itself)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#calling file
with open('issues.json') as f: #<---------------- Change here to connect to the file
    data = json.load(f)

#separating json file into list to embed
titles = []
ids = []
for i in data:
    titles.append(i["title"])
    ids.append(i["number"])

# vector embeddings created from lists
embeddings = model.encode(titles)

#imputing query
print("Ready!")
string = input("What is the title for your issue?\n>")
# string = "update Getting Started link to redirect to new Quick Start documentation"

# query vector embedding
query_embedding = model.encode(f"{string}")

# define our distance metric
def cosine_similarity(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))

# run semantic similarity search
print(f"Query: {string}\n")
similarity_score = []
for embedding, title in zip(embeddings, titles):
    # print(title, " ----->  ",
    #      cosine_similarity(embedding, query_embedding))
    cosine_similarity(embedding, query_embedding) #<-------------- cosine similarity search HERE
    similarity_score.append(cosine_similarity(embedding, query_embedding))

# creating data frame for score manipulation and viz
df = pd.DataFrame(columns=["Id", "Title", "Score"])

# loop to iterate over both lists simultaneously and append the items to df:
for ids, title, simi_score in zip(ids, titles, similarity_score):
    df = df.append({"Id": ids, "Title": title, "Score": simi_score}, ignore_index=True)

# Sort DataFrame in descending order by highst similarity score
df = df.sort_values('Score', ascending=False)

# Filtering top score ABOVE 50% similarity
filtered_df = df[df["Score"] > 0.5]
print(filtered_df)

search = []
for i in filtered_df["Id"]:
    search_json = i
    search_json_int = int(search_json)
    search.append(search_json_int)

def search_in_json(data, number):      
    for item in data:
        if item.get('number') == number:
            print(item)
            return item

col_to_print = ["Id", "Score"]
sim_list = filtered_df[col_to_print]

# print(filtered_df["Id"])
for i in filtered_df["Score"]:
    # print(i)
    n1 = i
    n2 = round((n1 * 100),2)

input("Press Enter to continue\n>")
#asking user
print(f"There are {len(search)} posible issues that it can help you solve your issue")
sleep(.5)
print("It's hard to view all at the same time, therefore, lets go one by one")
sleep(.5)
print(f"out of those {len(search)} this are the following similarity scores:\n {sim_list}\n")
sleep(.5)
print("The following issues are similar to your current issue and can help you:")
sleep(.5)
input("Press enter to continue and visualize the full the top similar issues\n>")
print(f"{'-'*50}")
def pretty_print(data):
    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key}:")
            for i, v in enumerate(value):
                print(f"  Item {i + 1}:")
                for line in v.split('\n'):
                    print(f"    {line}")
        else:
            print(f"{key}: {value}")
        print()

counter = 0
for i in search:
    pprint = search_in_json(data, search[counter])
    # print(pprint)
    pretty_print(pprint)
    counter =+ 1
