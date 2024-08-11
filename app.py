import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

##Langsmith tracking 
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Simple Q&A Chat Bot"

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ('system','you are a helpful assistant please response to user queries'),
        ('user','Question {question}')
    ]
)

def generate_response(question,api_key,llm,temperature,max_token):
    openai.api_key = api_key
    llm= ChatOpenAI(model = llm)
    output_parser = StrOutputParser()
    chain = prompt | llm |output_parser
    answer = chain.invoke({'question':question})

    return answer

#Streamlit App
st.title('Enhansed Q&A Bot')
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Your API Key Here",type='password')

## Dropdown to select Openai Model
llm = st.sidebar.selectbox("Select Openai Model",["gpt-4o","gpt-4-turbo","gpt-4"])

##Adjust parameter using slider
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max tokens", min_value=50,max_value=300,value=150)

##Main Interface for user Input

st.write("Ask Whats In Your Mind..😁")
user_input = st.text_input('You:')


if user_input:
    response = generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)

else:
    st.write("Please Mention Your Queries, I Am Happy To Help😍")    

