# RAG Chatbot - FinSolve Technologies

A comprehensive Retrieval-Augmented Generation (RAG) chatbot system built with LangChain, LangGraph, FastAPI, and Streamlit. This enterprise-grade solution provides role-based access control and domain-specific knowledge retrieval for different organizational departments.

![Chat UI](docs/chat-ui.png)

![Chat UI](docs/user-flow.png)

## 🔒 Data Privacy & Security

In traditional RAG systems, users can potentially craft malicious prompts to access sensitive information across organizational silos, bypassing intended data boundaries. This poses significant security risks where employees might gain unauthorized access to confidential documents from other departments through clever prompt engineering.

**Our Solution**: This system implements **role-based retrieval and response generation** at the vector database level, ensuring that users can only access documents relevant to their organizational role. The retrieval mechanism filters documents based on user permissions before any LLM processing occurs, preventing data leakage through prompt manipulation.

## 🚀 Features

- **Role-Based Access Control**: Different access levels for various departments (Engineering, Marketing, Finance, HR, C-Level)
- **RAG Architecture**: Combines retrieval and generation for accurate, context-aware responses
- **Vector Database**: ChromaDB for efficient document storage and retrieval
- **Modern UI**: Streamlit-based frontend with authentication
- **FastAPI Backend**: RESTful API with HTTP Basic Authentication

## 🏗️ Architecture

The project consists of three main components:

### 1. Backend (`/backend`)

- **FastAPI** server with authentication and chat endpoints
- **LangGraph** agents for conversation flow management
- **ChromaDB** vector store for document retrieval
- Role-based access control system

### 2. Frontend (`/frontend`)

- **Streamlit** web interface
- User authentication and session management
- Real-time chat interface

### 3. Training (`/training`)

- Data processing and vector store creation
- Jupyter notebooks for experimentation
- Document ingestion pipeline

## 📋 Prerequisites

- Python 3.12+
- UV package manager (recommended) or pip
- Google Gemini API key (for LLM integration)

## 🛠️ Installation

### 1. Clone the Repository

```bash
mkdir RAG-chatbot
git clone https://github.com/shashanksrajak/RBAC-RAG-chatbot.git .
cd RAG-chatbot
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 3. Install Dependencies

#### Using UV (Recommended)

```bash
# Backend
cd backend
uv sync

# Frontend
cd ../frontend
uv sync

# Training (optional)
cd ../training
uv sync
```

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
cd backend
uv run src/main.py
```

The backend will be available at `http://localhost:6001`

### 2. Launch the Frontend

```bash
cd frontend
uv run streamlit run main.py
```

The frontend will be available at `http://localhost:8501`

### 3. Login with Demo Credentials

Use any of these demo accounts:

| Username | Password    | Role        | Access Level        |
| -------- | ----------- | ----------- | ------------------- |
| Tony     | password123 | Engineering | Technical documents |
| Bruce    | securepass  | Marketing   | Marketing reports   |
| Sam      | financepass | Finance     | Financial data      |
| Natasha  | hrpass123   | HR          | HR policies         |
| Shashank | password123 | C-Level     | All documents       |

## 📁 Project Structure

```
RAG-chatbot/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── agents/            # LangGraph agents
│   │   │   ├── graph.py       # Agent workflow
│   │   │   ├── nodes.py       # Processing nodes
│   │   │   ├── prompts.py     # LLM prompts
│   │   │   └── states.py      # State management
│   │   ├── services/          # Business logic
│   │   │   └── chatbot.py     # Chatbot service
│   │   └── main.py            # FastAPI application
│   └── pyproject.toml
├── frontend/                   # Streamlit frontend
│   ├── main.py                # Streamlit app
│   └── pyproject.toml
├── training/                   # Data processing
│   ├── data/                  # Source documents
│   │   ├── engineering/       # Technical docs
│   │   ├── finance/          # Financial reports
│   │   ├── general/          # General policies
│   │   ├── hr/               # HR documents
│   │   └── marketing/        # Marketing materials
│   ├── chatbot_agent.ipynb   # Training notebook
│   └── RAG_intro.ipynb       # RAG introduction
└── docs/                      # Documentation
```

## 🔧 API Endpoints

### Authentication

- `GET /login` - Authenticate user and get role information
- `GET /test` - Test authenticated access

### Chat

- `POST /chat` - Send message to chatbot (requires authentication)
  - Parameters: `message` (string)
  - Returns: AI response based on user's role and access level

### Health Check

- `GET /` - Server status check

## 🧠 AI Components

### LangChain Integration

- **Google Gemini**: Primary LLM for response generation
- **ChromaDB**: Vector database for document storage
- **Text Splitters**: Intelligent document chunking
- **Retrieval Chain**: Semantic search and context retrieval

### LangGraph Workflow

- **Retrieve Node**: Fetches relevant documents based on query and access level
- **Generate Node**: Creates contextual responses using retrieved information
- **State Management**: Maintains conversation context and user permissions

## 📊 Supported Document Types

- Markdown (.md)
- CSV (.csv)
- More formats can be added by extending the document loaders

## 🎯 Use Cases

- **Internal Knowledge Base**: Company-wide information retrieval
- **Department-Specific Queries**: Role-based information access
- **Document Q&A**: Natural language queries over company documents
- **Compliance and Policy**: Easy access to HR and legal documents
- **Technical Support**: Engineering documentation assistance

---

**Note**: This is a demonstration project with hardcoded credentials. For production use, implement proper authentication and authorization mechanisms.
