import litellm
from flask import current_app
import os

def configure_litellm():
    """Configures LiteLLM based on environment variables."""
    current_app.logger.info("LiteLLM configured (primarily relies on environment variables for API keys).")

def completion(*args, **kwargs):
    """Wrapper around litellm.completion with centralized error handling."""
    try:
        response = litellm.completion(*args, **kwargs)
        return response
    except Exception as e:
        if isinstance(e, litellm.exceptions.APIConnectionError):
            pass
        elif isinstance(e, litellm.exceptions.AuthenticationError):
            pass
        raise

def embedding(*args, **kwargs):
    """Wrapper around litellm.embedding with centralized error handling."""
    try:
        response = litellm.embedding(*args, **kwargs)
        return response
    except Exception as e:
        raise