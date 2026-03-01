# LLM-PCG: Asset Search & Pipeline System

A sophisticated asset discovery system that combines local asset searching with intelligent web search, powered by LangGraph and OpenAI. Designed to find Unreal Engine assets based on natural language queries.

## 📋 Overview

This system uses a multi-agent workflow to:
1. **Analyze intent** from user queries (extract cleaned query, keywords, asset type)
2. **Determine license preferences** (free_only, any, paid_only)
3. **Decide search strategy** (local_first vs web_first)
4. **Execute searches** across local filesystem and web
5. **Rank results** using LLM-powered relevance scoring

## 🏗️ Architecture

### Agents (`agents/`)
- **`decision_agent.py`** - Parses user messages into structured search parameters
- **`license_agent.py`** - Determines license preferences from query intent
- **`strategy_agent.py`** - Decides whether to prioritize local or web search
- **`ranking_agent.py`** - Ranks combined results using LLM scoring
- **`search_nodes.py`** - Executes local and web searches
- **`graph.py`** - Orchestrates the workflow using LangGraph
- **`state.py`** - Defines the shared state structure

### Asset Pipeline (`asset_pipeline/`)
- **`local_search.py`** - Searches local filesystem with keyword matching and asset type detection
- **`web_search.py`** - Web searches using Tavily API with domain filtering and license preference
- **`models.py`** - Data models
- **`indexer.py`** - Asset indexing utilities
- **`downloader.py`** - Asset download utilities

### Application (`app/`)
- **`main.py`** - FastAPI server exposing `/search` endpoint

## ⚙️ Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Tavily API key (for web search)

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
SERP_API_KEY=your_serp_api_key
```

4. Update asset root path in `config.py`:
```python
ASSET_ROOT = r"C:\path\to\your\unreal\assets"
```

## 🚀 Usage

### API Endpoint

Start the server:
```bash
uvicorn app.main:app --reload
```

Search for assets:
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"message": "Find a free pine tree static mesh"}'
```

Example response:
```json
{
  "analysis": {
    "cleaned_query": "free pine tree static mesh",
    "asset_type": "StaticMesh",
    "license_preference": "free_only",
    "priority": "local_first"
  },
  "best_source": "mixed",
  "decision_reason": "Results ranked by LLM relevance scoring.",
  "final_results": []
}
```

### Testing

Run tests:
```bash
python test_search.py
```

## 🔄 Workflow Flow

```
intent (analyze_request)
  ↓
license (analyze_license)
  ↓
strategy (analyze_strategy)
  ↓
local_search (local_search_node)
  ↓
[Conditional: local_first + has results?]
  ├─ Yes → ranking
  └─ No → web_search
  ↓
web_search (web_search_node)
  ↓
ranking (rank_results)
  ↓
END
```

## ⚡ Configuration

### Asset Detection (`config.py`)
- **`ASSET_ROOT`** - Path to your Unreal Engine assets directory
- **`ALLOWED_EXTENSIONS`** - File types to index (.uasset, .fbx, .png, etc.)

### Search Behavior (`agents/search_nodes.py`)
- **`ALLOWED_DOMAINS`** - Restrict web searches to specific domains

### Local Search Tuning (`asset_pipeline/local_search.py`)
- **`MESH_ONLY`** - Set to `True` to only return static meshes
- Keyword filtering removes common weak terms

## ✨ Key Features

✅ **Multi-source search** - Combines local assets with web results  
✅ **Smart filtering** - License preference-aware results  
✅ **LLM ranking** - Relevance scoring llm 
✅ **Domain restriction** - Web search constrained to trusted sources  
✅ **Asset type detection** - Automatically categorizes StaticMesh, Material, Texture  
✅ **Unreal path conversion** - Generates valid Unreal Engine import paths  

## 📦 Dependencies

See `requirements.txt` for complete list:
- `fastapi` - Web framework
- `langgraph` - Agentic workflows
- `python-dotenv` - Environment config
- `tavily-python` - Web search API
- `openai` - LLM integration

## 🔮 Future Enhancements

- [ ] Semantic search using embeddings
- [ ] Asset caching/indexing with vector DB
- [ ] Download and import automation
- [ ] Batch search support
- [ ] User feedback loop for ranking optimization
