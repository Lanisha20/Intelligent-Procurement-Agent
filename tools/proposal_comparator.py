import json
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI

llm = VertexAI(model_name="gemini-2.5-pro", temperature=0.3)

comparison_template = PromptTemplate.from_template("""
You are a procurement analyst. Given supplier proposals in JSON format, compare them and recommend the best supplier.

Evaluate based on:
- Price per unit (lower is better)
- Delivery lead time (shorter is better)
- Warranty years (longer is better)

Here are the proposals:
{proposals}

Provide:
1. A ranked list of suppliers (best to worst)
2. A short explanation
""")

def compare_proposals(proposals: list[dict]) -> str:
    proposals_json = json.dumps(proposals, indent=2)
    prompt = comparison_template.format(proposals=proposals_json)
    result = llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)
