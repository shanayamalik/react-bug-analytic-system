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
