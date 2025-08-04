from typing import TypedDict, Optional, List, Literal

class AgentState(TypedDict, total=False):
    user_input: str
    product: Optional[str]
    quantity: Optional[str]
    delivery_time: Optional[str]
    notes: Optional[str]
    suppliers: Optional[str]
    rfq: Optional[str]
    proposals: Optional[List[dict]]
    recommendation: Optional[str]
    next_step: Optional[Literal["find_suppliers", "generate_rfq", "compare_proposals", "done"]]
