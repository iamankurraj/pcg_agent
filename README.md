# 🧠 AI-Driven Asset Discovery Agent (LLM-PCG)

An intelligent agent system that analyzes Unreal Engine asset requirements, searches both local project files and the web, ranks candidate assets semantically, and returns structured recommendations.

This project is part of a larger AI-powered Procedural Content Generation (PCG) system focused on intelligent asset selection and environment optimization.

---

# 🚀 How to Run the Project

## 1. Clone the Repository

git clone https://github.com/yourusername/llm-pcg.git  
cd llm-pcg  

## 2. Create a Virtual Environment

### Windows

python -m venv venv  
venv\Scripts\activate  

### Linux / macOS

python3 -m venv venv  
source venv/bin/activate  

## 3. Install Dependencies

pip install -r requirements.txt  

If requirements.txt does not exist yet:

pip freeze > requirements.txt  

## 4. Set Environment Variables

Create a `.env` file in the project root:

OPENAI_API_KEY=your_openai_api_key_here  

Make sure your `.gitignore` contains:

.env  
venv/  
__pycache__/  

Never commit your API key.

## 5. Run the FastAPI Server

uvicorn app.main:app --reload  

Server will run at:

http://127.0.0.1:8000  

## 6. Test the API

Open in your browser:

http://127.0.0.1:8000/docs  

Use the `/search` endpoint.

Example request body:

{
  "query": "medieval brick wall for Unreal Engine 5"
}

---

# 📌 What This Project Does

This system acts as an AI Asset Planning and Discovery Agent.

Given a user query, it:

1. Cleans and interprets the request using an LLM  
2. Determines asset type (StaticMesh, Texture, Material, FullPack)  
3. Chooses search priority (local-first or web-first)  
4. Searches local Unreal project files  
5. Searches the web for relevant assets  
6. Scores and ranks candidates  
7. Returns structured JSON output  

---

# 🏗 Architecture Overview

User Query  
↓  
Intent Analyzer (LLM)  
↓  
Asset Type Classification  
↓  
Search Decision Layer  
↓  
Local Asset Scanner + Web Search Agent  
↓  
Scoring & Ranking Engine  
↓  
Final Recommendation  

---

# 🧩 Core Components

## Decision Agent (decision_agent.py)

Uses OpenAI to:

- Clean user query  
- Extract asset type  
- Determine search priority  
- Generate search keywords  

Example output:

{
  "cleaned_query": "medieval brick wall",
  "asset_type": "StaticMesh",
  "priority": "web_first",
  "keywords": ["medieval", "brick", "wall"]
}

---

## Local Asset Scanner

- Scans Unreal project directories  
- Extracts `.uasset` files  
- Maps filesystem path  
- Maps Unreal path (/Game/...)  
- Scores based on relevance  

---

## Web Search Layer

- Queries search APIs  
- Retrieves asset candidates  
- Extracts metadata  
- Ranks based on semantic match  

---

## Scoring Engine

Assets are scored using:

- Semantic similarity  
- Keyword match  
- Asset type match  
- Source priority  
- Quality indicators (extensible)  

Scores are normalized to ensure fair comparison between local and web results.

---

# 📦 Example Output

{
  "analysis": {
    "cleaned_query": "medieval brick wall",
    "asset_type": "StaticMesh",
    "priority": "web_first"
  },
  "best_source": "local",
  "decision_reason": "High semantic similarity found locally",
  "final_results": [
    {
      "name": "SM_Wall_01.uasset",
      "type": "StaticMesh",
      "unreal_path": "/Game/Meshes/Walls_Columns/SM_Wall_01",
      "score": 0.87
    }
  ]
}

---

# 🎯 Project Goals

- Intelligent asset discovery  
- Semantic matching instead of keyword-only search  
- Unified scoring for local and web assets  
- Modular agent-based architecture  
- Foundation for AI-driven PCG workflows  

---

# 🔮 Future Improvements

- Embedding-based similarity scoring (FAISS / sentence-transformers)  
- CLIP-based texture similarity  
- Automatic Unreal asset import  
- Multi-agent planning using LangGraph  
- License validation system  
- UI dashboard  

---

# 🛠 Tech Stack

- Python  
- FastAPI  
- LangGraph  
- OpenAI API  
- Uvicorn  
- Dotenv  

---
