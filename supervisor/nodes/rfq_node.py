# from tools.supplier_finder import find_suppliers

# def supplier_node(state):
#     query = state.get("user_input", "")
#     result = find_suppliers(query)
#     return {"suppliers": result, "next_step": "generate_rfq"}

from tools.rfq_generator import generate_rfq_from_user_input

def rfq_node(state):
    user_input = state.get("user_input", "")
    rfq = generate_rfq_from_user_input(user_input)
    return {
        "rfq": rfq,
        "next_step": "compare_proposals"
    }

