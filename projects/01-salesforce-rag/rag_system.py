"""
============================================================
SALESFORCE RAG SYSTEM - Complete Implementation
============================================================
A production-ready RAG system for Salesforce knowledge base.

Run: python3 rag_system.py
============================================================
"""

import json
import os
from typing import List, Dict, Any

# ============================================================
# STEP 1: IMPORTS AND SETUP
# ============================================================
print("="*60)
print("🔍 SALESFORCE RAG SYSTEM")
print("="*60)

print("\n📦 Loading dependencies...")

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    print("  ✅ ChromaDB loaded")
    print("  ✅ SentenceTransformers loaded")
except ImportError as e:
    print(f"  ❌ Missing dependency: {e}")
    print("  Run: pip install chromadb sentence-transformers")
    exit(1)

# Check for Anthropic (optional, for Claude integration)
CLAUDE_AVAILABLE = False
try:
    from anthropic import Anthropic
    if os.environ.get('ANTHROPIC_API_KEY'):
        CLAUDE_AVAILABLE = True
        print("  ✅ Anthropic API available")
    else:
        print("  ⚠️  ANTHROPIC_API_KEY not set - will skip Claude integration")
except ImportError:
    print("  ⚠️  Anthropic not installed - will skip Claude integration")


# ============================================================
# STEP 2: RAG SYSTEM CLASS
# ============================================================

class SalesforceRAG:
    """
    Complete RAG system for Salesforce knowledge base.
    
    Usage:
        rag = SalesforceRAG()
        rag.index_documents("knowledge_base.json")
        answer = rag.query("How do I convert a lead?")
    """
    
    def __init__(self, collection_name: str = "salesforce_kb"):
        """Initialize the RAG system."""
        print("\n🔧 Initializing RAG system...")
        
        # Initialize embedding model (runs locally!)
        print("  Loading embedding model...")
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        print(f"  ✅ Embedding model loaded (dimension: {self.embed_model.get_sentence_embedding_dimension()})")
        
        # Initialize ChromaDB (in-memory for demo, can use persistent)
        print("  Initializing vector database...")
        self.chroma_client = chromadb.Client()  # In-memory
        # For persistent storage, use:
        # self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Salesforce Knowledge Base"}
        )
        print(f"  ✅ Collection '{collection_name}' ready")
        
        # Initialize Claude client if available
        if CLAUDE_AVAILABLE:
            self.anthropic = Anthropic()
            print("  ✅ Claude client initialized")
        else:
            self.anthropic = None
    
    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Why chunk?
        - Embeddings work better on focused text
        - Smaller chunks = more precise retrieval
        - Overlap preserves context at boundaries
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk) > 50:  # Skip very small chunks
                chunks.append(chunk)
        
        return chunks if chunks else [text]  # Return original if too short
    
    def index_documents(self, json_file: str) -> int:
        """
        Load and index documents from JSON file.
        
        Returns number of chunks indexed.
        """
        print(f"\n📄 Indexing documents from {json_file}...")
        
        # Load documents
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        articles = data.get('articles', [])
        print(f"  Found {len(articles)} articles")
        
        # Process each article
        all_chunks = []
        all_ids = []
        all_metadatas = []
        
        for article in articles:
            # Combine title and content for better context
            full_text = f"{article['title']}\n\n{article['content']}"
            
            # Chunk the document
            chunks = self.chunk_text(full_text)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{article['id']}_chunk_{i}"
                all_chunks.append(chunk)
                all_ids.append(chunk_id)
                all_metadatas.append({
                    'article_id': article['id'],
                    'title': article['title'],
                    'category': article['category'],
                    'chunk_index': i
                })
        
        print(f"  Created {len(all_chunks)} chunks")
        
        # Create embeddings
        print("  Creating embeddings...")
        embeddings = self.embed_model.encode(all_chunks).tolist()
        
        # Add to ChromaDB
        print("  Storing in vector database...")
        self.collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas
        )
        
        print(f"  ✅ Indexed {len(all_chunks)} chunks from {len(articles)} articles")
        return len(all_chunks)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant documents.
        
        Returns list of {document, metadata, score} dicts.
        """
        # Embed the query
        query_embedding = self.embed_model.encode([query]).tolist()
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return formatted
    
    def build_prompt(self, query: str, context_docs: List[Dict]) -> str:
        """Build a prompt with retrieved context."""
        
        context = "\n\n---\n\n".join([
            f"[Source: {doc['metadata']['title']}]\n{doc['document']}"
            for doc in context_docs
        ])
        
        prompt = f"""You are a helpful Salesforce assistant. Answer the question using ONLY the provided context from the knowledge base.

If the context doesn't contain enough information to answer the question, say "I don't have specific information about that in my knowledge base, but..." and provide general guidance if possible.

Always cite which article your information comes from.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
        
        return prompt
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Complete RAG query: search + generate answer.
        
        Returns dict with answer, sources, and search results.
        """
        print(f"\n🔍 Query: {question}")
        
        # Step 1: Retrieve relevant documents
        print("  Searching knowledge base...")
        search_results = self.search(question, top_k=top_k)
        
        print(f"  Found {len(search_results)} relevant chunks:")
        for i, doc in enumerate(search_results, 1):
            print(f"    {i}. {doc['metadata']['title']} (similarity: {doc['similarity']:.3f})")
        
        # Step 2: Build prompt with context
        prompt = self.build_prompt(question, search_results)
        
        # Step 3: Generate answer with Claude (if available)
        if self.anthropic:
            print("  Generating answer with Claude...")
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.content[0].text
        else:
            answer = "[Claude not available - showing retrieved context only]\n\n"
            answer += "Based on the knowledge base, here's the relevant information:\n\n"
            for doc in search_results:
                answer += f"From '{doc['metadata']['title']}':\n{doc['document'][:500]}...\n\n"
        
        return {
            'question': question,
            'answer': answer,
            'sources': [doc['metadata']['title'] for doc in search_results],
            'search_results': search_results
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed documents."""
        count = self.collection.count()
        return {
            'total_chunks': count,
            'collection_name': self.collection.name,
            'embedding_dimension': self.embed_model.get_sentence_embedding_dimension()
        }


# ============================================================
# STEP 3: MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    
    # Initialize RAG system
    rag = SalesforceRAG()
    
    # Index documents
    print("\n" + "="*60)
    print("INDEXING PHASE")
    print("="*60)
    
    rag.index_documents("knowledge_base.json")
    
    # Show stats
    stats = rag.get_stats()
    print(f"\n📊 Index Statistics:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Embedding dimension: {stats['embedding_dimension']}")
    
    # Test queries
    print("\n" + "="*60)
    print("QUERY PHASE - Testing RAG System")
    print("="*60)
    
    test_queries = [
        "How do I convert a lead in Salesforce?",
        "What are the different opportunity stages?",
        "How does security work in Salesforce?",
        "What's the difference between Flow and Process Builder?",
        "How do I create a report?"
    ]
    
    for query in test_queries:
        result = rag.query(query)
        print(f"\n{'='*60}")
        print(f"❓ Question: {result['question']}")
        print(f"📚 Sources: {', '.join(result['sources'])}")
        print(f"\n💬 Answer:")
        print(result['answer'][:800] + "..." if len(result['answer']) > 800 else result['answer'])
        print("="*60)
        
        # Pause between queries for readability
        input("\n[Press Enter for next query...]")
    
    # Interactive mode
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("Ask any question about Salesforce (type 'quit' to exit)")
    
    while True:
        user_query = input("\n🔍 Your question: ").strip()
        
        if user_query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_query:
            continue
        
        result = rag.query(user_query)
        print(f"\n📚 Sources: {', '.join(result['sources'])}")
        print(f"\n💬 Answer:\n{result['answer']}")
