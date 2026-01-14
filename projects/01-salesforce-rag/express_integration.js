/**
 * ============================================================
 * RAG INTEGRATION FOR EXPRESS SERVER
 * ============================================================
 * 
 * Add these snippets to your existing index.js to integrate
 * the Python RAG API with your Express server.
 * 
 * SETUP:
 * 1. Start Python RAG API: python3 rag_api.py (runs on port 5000)
 * 2. Start Express server: node index.js (runs on port 3000)
 * 3. Claude can now use both Salesforce tools AND RAG search!
 */

// ============================================================
// ADD THIS: Import fetch for calling RAG API
// ============================================================
// Add at top of file (Node 18+ has built-in fetch, or install node-fetch)

// If using Node < 18:
// const fetch = require('node-fetch');

const RAG_API_URL = 'http://localhost:5000';


// ============================================================
// ADD THIS: RAG Helper Function
// ============================================================
// Add after your Salesforce helper functions

async function searchKnowledgeBase(query) {
  try {
    const response = await fetch(`${RAG_API_URL}/api/rag/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: query, top_k: 3 })
    });
    
    const result = await response.json();
    
    if (result.success) {
      return {
        answer: result.answer,
        sources: result.sources,
        search_results: result.search_results
      };
    } else {
      throw new Error(result.error || 'RAG query failed');
    }
  } catch (error) {
    throw new Error(`Knowledge base error: ${error.message}`);
  }
}


// ============================================================
// ADD THIS: RAG Tool Definition
// ============================================================
// Add to your tools array

const ragTool = {
  name: 'search_knowledge_base',
  description: 'Search the Salesforce knowledge base for best practices, how-to guides, and documentation. Use this when you need information about Salesforce features, processes, or best practices.',
  input_schema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'The question or topic to search for in the knowledge base (e.g., "How do I convert a lead?" or "Apex trigger best practices")',
      },
    },
    required: ['query'],
  },
};

// Then add ragTool to your tools array:
// const tools = [...existingTools, ragTool];


// ============================================================
// ADD THIS: RAG Tool Handler
// ============================================================
// Add inside your executeTool function switch/if statement

/*
} else if (toolUse.name === 'search_knowledge_base') {
  const result = await searchKnowledgeBase(toolUse.input.query);
  toolResult = {
    success: true,
    answer: result.answer,
    sources: result.sources,
  };
*/


// ============================================================
// COMPLETE UPDATED executeTool FUNCTION
// ============================================================
// Replace your existing executeTool function with this:

async function executeToolWithRAG(toolUse) {
  let toolResult;

  try {
    if (toolUse.name === 'sf_query') {
      const records = await executeSalesforceQuery(toolUse.input.query);
      toolResult = {
        success: true,
        records: records,
        totalSize: records.length,
      };
    } else if (toolUse.name === 'sf_get_account') {
      const record = await getSalesforceRecord('Account', toolUse.input.accountId);
      toolResult = {
        success: true,
        record: record,
      };
    } else if (toolUse.name === 'sf_create_record') {
      const result = await createSalesforceRecord(
        toolUse.input.objectType,
        toolUse.input.fields
      );
      toolResult = {
        success: true,
        result: result,
      };
    } else if (toolUse.name === 'sf_update_record') {
      const result = await updateSalesforceRecord(
        toolUse.input.objectType,
        toolUse.input.recordId,
        toolUse.input.fields
      );
      toolResult = {
        success: true,
        result: result,
      };
    } else if (toolUse.name === 'sf_search_accounts') {
      const records = await searchSalesforceAccounts(toolUse.input.searchTerm);
      toolResult = {
        success: true,
        records: records,
        totalSize: records.length,
      };
    // ========== NEW: RAG TOOL ==========
    } else if (toolUse.name === 'search_knowledge_base') {
      const result = await searchKnowledgeBase(toolUse.input.query);
      toolResult = {
        success: true,
        answer: result.answer,
        sources: result.sources,
      };
    // ===================================
    } else {
      toolResult = {
        success: false,
        error: `Unknown tool: ${toolUse.name}`,
      };
    }
  } catch (error) {
    toolResult = {
      success: false,
      error: error.message,
    };
  }

  return toolResult;
}


// ============================================================
// EXAMPLE: Smart Agent Prompt with RAG
// ============================================================
// Update your agent prompt to mention the knowledge base:

const smartAgentPrompt = `You are an intelligent Salesforce assistant with access to:

1. LIVE SALESFORCE DATA - Query accounts, leads, opportunities, contacts
2. KNOWLEDGE BASE - Search for Salesforce best practices and how-to guides

When helping users:
- Use sf_query to get real-time data from Salesforce
- Use search_knowledge_base to find best practices and documentation
- Combine both to give comprehensive answers

For example, if asked "How should I handle this lead?":
1. Query the lead details from Salesforce
2. Search knowledge base for lead qualification best practices
3. Provide recommendation based on both

Be thorough and always cite your sources.`;


// ============================================================
// DIRECT RAG ENDPOINT (Optional)
// ============================================================
// Add this endpoint to allow direct RAG queries from LWC

/*
app.post('/api/rag/query', async (req, res) => {
  try {
    const { question } = req.body;
    
    if (!question) {
      return res.status(400).json({ error: 'Question is required' });
    }
    
    const result = await searchKnowledgeBase(question);
    res.json(result);
    
  } catch (error) {
    res.status(500).json({
      error: 'RAG query failed',
      message: error.message
    });
  }
});
*/


// ============================================================
// TESTING
// ============================================================
// Test the RAG integration with:
//
// curl -X POST http://localhost:3000/api/chat \
//   -H "Content-Type: application/json" \
//   -d '{"message": "Search the knowledge base for how to convert a lead"}'

module.exports = { searchKnowledgeBase, ragTool };
