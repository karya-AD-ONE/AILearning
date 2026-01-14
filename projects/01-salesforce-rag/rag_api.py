"""
============================================================
RAG API SERVER - Flask wrapper for Node.js integration
============================================================
Run this alongside your Express server to add RAG capabilities.

Start: python3 rag_api.py
Endpoint: POST http://localhost:5001/api/rag/query

Then call from your Express server or LWC.
============================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# Import our RAG system
from rag_system import SalesforceRAG

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize RAG system once at startup
print("🚀 Starting RAG API Server...")
rag = SalesforceRAG()
rag.index_documents("knowledge_base.json")
print("✅ RAG system ready!")


@app.route('/api/rag/query', methods=['POST'])
def rag_query():
    """
    RAG query endpoint.
    
    Request body:
    {
        "question": "How do I convert a lead?",
        "top_k": 3  // optional, default 3
    }
    
    Response:
    {
        "success": true,
        "question": "...",
        "answer": "...",
        "sources": ["Article 1", "Article 2"],
        "search_results": [...]
    }
    """
    try:
        data = request.get_json()
        question = data.get('question')
        top_k = data.get('top_k', 3)
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400
        
        # Query RAG system
        result = rag.query(question, top_k=top_k)
        
        return jsonify({
            'success': True,
            'question': result['question'],
            'answer': result['answer'],
            'sources': result['sources'],
            'search_results': [
                {
                    'title': r['metadata']['title'],
                    'category': r['metadata']['category'],
                    'similarity': r['similarity'],
                    'snippet': r['document'][:200] + '...'
                }
                for r in result['search_results']
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rag/search', methods=['POST'])
def rag_search():
    """
    Search-only endpoint (no answer generation).
    Useful for showing relevant articles.
    """
    try:
        data = request.get_json()
        query = data.get('query')
        top_k = data.get('top_k', 5)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        results = rag.search(query, top_k=top_k)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': [
                {
                    'title': r['metadata']['title'],
                    'category': r['metadata']['category'],
                    'similarity': r['similarity'],
                    'content': r['document']
                }
                for r in results
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rag/stats', methods=['GET'])
def rag_stats():
    """Get RAG system statistics."""
    stats = rag.get_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/rag/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'OK',
        'service': 'Salesforce RAG API',
        'indexed_chunks': rag.get_stats()['total_chunks']
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔍 RAG API Server")
    print("="*60)
    print(f"  POST http://localhost:5000/api/rag/query")
    print(f"  POST http://localhost:5001/api/rag/search")
    print(f"  GET  http://localhost:5001/api/rag/stats")
    print(f"  GET  http://localhost:5001/api/rag/health")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
