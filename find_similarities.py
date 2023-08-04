
Conversation opened. 1 read message.

Skip to content
Using ORO NETWORKS LLC Mail with screen readers

1 of 44
Scripts for eclidean and cosine
Inbox

Gino Limon
Attachments
5:55 PM (53 minutes ago)
to me

the main script to use it the one that its called cosines and eclidean that is the main one that works perfectly.

I will send more to consider for the repository as proof of work 
 issues.json

7
 Attachments
  •  Scanned by Gmail
Thanks, I'll check it out!Thanks, I'll check them out.Thank you!

from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain import PromptTemplate

llm = OpenAI(model_name="text-davinci-003", openai_api_key='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')

# Notice "location" below, that is a placeholder for another value later
template = """
I really want to travel to {location}. What should I do there?

Respond in one short sentence
"""

prompt = PromptTemplate(
    input_variables=["location"],
    template=template,
)
print('Hi where do you want to travel?')
final_prompt = prompt.format(location= input(''))

print (f"Final Prompt: {final_prompt}")
print ("-----------")
print (f"LLM Output: {llm(final_prompt)}")


####### start here

#connecting to pinecone data base
import pinecone
pinecone.init(
    api_key= "b26a180f-ca1c-482e-b88e-09e5c794753b",
    environment= "us-west4-gcp-free"
)

index = pinecone.Index('json-embedding-768')

index.describe_index_stats()
find_similarity.py
Displaying find_similarity.py.
