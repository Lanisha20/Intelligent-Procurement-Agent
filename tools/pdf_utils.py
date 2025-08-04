from langchain_google_vertexai import VertexAI
import fitz
import re

llm = VertexAI(model_name="gemini-2.5-pro", temperature=0.3)

def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)  # Rewind file stream
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_structured_proposal(raw_text: str) -> dict:
    prompt = f"""
You are a procurement assistant. Extract the following fields from the supplier proposal below:
- supplier
- price_per_unit (number, in USD)
- lead_time_days (number of days)
- warranty_years (number of years)

Return the result as a JSON object with exactly those keys and lowercase snake_case.

Proposal Text:
"""
    result = llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)
