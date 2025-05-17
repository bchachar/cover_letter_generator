import streamlit as st
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

template = """
You are a professional career assistant and cover letter writer.

Generate a tailored cover letter for the following job description and CV:
Job Description:
{job_description}

Candidate CV:
{cv_text}

Do not use any placeholders like [Your Name], [Company Name], etc. Use real information found in the CV and job description. Do not repeat the job description verbatim. Reflect alignment between the candidate's skills and the job requirements.

If the candidate's name is present in the CV, use it. If the company name or job title is present in the job description, use it. Otherwise, gracefully omit them.

"""
def generate_cover_letter_with_ollama(job_description: str, cv_text: str, model_name="llama3") -> str:
    # Define the prompt template
    prompt = PromptTemplate(template=template, input_variables=["job_description", "cv_text"])

    # Load the Ollama model via LangChain
    llm = ChatOllama(model=model_name)

    # Run the chain
    chain = prompt | llm | StrOutputParser()

    # Call the chain with input
    return chain.invoke({
        "job_description": job_description,
        "cv_text": cv_text
    })


st.set_page_config(page_title="Cover Letter Generator", layout="centered")

st.title("📄 AI Cover Letter Generator")

# Job description input
job_description = st.text_area(
    "Paste the Job Description",
    height=300,
    placeholder="Paste the full job description here..."
)

# CV upload input
cv_file = st.file_uploader("Upload Your CV (PDF or TXT)", type=["pdf", "txt"])

# Generate button
generate_button = st.button("Generate Cover Letter")

# Helper function to extract text from uploaded CV
def extract_cv_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type.startswith("text/"):
        return uploaded_file.read().decode("utf-8")
    else:
        return ""

# Placeholder for the generated cover letter
if generate_button:
    if not job_description or not cv_file:
        st.error("Please provide both the job description and upload your CV.")
    else:
        with st.spinner("Generating your cover letter..."):
            cv_text = extract_cv_text(cv_file)

            st.subheader("📝 Generated Cover Letter")
            cover_letter = generate_cover_letter_with_ollama(job_description, cv_text)
            st.text_area("Cover Letter", value=cover_letter, height=400)

