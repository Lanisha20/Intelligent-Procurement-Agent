import streamlit as st
import json
import pandas as pd
from tools.proposal_comparator import compare_proposals
from tools.pdf_utils import extract_text_from_pdf, extract_structured_proposal

st.set_page_config(page_title="Supplier Proposal Comparator", layout="wide")
st.title("Supplier Proposal Comparator")

st.markdown("Upload one or more supplier proposals in **JSON** or **PDF** format. We'll extract price, lead time, and warranty, compare them, and recommend the best supplier.")

uploaded_files = st.file_uploader("Upload proposal files", type=["json", "pdf"], accept_multiple_files=True)

proposals = []

for file in uploaded_files:
    try:
        if file.type == "application/json":
            data = json.load(file)
            proposals.append(data)
            st.success(f"Loaded JSON: {data.get('supplier', 'Unnamed Supplier')}")
        elif file.type == "application/pdf":
            raw_text = extract_text_from_pdf(file)
            st.text_area(f"Extracted text from {file.name}", raw_text[:1000], height=200)

            if st.button(f"Parse PDF: {file.name}"):
                with st.spinner("Extracting structured proposal..."):
                    extracted_json = extract_structured_proposal(raw_text)
                    try:
                        parsed = json.loads(extracted_json)
                        proposals.append(parsed)
                        st.success(f"Parsed proposal from: {parsed.get('supplier', 'Unknown Supplier')}")
                        st.json(parsed)
                    except Exception as parse_error:
                        st.error(f"Gemini returned invalid JSON: {parse_error}")
                        st.code(extracted_json, language="json")
    except Exception as e:
        st.error(f"Failed to process {file.name}: {e}")

if len(proposals) >= 2:
    df = pd.DataFrame(proposals)
    st.subheader("Proposal Summary Table")
    st.text(f"Detected columns: {df.columns.tolist()}")

    required_columns = {"supplier", "price_per_unit", "lead_time_days", "warranty_years"}

    def highlight_best(series, best="min"):
        if best == "min":
            is_best = series == series.min()
        else:
            is_best = series == series.max()
        return ["background-color: #264653" if v else "" for v in is_best]

    if required_columns.issubset(df.columns):
        styled_df = df.style \
            .apply(highlight_best, subset="price_per_unit", best="min") \
            .apply(highlight_best, subset="lead_time_days", best="min") \
            .apply(highlight_best, subset="warranty_years", best="max")

        st.dataframe(styled_df, use_container_width=True)
    else:
        st.warning("Missing required fields. Showing raw data without highlighting.")
        st.dataframe(df, use_container_width=True)

    if st.button("Compare Proposals and Recommend"):
        with st.spinner("Analyzing with Gemini..."):
            result = compare_proposals(proposals)
            st.subheader("Supplier Recommendation")
            st.markdown(result)
else:
    st.info("Upload at least 2 supplier proposals to enable comparison.")
