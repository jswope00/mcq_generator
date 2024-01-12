import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

# Template and prompt initialization
template = """
Based {focus_text} on the following text {topic_content}, please write {questions_num} multiple-choice question with {correct_ans_num} correct answer  and {distractors_num} distractors.
"""



# Access the API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check for API key
if openai_api_key is None:
    st.warning("OpenAI API Key not found. Please set it as an environment variable.")
else:
    # Load language model
    def load_LLM():
        """Logic for loading the chain you want to use should go here."""
        llm = OpenAI(temperature=0.5)
        return llm

    llm = load_LLM()

# Streamlit app configuration
st.set_page_config(page_title="MCQ Generator", page_icon=":robot:")
st.header("MCQ Generator")

st.markdown("This micro-app allows you to generate multiple-choice questions quickly and consistently, with a number of useful configurations so that you don't have to remember or write out long prompts in ChatGPT")

st.markdown("## Topic")

# User input for topic
topic_content = st.text_area("What is the content you’d like to generate questions for? Be as specific or general as you like. ", key="topic_content")

# User input for focus
original_content_only = st.checkbox("Focus only on the provided text", key="original_content_only")
focus_text = "solely" if original_content_only else "as well as your overall knowledge"

# User input for learning objective
learning_objective = st.text_area("Is there a specific learning objective you’d like to assess? If so, write it here.", key="learning_objective")

# User input for questions configuration
questions_num = st.selectbox("How many questions?", [1, 2, 3, 4, 5], key="questions_num")
correct_ans_num = st.selectbox("How many correct answers per question?", [1, 2, 3, 4], key="correct_ans_num")

# User input for question level
question_level_options = ['Grade School', 'High School', 'University', 'Other']
question_level = st.selectbox("What level questions?", question_level_options, key="question_level")

# If user selects "Other," allow them to input custom text
if question_level == 'Other':
    custom_question_level = st.text_input("Specify other level:", key="custom_question_level")
else:
    custom_question_level = None

# User input for distractors configuration
distractors_num = st.selectbox("How many distractors?", [1, 2, 3, 4, 5], key="distractors_num")
distractors_difficulty = st.selectbox("Should the distractors be:",
                                      ['Normal difficulty', 'Obvious', 'Challenging'], key="distractors_difficulty")

# User input for feedback and hinting
learner_feedback = st.checkbox("Include Learner Feedback?", key="learner_feedback")
hints = st.checkbox("Include hints?", key="hints")

# User input for output format
output_format = st.selectbox("What output format?", ['Plain Text', 'OLX'], key="output_format")

# Generate question button
if st.button('Generate MCQ Questions'):
    # Use the user inputs to generate a prompt
    prompt_values = {
        "focus_text": focus_text,
        "topic_content": topic_content,
        "distractors_num": distractors_num,
        "correct_ans_num": correct_ans_num,
        "questions_num": questions_num
    }

    if hints is True:
        template = template + 'Also write a hint:'  

    prompt_template = PromptTemplate(
        input_variables=["focus_text", "topic_content", "distractors_num"],
        template=template,
    )
    


    # Generate MCQ questions using the PromptTemplate
    mcq_prompt = prompt_template.format(**prompt_values)

    st.subheader("Generated MCQ Questions:")
    st.write(mcq_prompt)

    # To submit the prompt to the language model
    if openai_api_key is not None:
        llm_response = llm(mcq_prompt)
        st.subheader("Response from language model:")
        st.write(llm_response)
    else:
        st.warning("OpenAI API Key not found. Please set it as an environment variable.")


