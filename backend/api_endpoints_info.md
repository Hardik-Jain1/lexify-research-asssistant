Here's a summary of the backend API endpoints that frontend will primarily interact with. This will serve as a good reference for the frontend API service integration.

All endpoints are prefixed with `/api`. For example, `/auth/register` becomes `/api/auth/register`.

-----

## Backend API Endpoint Collection

### Authentication (`/api/auth`)

1.  **User Registration**

      * **Endpoint:** `/register`
      * **Method:** `POST`
      * **Auth Required:** No
      * **Request Body (JSON):**
        ```json
        {
            "username": "your_username",
            "email": "user@example.com",
            "password": "your_password"
        }
        ```
      * **Success Response (201 Created):**
        ```json
        {
            "msg": "User created successfully",
            "user_id": 1
        }
        ```
      * **Error Responses:** 400 (Missing fields), 409 (User already exists)

2.  **User Login**

      * **Endpoint:** `/login`
      * **Method:** `POST`
      * **Auth Required:** No
      * **Request Body (JSON):**
        ```json
        {
            "username_or_email": "your_username_or_email",
            "password": "your_password"
        }
        ```
      * **Success Response (200 OK):**
        ```json
        {
            "access_token": "your_jwt_access_token",
            "user_id": 1,
            "username": "your_username"
        }
        ```
      * **Error Responses:** 400 (Missing fields), 401 (Bad username or password)

3.  **User Logout**

      * **Endpoint:** `/logout`
      * **Method:** `POST`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **Success Response (200 OK):**
        ```json
        {
            "msg": "Logout successful. Please discard your token."
            // Or, if blocklisting is implemented:
            // "msg": "Logout successful. Token has been revoked."
        }
        ```
      * **Error Responses:** 401 (Unauthorized if token is missing/invalid)

4.  **Protected Route Example (for testing auth)**

      * **Endpoint:** `/protected`
      * **Method:** `GET`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **Success Response (200 OK):**
        ```json
        {
            "logged_in_as": "current_username",
            "user_id": 1
        }
        ```

-----

### Papers (`/api/papers`)

1.  **Search Papers & Get Summaries**

      * **Endpoint:** `/search`
      * **Method:** `POST`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body (JSON):**
        ```json
        {
            "query": "your research query"
        }
        ```
      * **Success Response (200 OK):**
        ```json
        {
            "consolidated_summary": "A synthesized paragraph summary...",
            "token_usage_consolidated": { "input": null, "output": null },
            "papers": [
                {
                    "db_id": 1,
                    "paper_id": "arxiv_id_1",
                    "title": "Paper Title 1",
                    "authors": ["Author A", "Author B"],
                    "published": "YYYY-MM-DD",
                    "pdf_url": "url_to_pdf_1",
                    "abstract": "Abstract of paper 1...",
                    "individual_summary": "LLM summary of paper 1...",
                    "source": "arXiv",
                    "is_processed_for_chat": false, // Initially
                    "qdrant_collection_name": null  // Initially
                },
                // ... more papers
            ]
        }
        ```
      * **Error Responses:** 400 (Missing query), 401 (Unauthorized), 404 (No papers found), 500 (Internal error)

2.  **Get Paper Processing Status**

      * **Endpoint:** `/<int:paper_db_id>/status`
      * **Method:** `GET`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **URL Parameter:** `paper_db_id` (Integer ID of the paper from the database)
      * **Success Response (200 OK):**
        ```json
        {
            "paper_id": "arxiv_id_of_paper",
            "db_id": 1,
            "title": "Title of Paper",
            "downloaded_at": "iso_timestamp_or_null",
            "text_extracted_at": "iso_timestamp_or_null",
            "cleaned_text_at": "iso_timestamp_or_null",
            "indexed_at": "iso_timestamp_or_null",
            "qdrant_collection_name": "name_or_null",
            "is_ready_for_chat": true_or_false,
            "processing_status_notes": "Status like arXiv, or error messages"
        }
        ```
      * **Error Responses:** 401 (Unauthorized), 404 (Paper not found)

3.  **Manually Trigger Paper Processing (Optional for Frontend Retry)**

      * **Endpoint:** `/<int:paper_db_id>/process-manual`
      * **Method:** `POST`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **URL Parameter:** `paper_db_id`
      * **Success Response (202 Accepted):**
        ```json
        {
            "msg": "Processing re-initiated for paper <arxiv_id>. Check status endpoint."
        }
        ```
      * **Other Responses:** 200 (Already processed), 404 (Paper not found)

-----

### RAG Chat & History (`/api/rag`)

1.  **Chat with Selected Papers**

      * **Endpoint:** `/chat`
      * **Method:** `POST`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body (JSON):**
        ```json
        {
            "query": "Your question about the selected papers",
            "selected_paper_ids": [1, 2], // List of DB PaperMetadata IDs that are processed
            "chat_session_id": null // Or an existing session ID to continue a chat
        }
        ```
      * **Success Response (200 OK):**
        ```json
        {
            "chat_session_id": 123, // ID of the current/new chat session
            "response": "LLM's answer to your query...",
            "sources": { // Dictionary of context chunks used, keyed by paper_id
                "arxiv_id_1": {
                    "title": "Paper Title 1",
                    "text": "Combined retrieved text from paper 1...",
                    "_chunks": [
                        {"chunk_id": 0, "score": 0.89, "text": "Relevant chunk 1..."},
                        // ... more chunks
                    ]
                }
                // ... context from other selected papers
            },
            "token_usage": { "input": null, "output": null, "total_tokens": null }
        }
        ```
      * **Error Responses:** 400 (Missing fields, or paper not processed), 401 (Unauthorized), 403 (Session access denied), 404 (Paper not found), 500 (Internal error)

2.  **List User's Chat Sessions**

      * **Endpoint:** `/sessions`
      * **Method:** `GET`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **Success Response (200 OK):**
        ```json
        [
            {
                "id": 123,
                "session_name": "Chat about 'Paper Title Snippet' & others",
                "created_at": "iso_timestamp",
                "updated_at": "iso_timestamp",
                "paper_ids_in_session": [1, 2] // DB IDs of papers involved
            },
            // ... more sessions
        ]
        ```
      * **Error Responses:** 401 (Unauthorized)

3.  **Get Messages for a Specific Chat Session**

      * **Endpoint:** `/sessions/<int:session_id>/messages`
      * **Method:** `GET`
      * **Auth Required:** Yes (JWT Bearer Token)
      * **Request Body:** None
      * **URL Parameter:** `session_id` (Integer ID of the chat session)
      * **Success Response (200 OK):**
        ```json
        {
            "session_id": 123,
            "session_name": "Chat about 'Paper Title Snippet' & others",
            "associated_paper_titles": ["Paper Title 1", "Paper Title 2"],
            "messages": [
                {
                    "id": 1, "session_id": 123, "timestamp": "iso_timestamp",
                    "role": "user", "content": "User's first question..."
                },
                {
                    "id": 2, "session_id": 123, "timestamp": "iso_timestamp",
                    "role": "assistant", "content": "Assistant's first answer..."
                },
                // ... more messages
            ]
        }
        ```
      * **Error Responses:** 401 (Unauthorized), 403 (Session access denied), 404 (Session not found)

-----

This list should cover all the interactions your frontend will need with the backend. 