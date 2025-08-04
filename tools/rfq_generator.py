# from langchain.prompts import PromptTemplate
# from langchain_google_vertexai import VertexAI

# # Set up Gemini model
# llm = VertexAI(model_name="gemini-2.5-pro", temperature=0.4)

# # Template to structure the RFQ
# rfq_template = PromptTemplate.from_template("""
# Create a professional Request for Quotation (RFQ) document using the following details:

# Product or Category: {product}
# Quantity: {quantity}
# Delivery Time: {delivery_time}
# Other Notes: {notes}

# Respond with a clean RFQ format ready to send to a supplier.
# """)

# def generate_rfq(product: str, quantity: str, delivery_time: str, notes: str = "") -> str:
#     prompt = rfq_template.format(
#         product=product,
#         quantity=quantity,
#         delivery_time=delivery_time,
#         notes=notes
#     )
#     return llm.invoke(prompt)

from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
import re

llm = VertexAI(model_name="gemini-2.5-pro", temperature=0.4)

rfq_template = PromptTemplate.from_template("""
Create a professional Request for Quotation (RFQ) using the following:

- Product: {product}
- Quantity: {quantity}
- Delivery Time: {delivery_time}
- Notes: {notes}

Respond with a clean RFQ format ready to send to a supplier.
""")

def extract_rfq_fields(user_input: str):
    quantity_match = re.search(r"\b(\d+)\s*(units|boxes|chairs|monitors)?", user_input, re.I)
    delivery_match = re.search(r"(?:in|within)\s*(\d+)\s*(days|weeks)", user_input, re.I)
    product_match = re.search(r"for\s+([\w\s\-]+)", user_input, re.I)

    quantity = quantity_match.group(0) if quantity_match else "unspecified"
    delivery_time = f"{delivery_match.group(1)} {delivery_match.group(2)}" if delivery_match else "unspecified"
    product = product_match.group(1).strip() if product_match else "unspecified"

    return product, quantity, delivery_time

def generate_rfq_from_user_input(user_input: str) -> str:
    product, quantity, delivery_time = extract_rfq_fields(user_input)
    
    prompt = rfq_template.format(
        product=product,
        quantity=quantity,
        delivery_time=delivery_time,
        notes=user_input
    )

    result = llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)
