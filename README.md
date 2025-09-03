# Lexify
**AI Research Assistant**

An AI-powered research assistant that helps users discover, analyze, and interact with academic papers through intelligent search, summarization, and conversational AI using RAG (Retrieval-Augmented Generation) technology.

![Lexify Research Assistant](https://img.shields.io/badge/Vue.js-3.x-green) ![Flask](https://img.shields.io/badge/Flask-2.x-blue) ![Python](https://img.shields.io/badge/Python-3.9+-yellow) ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue) ![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-purple) ![LiteLLM](https://img.shields.io/badge/LiteLLM-Multi_Provider-orange)

*Empowering researchers with AI-driven paper analysis and intelligent conversation*

## 🎯 What It Does

Lexify transforms academic research by allowing users to:
1. **Search & Discover** papers from ArXiv with AI-generated summaries
2. **Select & Process** papers for interactive analysis
3. **Chat & Analyze** with multiple papers simultaneously using conversational AI
4. **Save & Resume** research sessions across multiple visits

## 🎥 Demo Video

See Lexify in action! Watch the comprehensive demo showcasing the complete research workflow:

https://github.com/user-attachments/assets/4df35784-6bc4-4c83-beb4-1f24867e8fd4

*The demo covers: paper search, AI summarization, paper selection, background processing, and interactive chat with citations.*

## 🔄 Research Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Search    │    │  Summarize  │    │   Select    │    │    Chat     │
│   Papers    │───►│   & Review  │───►│   Papers    │───►│  with AI    │
│             │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
 ArXiv Search       AI Summarization    Background Processing    RAG Chat
```

### User Journey
1. **Login/Register** → Secure access to personal research space
2. **Enter Research Query** → System searches ArXiv and generates summaries
3. **Review Papers** → Browse individual summaries and consolidated insights
4. **Select Papers** → Choose papers for interactive chat (auto-processed in background)
5. **Ask Questions** → Get contextual answers with precise citations
6. **Save Sessions** → See conversations histories anytime

## ⚡ Key Features

### 🔍 Smart Research Discovery
- **ArXiv Integration** with real-time search
- **AI Summarization** of individual papers and consolidated insights
- **Automatic Processing** of PDFs in background for instant chat readiness

### 💬 Conversational Analysis
- **Multi-Paper Chat** - Ask questions across multiple selected papers
- **Contextual Responses** - Answers grounded in actual paper content
- **Source Citations** - Every response includes clickable references

### 🧠 RAG-Powered Intelligence
- **Semantic Search** through paper content using vector embeddings
- **Context-Aware Retrieval** for relevant information
- **Citation Tracking** with inline paper references

## 🏗️ Architecture

```
Frontend (Vue 3 + TypeScript)           Backend (Flask + Python)              External Services
┌─────────────────────┐                ┌─────────────────────┐               ┌─────────────────┐
│ • Research Interface │◄──────────────►│ • REST API          │◄─────────────►│ • ArXiv API     │
│ • Chat Interface     │                │ • RAG Pipeline      │               │ • LiteLLM       │
│ • User Management    │                │ • Background Tasks  │               │ • Qdrant Cloud  │
│ • Session History    │                │ • Authentication    │               │ • Gemini API    │
└─────────────────────┘                └─────────────────────┘               └─────────────────┘
```

## 🛠️ Tech Stack

**Frontend**: Vue 3, TypeScript, Tailwind CSS, Pinia, Vue Router  
**Backend**: Flask, SQLAlchemy, JWT Authentication, Threading  
**AI/ML**: LiteLLM (Gemini/OpenAI), Qdrant Vector DB, PyMuPDF  
**Database**: PostgreSQL/MySQL/SQLite support

## 📦 Quick Start

### Prerequisites
- Python 3.9+, Node.js 16+
- Qdrant Cloud account
- LiteLLM API keys (Gemini/OpenAI)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure .env file
cp .env.example .env  # Edit with your API keys

# Initialize database
flask db init && flask db migrate && flask db upgrade

# Start server
python run.py  # Runs on http://localhost:5000
```

### Frontend Setup
```bash
cd frontend
npm install

# Configure environment
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env.local

# Start development server
npm run dev  # Runs on http://localhost:5173
```

## 📁 Project Structure

```
lexify_research_assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Flask app factory
│   │   ├── config.py             # Configuration classes
│   │   ├── extensions.py         # Flask extensions
│   │   ├── api/                  # API Blueprint modules
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── papers.py        # Paper search & processing
│   │   │   └── rag.py           # RAG chat endpoints
│   │   ├── models/               # Database models
│   │   │   ├── user.py          # User model
│   │   │   ├── paper.py         # Paper metadata model
│   │   │   └── chat.py          # Chat session models
│   │   ├── core/                 # Business logic services
│   │   │   ├── arxiv_service.py # ArXiv integration
│   │   │   ├── download_service.py # PDF downloading
│   │   │   ├── processing_service.py # Text processing
│   │   │   ├── summarizer_service.py # Summarization
│   │   │   └── rag_service.py   # RAG pipeline
│   │   ├── utils/                # Utility modules
│   │   │   ├── retriever/       # Paper retrieval
│   │   │   ├── processor/       # Text processing
│   │   │   ├── summarizer/      # Summarization
│   │   │   └── rag/             # RAG components
│   │   └── services/             # External services
│   │       ├── qdrant_client_setup.py
│   │       ├── litellm_service.py
│   │       └── embedding_service.py
│   ├── prompts/                  # LLM prompt templates
│   ├── data/papers/              # Downloaded PDFs
│   ├── logs/                     # Application logs
│   ├── migrations/               # Database migrations
│   ├── requirements.txt          # Python dependencies
│   ├── run.py                    # Application entry point
│   └── .env                      # Environment variables
|
├── frontend/
│   ├── src/
│   │   ├── components/           # Vue components
│   │   │   ├── chat/            # Chat interface
│   │   │   ├── paper/           # Paper components
│   │   │   └── layout/          # Layout components
│   │   ├── views/                # Page components
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── ResearchView.vue
│   │   │   └── ChatHistoryView.vue
│   │   ├── services/             # API service layer
│   │   │   ├── api.ts           # Base API configuration
│   │   │   ├── authService.ts   # Authentication
│   │   │   ├── paperService.ts  # Paper operations
│   │   │   └── ragService.ts    # RAG operations
│   │   ├── store/                # Pinia stores
│   │   │   └── authStore.ts     # Authentication state
│   │   ├── types/                # TypeScript definitions
│   │   │   └── index.ts         # Type definitions
│   │   ├── router/               # Vue Router
│   │   │   └── index.ts         # Route configuration
│   │   ├── App.vue               # Root component
│   │   └── main.ts               # Application entry
│   ├── package.json              # Dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── tailwind.config.js        # Tailwind CSS config
│   └── .env.local                # Environment variables
└── README.md
```

## 🛡️ API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - User registration
- `POST /login` - User login  
- `POST /logout` - User logout
- `GET /protected` - Protected route example

### Papers (`/api/papers`)
- `POST /search` - Search and summarize papers
- `GET /<id>/status` - Get paper processing status
- `POST /<id>/process-manual` - Manual processing trigger

### RAG & Chat (`/api/rag`)
- `POST /chat` - Send chat message with selected papers
- `GET /sessions` - List user's chat sessions
- `GET /sessions/<id>/messages` - Get session messages


## 🌟 Example Usage

1. **Search**: "machine learning interpretability"
2. **Review**: Browse AI-generated summaries of relevant papers
3. **Select**: Choose 3-5 papers for detailed analysis
4. **Chat**: "How do these papers approach model explainability?"
5. **Get Response**: Contextual answer with citations from selected papers

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes with proper TypeScript/Python typing
4. Test thoroughly (backend and frontend)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## 📄 License

MIT License - Built with ❤️ for the research community

---

**Transform your research workflow with AI-powered paper analysis and intelligent conversation**
