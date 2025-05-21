# AI Research Assistant - Backend

This is the backend for the AI Research Assistant, a full-stack application designed to help users with academic or scientific research. It enables users to search for research papers, summarize content using LLMs, interactively chat with papers using Retrieval-Augmented Generation (RAG), and manages user authentication and chat history.

## Core Features

* **User Authentication:** Secure user registration, login, and JWT-based session management, including logout.
* **Research Paper Search:** Query ArXiv for relevant academic papers via an external API.
* **Paper Summarization:**
    * Generate individual summaries for fetched papers using LLMs (via LiteLLM, supporting Gemini and others).
    * Synthesize a consolidated one-paragraph summary from multiple papers.
* **PDF Processing Pipeline:**
    * Download PDFs from URLs.
    * Extract text content from PDFs.
    * Clean extracted text for optimal LLM processing.
* **RAG (Retrieval-Augmented Generation) System:**
    * Chunk processed text from papers.
    * Generate vector embeddings for text chunks.
    * Index embeddings in Qdrant Cloud vector database.
    * Retrieve relevant context from selected papers based on user queries.
    * Enable interactive, conversational Q&A with selected papers, maintaining chat history.
* **Persistent Data Storage:**
    * Store user accounts, paper metadata, chat sessions, and individual chat messages in a relational database (e.g., PostgreSQL, MySQL, or SQLite for development).
* **Cloud-Ready Architecture:** Designed for deployment on platforms like Render.com.
* **File-based Logging:** Application logs are stored in `logs/app.log` with rotation.

## Tech Stack

* **Backend Framework:** Flask (Python)
* **Database ORM:** SQLAlchemy
* **Database Migration:** Flask-Migrate
* **Authentication:** Flask-JWT-Extended (JWTs)
* **Vector Database:** Qdrant Cloud (or local instance)
* **LLM Interaction:** LiteLLM (for connecting to various LLMs like Google Gemini)
* **PDF Processing:** PyMuPDF (fitz), ftfy
* **Text Processing:** Langchain (for text splitting)
* **External APIs:** ArXiv API
* **Supported Databases:** PostgreSQL, MySQL, SQLite (default for development)

## Prerequisites

* Python 3.9+
* Pip (Python package installer)
* A running Qdrant instance (local or cloud) accessible to the backend.
* Access to an LLM provider API key supported by LiteLLM (e.g., Google AI Studio API Key for Gemini).
* (Optional for production) A PostgreSQL or MySQL database server.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd backend
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the project root directory. Fill in your specific configurations:
    ```env
    # Flask Core
    SECRET_KEY='your_very_strong_random_secret_key_for_flask_sessions'
    FLASK_APP='run.py' # Should be in .flaskenv, but can be here too
    FLASK_ENV='development' # Should be in .flaskenv, set to 'production' for deployment

    # JWT Configuration
    JWT_SECRET_KEY='your_very_strong_random_secret_key_for_jwt'

    # Database (Example for SQLite, adjust for PostgreSQL/MySQL)
    DATABASE_URL='sqlite:///../instance/dev.db'
    # Example for PostgreSQL:
    # DATABASE_URL='postgresql://user:password@host:port/dbname'

    # Qdrant Configuration
    QDRANT_URL='http://localhost:6333' # Or your Qdrant Cloud URL
    QDRANT_API_KEY='your_qdrant_cloud_api_key' # Optional, if your Qdrant instance requires it

    # LiteLLM / LLM Provider API Keys (Example for Google Gemini)
    GEMINI_API_KEY='your_google_ai_studio_api_key'
    # OPENAI_API_KEY='your_openai_api_key' # If using OpenAI models via LiteLLM

    # LiteLLM Model Configuration (Defaults are in app/config.py, can be overridden here)
    # LITELLM_MODEL_SUMMARIZE='gemini/gemini-2.0-flash'
    # LITELLM_MODEL_CHAT='gemini/gemini-2.0-flash'
    # EMBEDDING_MODEL_NAME='gemini/text-embedding-004' # Google's model via LiteLLM for embeddings

    # Application Specific Paths (Defaults are in app/config.py)
    # PAPER_SAVE_DIR='data/papers'
    # PROMPTS_DIR='prompts'
    ```
    Create a `.flaskenv` file in the project root for Flask CLI specific variables:
    ```env
    FLASK_APP=run.py
    FLASK_ENV=development # Change to 'production' for production builds
    FLASK_DEBUG=1         # Set to 0 in production
    ```

5.  **Initialize and Migrate Database:**
    Ensure your `DATABASE_URL` in `.env` is correctly configured.
    ```bash
    flask db init  # Run only once to create the migrations directory
    flask db migrate -m "Initial database schema." # Or a descriptive message for changes
    flask db upgrade # Apply migrations to the database
    ```
    This will create an `instance` folder with `dev.db` if using the default SQLite setup.
    And also add `sqlalchemy.url = DATABASE_URL` line in [alembic] part of migrations/alembic.ini file

6.  **Verify Prompt Files:**
    Ensure the `prompts/` directory exists in the project root and contains the necessary prompt template files:
    * `sys_role_paper_sum.txt`
    * `user_prompt_paper_sum.txt`
    * `sys_role_final_response.txt`
    * `user_prompt_final_response.txt`
    * `sys_role_chat.txt`
    * `user_prompt_chat.txt`

7.  **Create Log Directory:**
    Ensure a `logs/` directory exists in the project root for storing log files. The application will attempt to create it if `FLASK_ENV` is not `development`.

## Running the Application

1.  **Ensure your virtual environment is activated.**
2.  **Start the Flask Development Server:**
    ```bash
    python run.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`. Check the console output for the exact URL and port.

## API Endpoints Overview

The backend exposes RESTful APIs under the `/api` prefix. Key groups include:

* **`/api/auth/`**: User registration (`/register`), login (`/login`), logout (`/logout`), and protected route example (`/protected`).
* **`/api/papers/`**:
    * `/search`: Search for papers, get summaries, and initiate background processing.
    * `/<paper_db_id>/status`: Get the processing status of a specific paper.
    * `/<paper_db_id>/process-manual`: Manually trigger processing for a paper (e.g., for retries).
* **`/api/rag/`**:
    * `/chat`: Interact with selected, processed papers.
    * `/sessions`: List chat sessions for the logged-in user.
    * `/sessions/<session_id>/messages`: Retrieve messages for a specific chat session.

Refer to the API implementation in `app/api/` for detailed request/response formats.

## Project Structure
```
backend/
├── app/                     # Main application package
│   ├── init.py          # Application factory, logging setup
│   ├── api/                 # API Blueprints (auth, papers, rag)
│   ├── core/                # Core business logic services
│   ├── models/              # SQLAlchemy database models
│   ├── services/            # External service integrations (Qdrant, LiteLLM, Embeddings)
│   ├── config.py            # Configuration classes
│   └── extensions.py        # Flask extension initializations (db, jwt, migrate)
├── data/papers/             # Default directory for downloaded PDFs (gitignored)
├── instance/                # Instance folder, e.g., for SQLite DB (gitignored)
├── logs/                    # Application log files (gitignored)
├── migrations/              # Database migration scripts
├── prompts/                 # LLM prompt templates
├── retriever/               # Original paper retrieval scripts
├── summarizer/              # Original summarization scripts
├── processor/               # Original PDF processing scripts
├── rag/                     # Original RAG logic scripts
├── tests/                   # (Placeholder for tests)
├── venv/                    # Python virtual environment (gitignored)
├── .env                     # Environment variables (gitignored)
├── .flaskenv                # Flask CLI environment variables
├── requirements.txt         # Python dependencies
├── run.py                   # Script to run the Flask application
└── README.md                # This file
```
