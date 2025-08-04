# from dotenv import load_dotenv
# load_dotenv()

# from langchain_google_vertexai import VertexAI
# from langchain.agents import Tool, initialize_agent
# from langchain.agents.agent_types import AgentType
# from tools.supplier_finder import find_suppliers
# from tools.rfq_generator import generate_rfq

# # 🔐 Load the Vertex AI model
# llm = VertexAI(
#     model_name="gemini-2.5-pro",
#     temperature=0.3,
#     max_output_tokens=1024
# )

# # 🔧 Define the Supplier Finder Tool
# supplier_tool = Tool(
#     name="SupplierFinder",
#     func=find_suppliers,
#     description="Useful for finding the best suppliers based on the user's query"
# )

# # ✉️ Define the RFQ Generator Tool
# rfq_tool = Tool(
#     name="RFQGenerator",
#     func=lambda q: generate_rfq("IT Equipment", "50 boxes", "10 days", q),
#     description="Use this to generate an RFQ document from user input. You can provide additional notes as input."
# )

# # 🧠 Initialize the LangChain Agent
# agent = initialize_agent(
#     tools=[supplier_tool, rfq_tool],
#     llm=llm,
#     agent=AgentType.OPENAI_FUNCTIONS,
#     handle_parsing_errors=True,
#     verbose=True
# )

# example_proposals = [
#     {
#         "supplier": "Initech",
#         "price_per_unit": 315.75,
#         "lead_time_days": 12,
#         "warranty_years": 2
#     },
#     {
#         "supplier": "Stark Industries",
#         "price_per_unit": 289.50,
#         "lead_time_days": 14,
#         "warranty_years": 1
#     },
#     {
#         "supplier": "Acme Corp",
#         "price_per_unit": 310.00,
#         "lead_time_days": 9,
#         "warranty_years": 3
#     }
# ]
# # Run the agent
# # if __name__ == "__main__":
# #     print("Intelligent Procurement Agent Ready.")
# #     while True:
# #         user_input = input("\n🧑 You: ")
# #         if user_input.lower() in ["exit", "quit"]:
# #             break
# #         result = agent.invoke(user_input)
# #         print(f"\n🤖 Agent: {result}")

# # if __name__ == "__main__":
# #     # 🔧 Manual test of RFQ generator
# #     print("\n🧪 Testing RFQ Generator Tool...\n")
# #     result = generate_rfq(
# #         product="Monitors",
# #         quantity="100",
# #         delivery_time="7 days",
# #         notes="Need these urgently for remote work setup"
# #     )
# #     print(result)


# from tools.proposal_comparator import compare_proposals

# if __name__ == "__main__":
#     mock_data = [
#         {"supplier": "Initech", "price_per_unit": 315.75, "lead_time_days": 12, "warranty_years": 2},
#         {"supplier": "Stark Industries", "price_per_unit": 289.50, "lead_time_days": 14, "warranty_years": 1},
#         {"supplier": "Acme Corp", "price_per_unit": 310.00, "lead_time_days": 9, "warranty_years": 3}
#     ]
#     print("🔍 Comparing proposals...\n")
#     print(compare_proposals(mock_data))


# # test ?

from dotenv import load_dotenv
load_dotenv()

# from supervisor.supervisor_graph import Runnable
from supervisor.state import AgentState

from supervisor.supervisor_graph import create_graph

# Example proposals to compare (used by compare_node)
example_proposals = [
    {
        "supplier": "Initech",
        "price_per_unit": 315.75,
        "lead_time_days": 12,
        "warranty_years": 2
    },
    {
        "supplier": "Stark Industries",
        "price_per_unit": 289.50,
        "lead_time_days": 14,
        "warranty_years": 1
    },
    {
        "supplier": "Acme Corp",
        "price_per_unit": 310.00,
        "lead_time_days": 9,
        "warranty_years": 3
    }
]

if __name__ == "__main__":
    graph = create_graph()

    result = graph.invoke({
        "user_input": "We need 200 ergonomic chairs delivered within 10 days",
        "proposals": example_proposals
    })

    print("\n🧠 Supervisor Agent Result:")
    for k, v in result.items():
        print(f"{k}:\n{v}\n")
