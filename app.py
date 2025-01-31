import streamlit as st
import asyncio
import fitz
from models.model import question_agent, oneline_agent

def get_results_multi(text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    results = loop.run_until_complete(question_agent.run_sync("Generate 5 questions from this text", deps=text))

    return results.data

def get_results_one(text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    results = loop.run_until_complete(oneline_agent.run_sync("Generate 5 questions from this text", deps=text))

    return results.data


def extract_text_from_pdf(pdf_file):

    text = ""

    pdf = fitz.open(stream=pdf_file, filetype="pdf")

    for page in pdf:
        text += page.get_text() + "\n"


    return text.strip()
    


def extract_text_from_txt(txt_file):
    return txt_file.read().decode("utf-8").strip()

async def generate_quiz(text):
    result = await question_agent.run("Generate 5 questions from the text", deps=text)
    result_one = await oneline_agent.run("Generate 5 questions from the text", deps=text)
    return [result.data, result_one.data]

def get_quiz_questions(text):
    return asyncio.run(generate_quiz(text))

# async def generate_quiz_one(text):
#     result = await oneline_agent.run("Generate 5 questions from the text", deps=text)
#     return result.data

# def get_quiz_questions_one(text):
#     return asyncio.run(generate_quiz_one(text))

st.title("AI-Generated Quiz from PDF/TXT")

# uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])


# if uploaded_file:
#     if uploaded_file.type == "application/pdf":
#         extracted_text = extract_text_from_pdf(uploaded_file)
#     elif uploaded_file.type == "text/plain":
#         extracted_text = extract_text_from_txt(uploaded_file)
extracted_text = st.text_area("Enter the text :")
if True:
    if extracted_text:
        st.subheader("Extracted Text Preview:")
        st.text_area("Extracted Content:", extracted_text, height=200)
        
        with st.spinner("Generating quiz..."):
            result = get_quiz_questions(text=extracted_text)
        st.subheader("Quiz Questions:")
        if result[0]:
            idx = 0
            for q in result[0]:
                st.write(f"{idx + 1}. {q.question}")
                
                
                st.write(q.choice_1)
                st.write(q.choice_2)
                st.write(q.choice_3)
                st.write(q.choice_4)

                st.write(f"Answer : {q.answer}")
                
                idx += 1
        else:
            st.write("No questions Generated")

        # with st.spinner("Generating quiz..."):
        #     result = get_quiz_questions_one(text=extracted_text)
        
    
        if result[1]:
                idx = 0
                for q in result[1]:
                    st.write(f"{idx + 1}. {q.question}")
                    
                    st.write(f"Answer : {q.answer}")
                    
                    idx += 1
        else:
                st.write("No questions Generated")