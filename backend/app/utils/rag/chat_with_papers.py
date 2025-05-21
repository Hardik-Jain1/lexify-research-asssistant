# rag/chat_with_papers.py
# from .context_retriever import retrieve_context # This will be called by the service layer
from .format_context import format_llm_context # This can remain as is
# import litellm # Remove if using llm_completion_func
import os

def chat_with_papers(
    # selected_papers_metadata: list, # This will be handled by the calling service which prepares context
    llm_context: str, # Directly pass the formatted context string
    query: str,
    config, # Pass Flask app.config or relevant parts
    llm_completion_func, # Pass the completion function
    chat_history: list = None,
    history_window: int = 10, # Consider making this configurable
    # model_name will come from config
    max_tokens: int = 4096, # Default, can be overridden by config
    temperature: float = 0.0,
    top_p: float = 0.5,
) -> dict:
    # context_dict = retrieve_context(selected_papers_metadata, query, top_k=5) # Moved to service layer
    # llm_context = format_llm_context(context_dict) # Context is now passed directly

    prompts_dir = config.get('PROMPTS_DIR', 'prompts/')
    model_name = config.get('LITELLM_MODEL_CHAT', 'gemini/gemini-2.0-flash')
    # max_tokens_chat = config.get('MAX_TOKENS_CHAT', max_tokens) # Allow override from config

    with open(os.path.join(prompts_dir, "sys_role_chat.txt"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(os.path.join(prompts_dir, "user_prompt_chat.txt"), "r", encoding="utf-8") as f:
        user_prompt_template = f.read()

    chat_history = chat_history or []
    # Ensure history window considers pairs of user/assistant messages
    if history_window > 0 and chat_history:
        # Keep last 'history_window' pairs of messages (user + assistant)
        # Each pair is 2 messages, so look for 2 * history_window
        # Ensure we don't slice with a negative start if history is shorter
        start_index = max(0, len(chat_history) - (history_window * 2))
        processed_chat_history = chat_history[start_index:]
    else:
        processed_chat_history = []


    messages = []
    messages.append({"role": "system", "content": system_prompt})

    # Add historical messages
    for msg in processed_chat_history: # Use the sliced history
        # Ensure msg has 'role' and 'content'
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            messages.append({"role": msg["role"], "content": msg["content"]})
        # If using ChatMessage objects from DB, convert them:
        # messages.append({"role": msg.role, "content": msg.content})


    # Current user query with context
    user_prompt = user_prompt_template.format(context=llm_context, user_query=query)
    messages.append({"role": "user", "content": user_prompt})

    response = llm_completion_func(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens, # Use max_tokens_chat if defined
        temperature=temperature,
        top_p=top_p,
    )

    # ... (rest of your response parsing logic for content and token_usage remains the same)
    if hasattr(response, "choices"):
        content = response.choices[0].message.content
    elif isinstance(response, dict) and "choices" in response:
        content = response["choices"][0]["message"]["content"]
    elif hasattr(response, "content"):
        content = response.content
    else:
        content = str(response) # Fallback

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
    else: # Fallback if usage info is structured differently or absent
        token_usage = {"input_tokens": None, "output_tokens": None, "total_tokens": None}


    return {
        "response": content,
        # "sources": context_dict, # This is now passed into the function as llm_context, sources are better handled by caller
        "token_usage": token_usage
    }