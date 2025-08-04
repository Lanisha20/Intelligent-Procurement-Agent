# import streamlit as st
# from supervisor.supervisor_graph import create_graph

# st.set_page_config(page_title="Procurement Agent", layout="wide")
# st.title("Intelligent Procurement Assistant (LangGraph)")

# st.markdown("Describe what you need. The assistant will find suppliers, generate an RFQ, compare proposals, and recommend the best option.")

# user_query = st.text_area("Enter your procurement request", height=100, placeholder="e.g. We need 200 ergonomic chairs delivered within 10 days.")

# default_proposals = [
#     {"supplier": "Initech", "price_per_unit": 296.69, "lead_time_days": 7, "warranty_years": 2},
#     {"supplier": "Stark Industries", "price_per_unit": 492.68, "lead_time_days": 15, "warranty_years": 1},
#     {"supplier": "Acme Corp", "price_per_unit": 353.76, "lead_time_days": 43, "warranty_years": 3},
#     {"supplier": "Soylent Corp", "price_per_unit": 343.88, "lead_time_days": 4, "warranty_years": 2},
#     {"supplier": "Hooli Procurement", "price_per_unit": 252.12, "lead_time_days": 30, "warranty_years": 2},
#     {"supplier": "Umbrella Supplies", "price_per_unit": 403.50, "lead_time_days": 18, "warranty_years": 3},
#     {"supplier": "Globex Inc", "price_per_unit": 113.56, "lead_time_days": 33, "warranty_years": 2},
#     {"supplier": "Soylent Corp", "price_per_unit": 291.69, "lead_time_days": 4, "warranty_years": 2},
#     {"supplier": "Acme Corp", "price_per_unit": 296.28, "lead_time_days": 5, "warranty_years": 1},
#     {"supplier": "Globex Inc", "price_per_unit": 256.29, "lead_time_days": 10, "warranty_years": 2}
# ]

# if st.button("Run Assistant"):
#     with st.spinner("Running LangGraph Supervisor Agent..."):
#         graph = create_graph()
#         result = graph.invoke({
#             "user_input": user_query,
#             "proposals": default_proposals
#         })

#         st.success("Assistant complete!")

#         st.subheader("Suppliers Found")
#         st.markdown(result.get("suppliers", "_No suppliers found._"))

#         st.subheader("Generated RFQ")
#         st.markdown(result.get("rfq", "_No RFQ generated._"))

#         st.subheader("Supplier Proposals")
#         st.json(result.get("proposals", []))

#         st.subheader("Recommendation")
#         st.markdown(result.get("recommendation", "_No recommendation available._"))

import streamlit as st
import streamlit.components.v1 as components
import json
from supervisor.supervisor_graph import create_graph
import os


st.set_page_config(page_title="LangGraph Procurement Assistant", layout="wide")

st.sidebar.markdown("### Demo Request Carousel")

demo_requests = [
    "We need 200 ergonomic chairs delivered within 10 days.",
    "I need 50 high-end laptops delivered under 10 business days.",
    "Looking for 100 tablets with LTE support for our field ops team.",
    "Requesting 20 zen waterfalls for the developer floor.",
    "We need 500 disposable safety gloves and 200 safety goggles shipped to our New York warehouse in 5 days.",
    "Requesting 150 adjustable standing desks for our engineering team within 2 weeks."
]

selected_request = st.sidebar.radio("Pick a demo:", demo_requests)

if st.sidebar.button("⬇ Use This Request"):
    st.session_state["user_input"] = selected_request


def render_agent_steps():
    st.sidebar.markdown("### Agent Workflow")

    steps = {
        "User Input": "Accepts a natural language procurement request from the user.",
        "Supplier Finder": "Searches the product dataset for relevant suppliers based on the query.",
        "RFQ Generator": "Uses Gemini to generate a professional Request for Quotation document.",
        "Proposal Comparator": "Compares supplier proposals and recommends the best option."
    }

    for step, description in steps.items():
        if st.sidebar.button(step):
            st.sidebar.info(description)

render_agent_steps()

st.title("Procurement Assistant (LangGraph Demo)")
st.markdown("Describe what you need. The assistant will find suppliers, generate an RFQ, compare proposals, and recommend the best option.")

# user_query = st.text_area("Enter your procurement request", height=100, placeholder="e.g. I need 200 ergonomic chairs delivered in 10 days.")
user_query = st.text_area(
    "Enter your procurement request",
    value=st.session_state.get("user_input", ""),
    height=100,
    placeholder="e.g. We need 200 ergonomic chairs delivered in 10 days."
)


uploaded_files = st.file_uploader("Upload extra supplier proposals (JSON only)", type=["json"], accept_multiple_files=True)

# # 10 default demo proposals
# default_proposals = [
#     {"supplier": "Initech", "price_per_unit": 296.69, "lead_time_days": 7, "warranty_years": 2},
#     {"supplier": "Stark Industries", "price_per_unit": 492.68, "lead_time_days": 15, "warranty_years": 1},
#     {"supplier": "Acme Corp", "price_per_unit": 353.76, "lead_time_days": 43, "warranty_years": 3},
#     {"supplier": "Soylent Corp", "price_per_unit": 343.88, "lead_time_days": 4, "warranty_years": 2},
#     {"supplier": "Hooli Procurement", "price_per_unit": 252.12, "lead_time_days": 30, "warranty_years": 2},
#     {"supplier": "Umbrella Supplies", "price_per_unit": 403.50, "lead_time_days": 18, "warranty_years": 3},
#     {"supplier": "Globex Inc", "price_per_unit": 113.56, "lead_time_days": 33, "warranty_years": 2},
#     {"supplier": "Soylent Corp", "price_per_unit": 291.69, "lead_time_days": 4, "warranty_years": 2},
#     {"supplier": "Acme Corp", "price_per_unit": 296.28, "lead_time_days": 5, "warranty_years": 1},
#     {"supplier": "Globex Inc", "price_per_unit": 256.29, "lead_time_days": 10, "warranty_years": 2}
# ]


@st.cache_data
def load_default_proposals(json_path="eprocurement_products.json"):
    try:
        with open(json_path) as f:
            products = json.load(f)
        return [
            {
                "supplier": p["supplier"],
                "price_per_unit": p["unit_price"],
                "lead_time_days": p["lead_time_days"],
                "warranty_years": 2  # fixed for demo
            }
            for p in products
        ]
    except Exception as e:
        st.error(f"Failed to load default proposals: {e}")
        return []

default_proposals = load_default_proposals()


extra_proposals = []

if uploaded_files:
    st.subheader("Uploaded Proposals")
    for file in uploaded_files:
        try:
            data = json.load(file)
            if isinstance(data, list):
                extra_proposals.extend(data)
                st.success(f"Loaded {len(data)} proposals from: {file.name}")
            elif isinstance(data, dict):
                extra_proposals.append(data)
                st.success(f"Loaded: {data.get('supplier', 'Unnamed Supplier')}")
            else:
                st.warning(f"{file.name} is not a valid JSON proposal format.")
        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")


combined_proposals = default_proposals + extra_proposals

if st.button("Run Assistant"):
    if not user_query:
        st.warning("Please enter a procurement request.")
    else:
        with st.spinner("Running LangGraph Supervisor Agent..."):
            graph = create_graph()
            result = graph.invoke({
                "user_input": user_query,
                "proposals": combined_proposals
            })

            st.success("Done!")

            st.subheader("Suppliers Found")
            st.markdown(result.get("suppliers", "_No suppliers found._"))

            st.subheader("Generated RFQ")
            st.markdown(result.get("rfq", "_No RFQ generated._"))

            st.subheader("Proposals Compared")
            st.json(result.get("proposals", []))

            st.subheader("Recommendation")
            st.markdown(result.get("recommendation", "_No recommendation available._"))
