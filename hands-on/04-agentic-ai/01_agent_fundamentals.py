"""
============================================================
MODULE 4: AGENTIC AI - AUTONOMOUS INTELLIGENT SYSTEMS
============================================================
Time: 90-120 minutes
Goal: Master agentic AI patterns and build sophisticated agents

You already built a Lead Qualification Agent! Now let's understand
the theory and build more advanced systems.

SETUP:
    pip install langchain langchain-anthropic langgraph

============================================================
"""

import os
import json
from typing import List, Dict, Any, Optional

print("="*60)
print("🤖 AGENTIC AI: AUTONOMOUS INTELLIGENT SYSTEMS")
print("="*60)

# ============================================================
# PART 1: WHAT IS AGENTIC AI?
# ============================================================
print("""
┌─────────────────────────────────────────────────────────────┐
│                    WHAT IS AGENTIC AI?                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TRADITIONAL AI (Chat):                                     │
│  User asks → AI responds → Done                             │
│  One turn, no actions, no autonomy                          │
│                                                             │
│  AGENTIC AI:                                                │
│  User gives goal → AI PLANS → EXECUTES → OBSERVES →        │
│  ADJUSTS → Repeats until goal achieved                      │
│                                                             │
│  KEY DIFFERENCES:                                           │
│  ┌─────────────────┬─────────────────────────────────────┐ │
│  │ Traditional     │ Agentic                             │ │
│  ├─────────────────┼─────────────────────────────────────┤ │
│  │ Single response │ Multiple steps                      │ │
│  │ No tools        │ Uses tools (APIs, DBs, etc.)        │ │
│  │ No memory       │ Maintains state                     │ │
│  │ User-driven     │ Goal-driven, autonomous             │ │
│  │ Reactive        │ Proactive                           │ │
│  └─────────────────┴─────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘

YOUR LEAD QUALIFICATION AGENT IS AGENTIC!

What it does:
1. Receives goal: "Qualify this lead"
2. Plans: Need to get lead details, check for existing accounts
3. Executes: Calls sf_query, sf_get_account tools
4. Observes: Analyzes results
5. Decides: Score as Hot/Warm/Cold
6. Acts: Updates the lead record

That's autonomous, multi-step, tool-using AI = AGENT!
""")


# ============================================================
# PART 2: THE AGENT ARCHITECTURE
# ============================================================
print("\n" + "="*60)
print("🏗️ PART 2: AGENT ARCHITECTURE")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                   AGENT COMPONENTS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                      AGENT                            │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │                 LLM (Brain)                     │ │  │
│  │  │  • Reasoning and planning                       │ │  │
│  │  │  • Decision making                              │ │  │
│  │  │  • Natural language understanding               │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │                        │                              │  │
│  │  ┌─────────────────────▼─────────────────────────┐   │  │
│  │  │              TOOLS (Hands)                     │   │  │
│  │  │  • sf_query - Query Salesforce                 │   │  │
│  │  │  • sf_create_record - Create records           │   │  │
│  │  │  • web_search - Search internet                │   │  │
│  │  │  • calculator - Do math                        │   │  │
│  │  │  • ANY API or function!                        │   │  │
│  │  └─────────────────────┬─────────────────────────┘   │  │
│  │                        │                              │  │
│  │  ┌─────────────────────▼─────────────────────────┐   │  │
│  │  │              MEMORY (Context)                  │   │  │
│  │  │  • Conversation history                        │   │  │
│  │  │  • Previous tool results                       │   │  │
│  │  │  • User preferences                            │   │  │
│  │  │  • Long-term knowledge                         │   │  │
│  │  └───────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

THE AGENT LOOP:

    ┌─────────────┐
    │   OBSERVE   │ ← Receive input / tool results
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │   THINK     │ ← Analyze, reason, plan
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │    ACT      │ ← Use tool or respond
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  EVALUATE   │ ← Did it work? Goal achieved?
    └──────┬──────┘
           │
      No   │   Yes
    ┌──────┴──────┐
    │             │
    ▼             ▼
  LOOP         FINISH
""")


# ============================================================
# PART 3: AGENT PATTERNS
# ============================================================
print("\n" + "="*60)
print("📋 PART 3: COMMON AGENT PATTERNS")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                   AGENT PATTERNS                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ReAct (Reasoning + Acting)                              │
│     ─────────────────────────                               │
│     Thought: I need to find the account first               │
│     Action: sf_query("SELECT Id FROM Account WHERE...")     │
│     Observation: Found Account ID 001xxx                    │
│     Thought: Now I can get the opportunities                │
│     Action: sf_query("SELECT ... FROM Opportunity...")      │
│     ...continues until done                                 │
│                                                             │
│     ✅ Your current implementation uses this!               │
│                                                             │
│  2. Plan-and-Execute                                        │
│     ──────────────────                                      │
│     Step 1: Create full plan upfront                        │
│     Step 2: Execute each step in order                      │
│     Step 3: Replan if something fails                       │
│                                                             │
│     Good for: Complex multi-step tasks                      │
│                                                             │
│  3. Tree of Thoughts                                        │
│     ─────────────────                                       │
│     Explore multiple reasoning paths                        │
│     Evaluate each path                                      │
│     Choose best one                                         │
│                                                             │
│     Good for: Complex reasoning, problem solving            │
│                                                             │
│  4. Reflection                                              │
│     ──────────                                              │
│     Agent critiques its own output                          │
│     Improves based on self-feedback                         │
│                                                             │
│     Good for: Quality improvement, accuracy                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# PART 4: BUILD A ReAct AGENT FROM SCRATCH
# ============================================================
print("\n" + "="*60)
print("🛠️ PART 4: BUILD A ReAct AGENT")
print("="*60)

# Define tools (simulated for demo)
TOOLS = {
    "search_accounts": {
        "description": "Search for Salesforce accounts by name",
        "parameters": ["search_term"]
    },
    "get_opportunities": {
        "description": "Get opportunities for an account",
        "parameters": ["account_id"]
    },
    "create_task": {
        "description": "Create a follow-up task",
        "parameters": ["subject", "related_to", "due_date"]
    },
    "send_email": {
        "description": "Send an email to a contact",
        "parameters": ["to", "subject", "body"]
    }
}

# Simulated tool execution
def execute_tool(tool_name: str, params: dict) -> dict:
    """Simulate tool execution"""
    if tool_name == "search_accounts":
        return {
            "success": True,
            "results": [
                {"id": "001ABC", "name": "Acme Corp", "industry": "Technology"},
                {"id": "001DEF", "name": "Acme Industries", "industry": "Manufacturing"}
            ]
        }
    elif tool_name == "get_opportunities":
        return {
            "success": True,
            "results": [
                {"id": "006AAA", "name": "Acme - Enterprise Deal", "amount": 500000, "stage": "Negotiation"},
                {"id": "006BBB", "name": "Acme - Phase 2", "amount": 250000, "stage": "Proposal"}
            ]
        }
    elif tool_name == "create_task":
        return {"success": True, "task_id": "00TXXX", "message": "Task created"}
    elif tool_name == "send_email":
        return {"success": True, "message": "Email sent"}
    return {"success": False, "error": "Unknown tool"}


class SimpleReActAgent:
    """
    A simple ReAct (Reasoning + Acting) agent implementation.
    This mimics what your Express server does with Claude!
    """
    
    def __init__(self, tools: dict, max_iterations: int = 10):
        self.tools = tools
        self.max_iterations = max_iterations
        self.memory = []  # Conversation history
    
    def think(self, goal: str, observations: List[str]) -> dict:
        """
        Simulate the LLM's reasoning process.
        In real implementation, this calls Claude API.
        """
        # Build context
        context = f"Goal: {goal}\n\n"
        if observations:
            context += "Previous observations:\n"
            for obs in observations:
                context += f"- {obs}\n"
        
        context += f"\nAvailable tools: {list(self.tools.keys())}"
        
        # In reality, you'd call Claude here:
        # response = anthropic.messages.create(
        #     model="claude-sonnet-4-20250514",
        #     tools=self.tools,
        #     messages=[{"role": "user", "content": context}]
        # )
        
        # Simulated reasoning for demo
        if not observations:
            return {
                "thought": "I need to search for the account first",
                "action": "search_accounts",
                "params": {"search_term": "Acme"}
            }
        elif len(observations) == 1:
            return {
                "thought": "Found accounts. Now let me check opportunities for Acme Corp",
                "action": "get_opportunities",
                "params": {"account_id": "001ABC"}
            }
        elif len(observations) == 2:
            return {
                "thought": "Found $750k in pipeline. I should create a follow-up task.",
                "action": "create_task",
                "params": {
                    "subject": "Follow up on Acme opportunities",
                    "related_to": "001ABC",
                    "due_date": "2024-01-15"
                }
            }
        else:
            return {
                "thought": "Task created. Goal achieved!",
                "action": None,
                "final_answer": "Found Acme Corp with $750,000 in pipeline (2 opportunities). Created follow-up task."
            }
    
    def run(self, goal: str) -> dict:
        """Execute the agent loop"""
        print(f"\n🎯 GOAL: {goal}\n")
        print("-" * 50)
        
        observations = []
        
        for i in range(self.max_iterations):
            # THINK
            decision = self.think(goal, observations)
            print(f"\n💭 THOUGHT: {decision['thought']}")
            
            # Check if done
            if decision.get('action') is None:
                print(f"\n✅ FINAL ANSWER: {decision['final_answer']}")
                return {
                    "success": True,
                    "answer": decision['final_answer'],
                    "steps": len(observations)
                }
            
            # ACT
            print(f"🔧 ACTION: {decision['action']}({decision['params']})")
            result = execute_tool(decision['action'], decision['params'])
            
            # OBSERVE
            observation = f"{decision['action']} returned: {result}"
            observations.append(observation)
            print(f"👁️ OBSERVATION: {result}")
        
        return {"success": False, "error": "Max iterations reached"}


# Run the agent
print("\n--- RUNNING ReAct AGENT ---")
agent = SimpleReActAgent(TOOLS)
result = agent.run("Find information about Acme company and create a follow-up task")

print(f"\n--- AGENT RESULT ---")
print(f"Success: {result['success']}")
print(f"Steps taken: {result.get('steps', 'N/A')}")


# ============================================================
# PART 5: YOUR EXISTING AGENT (CODE REVIEW)
# ============================================================
print("\n" + "="*60)
print("🔍 PART 5: YOUR LEAD QUALIFICATION AGENT")
print("="*60)

print("""
Let's analyze your existing agent in index.js:

YOUR AGENT ENDPOINT:
```javascript
app.post('/api/agent/qualify-lead', async (req, res) => {
    const { leadId } = req.body;
    
    // SYSTEM PROMPT - Defines agent's goal and behavior
    const agenticPrompt = `You are a lead qualification agent...
        1. Get the lead details
        2. Search for existing accounts
        3. Check for past opportunities
        4. Analyze and score
        5. Update the lead`;
    
    // AGENT LOOP
    while (response.stop_reason === 'tool_use' && iterations < maxIterations) {
        // Get tool request from Claude
        const toolUse = response.content.find(block => block.type === 'tool_use');
        
        // Execute the tool
        const toolResult = await executeTool(toolUse);
        
        // Send result back to Claude
        messages.push({role: 'user', content: [{
            type: 'tool_result',
            tool_use_id: toolUse.id,
            content: JSON.stringify(toolResult)
        }]});
        
        // Get next decision from Claude
        response = await anthropic.messages.create({...});
    }
});
```

THIS IS A PROPER ReAct AGENT!

✅ Goal-driven (qualify the lead)
✅ Multi-step (queries, analysis, updates)
✅ Tool-using (sf_query, sf_update_record, etc.)
✅ Autonomous (Claude decides what to do next)
✅ Observable (you log each step)

IMPROVEMENTS YOU COULD MAKE:
1. Add memory persistence (store agent history)
2. Add error recovery (retry failed tool calls)
3. Add human-in-the-loop (pause for approval on updates)
4. Add parallel tool execution (multiple queries at once)
""")


# ============================================================
# PART 6: MULTI-AGENT SYSTEMS
# ============================================================
print("\n" + "="*60)
print("👥 PART 6: MULTI-AGENT SYSTEMS")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                  MULTI-AGENT SYSTEMS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Instead of ONE agent doing everything, multiple            │
│  SPECIALIZED agents collaborate.                            │
│                                                             │
│  EXAMPLE: Sales Intelligence Team                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   ORCHESTRATOR                       │   │
│  │            (Coordinates the team)                    │   │
│  └───────────────────────┬─────────────────────────────┘   │
│                          │                                  │
│          ┌───────────────┼───────────────┐                 │
│          │               │               │                  │
│          ▼               ▼               ▼                  │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐     │
│  │  RESEARCHER   │ │   ANALYST     │ │    WRITER     │     │
│  │               │ │               │ │               │     │
│  │ • Web search  │ │ • Data query  │ │ • Draft emails│     │
│  │ • Company info│ │ • Scoring     │ │ • Reports     │     │
│  │ • News        │ │ • Trends      │ │ • Summaries   │     │
│  └───────────────┘ └───────────────┘ └───────────────┘     │
│                                                             │
│  WORKFLOW:                                                  │
│  1. Orchestrator receives "Research Acme Corp"              │
│  2. Assigns Researcher to gather company info               │
│  3. Researcher returns findings                             │
│  4. Assigns Analyst to score the opportunity                │
│  5. Analyst returns score + reasoning                       │
│  6. Assigns Writer to draft outreach email                  │
│  7. Writer returns personalized email                       │
│  8. Orchestrator compiles final report                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

FRAMEWORKS FOR MULTI-AGENT:
• CrewAI - Easy to use, role-based
• AutoGen (Microsoft) - Conversational agents
• LangGraph - Graph-based workflows
• Agency Swarm - Production-ready
""")


# Simple multi-agent example
class Agent:
    def __init__(self, name: str, role: str, skills: List[str]):
        self.name = name
        self.role = role
        self.skills = skills
    
    def execute(self, task: str) -> str:
        """Simulate agent execution"""
        return f"[{self.name}] Completed: {task}"


class MultiAgentTeam:
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, agent: Agent):
        self.agents[agent.role] = agent
    
    def delegate(self, task: str, role: str) -> str:
        if role in self.agents:
            return self.agents[role].execute(task)
        return f"No agent for role: {role}"
    
    def run_workflow(self, goal: str) -> List[str]:
        """Run a simple sequential workflow"""
        results = []
        
        # Step 1: Research
        results.append(self.delegate("Gather company information", "researcher"))
        
        # Step 2: Analyze
        results.append(self.delegate("Score and analyze the data", "analyst"))
        
        # Step 3: Write
        results.append(self.delegate("Draft outreach email", "writer"))
        
        return results


# Demo
print("\n--- MULTI-AGENT DEMO ---")
team = MultiAgentTeam()
team.add_agent(Agent("Alex", "researcher", ["web_search", "company_lookup"]))
team.add_agent(Agent("Jordan", "analyst", ["data_analysis", "scoring"]))
team.add_agent(Agent("Sam", "writer", ["email_drafting", "reporting"]))

results = team.run_workflow("Prepare outreach for Acme Corp")
for result in results:
    print(result)


# ============================================================
# PART 7: AGENT + RAG COMBINATION
# ============================================================
print("\n" + "="*60)
print("🔗 PART 7: COMBINING AGENTS WITH RAG")
print("="*60)

print("""
THE POWER COMBINATION: Agent + RAG

┌─────────────────────────────────────────────────────────────┐
│                    RAG-ENHANCED AGENT                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User: "How should I approach the Acme renewal?"            │
│                                                             │
│  AGENT WORKFLOW:                                            │
│                                                             │
│  Step 1: RETRIEVE from Salesforce                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tool: sf_query                                       │   │
│  │ Get: Account details, opportunity history,           │   │
│  │      past communications, support tickets            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Step 2: RETRIEVE from Knowledge Base (RAG)                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tool: rag_search                                     │   │
│  │ Get: Best practices for renewals, similar deals,     │   │
│  │      competitor intel, pricing guidelines            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Step 3: ANALYZE & SYNTHESIZE                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ LLM combines:                                        │   │
│  │ • Acme's history ($2M account, 3 years)              │   │
│  │ • Their recent support issues (resolved)             │   │
│  │ • Industry best practices from KB                    │   │
│  │ • Similar successful renewals                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Step 4: GENERATE PERSONALIZED RECOMMENDATION               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "Based on Acme's history and our playbook:           │   │
│  │  1. Lead with the support improvements               │   │
│  │  2. Offer multi-year discount (they value stability) │   │
│  │  3. Highlight new features relevant to tech industry │   │
│  │  Similar approach worked with TechCorp (won $1.5M)"  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

THIS IS YOUR NEXT PROJECT!

Add a RAG tool to your agent:
1. Index your Salesforce Knowledge Articles
2. Create a 'rag_search' tool
3. Agent can now query both live data AND knowledge base
""")


# ============================================================
# PART 8: AGENT SAFETY & GUARDRAILS
# ============================================================
print("\n" + "="*60)
print("🛡️ PART 8: AGENT SAFETY & GUARDRAILS")
print("="*60)

print("""
CRITICAL: Agents can take REAL ACTIONS!

YOUR AGENT CAN:
• Query data (safe)
• CREATE records (careful!)
• UPDATE records (dangerous!)
• DELETE records (very dangerous!)

GUARDRAILS TO IMPLEMENT:

1. APPROVAL GATES
   ─────────────
   Before destructive actions, pause for human approval:
   
   if (action.type === 'update' || action.type === 'delete') {
       return { needs_approval: true, action: action };
   }

2. SANDBOXING
   ──────────
   • Test in sandbox first
   • Use separate API credentials with limited permissions
   • Never give agent admin access

3. RATE LIMITING
   ─────────────
   • Limit iterations (you have maxIterations = 20)
   • Limit records affected per run
   • Limit API calls per minute

4. AUDIT LOGGING
   ─────────────
   Log EVERYTHING:
   • What actions were taken
   • What data was accessed
   • What was modified
   • Who initiated the agent

5. ROLLBACK CAPABILITY
   ───────────────────
   • Store previous state before updates
   • Ability to undo agent actions
   • Version history

6. SCOPE LIMITATION
   ────────────────
   • Agent should only access relevant objects
   • Define explicit tool boundaries
   • No arbitrary code execution

YOUR CODE ALREADY HAS SOME GUARDRAILS:
✅ maxIterations = 20 (prevents infinite loops)
✅ Logging each step
✅ Specific tool definitions (no arbitrary queries)

ADD THESE:
⬜ Approval for updates
⬜ Record limit per operation
⬜ Error recovery
""")


# ============================================================
# PART 9: HANDS-ON PROJECT
# ============================================================
print("\n" + "="*60)
print("🎯 PART 9: HANDS-ON PROJECT")
print("="*60)

print("""
PROJECT: BUILD A SALESFORCE RESEARCH AGENT

Enhance your existing API server with a new agent that:

1. Takes a company name as input
2. Searches Salesforce for matching accounts
3. Gets all related opportunities, contacts, cases
4. Queries your RAG knowledge base for industry insights
5. Generates a comprehensive account summary
6. Optionally creates a Task with recommended actions

NEW ENDPOINT:
```javascript
app.post('/api/agent/research-account', async (req, res) => {
    const { companyName } = req.body;
    
    const prompt = `You are an account research agent.
    
    Research "${companyName}" by:
    1. Search for the account in Salesforce
    2. Get all opportunities (open and closed)
    3. Get all contacts and their roles
    4. Get recent cases/support tickets
    5. Search knowledge base for industry insights
    6. Compile a comprehensive summary with:
       - Account health score (1-10)
       - Key relationships
       - Revenue history
       - Risk factors
       - Recommended actions
    
    Be thorough and use multiple queries.`;
    
    // ... agent loop
});
```

NEW TOOLS TO ADD:
```javascript
{
    name: 'sf_get_contacts',
    description: 'Get all contacts for an account',
    input_schema: {
        type: 'object',
        properties: {
            accountId: { type: 'string' }
        }
    }
},
{
    name: 'sf_get_cases',
    description: 'Get support cases for an account',
    input_schema: {
        type: 'object',
        properties: {
            accountId: { type: 'string' }
        }
    }
},
{
    name: 'rag_search',
    description: 'Search knowledge base for relevant information',
    input_schema: {
        type: 'object',
        properties: {
            query: { type: 'string' }
        }
    }
}
```

TRY IT:
1. Add these tools to your index.js
2. Implement the tool handlers
3. Create the new endpoint
4. Test with a real account from your sandbox
""")


# ============================================================
# 🏆 INTERVIEW QUESTIONS
# ============================================================
print("\n" + "="*60)
print("🏆 AGENTIC AI INTERVIEW QUESTIONS")
print("="*60)

print("""
1. What is an AI agent?
   → Autonomous system that uses LLM + tools to achieve goals
   → Makes decisions, takes actions, observes results
   → Loops until goal is achieved

2. What is the ReAct pattern?
   → Reasoning + Acting
   → Think → Act → Observe → Repeat
   → Most common agent pattern

3. How do agents use tools?
   → LLM outputs structured tool calls
   → System executes tool, returns result
   → LLM processes result, decides next action

4. What's the difference between a chatbot and an agent?
   → Chatbot: Single response, no actions
   → Agent: Multi-step, uses tools, autonomous

5. What are the risks of AI agents?
   → Unintended actions, data modification
   → Infinite loops, runaway costs
   → Security vulnerabilities

6. How do you make agents safe?
   → Approval gates, sandboxing, rate limits
   → Audit logging, rollback capability
   → Scope limitation, least privilege

7. What is a multi-agent system?
   → Multiple specialized agents collaborating
   → Each agent has specific role/skills
   → Orchestrator coordinates the team

8. How do you combine RAG with agents?
   → RAG tool for knowledge retrieval
   → Agent decides when to query knowledge base
   → Combines live data with static knowledge

9. What is LangGraph?
   → Graph-based agent orchestration
   → Defines agent workflows as state machines
   → Better control flow than simple loops

10. When should you use agents vs simple prompts?
    → Agents: Complex tasks, multiple steps, tool use
    → Simple prompts: Q&A, generation, single-turn
""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 AGENTIC AI MODULE COMPLETE!")
print("="*60)
print("""
You now understand:
✅ What makes AI "agentic" (autonomous, tool-using, goal-driven)
✅ Agent architecture (LLM + Tools + Memory)
✅ ReAct pattern (your current implementation!)
✅ Multi-agent systems
✅ Combining RAG with agents
✅ Safety and guardrails
✅ How to build sophisticated agents

YOUR EXISTING WORK:
• Lead Qualification Agent ✅
• Tool-calling infrastructure ✅
• Agent loop implementation ✅

NEXT ENHANCEMENTS:
1. Add RAG tool to your agent
2. Build Account Research Agent
3. Add approval gates for updates
4. Implement multi-agent workflows

NEXT MODULE:
python3 hands-on/05-advanced-patterns/01_langgraph_workflows.py
(Coming next!)
""")
