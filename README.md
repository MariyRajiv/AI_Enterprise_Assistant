# AI Enterprise Assistant using RAG & Agentic Workflows

An enterprise-grade, full-stack AI application that allows users to securely query internal documents using Retrieval-Augmented Generation (RAG) and automate reasoning tasks using LangGraph agents. 

This system dynamically routes questions to specialized Vector databases based on the domain (e.g., University vs Company documents).

---

## 🛠️ Tech Stack
*   **Backend**: Python, FastAPI
*   **Frontend**: React, Vite, TailwindCSS
*   **Vector DB**: ChromaDB
*   **LLM & Embeddings**: Ollama (Mistral) & HuggingFace (`all-MiniLM-L6-v2`)
*   **Database**: MongoDB (Chat History)
*   **Agent Framework**: LangGraph

---

## 📂 1. How to Upload Data

The system uses a Domain-Driven data ingestion pipeline. To upload your own custom data:
1. Navigate to the `data/` folder in the root directory.
2. You will see three domains:
   - `data/university/`: Put admissions, syllabus, or placement PDFs here.
   - `data/company/`: Put company HR policies or overviews (PDF/CSV/TXT) here.
   - `data/custom/`: Put general FAQs here.
3. Simply drop your files into the appropriate folder. The ingestion script will automatically tag them with the correct metadata domain when you run it!

---

## ⚙️ 2. Local Setup & Installation

### Prerequisites
1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Install [Node.js](https://nodejs.org/en/).
3. Install [MongoDB](https://www.mongodb.com/try/download/community) locally and ensure it's running on port `27017`.
4. Install [Ollama](https://ollama.com/) and pull the Mistral model:
   ```bash
   ollama pull mistral
   ```

### Backend Setup
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On Mac/Linux
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the data ingestion script to read your PDFs and build the Vector Database:
   ```bash
   python -m app.rag.ingestion
   ```
   *(Note: Make sure your virtual environment is activated when you run this!)*

### Frontend Setup
1. Open a **new** terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```

---

## 🚀 3. How to Run Locally

You need two terminals running simultaneously.

**Terminal 1 (Backend - FastAPI)**
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
*The backend will be live at `http://localhost:8000`*

**Terminal 2 (Frontend - React)**
```bash
cd frontend
npm run dev
```
*The frontend UI will be live at `http://localhost:5173`*

---

## ☁️ 4. How to Deploy (Render & Vercel)

### Deploying the Backend to Render.com
1. Create a `render.yaml` file or use the Render Dashboard.
2. Select **Web Service** and connect your GitHub repository.
3. Configure the following settings for the backend service:
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add Environment Variables in Render:
   - `MONGO_URL` = `mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/` (You'll need to use MongoDB Atlas for production).
   - `OLLAMA_API_BASE` = If you deploy Ollama separately, point to it here. Otherwise, you may need to use an external API (like OpenAI) for production if hosting Ollama on Render is too resource-heavy.
5. Click **Deploy**. Render will give you a public URL (e.g., `https://enterprise-assistant-api.onrender.com`).

### Deploying the Frontend to Vercel
1. Go to [Vercel](https://vercel.com/) and connect your GitHub repo.
2. Import the project and configure the settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`
3. Before deploying, update the `API_BASE_URL` inside `frontend/src/services/api.js` to point to your new Render URL:
   ```javascript
   const API_BASE_URL = 'https://enterprise-assistant-api.onrender.com/api/v1';
   ```
4. Click **Deploy**. Vercel will build your UI and provide you with a live URL.

---

## 🎯 Architecture Highlights
* **LangGraph Classification**: Dynamically routes user queries to the most relevant subset of data, preventing cross-domain hallucinations.
* **Voice Chat**: Native browser integrations for Speech-to-Text input and Text-to-Speech output.
* **Metadata Filtering**: ChromaDB enforces strict domain-based vector searches.
