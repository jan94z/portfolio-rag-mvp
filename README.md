# Retrieval Augmented Generation Portfolio Project
**Status**: *Work in progress* \
[Project Kanban Board](https://github.com/users/jan94z/projects/4)

Portfolio RAG MVP is a full-stack GenAI application that showcases a modern Retrieval-Augmented Generation pipeline. It allows users to ask questions about Jan (the project author) and get answers grounded in a private document knowledge base. The app demonstrates a production-oriented design with a FastAPI backend, vector database, Streamlit frontend, authentication, and infrastructure-as-code deployment.

## Features
* LLM Q&A Chatbot: Utilizes OpenAI GPT-3.5/4 to answer user questions about Jan, augmented with retrieval of relevant info from documents (Resume, projects, etc.).
* Document Vector Search: Integrates Qdrant (vector DB) to store and retrieve document embeddings for context. Uses a sentence-transformer model to embed text.
* FastAPI REST API: Provides endpoints for login, user info, and RAG query (/api/v1/rag) with JWT-based auth and rate limiting (to prevent abuse).
* Streamlit Web UI: Offers an interactive chat interface with login page and admin controls. Non-admin users are limited to pre-set model parameters, while admin can tweak setting(temperature, max tokens, etc.) in real-time.
* Authentication & Usage Limits: Implements secure JWT authentication and per-user usage quotas (e.g., limit of 10 queries per minute, configurable). Admin users have higher limits and a special role.
* DevOps & MLOps: Containerized with Docker & ready for Kubernetes. Includes Terraform scripts to deploy cloud infrastructure (Virtual Machine, Networking) on DigitalOcean. CI pipeline (GitHub Actions) lint-checks code, Docker, and IaC for quality.
* Monitoring Ready: (Planned) Setup for basic monitoring/logging with Prometheus & Grafana. (Note: This is a future goal – currently using DigitalOcean’s monitoring as placeholder.)

## Architecture
This project follows a modular, scalable architecture:
* Frontend: Streamlit app (Python) running in Docker, served on port 8501. It handles user interaction (login form and chat UI) and communicates with the backend via internal API calls.
* Backend: FastAPI app (Python) running in Docker (Uvicorn server on port 8000). Provides JSON endpoints under /api/v1/…:
  * POST /api/v1/login – Authenticate user and return JWT token.
  * GET /api/v1/me – Get current user profile (requires JWT).
  * POST /api/v1/rag – Main endpoint to answer a question using RAG.
* LLM Retrieval Workflow: When a user asks a question, the backend:
  * Embeds the Query – using a local HuggingFace model (all-MiniLM-L6-v2).
  * Vector Search – finds relevant text chunks via Qdrant (vector DB).
  * Assembles Prompt – combines the retrieved text with a pre-defined system prompt (instructions about Jan’s profile) and the user’s question.
  * Calls OpenAI API – (GPT-3.5-Turbo or GPT-4) to get a completion answering the question based on the provided context.
  * Responds – returns the answer (and updates the user’s usage count in the database).
* Data Storage:
  * PostgreSQL stores user accounts, hashed passwords, and a log of questions/answers (for auditing usage).
  * Qdrant stores vectors for each document chunk, enabling semantic search for relevant context.
* Infrastructure: Everything runs in containers. For local development, Docker Compose can spin up the whole stack. For cloud, Terraform provisions a VM and restricts ports via a firewall.

## Tech Stack
* Language & ML: Python 3.10/3.11, OpenAI GPT-3.5/GPT-4/GPT-4.1 API, HuggingFace SentenceTransformers.
* Backend: FastAPI (REST framework), SQLAlchemy (database ORM), Pydantic (data models), PyJWT via Python-JOSE (JWT auth), SlowAPI (rate limiting).
* Database: PostgreSQL (relational DB for user data and logs), Qdrant (vector similarity search engine).
* DevOps: Docker & Docker Compose for containerization, Terraform (Infrastructure as Code for DigitalOcean cloud resources), GitHub Actions (CI for linting and validation).
* Frontend: Streamlit for UI (quick deployment of a data app interface), Requests/HTTP for API calls.
* Misc: bcrypt (password hashing), passlib, httpx, etc. (see requirements.txt for full list).

## Project Background and Goals
This project was created by Jan Zimmermann as a portfolio piece to demonstrate skills in:
* Backend Engineering: Building a robust API with authentication, database integration, and external service integration (LLM API).
* Machine Learning Engineering: Implementing an NLP pipeline (document parsing, chunking, vectorization, prompt engineering, model inference) and handling LLM interactions responsibly.
* DevOps/Cloud: Containerizing applications, writing Infrastructure-as-Code, and considering deployment security and scalability.
* Full-Stack Integration: Creating a usable interface and tying together the frontend and backend seamlessly.

The emphasis is on a production-like design for a GenAI application, showing understanding of not just coding the happy path, but also configuration, security, and scalability considerations.

## Contributing
As this is a personal portfolio project, external contributions may not be expected. However, feedback or suggestions are welcome! Feel free to open an issue or pull request on GitHub if you have ideas to improve the project. 🤝
