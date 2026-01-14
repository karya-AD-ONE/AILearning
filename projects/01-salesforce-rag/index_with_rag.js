require('dotenv').config();

const express = require('express');
const cors = require('cors');
const Anthropic = require('@anthropic-ai/sdk');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

const app = express();
const PORT = 3000;
const RAG_API_URL = 'http://localhost:5001';  // Python RAG service

app.use(cors({
  origin: '*',
  credentials: true
}));
app.use(express.json());

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const SF_ORG_ALIAS = 'storecapitalUAT'; // Change to your org alias

// ============================================
// SALESFORCE HELPER FUNCTIONS
// ============================================

async function executeSalesforceQuery(query) {
  try {
    const { stdout } = await execAsync(
      `sf data query --query "${query}" --target-org ${SF_ORG_ALIAS} --json`
    );
    const result = JSON.parse(stdout);
    
    if (result.status === 0) {
      return result.result.records;
    } else {
      throw new Error(result.message || 'Query failed');
    }
  } catch (error) {
    throw new Error(`Salesforce query error: ${error.message}`);
  }
}

async function getSalesforceRecord(objectType, recordId) {
  try {
    const query = `SELECT FIELDS(ALL) FROM ${objectType} WHERE Id = '${recordId}' LIMIT 1`;
    const records = await executeSalesforceQuery(query);
    return records[0] || null;
  } catch (error) {
    throw new Error(`Failed to get record: ${error.message}`);
  }
}

async function createSalesforceRecord(objectType, fields) {
  try {
    const fieldsJson = JSON.stringify(fields).replace(/"/g, '\\"');
    const { stdout } = await execAsync(
      `sf data create record --sobject ${objectType} --values "${fieldsJson}" --target-org ${SF_ORG_ALIAS} --json`
    );
    const result = JSON.parse(stdout);
    
    if (result.status === 0) {
      return result.result;
    } else {
      throw new Error(result.message || 'Create failed');
    }
  } catch (error) {
    throw new Error(`Failed to create record: ${error.message}`);
  }
}

async function updateSalesforceRecord(objectType, recordId, fields) {
  try {
    const fieldsJson = JSON.stringify(fields).replace(/"/g, '\\"');
    const { stdout } = await execAsync(
      `sf data update record --sobject ${objectType} --record-id ${recordId} --values "${fieldsJson}" --target-org ${SF_ORG_ALIAS} --json`
    );
    const result = JSON.parse(stdout);
    
    if (result.status === 0) {
      return { success: true, recordId: recordId };
    } else {
      throw new Error(result.message || 'Update failed');
    }
  } catch (error) {
    throw new Error(`Failed to update record: ${error.message}`);
  }
}

async function searchSalesforceAccounts(searchTerm) {
  try {
    const query = `SELECT Id, Name, Industry, NumberOfEmployees FROM Account WHERE Name LIKE '%${searchTerm}%' LIMIT 10`;
    return await executeSalesforceQuery(query);
  } catch (error) {
    throw new Error(`Failed to search accounts: ${error.message}`);
  }
}

// ============================================
// RAG HELPER FUNCTION (NEW!)
// ============================================

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

// ============================================
// TOOL DEFINITIONS (WITH RAG!)
// ============================================

const tools = [
  {
    name: 'sf_query',
    description: 'Execute a SOQL query on Salesforce and return results',
    input_schema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'The SOQL query to execute (e.g., SELECT Id, Name FROM Account LIMIT 10)',
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'sf_get_account',
    description: 'Get details of a Salesforce Account by ID',
    input_schema: {
      type: 'object',
      properties: {
        accountId: {
          type: 'string',
          description: 'The Salesforce Account ID',
        },
      },
      required: ['accountId'],
    },
  },
  {
    name: 'sf_create_record',
    description: 'Create a new record in Salesforce',
    input_schema: {
      type: 'object',
      properties: {
        objectType: {
          type: 'string',
          description: 'The Salesforce object type (e.g., Account, Contact, Lead)',
        },
        fields: {
          type: 'object',
          description: 'The fields and values for the new record',
        },
      },
      required: ['objectType', 'fields'],
    },
  },
  {
    name: 'sf_update_record',
    description: 'Update an existing Salesforce record',
    input_schema: {
      type: 'object',
      properties: {
        objectType: {
          type: 'string',
          description: 'The Salesforce object type (e.g., Lead, Account)',
        },
        recordId: {
          type: 'string',
          description: 'The ID of the record to update',
        },
        fields: {
          type: 'object',
          description: 'The fields to update with new values',
        },
      },
      required: ['objectType', 'recordId', 'fields'],
    },
  },
  {
    name: 'sf_search_accounts',
    description: 'Search for accounts by name or other criteria',
    input_schema: {
      type: 'object',
      properties: {
        searchTerm: {
          type: 'string',
          description: 'The term to search for in account names',
        },
      },
      required: ['searchTerm'],
    },
  },
  // ========== NEW: RAG TOOL ==========
  {
    name: 'search_knowledge_base',
    description: 'Search the Salesforce knowledge base for best practices, how-to guides, and documentation. Use this when you need information about Salesforce features, processes, or best practices like lead conversion, opportunity stages, security, automation, Apex development, etc.',
    input_schema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'The question or topic to search for (e.g., "How do I convert a lead?" or "Apex trigger best practices")',
        },
      },
      required: ['query'],
    },
  },
];

// ============================================
// TOOL EXECUTION HELPER (WITH RAG!)
// ============================================

async function executeTool(toolUse) {
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
    // ========== NEW: RAG TOOL HANDLER ==========
    } else if (toolUse.name === 'search_knowledge_base') {
      const result = await searchKnowledgeBase(toolUse.input.query);
      toolResult = {
        success: true,
        answer: result.answer,
        sources: result.sources,
      };
    // ============================================
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

// ============================================
// STANDARD CHAT ENDPOINT
// ============================================

app.post('/api/chat', async (req, res) => {
  try {
    const { message, conversationHistory = [] } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    console.log(`📩 Received message: ${message}`);

    const messages = [
      ...conversationHistory,
      {
        role: 'user',
        content: message,
      },
    ];

    let response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      system: `You are an intelligent Salesforce assistant with access to:
1. LIVE SALESFORCE DATA - Query accounts, leads, opportunities using sf_* tools
2. KNOWLEDGE BASE - Search for best practices using search_knowledge_base

Combine both to give comprehensive answers. Always cite sources when using knowledge base.`,
      tools: tools,
      messages: messages,
    });

    console.log(`🤖 Claude response received`);

    while (response.stop_reason === 'tool_use') {
      const toolUse = response.content.find((block) => block.type === 'tool_use');

      if (!toolUse) break;

      console.log(`🔧 Tool requested: ${toolUse.name}`);

      const toolResult = await executeTool(toolUse);

      console.log(`✅ Tool executed: ${toolUse.name}`);

      messages.push({
        role: 'assistant',
        content: response.content,
      });

      messages.push({
        role: 'user',
        content: [
          {
            type: 'tool_result',
            tool_use_id: toolUse.id,
            content: JSON.stringify(toolResult),
          },
        ],
      });

      response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        tools: tools,
        messages: messages,
      });
    }

    const textContent = response.content.find((block) => block.type === 'text');
    const responseText = textContent ? textContent.text : 'No response generated';

    console.log(`✅ Sending response to client`);

    res.json({
      response: responseText,
      conversationHistory: messages,
    });
  } catch (error) {
    console.error('❌ Error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message,
    });
  }
});

// ============================================
// DIRECT RAG ENDPOINT (NEW!)
// ============================================

app.post('/api/rag/query', async (req, res) => {
  try {
    const { question } = req.body;
    
    if (!question) {
      return res.status(400).json({ error: 'Question is required' });
    }
    
    console.log(`🔍 RAG query: ${question}`);
    const result = await searchKnowledgeBase(question);
    
    res.json({
      success: true,
      ...result
    });
    
  } catch (error) {
    console.error('❌ RAG Error:', error);
    res.status(500).json({
      success: false,
      error: 'RAG query failed',
      message: error.message
    });
  }
});

// ============================================
// SMART AGENT ENDPOINT (NEW!)
// ============================================

app.post('/api/agent/smart-assist', async (req, res) => {
  try {
    const { question } = req.body;

    if (!question) {
      return res.status(400).json({ error: 'Question is required' });
    }

    console.log(`🧠 Smart Agent: ${question}`);

    const systemPrompt = `You are an expert Salesforce consultant with access to:

1. LIVE SALESFORCE DATA (sf_query, sf_get_account, sf_search_accounts)
   - Use these to get real-time data from the org
   
2. KNOWLEDGE BASE (search_knowledge_base)  
   - Use this for best practices, how-to guides, documentation

Your approach:
- If the question is about specific data → Query Salesforce first
- If the question is about how to do something → Search knowledge base first
- For comprehensive help → Use BOTH to combine real data with best practices

IMPORTANT: Use tools ONE AT A TIME. Wait for results before using the next tool.

Always be thorough and cite your sources.`;

    const messages = [
      { role: 'user', content: question }
    ];

    let response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      system: systemPrompt,
      tools: tools,
      messages: messages,
    });

    const steps = [];
    let iterations = 0;
    const maxIterations = 15;

    while (response.stop_reason === 'tool_use' && iterations < maxIterations) {
      // Get ALL tool_use blocks from the response
      const toolUseBlocks = response.content.filter((block) => block.type === 'tool_use');
      if (toolUseBlocks.length === 0) break;

      // Process all tool calls
      const toolResults = [];
      for (const toolUse of toolUseBlocks) {
        iterations++;
        console.log(`  Step ${iterations}: ${toolUse.name}`);
        
        steps.push({
          step: iterations,
          tool: toolUse.name,
          input: toolUse.input,
        });

        const toolResult = await executeTool(toolUse);
        steps[steps.length - 1].result = toolResult;

        toolResults.push({
          type: 'tool_result',
          tool_use_id: toolUse.id,
          content: JSON.stringify(toolResult),
        });
      }

      messages.push({
        role: 'assistant',
        content: response.content,
      });

      messages.push({
        role: 'user',
        content: toolResults,
      });

      response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        system: systemPrompt,
        tools: tools,
        messages: messages,
      });
    }

    const textContent = response.content.find((block) => block.type === 'text');
    const finalResponse = textContent ? textContent.text : 'No response';

    console.log(`✅ Smart agent complete: ${iterations} steps`);

    res.json({
      success: true,
      question: question,
      answer: finalResponse,
      steps: steps,
      totalSteps: iterations,
    });
  } catch (error) {
    console.error('❌ Smart Agent Error:', error);
    res.status(500).json({
      success: false,
      error: 'Smart agent failed',
      message: error.message,
    });
  }
});

// ============================================
// AGENTIC WORKFLOW ENDPOINT
// ============================================

app.post('/api/agent/qualify-lead', async (req, res) => {
  try {
    const { leadId } = req.body;

    if (!leadId) {
      return res.status(400).json({ error: 'leadId is required' });
    }

    console.log(`🤖 Starting lead qualification agent for: ${leadId}`);

    const agenticPrompt = `You are a lead qualification agent. Your job is to analyze a lead and determine if it's worth pursuing.

LEAD ID: ${leadId}

YOUR TASK:
1. Get the lead details (company name, industry, email, phone, etc.)
2. Search for existing accounts with similar company names
3. If account exists, check for past opportunities related to that account
4. Search the knowledge base for lead qualification best practices
5. Analyze the lead's quality based on:
   - Company information (if available)
   - Past relationship history (if any)
   - Lead source and current status
   - Best practices from knowledge base
6. Assign a score: HOT (definitely pursue), WARM (maybe pursue), or COLD (low priority)
7. Update the lead with:
   - Rating field: Hot/Warm/Cold
   - Description: Add your detailed reasoning for the score

Think step-by-step and use the available tools to complete this analysis autonomously.`;

    const messages = [
      {
        role: 'user',
        content: agenticPrompt,
      },
    ];

    let response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      tools: tools,
      messages: messages,
    });

    const steps = [];
    let iterations = 0;
    const maxIterations = 20;

    while (response.stop_reason === 'tool_use' && iterations < maxIterations) {
      const toolUse = response.content.find((block) => block.type === 'tool_use');
      if (!toolUse) break;

      iterations++;
      console.log(`  Step ${iterations}: ${toolUse.name}`);
      
      steps.push({
        step: iterations,
        tool: toolUse.name,
        input: toolUse.input,
      });

      const toolResult = await executeTool(toolUse);
      steps[steps.length - 1].result = toolResult;

      messages.push({
        role: 'assistant',
        content: response.content,
      });

      messages.push({
        role: 'user',
        content: [
          {
            type: 'tool_result',
            tool_use_id: toolUse.id,
            content: JSON.stringify(toolResult),
          },
        ],
      });

      response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        tools: tools,
        messages: messages,
      });
    }

    const textContent = response.content.find((block) => block.type === 'text');
    const finalResponse = textContent ? textContent.text : 'No response';

    console.log(`✅ Lead qualification complete after ${iterations} steps`);

    res.json({
      leadId: leadId,
      steps: steps,
      analysis: finalResponse,
      totalSteps: iterations,
      success: true,
    });
  } catch (error) {
    console.error('❌ Agent error:', error);
    res.status(500).json({
      error: 'Agent execution failed',
      message: error.message,
    });
  }
});

// ============================================
// GENERIC AGENTIC ENDPOINT (FOR ANY TASK)
// ============================================

app.post('/api/agent/execute', async (req, res) => {
  try {
    const { task, maxSteps = 15 } = req.body;

    if (!task) {
      return res.status(400).json({ error: 'task is required' });
    }

    console.log(`🤖 Starting agentic task: ${task}`);

    const messages = [
      {
        role: 'user',
        content: `You are an autonomous agent with access to Salesforce tools AND a knowledge base. Execute this task step-by-step:\n\n${task}\n\nUse the available tools to complete this task. Think through each step and execute autonomously. Use search_knowledge_base when you need best practices or how-to information.`,
      },
    ];

    let response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      tools: tools,
      messages: messages,
    });

    const steps = [];
    let iterations = 0;

    while (response.stop_reason === 'tool_use' && iterations < maxSteps) {
      const toolUse = response.content.find((block) => block.type === 'tool_use');
      if (!toolUse) break;

      iterations++;
      console.log(`  Step ${iterations}: ${toolUse.name}`);
      
      steps.push({
        step: iterations,
        tool: toolUse.name,
        input: toolUse.input,
      });

      const toolResult = await executeTool(toolUse);
      steps[steps.length - 1].result = toolResult;

      messages.push({
        role: 'assistant',
        content: response.content,
      });

      messages.push({
        role: 'user',
        content: [
          {
            type: 'tool_result',
            tool_use_id: toolUse.id,
            content: JSON.stringify(toolResult),
          },
        ],
      });

      response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        tools: tools,
        messages: messages,
      });
    }

    const textContent = response.content.find((block) => block.type === 'text');
    const finalResponse = textContent ? textContent.text : 'No response';

    console.log(`✅ Agent task complete after ${iterations} steps`);

    res.json({
      task: task,
      steps: steps,
      result: finalResponse,
      totalSteps: iterations,
      success: true,
    });
  } catch (error) {
    console.error('❌ Agent error:', error);
    res.status(500).json({
      error: 'Agent execution failed',
      message: error.message,
    });
  }
});

// ============================================
// ACCOUNT RESEARCH AGENT (PROJECT 3)
// ============================================

app.post('/api/agent/research-account', async (req, res) => {
  try {
    const { companyName } = req.body;

    if (!companyName) {
      return res.status(400).json({ error: 'companyName is required' });
    }

    console.log(`🔬 Account Research Agent: ${companyName}`);

    const systemPrompt = `You are an expert Account Research Agent. Your job is to compile a comprehensive research report on a company.

You have access to:
1. SALESFORCE DATA - Query accounts, contacts, opportunities, cases
2. KNOWLEDGE BASE - Search for industry best practices and insights

For the company "${companyName}", gather ALL of the following:

1. **ACCOUNT DETAILS**
   - Search for the account by name
   - Get full account record with all available fields

2. **CONTACTS**
   - Find all contacts associated with this account
   - Note their roles, titles, and contact info

3. **OPPORTUNITIES**
   - Get all opportunities (open and closed)
   - Include amounts, stages, close dates

4. **CASES/SUPPORT HISTORY**
   - Find any support cases
   - Note status and any issues

5. **INDUSTRY INSIGHTS**
   - Search knowledge base for relevant industry best practices
   - Find any applicable guidance

After gathering data, compile a COMPREHENSIVE REPORT with:
- Executive Summary
- Account Health Score (1-10)
- Key Relationships
- Revenue/Pipeline Summary
- Risk Factors
- Recommended Next Actions

Use tools ONE AT A TIME. Be thorough - this report will be used for strategic planning.`;

    const messages = [
      { role: 'user', content: `Research this company thoroughly: ${companyName}` }
    ];

    let response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      system: systemPrompt,
      tools: tools,
      messages: messages,
    });

    const steps = [];
    let iterations = 0;
    const maxIterations = 20;

    while (response.stop_reason === 'tool_use' && iterations < maxIterations) {
      const toolUseBlocks = response.content.filter((block) => block.type === 'tool_use');
      if (toolUseBlocks.length === 0) break;

      const toolResults = [];
      for (const toolUse of toolUseBlocks) {
        iterations++;
        console.log(`  Step ${iterations}: ${toolUse.name}`);
        
        steps.push({
          step: iterations,
          tool: toolUse.name,
          input: toolUse.input,
        });

        const toolResult = await executeTool(toolUse);
        steps[steps.length - 1].result = toolResult;

        toolResults.push({
          type: 'tool_result',
          tool_use_id: toolUse.id,
          content: JSON.stringify(toolResult),
        });
      }

      messages.push({
        role: 'assistant',
        content: response.content,
      });

      messages.push({
        role: 'user',
        content: toolResults,
      });

      response = await anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        system: systemPrompt,
        tools: tools,
        messages: messages,
      });
    }

    const textContent = response.content.find((block) => block.type === 'text');
    const report = textContent ? textContent.text : 'No report generated';

    console.log(`✅ Account research complete: ${iterations} steps`);

    res.json({
      success: true,
      companyName: companyName,
      report: report,
      steps: steps,
      totalSteps: iterations,
    });
  } catch (error) {
    console.error('❌ Research Agent Error:', error);
    res.status(500).json({
      success: false,
      error: 'Account research failed',
      message: error.message,
    });
  }
});

// ============================================
// HEALTH CHECK
// ============================================

app.get('/api/health', async (req, res) => {
  // Check RAG service health
  let ragStatus = 'unknown';
  try {
    const ragResponse = await fetch(`${RAG_API_URL}/api/rag/health`);
    if (ragResponse.ok) {
      ragStatus = 'connected';
    } else {
      ragStatus = 'error';
    }
  } catch {
    ragStatus = 'disconnected';
  }

  res.json({ 
    status: 'OK', 
    message: 'API server is running',
    ragService: ragStatus,
    endpoints: {
      chat: 'POST /api/chat',
      ragQuery: 'POST /api/rag/query',
      smartAssist: 'POST /api/agent/smart-assist',
      researchAccount: 'POST /api/agent/research-account',
      qualifyLead: 'POST /api/agent/qualify-lead',
      executeAgent: 'POST /api/agent/execute',
    }
  });
});

// ============================================
// START SERVER
// ============================================

app.listen(PORT, () => {
  console.log(`🚀 API Server running on http://localhost:${PORT}`);
  console.log(`📊 Connected to Salesforce org: ${SF_ORG_ALIAS}`);
  console.log(`🔍 RAG Service expected at: ${RAG_API_URL}`);
  console.log(`\n📍 Endpoints:`);
  console.log(`  POST http://localhost:${PORT}/api/chat`);
  console.log(`  POST http://localhost:${PORT}/api/rag/query`);
  console.log(`  POST http://localhost:${PORT}/api/agent/smart-assist`);
  console.log(`  POST http://localhost:${PORT}/api/agent/research-account`);
  console.log(`  POST http://localhost:${PORT}/api/agent/qualify-lead`);
  console.log(`  POST http://localhost:${PORT}/api/agent/execute`);
  console.log(`  GET  http://localhost:${PORT}/api/health\n`);
});
