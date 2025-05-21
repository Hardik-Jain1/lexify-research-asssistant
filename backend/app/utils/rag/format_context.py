def format_llm_context(context_dict):
    context_parts = []
    for paper_id, paper_data in context_dict.items():
        context_parts.append(
            f"=== Paper: {paper_id} ===\n"
            f"Title: {paper_data['title']}\n"
            f"Content:\n{paper_data['text']}\n"
        )
    return "\n".join(context_parts)