from flask import current_app
import os

def get_llm_completion_function():
    import litellm
    return litellm.completion

def summarize_arxiv_papers(
    arxiv_results,
    config,
    llm_completion_func,
    max_tokens_per_summary=1024,
    temperature=0.0,
    top_p=0.5,
):
    prompts_dir = config.get('PROMPTS_DIR', 'prompts/')
    model_name = config.get('LITELLM_MODEL_SUMMARIZE', 'gemini/gemini-2.0-flash')

    with open(os.path.join(prompts_dir, "sys_role_paper_sum.txt"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(os.path.join(prompts_dir, "user_prompt_paper_sum.txt"), "r", encoding="utf-8") as f:
        user_prompt_template = f.read()

    summaries = []
    for paper in arxiv_results:
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        paper_id = paper.get("paper_id", "")
        if not abstract:
            summary = "Abstract not available to summarize."
            usage_info = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt_template.format(paper_title=title, paper_abstract=abstract)},
            ]
            response = llm_completion_func(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens_per_summary,
                temperature=temperature,
                top_p=top_p,
            )

            # Parse response content
            if hasattr(response, "choices"):
                summary = response.choices[0].message.content
            elif isinstance(response, dict) and "choices" in response:
                summary = response["choices"][0]["message"]["content"]
            elif hasattr(response, "content"):
                summary = response.content
            else:
                summary = str(response)

            usage_info = {"input_tokens": None, "output_tokens": None, "total_tokens": None}
            if hasattr(response, "usage"):
                 usage = response.usage
                 usage_info = {
                     "input_tokens": getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None),
                     "output_tokens": getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", None),
                     "total_tokens": getattr(usage, "total_tokens", None),
                 }
            elif isinstance(response, dict) and "usage" in response:
                 usage = response["usage"]
                 usage_info = {
                     "input_tokens": usage.get("prompt_tokens") or usage.get("input_tokens"),
                     "output_tokens": usage.get("completion_tokens") or usage.get("output_tokens"),
                     "total_tokens": usage.get("total_tokens"),
                 }

        summaries.append({
            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "summary": summary,
            "input_tokens": usage_info.get("input_tokens"),
            "output_tokens": usage_info.get("output_tokens"),
        })
    return summaries


def synthesize_insights_from_summaries(
    paper_summaries,
    query,
    config,
    llm_completion_func,
    max_tokens_synthesis=4096,
    temperature=0.0,
    top_p=0.5,
):
    prompts_dir = config.get('PROMPTS_DIR', 'prompts/')
    model_name = config.get('LITELLM_MODEL_SUMMARIZE', 'gemini/gemini-2.0-flash')

    with open(os.path.join(prompts_dir, "sys_role_final_response.txt"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(os.path.join(prompts_dir, "user_prompt_final_response.txt"), "r", encoding="utf-8") as f:
        user_prompt_template = f.read()

    summaries_str = "\n".join(
        f"[{paper['paper_id']}] Title: {paper['title']}\nSummary: {paper['summary']}"
        for paper in paper_summaries if paper.get("summary")
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_template.format(query=query, summaries=summaries_str)},
    ]
    response = llm_completion_func(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens_synthesis,
        temperature=temperature,
        top_p=top_p,
    )
    
    # Parse response content
    if hasattr(response, "choices"):
        content = response.choices[0].message.content
    elif isinstance(response, dict) and "choices" in response:
        content = response["choices"][0]["message"]["content"]
    elif hasattr(response, "content"):
        content = response.content
    else:
        content = str(response)

    result = {
        "content": content,
        "input_tokens": None,
        "output_tokens": None,
    }
    if hasattr(response, "usage"):
         usage = response.usage
         result["input_tokens"] = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None)
         result["output_tokens"] = getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", None)
    elif isinstance(response, dict) and "usage" in response:
         usage = response["usage"]
         result["input_tokens"] = usage.get("prompt_tokens") or usage.get("input_tokens")
         result["output_tokens"] = usage.get("completion_tokens") or usage.get("output_tokens")

    return result