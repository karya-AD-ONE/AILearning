# 🔍 Project 1: Salesforce RAG System

## What We're Building

A complete RAG (Retrieval Augmented Generation) system that:
1. Stores Salesforce knowledge articles in a vector database
2. Searches semantically (by meaning, not just keywords)
3. Answers questions using retrieved context + Claude
4. Can be integrated into your existing API server

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Knowledge Base  │────▶│    ChromaDB      │────▶│   RAG Query      │
│  (Documents)     │     │  (Vector Store)  │     │   + Claude       │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                         │                        │
   Index once              Semantic search           Generate answer
                           (embeddings)              with context
```

## Setup

### Step 1: Install Dependencies
```bash
cd /Users/arshdave/Documents/VS\ Code\ Workspace/GitRepoCloned/AILearning/AILearning
source venv/bin/activate
pip install chromadb sentence-transformers anthropic
```

### Step 2: Set API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Step 3: Run the RAG System
```bash
cd projects/01-salesforce-rag
python3 rag_system.py
```

## Files

| File | Description |
|------|-------------|
| `rag_system.py` | Complete RAG implementation |
| `knowledge_base.json` | Sample Salesforce knowledge articles |
| `test_rag.py` | Test queries to verify it works |

## How It Works

1. **Index Phase** (run once):
   - Load documents from knowledge base
   - Chunk into smaller pieces
   - Create embeddings (convert text to vectors)
   - Store in ChromaDB

2. **Query Phase** (every question):
   - Convert question to embedding
   - Find similar documents in ChromaDB
   - Build prompt with retrieved context
   - Send to Claude for answer

## Integration with Your API Server

After testing, add to your `index.js`:
```javascript
// Add RAG endpoint
app.post('/api/rag/query', async (req, res) => {
    // Call your Python RAG service
    // Or port the logic to JavaScript
});
```

## Next Steps

After completing this project:
1. ✅ Test with sample queries
2. Add real Salesforce Knowledge Articles
3. Integrate into your Express API
4. Add to your LWC chat interface
