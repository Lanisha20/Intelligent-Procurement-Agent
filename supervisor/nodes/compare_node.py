from tools.proposal_comparator import compare_proposals

def compare_node(state):
    proposals = state.get("proposals", [])

    if not proposals or not isinstance(proposals, list):
        return {
            "recommendation": "No valid proposals were provided to compare.",
            "next_step": "done"
        }

    result = compare_proposals(proposals)
    return {
        "recommendation": result,
        "next_step": "done"
    }
