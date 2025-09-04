from .format_context import format_llm_context
import os

def chat_with_papers(
    llm_context: str,
    query: str,
    config,
    llm_completion_func,
    chat_history: list = None,
    history_window: int = 10,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    top_p: float = 0.5,
) -> dict:
    prompts_dir = config.get('PROMPTS_DIR', 'prompts/')
    model_name = config.get('LITELLM_MODEL_CHAT', 'gemini/gemini-2.0-flash')

    with open(os.path.join(prompts_dir, "sys_role_chat.txt"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(os.path.join(prompts_dir, "user_prompt_chat.txt"), "r", encoding="utf-8") as f:
        user_prompt_template = f.read()

    chat_history = chat_history or []
    # Keep last 'history_window' pairs of messages
    if history_window > 0 and chat_history:
        start_index = max(0, len(chat_history) - (history_window * 2))
        processed_chat_history = chat_history[start_index:]
    else:
        processed_chat_history = []

    messages = []
    messages.append({"role": "system", "content": system_prompt})

    # Add historical messages
    for msg in processed_chat_history:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Current user query with context
    user_prompt = user_prompt_template.format(context=llm_context, user_query=query)
    messages.append({"role": "user", "content": user_prompt})

    response = llm_completion_func(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
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

    token_usage = {}
    if hasattr(response, "usage"):
        usage = response.usage
        token_usage = {
            "input_tokens": getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
    elif isinstance(response, dict) and "usage" in response:
        usage = response["usage"]
        token_usage = {
            "input_tokens": usage.get("prompt_tokens") or usage.get("input_tokens"),
            "output_tokens": usage.get("completion_tokens") or usage.get("output_tokens"),
            "total_tokens": usage.get("total_tokens"),
        }
    else:
        token_usage = {"input_tokens": None, "output_tokens": None, "total_tokens": None}

    return {
        "response": content,
        "token_usage": token_usage
    }