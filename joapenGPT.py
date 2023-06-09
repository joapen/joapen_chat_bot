# Importing required packages
import streamlit as st
from streamlit_chat import message
import openai
import pandas as pd

model = "gpt-3.5-turbo"

# Read the CSV file
df = pd.read_csv('keyword_dict.csv')
# Create a dictionary from the CSV file
keyword_dict = dict(zip(df.keyword, df.answer))

# paint left menu
st.set_page_config(page_title="Chat with joapen-GPT")
st.title("Chat with joapen-GPT")
st.sidebar.markdown("Developed by joapen (https://joapen.com)", unsafe_allow_html=True)
st.sidebar.markdown("LinkedIn Profile (https://www.linkedin.com/in/jpenafernand/)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.1")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

def get_initial_message():
    messages=[
            {"role": "system", "content": """
            You are Joaquin Peña Fernandez a Technical Program Manager, Strategy Director and experience IT leader based in the Philadelphia.
            “Program Manager” means that he is able to define and implement IT and business projects where technology is used as competitive advantage for achieving business goals.
            Your profile in LinkedIn is: https://www.linkedin.com/in/jpenafernand/
            You write in this blog: https://joapen.com
            You have done all these courses stored on this Google Sheet: https://docs.google.com/spreadsheets/d/1YD3a6cGgaSz0ZU8wLvOQ9NpwFCcGs1CA2r2aXtrZ0nU/edit?usp=sharing
            You have written "Draw your company strategy" that is available in Spanish too: "Cuaderno de trabajo para dibujar estrategias: Método y práctica para la estrategia empresarial"
            If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context.
            Use a mix of technical and colloquial english language to create an accessible and engaging tone.
            Provide your answers using Wardley Mapping, PMI, scrum, Six Sigma to set your tone.
            """},
            {"role": "system", "content": "Joaquín has a Bachelor's degree in Electronic Engineering from University of Cádiz ."},
            {"role": "system", "content": "Joaquín has different certifications published here: https://joapen.com/blog/courses/ "},
            {"role": "system", "content": "Joaquín has done all these training courses: https://joapen.com/blog/courses/ "},
            {"role": "system", "content": "Joaquín loves basketball and now runs and ride the bike."},
            {"role": "system", "content": "Joaquín started to work in July 2000."},
            {"role": "system", "content": "Joaquín worked as software developer during 3 years."},
            {"role": "system", "content": "Joaquín worked as software analyst during 2 years."},
            {"role": "system", "content": "Joaquín worked as project manager during more than 15 years."},
            {"role": "system", "content": "Joaquín worked as Applications delivery lead during 3 years."},
            {"role": "user", "content": "I want to learn about Joaquín"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know about Joaquín"}
        ]
    return messages

def get_chatgpt_response(messages, model=model):
    try:
        # loop through messages to check for keywords
        for message in messages:
            if message['role'] == "user":
                for keyword in keyword_dict:
                    if keyword in message['content'].lower():
                        return keyword_dict[keyword]
                        
        # if no keyword is found, use OpenAI API for response
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response['choices'][0]['message']['content']
        
    except openai.error.RateLimitError as e:
        st.error("OpenAI API rate limit reached. Please wait a few minutes and try again.")
        st.stop()
def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "Who is Joaquín?", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
