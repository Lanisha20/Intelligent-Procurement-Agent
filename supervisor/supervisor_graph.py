from langgraph.graph import StateGraph, END
from supervisor.state import AgentState
from supervisor.nodes.supplier_node import supplier_node
from supervisor.nodes.rfq_node import rfq_node
from supervisor.nodes.compare_node import compare_node

def create_graph():
    builder = StateGraph(AgentState)

    builder.add_node("supplier", supplier_node)
    builder.add_node("rfq", rfq_node)
    builder.add_node("compare", compare_node)

    builder.set_entry_point("supplier")

    builder.add_edge("supplier", "rfq")
    builder.add_edge("rfq", "compare")
    builder.add_edge("compare", END)

    return builder.compile()
