"""
============================================================
MODULE 3: RAG SYSTEMS - RETRIEVAL AUGMENTED GENERATION
============================================================
Time: 90-120 minutes
Goal: Build a complete RAG system from scratch

RAG is THE most in-demand AI skill. This module teaches:
- What is RAG and why it matters
- Building a vector database
- Semantic search implementation
- Complete RAG pipeline

SETUP:
    pip install chromadb sentence-transformers anthropic langchain

============================================================
"""

import os
import json
from typing import List, Dict, Any

print("="*60)
print("🔍 RAG SYSTEMS: RETRIEVAL AUGMENTED GENERATION")
print("="*60)

# ============================================================
# PART 1: WHAT IS RAG AND WHY IT MATTERS
# ============================================================
print("""
┌─────────────────────────────────────────────────────────────┐
│                    WHAT IS RAG?                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RAG = Retrieval Augmented Generation                       │
│                                                             │
│  Problem: LLMs have knowledge cutoffs and can hallucinate  │
│  Solution: Give them relevant context BEFORE they answer   │
│                                                             │
│  ┌─────────────┐                                            │
│  │   Query     │ "What's our refund policy?"                │
│  └──────┬──────┘                                            │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │  RETRIEVE   │ Search knowledge base for relevant docs   │
│  └──────┬──────┘                                            │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │  AUGMENT    │ Add retrieved context to prompt           │
│  └──────┬──────┘                                            │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │  GENERATE   │ LLM answers using context                 │
│  └─────────────┘                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

WHY RAG IS CRITICAL:
✅ Reduces hallucination - LLM uses YOUR data
✅ Up-to-date information - Not limited by training cutoff
✅ Domain-specific - Your company's knowledge
✅ Cost-effective - No need to fine-tune
✅ Auditable - You can see what sources were used

REAL WORLD EXAMPLES:
• Customer support chatbots
• Internal knowledge bases
• Document Q&A systems
• Code documentation search
• Legal document analysis
""")


# ============================================================
# PART 2: THE RAG PIPELINE
# ============================================================
print("\n" + "="*60)
print("📊 PART 2: THE COMPLETE RAG PIPELINE")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INDEXING PHASE (Done once, updated periodically)          │
│  ─────────────────────────────────────────────             │
│                                                             │
│  Documents → Chunking → Embedding → Vector DB              │
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │  PDF    │    │ Chunk 1 │    │ [0.2,   │    │ ChromaDB│  │
│  │  Word   │───▶│ Chunk 2 │───▶│  0.8,   │───▶│ Pinecone│  │
│  │  HTML   │    │ Chunk 3 │    │  ...]   │    │ Weaviate│  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                                             │
│  QUERY PHASE (Every user question)                         │
│  ───────────────────────────────                           │
│                                                             │
│  Query → Embed → Search → Retrieve → Augment → Generate   │
│                                                             │
│  "What's the                ┌──────────────────────────┐   │
│   refund     ───▶ [0.3,    │  Top 3 relevant chunks:  │   │
│   policy?"        0.7,...] │  1. Refund policy doc    │   │
│                    │        │  2. Return guidelines    │   │
│                    ▼        │  3. Customer FAQ         │   │
│              Vector Search  └──────────────────────────┘   │
│                                        │                    │
│                                        ▼                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PROMPT TO LLM:                                      │  │
│  │  "Using this context: [retrieved chunks]            │  │
│  │   Answer: What's the refund policy?"                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# PART 3: BUILDING A RAG SYSTEM - STEP BY STEP
# ============================================================
print("\n" + "="*60)
print("🛠️ PART 3: BUILD YOUR RAG SYSTEM")
print("="*60)

# Step 1: Sample Documents (Salesforce Knowledge Base)
documents = [
    {
        "id": "doc1",
        "title": "Lead Conversion Process",
        "content": """
        To convert a lead in Salesforce:
        1. Open the Lead record you want to convert
        2. Click the 'Convert' button in the top right
        3. Select an existing Account or create a new one
        4. Choose to create an Opportunity or not
        5. Select the Contact record options
        6. Click 'Convert'
        
        Important: Once converted, the Lead record is no longer accessible.
        All activities are moved to the Contact. The converted Lead status
        is updated to show the conversion date and resulting records.
        """
    },
    {
        "id": "doc2", 
        "title": "Creating Custom Objects",
        "content": """
        To create a custom object in Salesforce:
        1. Go to Setup > Object Manager > Create > Custom Object
        2. Enter the Object Label and Plural Label
        3. The Object Name will auto-populate
        4. Configure the record name format
        5. Select optional features like Reports, Activities, Tracking
        6. Choose deployment status (In Development/Deployed)
        7. Click Save
        
        Best practices: Use clear naming conventions, add help text,
        and consider relationships with standard objects.
        """
    },
    {
        "id": "doc3",
        "title": "Apex Trigger Best Practices",
        "content": """
        Apex Trigger Best Practices:
        1. One trigger per object - use handler classes
        2. Bulkify your code - never use SOQL/DML in loops
        3. Use trigger context variables correctly
        4. Implement recursion prevention
        5. Write test classes with 75%+ coverage
        
        Example pattern:
        trigger AccountTrigger on Account (before insert, after insert) {
            AccountTriggerHandler.handle(Trigger.new, Trigger.oldMap, 
                                         Trigger.operationType);
        }
        
        Governor limits: 100 SOQL queries, 150 DML statements per transaction.
        """
    },
    {
        "id": "doc4",
        "title": "Workflow Rules vs Process Builder vs Flow",
        "content": """
        Automation tool comparison:
        
        Workflow Rules (Legacy):
        - Simple if/then automation
        - Limited actions: field updates, email, tasks, outbound messages
        - Being retired, migrate to Flow
        
        Process Builder (Legacy):
        - Visual interface
        - Multiple criteria and actions
        - Also being retired
        
        Flow (Current Standard):
        - Most powerful automation tool
        - Screen flows for user interaction
        - Record-triggered for automation
        - Scheduled flows for batch processing
        - Supports complex logic and loops
        
        Recommendation: Use Flow for all new automation.
        """
    },
    {
        "id": "doc5",
        "title": "Salesforce Data Security Model",
        "content": """
        Salesforce security layers:
        
        1. Organization Level:
           - Login hours, IP restrictions, password policies
        
        2. Object Level (Profiles/Permission Sets):
           - CRUD permissions per object
           - Tab visibility
        
        3. Field Level Security:
           - Visibility and editability per field
           - Controlled via profiles or permission sets
        
        4. Record Level:
           - Organization-Wide Defaults (OWD): Private, Public Read, Public Read/Write
           - Role Hierarchy: Managers see subordinates' records
           - Sharing Rules: Extend access to groups
           - Manual Sharing: One-off record sharing
           - Apex Managed Sharing: Programmatic sharing
        
        Best practice: Start restrictive, then open up as needed.
        """
    }
]

print(f"Loaded {len(documents)} sample documents")
for doc in documents:
    print(f"  • {doc['title']}")


# Step 2: Chunking
print("\n--- Step 2: CHUNKING ---")

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Why chunk?
    - Embeddings work best on focused text
    - Context windows have limits
    - Retrieval is more precise with smaller chunks
    
    Why overlap?
    - Preserves context at boundaries
    - Ensures no information is "cut off"
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks

# Chunk all documents
all_chunks = []
for doc in documents:
    chunks = chunk_text(doc['content'])
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            'id': f"{doc['id']}_chunk_{i}",
            'doc_id': doc['id'],
            'title': doc['title'],
            'content': chunk
        })

print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
print(f"\nSample chunk:")
print(f"  Title: {all_chunks[0]['title']}")
print(f"  Content: {all_chunks[0]['content'][:100]}...")


# Step 3: Embeddings
print("\n--- Step 3: EMBEDDINGS ---")

try:
    from sentence_transformers import SentenceTransformer
    
    # Load embedding model (runs locally!)
    print("Loading embedding model...")
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create embeddings for all chunks
    print("Creating embeddings...")
    texts = [chunk['content'] for chunk in all_chunks]
    embeddings = embed_model.encode(texts)
    
    print(f"Created {len(embeddings)} embeddings")
    print(f"Embedding dimension: {embeddings[0].shape[0]}")
    
    # Store embeddings with chunks
    for i, chunk in enumerate(all_chunks):
        chunk['embedding'] = embeddings[i]
        
except ImportError:
    print("⚠️  sentence-transformers not installed")
    print("Run: pip install sentence-transformers")
    print("\nUsing simplified demo embeddings...")
    
    import numpy as np
    for chunk in all_chunks:
        # Create random embedding for demo
        chunk['embedding'] = np.random.rand(384)


# Step 4: Vector Database
print("\n--- Step 4: VECTOR DATABASE ---")

try:
    import chromadb
    
    # Create ChromaDB client (in-memory for demo)
    client = chromadb.Client()
    
    # Create collection
    collection = client.create_collection(
        name="salesforce_docs",
        metadata={"description": "Salesforce knowledge base"}
    )
    
    # Add documents
    collection.add(
        ids=[chunk['id'] for chunk in all_chunks],
        documents=[chunk['content'] for chunk in all_chunks],
        metadatas=[{'title': chunk['title'], 'doc_id': chunk['doc_id']} for chunk in all_chunks],
        embeddings=[chunk['embedding'].tolist() for chunk in all_chunks]
    )
    
    print(f"✅ Added {len(all_chunks)} chunks to ChromaDB")
    
    CHROMADB_AVAILABLE = True
    
except ImportError:
    print("⚠️  ChromaDB not installed. Run: pip install chromadb")
    CHROMADB_AVAILABLE = False

except Exception as e:
    print(f"ChromaDB error: {e}")
    CHROMADB_AVAILABLE = False


# Step 5: Semantic Search
print("\n--- Step 5: SEMANTIC SEARCH ---")

import numpy as np

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def simple_search(query: str, chunks: List[Dict], embed_model, top_k: int = 3) -> List[Dict]:
    """Simple semantic search using cosine similarity"""
    # Embed the query
    query_embedding = embed_model.encode([query])[0]
    
    # Calculate similarities
    results = []
    for chunk in chunks:
        similarity = cosine_similarity(query_embedding, chunk['embedding'])
        results.append({
            **chunk,
            'similarity': similarity
        })
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return results[:top_k]

# Test search
test_queries = [
    "How do I convert a lead?",
    "What are the best practices for Apex triggers?",
    "Explain Salesforce security model",
    "Should I use Process Builder or Flow?"
]

if 'embed_model' in dir():
    print("\nTesting semantic search:")
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = simple_search(query, all_chunks, embed_model, top_k=2)
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['title']} (similarity: {result['similarity']:.3f})")


# Step 6: RAG Pipeline
print("\n--- Step 6: COMPLETE RAG PIPELINE ---")

def build_rag_prompt(query: str, context_chunks: List[Dict]) -> str:
    """Build a prompt with retrieved context"""
    
    context = "\n\n".join([
        f"[Source: {chunk['title']}]\n{chunk['content']}"
        for chunk in context_chunks
    ])
    
    prompt = f"""You are a helpful Salesforce assistant. Answer the question using ONLY the provided context.
If the context doesn't contain the answer, say "I don't have information about that in my knowledge base."

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
    
    return prompt


def rag_query(query: str, chunks: List[Dict], embed_model, top_k: int = 3) -> Dict:
    """Complete RAG pipeline"""
    
    # Step 1: Retrieve relevant chunks
    relevant_chunks = simple_search(query, chunks, embed_model, top_k)
    
    # Step 2: Build augmented prompt
    prompt = build_rag_prompt(query, relevant_chunks)
    
    # Step 3: Would call LLM here
    # response = client.messages.create(...)
    
    return {
        'query': query,
        'retrieved_chunks': relevant_chunks,
        'prompt': prompt,
        'sources': [chunk['title'] for chunk in relevant_chunks]
    }

# Demo RAG query
if 'embed_model' in dir():
    print("\n🤖 RAG QUERY DEMO:")
    query = "How do I convert a lead to a contact in Salesforce?"
    result = rag_query(query, all_chunks, embed_model)
    
    print(f"\nQuery: {result['query']}")
    print(f"\nRetrieved sources:")
    for source in result['sources']:
        print(f"  • {source}")
    print(f"\nGenerated prompt (first 500 chars):")
    print(result['prompt'][:500] + "...")


# ============================================================
# PART 4: ADVANCED RAG TECHNIQUES
# ============================================================
print("\n" + "="*60)
print("🚀 PART 4: ADVANCED RAG TECHNIQUES")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│               ADVANCED RAG TECHNIQUES                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. HYBRID SEARCH                                           │
│     Combine semantic + keyword search                       │
│     Better for exact matches (IDs, codes, names)            │
│                                                             │
│  2. RE-RANKING                                              │
│     Initial retrieval gets top 20                           │
│     Re-ranker model picks best 3-5                          │
│     More accurate but slower                                │
│                                                             │
│  3. QUERY EXPANSION                                         │
│     "Lead conversion" → "Lead conversion, convert lead,     │
│      Lead status, qualification, opportunity creation"      │
│                                                             │
│  4. HYPOTHETICAL DOCUMENT EMBEDDINGS (HyDE)                 │
│     Generate hypothetical answer, embed that, search        │
│     Better matches for question-style queries               │
│                                                             │
│  5. MULTI-QUERY RAG                                         │
│     Rewrite query multiple ways                             │
│     Retrieve for each, combine results                      │
│                                                             │
│  6. CONTEXTUAL COMPRESSION                                  │
│     Extract only relevant sentences from chunks             │
│     Reduces noise in context                                │
│                                                             │
│  7. PARENT DOCUMENT RETRIEVER                               │
│     Index small chunks, return larger parent documents      │
│     Best of both: precise retrieval + complete context      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Hybrid Search Example
print("\n--- HYBRID SEARCH EXAMPLE ---")

def keyword_search(query: str, chunks: List[Dict], top_k: int = 3) -> List[Dict]:
    """Simple keyword-based search using BM25-like scoring"""
    query_terms = set(query.lower().split())
    
    results = []
    for chunk in chunks:
        content_terms = set(chunk['content'].lower().split())
        # Simple overlap score
        score = len(query_terms & content_terms) / len(query_terms)
        results.append({**chunk, 'keyword_score': score})
    
    results.sort(key=lambda x: x['keyword_score'], reverse=True)
    return results[:top_k]

def hybrid_search(query: str, chunks: List[Dict], embed_model, 
                  semantic_weight: float = 0.7, top_k: int = 3) -> List[Dict]:
    """Combine semantic and keyword search"""
    
    # Get both search results
    semantic_results = simple_search(query, chunks, embed_model, top_k=10)
    keyword_results = keyword_search(query, chunks, top_k=10)
    
    # Create score lookup
    semantic_scores = {r['id']: r['similarity'] for r in semantic_results}
    keyword_scores = {r['id']: r['keyword_score'] for r in keyword_results}
    
    # Combine scores
    all_ids = set(semantic_scores.keys()) | set(keyword_scores.keys())
    combined = []
    
    for chunk_id in all_ids:
        sem_score = semantic_scores.get(chunk_id, 0)
        kw_score = keyword_scores.get(chunk_id, 0)
        combined_score = (semantic_weight * sem_score) + ((1 - semantic_weight) * kw_score)
        
        # Find original chunk
        chunk = next((c for c in chunks if c['id'] == chunk_id), None)
        if chunk:
            combined.append({
                **chunk,
                'combined_score': combined_score,
                'semantic_score': sem_score,
                'keyword_score': kw_score
            })
    
    combined.sort(key=lambda x: x['combined_score'], reverse=True)
    return combined[:top_k]

if 'embed_model' in dir():
    print("\nHybrid Search: 'Apex trigger governor limits'")
    results = hybrid_search("Apex trigger governor limits", all_chunks, embed_model)
    for r in results:
        print(f"  • {r['title']}")
        print(f"    Combined: {r['combined_score']:.3f} (semantic: {r['semantic_score']:.3f}, keyword: {r['keyword_score']:.3f})")


# ============================================================
# PART 5: RAG EVALUATION
# ============================================================
print("\n" + "="*60)
print("📈 PART 5: RAG EVALUATION METRICS")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                  RAG EVALUATION METRICS                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RETRIEVAL METRICS:                                         │
│  ─────────────────                                          │
│  • Precision@K: Of top K retrieved, how many are relevant? │
│  • Recall@K: Of all relevant docs, how many retrieved?      │
│  • MRR (Mean Reciprocal Rank): Position of first relevant   │
│                                                             │
│  GENERATION METRICS:                                        │
│  ──────────────────                                         │
│  • Faithfulness: Is answer supported by context?            │
│  • Answer Relevancy: Does answer address the question?      │
│  • Context Relevancy: Is retrieved context actually useful? │
│                                                             │
│  TOOLS:                                                     │
│  ──────                                                     │
│  • RAGAS - Popular evaluation framework                     │
│  • TruLens - Logging and evaluation                         │
│  • LangSmith - LangChain's evaluation tool                  │
│                                                             │
│  EVALUATION APPROACH:                                       │
│  ────────────────────                                       │
│  1. Create test dataset (questions + expected answers)      │
│  2. Run RAG pipeline on test questions                      │
│  3. Compare retrieved chunks to expected sources            │
│  4. Score generated answers vs expected answers             │
│  5. Track metrics over time as you improve                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# PART 6: SALESFORCE RAG INTEGRATION
# ============================================================
print("\n" + "="*60)
print("☁️ PART 6: SALESFORCE RAG INTEGRATION")
print("="*60)

print("""
HOW TO BUILD SALESFORCE-POWERED RAG:

1. DATA SOURCES:
   • Knowledge Articles (Knowledge__kav)
   • Case resolutions
   • Account/Opportunity notes
   • Custom objects with documentation
   • Files and attachments

2. DATA EXTRACTION:
   ```python
   # Using your existing MCP server!
   query = '''
       SELECT Id, Title, ArticleBody 
       FROM Knowledge__kav 
       WHERE PublishStatus = 'Online'
   '''
   articles = await sf_query(query)
   ```

3. SYNC STRATEGY:
   • Initial bulk load
   • CDC (Change Data Capture) for updates
   • Scheduled refresh for critical content

4. ARCHITECTURE:
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │  Salesforce  │────▶│   ETL Job    │────▶│  Vector DB   │
   │  (Data)      │     │  (Extract,   │     │  (ChromaDB/  │
   │              │     │   Embed)     │     │   Pinecone)  │
   └──────────────┘     └──────────────┘     └──────────────┘
          │                                         │
          │                                         │
          ▼                                         ▼
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │  LWC Chat    │────▶│  API Server  │────▶│  Claude +    │
   │  Component   │◀────│  (Express)   │◀────│  RAG Context │
   └──────────────┘     └──────────────┘     └──────────────┘

5. YOUR NEXT PROJECT:
   Build a Knowledge Article RAG system:
   • Extract Knowledge Articles from Salesforce
   • Embed and store in ChromaDB
   • Add RAG retrieval to your chat API
   • Return answers with source citations
""")


# ============================================================
# 🎯 PRACTICE PROJECT
# ============================================================
print("\n" + "="*60)
print("🎯 HANDS-ON PROJECT: BUILD A SALESFORCE KB RAG")
print("="*60)

print("""
PROJECT: Salesforce Knowledge Base RAG System

STEPS:

1. Create sample Knowledge Articles (run in your sandbox):
   ```apex
   // Create test Knowledge Articles
   Knowledge__kav article = new Knowledge__kav();
   article.Title = 'How to Reset Password';
   article.Summary = 'Instructions for password reset';
   article.ArticleBody = 'Detailed instructions...';
   insert article;
   ```

2. Modify your API server to include RAG:
   ```javascript
   // In index.js
   const { ChromaClient } = require('chromadb');
   
   // Add endpoint
   app.post('/api/rag-query', async (req, res) => {
       const { question } = req.body;
       
       // 1. Retrieve from ChromaDB
       const results = await collection.query({
           queryTexts: [question],
           nResults: 3
       });
       
       // 2. Build context
       const context = results.documents[0].join('\\n\\n');
       
       // 3. Query Claude with context
       const response = await anthropic.messages.create({
           model: 'claude-sonnet-4-20250514',
           messages: [{
               role: 'user',
               content: `Context:\\n${context}\\n\\nQuestion: ${question}`
           }]
       });
       
       res.json({ 
           answer: response.content[0].text,
           sources: results.metadatas[0]
       });
   });
   ```

3. Add to your LWC chat:
   - Show source citations
   - Display confidence scores
   - Allow drilling into sources

4. Test and evaluate:
   - Create 10 test questions
   - Verify answers are grounded in sources
   - Measure latency and user satisfaction
""")


# ============================================================
# 🏆 INTERVIEW QUESTIONS
# ============================================================
print("\n" + "="*60)
print("🏆 RAG INTERVIEW QUESTIONS")
print("="*60)

print("""
1. What is RAG and why is it useful?
   → Retrieval Augmented Generation
   → Reduces hallucination by grounding in actual data
   → Provides up-to-date information beyond training cutoff

2. Explain the RAG pipeline.
   → Index: Chunk → Embed → Store in vector DB
   → Query: Embed query → Search → Retrieve → Augment prompt → Generate

3. What are embeddings and how do they enable semantic search?
   → Dense vector representations of text meaning
   → Similar meanings = close vectors in space
   → Search by vector similarity, not keywords

4. What is the difference between semantic and keyword search?
   → Keyword: Exact/fuzzy term matching (BM25)
   → Semantic: Meaning-based similarity (embeddings)
   → Hybrid combines both for best results

5. How do you handle documents larger than the context window?
   → Chunking with overlap
   → Hierarchical retrieval
   → Summarization
   → Map-reduce approaches

6. What chunking strategies are there?
   → Fixed size with overlap
   → Sentence-based
   → Paragraph-based
   → Semantic (topic-based)
   → Document structure-aware

7. How do you evaluate a RAG system?
   → Retrieval: Precision@K, Recall@K, MRR
   → Generation: Faithfulness, relevancy
   → End-to-end: User satisfaction, accuracy

8. What is re-ranking in RAG?
   → Two-stage retrieval
   → Fast initial retrieval (many results)
   → Precise re-ranker model (select best)

9. How do you handle updates to the knowledge base?
   → Incremental updates (add/update/delete)
   → CDC for real-time
   → Scheduled full refresh
   → Versioning for rollback

10. What vector databases have you worked with?
    → Pinecone: Managed, scalable, production-ready
    → ChromaDB: Open source, easy to start
    → Weaviate: Open source, GraphQL, hybrid search
    → Milvus: High performance, open source
""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 RAG SYSTEMS MODULE COMPLETE!")
print("="*60)
print("""
You now understand:
✅ What RAG is and why it matters
✅ The complete RAG pipeline (index + query)
✅ Chunking strategies
✅ Embeddings and vector similarity
✅ Vector databases (ChromaDB)
✅ Hybrid search (semantic + keyword)
✅ Advanced techniques (re-ranking, HyDE, multi-query)
✅ Evaluation metrics
✅ Salesforce integration approach

NEXT STEPS:
1. Complete the hands-on project above
2. Move to: 04-agentic-ai/ for multi-agent systems
3. Combine RAG + Agents for powerful applications!

RESOURCES:
• LangChain RAG Tutorial: python.langchain.com
• RAGAS Evaluation: github.com/explodinggradients/ragas
• ChromaDB Docs: docs.trychroma.com
""")
