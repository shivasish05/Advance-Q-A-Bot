import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Langsmith tracking 
# os.environ['LANGCHAIN_API_KEY'] = "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"
# os.environ['LANGCHAIN_TRACING_V2'] = 'true'
# os.environ['LANGCHAIN_PROJECT'] = "Simple Q&A Chat Bot"

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'you are a helpful assistant please respond to user queries'),
        ('user', 'Question {question}')
    ]
)

def generate_response(question, api_key, llm, temperature, max_token):
    os.environ['OPENAI_API_KEY'] = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})

    return answer

# Streamlit App
st.title('Enhanced Q&A Bot')
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Your API Key Here", type='password')

# Dropdown to select OpenAI Model
llm = st.sidebar.selectbox("Select OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

# Adjust parameters using sliders
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max tokens", min_value=50, max_value=300, value=150)

# Main Interface for user input
st.write("Ask What's On Your Mind..😁")
user_input = st.text_input('You:')

if st.button('Generate'):
    if user_input:
        with st.spinner('Generating response...'):
            response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.write(response)
    else:
        st.write("Please Mention Your Queries, I Am Happy To Help😍")


