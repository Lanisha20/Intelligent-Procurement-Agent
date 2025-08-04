# def find_suppliers(query: str) -> str:
#     """
#     Stub function to simulate supplier lookup.
#     Replace this with DB query, API call, or real logic.
#     """
#     if "laptop" in query.lower():
#         return "Top suppliers: Dell, Lenovo, HP"
#     elif "eco-friendly" in query.lower():
#         return "Top suppliers: EcoPack, GreenBox, BioWrap"
#     else:
#         return "No suppliers found for your query."

import json
import os

# Load product data once
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "../eprocurement_products.json")
with open(PRODUCTS_FILE, "r") as f:
    PRODUCTS = json.load(f)

def find_suppliers(query: str) -> str:
    import re

    query_keywords = re.findall(r"\w+", query.lower())

    matching = [
        p for p in PRODUCTS
        if any(
            keyword in p["category"].lower() or keyword in p["name"].lower()
            for keyword in query_keywords
        )
    ]

    if not matching:
        return "❌ No suppliers found for your query."

    supplier_summary = {}
    for p in matching:
        supplier = p["supplier"]
        if supplier not in supplier_summary:
            supplier_summary[supplier] = {
                "products": [],
                "avg_lead_time": [],
                "avg_price": []
            }
        supplier_summary[supplier]["products"].append(p["name"])
        supplier_summary[supplier]["avg_lead_time"].append(p["lead_time_days"])
        supplier_summary[supplier]["avg_price"].append(p["unit_price"])

    result = []
    for supplier, info in supplier_summary.items():
        avg_time = sum(info["avg_lead_time"]) / len(info["avg_lead_time"])
        avg_price = sum(info["avg_price"]) / len(info["avg_price"])
        products = ", ".join(info["products"])
        result.append(f"🔹 **{supplier}**\n  - Products: {products}\n  - Avg Lead Time: {avg_time:.1f} days\n  - Avg Price: ${avg_price:.2f}")

    return "\n\n".join(result)
