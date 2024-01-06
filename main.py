import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

template = """""
Say hello to me. My name is {name}.
"""

prompt = PromptTemplate(
	input_variables = ["name"],
	template=template,
	)


#Access the API key
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
	print("OpenAI API Key not found. Please set it as an environment variable")
else:
	def load_LLM():
		"""Logic for laoding the chain you want to use should go here."""
		llm=OpenAI(temperature=.5)
		return llm

	llm=load_LLM()

st.set_page_config(page_title="MCQ Generator", page_icon=":robot:")
st.header("MCQ Generator")

st.markdown("This micro-app allows you to generate multiple choice questions quickly and consistently, with a number of useful configurations so that you don't have to remember or write out long prompts in ChatGPT")

st.markdown("> Note to developer: For now, the task is to add all the fields from the requirement in this app and save them so that I can craft a prompt that uses those inputs.")

st.markdown("## Topic")


st.write("Find Requirements here: https://docs.google.com/document/d/1_L-XMBobxwtHhwyZ7f2RpXlAUACSv30J_5fRnyl2BJc/edit")


def get_name():
	input_text=st.text_area(label="What is your name (dummy question)", placeholder="This is just here as a demo of capturing data", key="name")
	return input_text

user_name = get_name()

if user_name is not None and st.button('Submit'):
	llm_prompt = prompt.format(name=user_name)
	llm_response = llm(llm_prompt)
	st.write(llm_response)

