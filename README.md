# Lexify Research Assistant

An AI-powered research assistant that helps users discover, analyze, and interact with academic papers through intelligent search, summarization, and conversational AI using advanced RAG (Retrieval-Augmented Generation) technology.

![Lexify Research Assistant](https://img.shields.io/badge/Vue.js-3.x-green) ![Flask](https://img.shields.io/badge/Flask-2.x-blue) ![Python](https://img.shields.io/badge/Python-3.9+-yellow) ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue) ![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-purple) ![LiteLLM](https://img.shields.io/badge/LiteLLM-Multi_Provider-orange)

## 🚀 Features

### 📊 Research Discovery
- **ArXiv Integration**: Direct search and retrieval from ArXiv academic papers
- **Smart Summarization**: AI-generated individual paper summaries and consolidated insights
- **Advanced Filtering**: Filter by publication date, categories, and relevance
- **Automatic Processing**: Background PDF download, text extraction, and vector indexing

### 💬 Intelligent Chat Interface
- **Conversational RAG**: Ask questions about selected research papers using context-aware AI
- **Multi-Paper Analysis**: Chat with multiple papers simultaneously for comparative analysis
- **Source Citations**: Every response includes precise references to source materials
- **Session Management**: Persistent chat sessions with full conversation history

### 🔍 RAG-Powered Analysis
- **Vector Search**: Semantic search through paper content using Qdrant embeddings
- **Context Retrieval**: Intelligent chunk selection based on query relevance
- **Citation Tracking**: Inline citations with clickable paper references
- **Real-time Processing**: Papers are processed asynchronously for immediate chat availability

### 👤 User Management
- **JWT Authentication**: Secure user registration and login system
- **Personal Library**: Organize and manage your research papers
- **Chat History**: Access and resume previous research conversations
- **Cross-Session Persistence**: Continue research across multiple sessions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Vue 3 + TS)  │    │   (Flask)       │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Vue Router    │    │ • REST API      │    │ • ArXiv API     │
│ • Pinia Store   │◄──►│ • SQLAlchemy    │◄──►│ • LiteLLM       │
│ • Tailwind CSS  │    │ • JWT Auth      │    │ • Qdrant Cloud  │
│ • TypeScript    │    │ • RAG Pipeline  │    │ • Gemini API    │
│ • Responsive UI │    │ • Async Tasks   │    │ • PDF Sources   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.x with modular Blueprint architecture
- **Database**: SQLAlchemy ORM with PostgreSQL/MySQL/SQLite support
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **AI Integration**: LiteLLM supporting multiple providers (Gemini, OpenAI, etc.)
- **Vector Database**: Qdrant Cloud for semantic search and embeddings
- **Document Processing**: PyMuPDF for PDF text extraction
- **Text Processing**: Advanced chunking and cleaning utilities
- **Async Processing**: Threading for background paper processing

### Frontend
- **Framework**: Vue 3 with Composition API and TypeScript
- **Styling**: Tailwind CSS with custom component design
- **State Management**: Pinia for reactive application state
- **Routing**: Vue Router 4 with authentication guards
- **HTTP Client**: Axios with interceptors for API communication
- **UI Components**: Custom responsive components with modern design
- **Build Tool**: Vite for fast development and optimized builds

### AI & Vector System
- **Vector Database**: Qdrant for high-performance semantic search
- **Embeddings**: Configurable embedding models via LiteLLM
- **LLM Integration**: Multi-provider support through LiteLLM
- **RAG Pipeline**: Custom context retrieval and response generation
- **Prompt Engineering**: Structured prompts for different use cases

## 📦 Installation

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Database** (PostgreSQL/MySQL recommended, SQLite for development)
- **Qdrant** (Cloud account or self-hosted instance)
- **LiteLLM API Keys** (Gemini, OpenAI, or other supported providers)

### Backend Setup

1. **Clone and Setup Environment**
```bash
git clone <repository-url>
cd lexify_research_assistant/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Environment Configuration**
Create `.env` file in backend directory:
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/lexify_db
# or for SQLite: sqlite:///instance/app.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# Qdrant Configuration
QDRANT_URL=https://your-qdrant-instance.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key

# LiteLLM Configuration  
LITELLM_MODEL_SUMMARIZE=gemini/gemini-2.0-flash
LITELLM_MODEL_CHAT=gemini/gemini-2.0-flash
EMBEDDING_MODEL_NAME=gemini/text-embedding-004

# API Keys (if using specific providers)
GOOGLE_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-key

# File Storage
PAPER_SAVE_DIR=data/papers
PROMPTS_DIR=prompts
```

3. **Flask Environment Setup**
Create `.flaskenv` file:
```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

4. **Database Initialization**
```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Create Required Directories**
```bash
mkdir -p data/papers logs
```

6. **Start Backend Server**
```bash
python run.py
# Server will run on http://localhost:5000
```

### Frontend Setup

1. **Navigate and Install**
```bash
cd ../frontend
npm install
```

2. **Environment Configuration**
Create `.env.local` file:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

3. **Start Development Server**
```bash
npm run dev
# Frontend will run on http://localhost:5173
```

## 🚀 Usage Guide

### 1. User Registration & Authentication
```typescript
// Register new account
POST /api/auth/register
{
  "username": "researcher",
  "email": "user@example.com", 
  "password": "securepassword"
}

// Login
POST /api/auth/login
{
  "username_or_email": "researcher",
  "password": "securepassword"
}
```

### 2. Research Workflow

**Step 1: Search Papers**
- Enter research query in the search interface
- System searches ArXiv and displays results
- Individual summaries and consolidated insights are generated
- Papers are automatically queued for processing

**Step 2: Review Results**
- Browse paper summaries with metadata
- Check processing status indicators
- Select papers for interactive chat

**Step 3: Interactive Chat**
- Start conversation with selected papers
- Ask questions about methodology, findings, implications
- Receive contextually grounded responses with citations
- Access chat history from previous sessions

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

## 🔧 Key Features Implementation

### RAG Pipeline
1. **Document Processing**: PDF text extraction and cleaning
2. **Chunking**: Intelligent text segmentation for context
3. **Embedding**: Vector representation using LiteLLM
4. **Indexing**: Storage in Qdrant with metadata
5. **Retrieval**: Context-aware chunk selection
6. **Generation**: LLM response with source citations

### Chat System
- **Session Management**: Persistent conversations
- **Context Awareness**: Multi-turn dialogue support
- **Source Tracking**: Citation mapping to original papers
- **Real-time Processing**: Background paper preparation

### User Experience
- **Responsive Design**: Mobile-friendly interface
- **Progress Indicators**: Processing status feedback
- **Error Handling**: Graceful error recovery
- **Performance**: Optimized loading and caching

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes with proper TypeScript/Python typing
4. Test thoroughly (backend and frontend)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the research community**

*Empowering researchers with AI-driven paper analysis and intelligent conversation*