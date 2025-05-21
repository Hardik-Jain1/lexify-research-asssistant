# app/services/litellm_service.py
import litellm
from flask import current_app
import os

def configure_litellm():
    """
    Configures LiteLLM based on environment variables.
    This function should be called once, perhaps during app initialization if needed,
    or LiteLLM will pick up env vars automatically.
    """
    # LiteLLM typically reads API keys from environment variables directly (e.g., OPENAI_API_KEY, GOOGLE_API_KEY)
    # You can set them programmatically if needed, but it's often better to manage them via .env
    
    # Example: if you need to set it from Flask config for some reason
    # if current_app.config.get('OPENAI_API_KEY'):
    #     litellm.api_key = current_app.config['OPENAI_API_KEY'] # For OpenAI
    # if current_app.config.get('GOOGLE_API_KEY'):
    # litellm.gemini_api_key = current_app.config['GOOGLE_API_KEY'] # For Gemini
    # litellm.vertex_project = "your-gcp-project"  # if using Vertex AI
    # litellm.vertex_location = "your-gcp-location" # if using Vertex AI

    # Set a callback for logging, if desired
    # litellm.success_callback = ["langfuse"] # Example for Langfuse
    # litellm.failure_callback = []

    # You can also set a global model alias or routing strategy here if complex
    current_app.logger.info("LiteLLM configured (primarily relies on environment variables for API keys).")

def completion(*args, **kwargs):
    """
    A wrapper around litellm.completion to potentially add more centralized logging,
    error handling, or default model selection from Flask config.
    """
    # Ensure LiteLLM is configured (idempotent or called once at app start)
    # configure_litellm() # Not strictly necessary here if env vars are set

    # Example: Add custom logging
    # current_app.logger.debug(f"LiteLLM completion called with model: {kwargs.get('model')}")
    try:
        response = litellm.completion(*args, **kwargs)
        # current_app.logger.debug(f"LiteLLM response: {response}")
        return response
    except Exception as e:
        # current_app.logger.error(f"LiteLLM completion error: {e}")
        # You might want to map specific LiteLLM exceptions to HTTP errors
        if isinstance(e, litellm.exceptions.APIConnectionError):
            # Handle connection error
            pass
        elif isinstance(e, litellm.exceptions.AuthenticationError):
            # Handle auth error - check your API keys
            pass
        # ... other specific exceptions
        raise # Re-raise the exception to be caught by the API layer

def embedding(*args, **kwargs):
    """
    A wrapper around litellm.embedding.
    """
    try:
        response = litellm.embedding(*args, **kwargs)
        return response
    except Exception as e:
        # current_app.logger.error(f"LiteLLM embedding error: {e}")
        raise