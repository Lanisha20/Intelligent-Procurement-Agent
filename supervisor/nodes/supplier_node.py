from tools.supplier_finder import find_suppliers

def supplier_node(state):
    query = state.get("user_input", "")
    result = find_suppliers(query)
    return {
        "suppliers": result,
        "next_step": "generate_rfq"
    }