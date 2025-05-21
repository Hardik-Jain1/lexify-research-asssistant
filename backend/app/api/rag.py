# app/api/rag.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.paper import PaperMetadata
from app.models.chat import ChatSession, ChatMessage
from app.core.rag_service import RAGService
import datetime

rag_bp = Blueprint('rag_bp', __name__)

@rag_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_selected_papers():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    user_query = data.get('query')
    selected_paper_db_ids = data.get('selected_paper_ids') # Expecting list of DB PaperMetadata IDs
    chat_session_id = data.get('chat_session_id') # Optional: to continue an existing session

    if not user_query or not selected_paper_db_ids:
        return jsonify({"msg": "Query and selected_paper_ids are required"}), 400

    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 401 # Should not happen if JWT is valid

    # Fetch PaperMetadata objects for selected IDs, ensuring they are processed
    selected_papers_metadata_objects = []
    for pid in selected_paper_db_ids:
        paper = db.session.get(PaperMetadata, pid)
        if not paper:
            return jsonify({"msg": f"Paper with DB ID {pid} not found."}), 404
        if not paper.indexed_at or not paper.qdrant_collection_name:
            return jsonify({"msg": f"Paper '{paper.title}' (ID: {paper.arxiv_id}) is not yet processed for chat."}), 400
        selected_papers_metadata_objects.append({
            "arxiv_id": paper.arxiv_id, # RAG service needs arxiv_id
            "title": paper.title,
            "qdrant_collection_name": paper.qdrant_collection_name
            # Add any other fields retrieve_context_external expects in selected_papers_metadata
        })

    if not selected_papers_metadata_objects:
        return jsonify({"msg": "No valid (processed) papers selected for chat."}), 400

    # Manage Chat Session and History
    if chat_session_id:
        chat_session = db.session.get(ChatSession, chat_session_id)
        if not chat_session or chat_session.user_id != user.id:
            return jsonify({"msg": "Chat session not found or access denied."}), 403
    else: # Create new session
        # Create a default name for the session, perhaps from the first query or paper titles
        first_paper_title = selected_papers_metadata_objects[0]['title'][:50] if selected_papers_metadata_objects else "Chat"
        session_name = f"Chat about '{first_paper_title}{'...' if len(selected_papers_metadata_objects[0]['title']) > 50 else ''}' & others"
        if len(selected_papers_metadata_objects) > 1:
            session_name += f" and {len(selected_papers_metadata_objects) -1} more"

        chat_session = ChatSession(user_id=user.id, session_name=session_name)
        db.session.add(chat_session)
        # Associate papers with this new session
        for pid in selected_paper_db_ids:
            paper_obj = db.session.get(PaperMetadata, pid)
            if paper_obj:
                 chat_session.papers_in_session.append(paper_obj)
        db.session.commit() # Commit to get chat_session.id

    # Retrieve chat history for this session
    # Ensure messages are ordered by timestamp
    db_chat_history = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
    # Format for RAGService: list of {'role': 'user'/'assistant', 'content': '...'}
    formatted_chat_history = [msg.to_dict() for msg in db_chat_history] # Use to_dict or manual conversion


    try:
        # Get RAG response
        rag_response_data = RAGService.get_chat_response(
            selected_papers_metadata=selected_papers_metadata_objects,
            query=user_query,
            chat_history=formatted_chat_history # Pass the history
        )

        # Save user message and assistant response to DB
        user_message = ChatMessage(session_id=chat_session.id, role="user", content=user_query)
        assistant_message = ChatMessage(
            session_id=chat_session.id,
            role="assistant",
            content=rag_response_data['response'],
            # sources_json=rag_response_data.get('sources'), # If you decide to store sources
            # token_usage_json=rag_response_data.get('token_usage') # If storing token usage
        )
        db.session.add_all([user_message, assistant_message])
        chat_session.updated_at = datetime.datetime.now(datetime.timezone.utc) # Update session timestamp
        db.session.commit()

        return jsonify({
            "chat_session_id": chat_session.id,
            "response": rag_response_data['response'],
            "sources": rag_response_data.get('sources'), # For frontend display
            "token_usage": rag_response_data.get('token_usage')
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in RAG chat: {e}", exc_info=True)
        return jsonify({"msg": "An error occurred during chat.", "error": str(e)}), 500

# from .papers import process_paper_background
# import threading
# @rag_bp.route('/chat', methods=['POST'])
# @jwt_required()
# def chat_with_selected_papers():
#     current_user_id = int(get_jwt_identity())
#     data = request.get_json()

#     user_query = data.get('query')
#     selected_paper_db_ids = data.get('selected_paper_ids') # Expecting list of DB PaperMetadata IDs
#     chat_session_id = data.get('chat_session_id') # Optional: to continue an existing session

#     if not user_query or not selected_paper_db_ids:
#         return jsonify({"msg": "Query and selected_paper_ids are required"}), 400

#     user = db.session.get(User, current_user_id)
#     if not user:
#         return jsonify({"msg": "User not found"}), 401 # Should not happen if JWT is valid

#     selected_papers_metadata_objects = []
#     papers_triggered_for_processing_info = []
#     # papers_not_ready_info list is removed

#     for pid in selected_paper_db_ids:
#         paper = db.session.get(PaperMetadata, pid)
#         if not paper:
#             return jsonify({"msg": f"Paper with DB ID {pid} not found."}), 404
        
#         if paper.indexed_at and paper.qdrant_collection_name:
#             selected_papers_metadata_objects.append({
#                 "arxiv_id": paper.arxiv_id,
#                 "title": paper.title,
#                 "qdrant_collection_name": paper.qdrant_collection_name
#             })
#         else:
#             # Paper is not processed, trigger processing
#             paper_info = {"db_id": paper.id, "title": paper.title, "arxiv_id": paper.arxiv_id}
#             papers_triggered_for_processing_info.append(paper_info)
#             current_app.logger.info(f"Paper '{paper.title}' (ID: {paper.arxiv_id}) is not processed. Triggering background processing from chat endpoint.")
#             app_ctx = current_app.app_context() # Create a copy of the app context
#             thread = threading.Thread(target=process_paper_background, args=(app_ctx, paper.id))
#             thread.start()

#     if not selected_papers_metadata_objects:
#         msg = "No selected papers are currently ready for chat."
#         response_payload = {"msg": msg}
#         if papers_triggered_for_processing_info:
#             response_payload["processing_initiated_for"] = papers_triggered_for_processing_info
#             msg += f" Processing has been initiated for {len(papers_triggered_for_processing_info)} paper(s)."
        
#         response_payload["msg"] = msg + " Please try again in a few moments or check paper statuses."
#         # Consider returning 202 Accepted if processing was initiated and no papers were ready
#         return jsonify(response_payload), 400 

#     # Manage Chat Session and History
#     if chat_session_id:
#         chat_session = db.session.get(ChatSession, chat_session_id)
#         if not chat_session or chat_session.user_id != user.id:
#             return jsonify({"msg": "Chat session not found or access denied."}), 403
#     else: # Create new session
#         # Create a default name for the session, perhaps from the first query or paper titles
#         first_paper_title = selected_papers_metadata_objects[0]['title'][:50] if selected_papers_metadata_objects else "Chat"
#         session_name = f"Chat about '{first_paper_title}{'...' if len(selected_papers_metadata_objects[0]['title']) > 50 else ''}' & others"
#         if len(selected_papers_metadata_objects) > 1:
#             session_name += f" and {len(selected_papers_metadata_objects) -1} more"

#         chat_session = ChatSession(user_id=user.id, session_name=session_name)
#         db.session.add(chat_session)
#         # Associate papers with this new session
#         for pid in selected_paper_db_ids:
#             paper_obj = db.session.get(PaperMetadata, pid)
#             if paper_obj:
#                  chat_session.papers_in_session.append(paper_obj)
#         db.session.commit() # Commit to get chat_session.id

#     # Retrieve chat history for this session
#     # Ensure messages are ordered by timestamp
#     db_chat_history = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
#     # Format for RAGService: list of {'role': 'user'/'assistant', 'content': '...'}
#     formatted_chat_history = [msg.to_dict() for msg in db_chat_history] # Use to_dict or manual conversion


#     try:
#         # Get RAG response
#         rag_response_data = RAGService.get_chat_response(
#             selected_papers_metadata=selected_papers_metadata_objects,
#             query=user_query,
#             chat_history=formatted_chat_history # Pass the history
#         )

#         # Save user message and assistant response to DB
#         user_message = ChatMessage(session_id=chat_session.id, role="user", content=user_query)
#         assistant_message = ChatMessage(
#             session_id=chat_session.id,
#             role="assistant",
#             content=rag_response_data['response'],
#             # sources_json=rag_response_data.get('sources'), # If you decide to store sources
#             # token_usage_json=rag_response_data.get('token_usage') # If storing token usage
#         )
#         db.session.add_all([user_message, assistant_message])
#         chat_session.updated_at = datetime.datetime.now(datetime.timezone.utc) # Update session timestamp
#         db.session.commit()

#         response_payload = {
#             "chat_session_id": chat_session.id,
#             "response": rag_response_data['response'],
#             "sources": rag_response_data.get('sources'),
#             "token_usage": rag_response_data.get('token_usage')
#         }
#         if papers_triggered_for_processing_info: # Add this info even if some papers were ready
#             response_payload["processing_initiated_for"] = papers_triggered_for_processing_info
        
#         return jsonify(response_payload), 200

#     except Exception as e:
#         current_app.logger.error(f"Error in RAG chat: {e}", exc_info=True)
#         return jsonify({"msg": "An error occurred during chat.", "error": str(e)}), 500



@rag_bp.route('/sessions', methods=['GET'])
@jwt_required()
def list_chat_sessions():
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 401

    sessions = ChatSession.query.filter_by(user_id=user.id).order_by(ChatSession.updated_at.desc()).all()
    
    return jsonify([{
        "id": session.id,
        "session_name": session.session_name,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat(),
        "paper_ids_in_session": [p.id for p in session.papers_in_session] # DB IDs
    } for session in sessions]), 200


@rag_bp.route('/sessions/<int:session_id>/messages', methods=['GET'])
@jwt_required()
def get_chat_session_messages(session_id):
    current_user_id = int(get_jwt_identity())
    chat_session = db.session.get(ChatSession, session_id)

    if not chat_session or chat_session.user_id != current_user_id:
        return jsonify({"msg": "Chat session not found or access denied."}), 403 # Or 404

    messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
    
    # Get associated paper titles for this session
    paper_titles = [p.title for p in chat_session.papers_in_session]

    return jsonify({
        "session_id": chat_session.id,
        "session_name": chat_session.session_name,
        "associated_paper_titles": paper_titles,
        "messages": [msg.to_dict() for msg in messages]
    }), 200