"""
============================================================
MODULE 2: GENAI FUNDAMENTALS - HOW LLMS REALLY WORK
============================================================
Time: 60-90 minutes
Goal: Deep understanding of LLMs for interviews + practical work

This module answers:
- What is a Large Language Model?
- How do Transformers work?
- What are embeddings and tokens?
- Prompt engineering best practices

SETUP:
    pip install anthropic openai tiktoken

HOW TO RUN:
    source ../venv/bin/activate
    export ANTHROPIC_API_KEY="your-key-here"
    python3 01_how_llms_work.py
============================================================
"""

import os
import json

# ============================================================
# PART 1: WHAT IS A LARGE LANGUAGE MODEL?
# ============================================================
print("="*60)
print("🧠 PART 1: WHAT IS A LARGE LANGUAGE MODEL?")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                 LARGE LANGUAGE MODEL (LLM)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Definition:                                                │
│  A neural network trained on MASSIVE amounts of text        │
│  to predict "what word comes next"                          │
│                                                             │
│  Examples:                                                  │
│  • GPT-4 (OpenAI)       - 1.7 trillion parameters          │
│  • Claude (Anthropic)   - Unknown, but very large          │
│  • LLaMA (Meta)         - 7B to 70B parameters             │
│  • Gemini (Google)      - Unknown                           │
│                                                             │
│  Key Insight:                                               │
│  Despite "just predicting next words", these models         │
│  emerge with reasoning, coding, and creative abilities      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

ANALOGY FOR SALESFORCE DEVELOPERS:
Think of an LLM like an extremely well-read colleague who:
• Has read every Salesforce doc ever written
• Has seen millions of code examples
• Can adapt their response based on how you ask
• Doesn't actually "know" anything - predicts likely responses

THE TRAINING PROCESS:
1. Collect MASSIVE text data (internet, books, code)
2. Train model to predict next token
3. Fine-tune on instruction-following
4. RLHF (Reinforcement Learning from Human Feedback)
5. Result: Model that can follow instructions and chat
""")


# ============================================================
# PART 2: TOKENS - THE LANGUAGE OF LLMS
# ============================================================
print("\n" + "="*60)
print("🔤 PART 2: TOKENS - HOW LLMS SEE TEXT")
print("="*60)

try:
    import tiktoken
    
    # GPT-4 tokenizer (similar to Claude's)
    encoder = tiktoken.get_encoding("cl100k_base")
    
    # Examples
    examples = [
        "Hello, world!",
        "Salesforce",
        "SELECT Id, Name FROM Account WHERE Industry = 'Technology'",
        "The quick brown fox jumps over the lazy dog.",
        "🚀 AI is amazing!",
    ]
    
    print("\nTokenization Examples:")
    print("-" * 50)
    
    for text in examples:
        tokens = encoder.encode(text)
        print(f"\nText: '{text}'")
        print(f"Tokens: {tokens}")
        print(f"Token count: {len(tokens)}")
        print(f"Decoded: {[encoder.decode([t]) for t in tokens]}")
    
    print("""
\n📊 TOKEN INSIGHTS:
• Common words = 1 token (the, is, and)
• Long/rare words = multiple tokens (Salesforce = 2-3 tokens)
• Spaces often included with words
• Code gets tokenized differently than English
• Emojis = multiple tokens
    
💰 WHY TOKENS MATTER:
• API pricing is per token (input + output)
• Context window limits (Claude: 100K-200K tokens)
• Longer prompts = more cost + latency
• Token efficiency = cost optimization
""")
    
except ImportError:
    print("Install tiktoken to see tokenization: pip install tiktoken")


# ============================================================
# PART 3: EMBEDDINGS - MEANING AS NUMBERS
# ============================================================
print("\n" + "="*60)
print("📊 PART 3: EMBEDDINGS - MEANING AS NUMBERS")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                    WHAT ARE EMBEDDINGS?                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Embeddings convert text into numerical vectors            │
│  that capture SEMANTIC MEANING                              │
│                                                             │
│  "King" → [0.2, 0.8, 0.1, 0.9, ...]  (1536 dimensions)     │
│  "Queen" → [0.25, 0.75, 0.15, 0.85, ...]                   │
│  "Apple" → [0.9, 0.1, 0.8, 0.2, ...]                        │
│                                                             │
│  Similar meanings = Similar vectors = Close in space        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

WHY EMBEDDINGS ARE CRITICAL FOR AI:
1. Semantic Search (RAG) - Find similar documents
2. Clustering - Group similar items
3. Classification - Categorize text
4. Recommendations - Find related content

THE FAMOUS EXAMPLE:
king - man + woman ≈ queen

This works because embeddings capture relationships!
""")

# Demonstrate with NumPy (simplified)
import numpy as np

# Simplified 4D embeddings for demonstration
embeddings = {
    "Salesforce": np.array([0.9, 0.2, 0.8, 0.3]),      # CRM, tech
    "HubSpot": np.array([0.85, 0.25, 0.75, 0.35]),     # Similar CRM
    "Python": np.array([0.3, 0.9, 0.4, 0.7]),          # Programming
    "JavaScript": np.array([0.35, 0.85, 0.45, 0.65]),  # Similar programming
    "Pizza": np.array([0.1, 0.1, 0.2, 0.9]),           # Food, unrelated
}

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\nEmbedding Similarities (Simplified Demo):")
print("-" * 50)

query = "Salesforce"
print(f"\nQuery: '{query}'")
print(f"Finding similar items...\n")

similarities = []
for word, vec in embeddings.items():
    if word != query:
        sim = cosine_similarity(embeddings[query], vec)
        similarities.append((word, sim))

similarities.sort(key=lambda x: x[1], reverse=True)
for word, sim in similarities:
    bar = "█" * int(sim * 30)
    print(f"  {word:15} {bar} {sim:.3f}")


# ============================================================
# PART 4: THE TRANSFORMER ARCHITECTURE
# ============================================================
print("\n" + "="*60)
print("🔧 PART 4: HOW TRANSFORMERS WORK")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│              THE TRANSFORMER (2017 - "Attention is All")   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     ┌──────────────┐                        │
│   Input Text  ───>  │  Tokenizer   │ ───> Tokens            │
│                     └──────────────┘                        │
│                            │                                │
│                            ▼                                │
│                     ┌──────────────┐                        │
│                     │  Embeddings  │ ───> Vectors           │
│                     └──────────────┘                        │
│                            │                                │
│                            ▼                                │
│   ┌────────────────────────────────────────────────────┐   │
│   │           TRANSFORMER LAYERS (96+ layers)           │   │
│   │  ┌─────────────────────────────────────────────┐   │   │
│   │  │  Self-Attention: "What should I focus on?"   │   │   │
│   │  │  Each token "looks at" all other tokens      │   │   │
│   │  └─────────────────────────────────────────────┘   │   │
│   │                        │                            │   │
│   │  ┌─────────────────────────────────────────────┐   │   │
│   │  │  Feed Forward: Process the information       │   │   │
│   │  └─────────────────────────────────────────────┘   │   │
│   │                        │                            │   │
│   │        (Repeat 96+ times with residual connections) │   │
│   └────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│                     ┌──────────────┐                        │
│                     │  Output Head │ ───> Next Token Probs  │
│                     └──────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

🔑 THE KEY INNOVATION: SELF-ATTENTION

When processing "The cat sat on the mat":
• "sat" needs to know about "cat" (who sat?)
• "mat" needs to know about "sat" and "on" (sat where?)

Attention lets each word "attend to" relevant other words,
regardless of their distance in the sentence.

This is why LLMs can:
• Understand context across long documents
• Maintain coherent conversations
• Follow complex instructions
""")


# ============================================================
# PART 5: USING THE ANTHROPIC API
# ============================================================
print("\n" + "="*60)
print("💻 PART 5: ANTHROPIC API - HANDS ON")
print("="*60)

# Check for API key
api_key = os.environ.get('ANTHROPIC_API_KEY')

if api_key:
    from anthropic import Anthropic
    
    client = Anthropic(api_key=api_key)
    
    # Basic completion
    print("\n--- Basic Message ---")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[
            {"role": "user", "content": "Explain what an LLM is in one sentence."}
        ]
    )
    print(f"Response: {response.content[0].text}")
    print(f"\nUsage: {response.usage.input_tokens} input, {response.usage.output_tokens} output tokens")
    
    # With system prompt
    print("\n--- With System Prompt ---")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system="You are a Salesforce expert. Be concise.",
        messages=[
            {"role": "user", "content": "What's the difference between a Lead and an Opportunity?"}
        ]
    )
    print(f"Response: {response.content[0].text}")
    
    # Multi-turn conversation
    print("\n--- Multi-turn Conversation ---")
    messages = [
        {"role": "user", "content": "I'm building a lead scoring system."},
        {"role": "assistant", "content": "That's a great project! Lead scoring helps prioritize which leads to focus on. What criteria are you thinking of using?"},
        {"role": "user", "content": "Company size and engagement. Can you suggest a simple scoring formula?"}
    ]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=messages
    )
    print(f"Response: {response.content[0].text}")
    
else:
    print("""
⚠️  ANTHROPIC_API_KEY not found in environment!

To run API examples:
1. Get your API key from console.anthropic.com
2. Set it: export ANTHROPIC_API_KEY="your-key-here"
3. Re-run this script

For now, here's what the API calls look like:
""")
    
    print("""
# Basic API call structure:
from anthropic import Anthropic

client = Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="Optional system prompt",
    messages=[
        {"role": "user", "content": "Your message here"}
    ]
)

print(response.content[0].text)
""")


# ============================================================
# PART 6: PROMPT ENGINEERING
# ============================================================
print("\n" + "="*60)
print("🎯 PART 6: PROMPT ENGINEERING BEST PRACTICES")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│              PROMPT ENGINEERING PRINCIPLES                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. BE SPECIFIC AND CLEAR                                   │
│     ❌ "Help me with leads"                                 │
│     ✅ "Analyze this lead and score it 1-100 based on..."  │
│                                                             │
│  2. PROVIDE CONTEXT                                         │
│     ❌ "Write code"                                         │
│     ✅ "Write a Python function that calls the Salesforce  │
│        REST API to create a new Account record"             │
│                                                             │
│  3. USE EXAMPLES (Few-shot learning)                        │
│     "Here's an example of the format I want:                │
│      Input: 'Acme Corp' → Output: 'ACME_CORP'"              │
│                                                             │
│  4. SPECIFY OUTPUT FORMAT                                   │
│     "Return your answer as JSON with keys: score, reason"  │
│                                                             │
│  5. BREAK DOWN COMPLEX TASKS                                │
│     "First analyze X, then based on that, do Y"            │
│                                                             │
│  6. ASK FOR REASONING                                       │
│     "Think step by step before giving your final answer"   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Prompt templates
print("\n--- PROMPT TEMPLATES FOR COMMON TASKS ---\n")

prompts = {
    "Lead Scoring": '''
You are a lead qualification expert. Analyze this lead and provide a score.

Lead Data:
- Company: {company}
- Industry: {industry}
- Employees: {employees}
- Lead Source: {source}

Scoring Criteria:
- Company size (>500 employees = +30 points)
- Technology or Finance industry = +20 points
- Referral source = +20 points
- Has complete contact info = +30 points

Return JSON: {"score": 0-100, "rating": "Hot/Warm/Cold", "reasoning": "..."}
''',
    
    "SOQL Generator": '''
You are a Salesforce SOQL expert. Generate a SOQL query based on the request.

Request: {request}

Rules:
- Use proper SOQL syntax
- Include only necessary fields
- Add appropriate LIMIT
- Handle relationships correctly

Return only the SOQL query, no explanation.
''',
    
    "Apex Code Review": '''
You are a senior Salesforce developer reviewing Apex code.

Code to review:
```apex
{code}
```

Analyze for:
1. Governor limit issues
2. Bulkification problems
3. Security vulnerabilities
4. Best practice violations

Provide specific, actionable feedback.
''',
    
    "Data Extraction": '''
Extract structured data from this text.

Text: {text}

Extract:
- Company names
- Contact names
- Email addresses
- Phone numbers
- Any mentioned amounts

Return as JSON array.
'''
}

for name, template in prompts.items():
    print(f"📋 {name}:")
    print("-" * 40)
    print(template[:200] + "..." if len(template) > 200 else template)
    print()


# ============================================================
# PART 7: TEMPERATURE AND PARAMETERS
# ============================================================
print("\n" + "="*60)
print("🌡️ PART 7: MODEL PARAMETERS")
print("="*60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                 KEY MODEL PARAMETERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TEMPERATURE (0.0 - 1.0)                                    │
│  Controls randomness/creativity                             │
│                                                             │
│  0.0  ████░░░░░░  Deterministic, focused, same output      │
│       Best for: Code, data extraction, factual answers     │
│                                                             │
│  0.5  █████████░  Balanced, some variety                    │
│       Best for: General tasks, conversations               │
│                                                             │
│  1.0  ██████████  Creative, varied, sometimes wild         │
│       Best for: Creative writing, brainstorming            │
│                                                             │
│  MAX_TOKENS                                                 │
│  Maximum output length                                      │
│  • 100 tokens ≈ 75 words                                    │
│  • Set based on expected response length                    │
│  • Higher = more cost but allows longer responses           │
│                                                             │
│  TOP_P (0.0 - 1.0)                                          │
│  Nucleus sampling - alternative to temperature              │
│  Usually use one or the other, not both                     │
│                                                             │
│  STOP SEQUENCES                                             │
│  Tokens that end generation                                 │
│  Useful for structured outputs                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# PART 8: CONNECTING TO YOUR EXISTING WORK
# ============================================================
print("\n" + "="*60)
print("🔗 PART 8: CONNECTING TO YOUR MCP SERVER")
print("="*60)

print("""
You've already built an API server that uses Claude with tools!
Let's understand what's happening under the hood:

YOUR CURRENT ARCHITECTURE:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Salesforce  │────▶│  API Server  │────▶│   Claude     │
│     LWC      │◀────│  (Express)   │◀────│   (Tool Use) │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Salesforce  │
                     │   CLI/API    │
                     └──────────────┘

WHAT HAPPENS WHEN USER SENDS MESSAGE:
1. LWC sends message to your API server
2. API server sends to Claude with tool definitions
3. Claude decides if it needs to use tools
4. If yes: Returns tool_use, your server executes it
5. Tool result sent back to Claude
6. Claude generates final response
7. Response sent back to LWC

THIS IS AGENTIC AI IN ACTION!
Claude is making decisions about what actions to take.
""")

# Show how their current code works
print("""
YOUR TOOL DEFINITION (from index.js):
```javascript
{
    name: 'sf_query',
    description: 'Execute a SOQL query on Salesforce',
    input_schema: {
        type: 'object',
        properties: {
            query: {
                type: 'string',
                description: 'The SOQL query to execute'
            }
        },
        required: ['query']
    }
}
```

CLAUDE'S RESPONSE WHEN IT WANTS TO USE A TOOL:
```json
{
    "type": "tool_use",
    "id": "toolu_123",
    "name": "sf_query",
    "input": {
        "query": "SELECT Id, Name FROM Account LIMIT 5"
    }
}
```

Your server executes the query, returns results, and Claude
uses those results to generate a helpful response.
""")


# ============================================================
# 🎯 PRACTICE EXERCISES
# ============================================================
print("\n" + "="*60)
print("🎯 PRACTICE EXERCISES")
print("="*60)

print("""
EXERCISE 1: Token Counting
--------------------------
Write a function that estimates token count for API cost calculation.
Approximate: 1 token ≈ 4 characters (rough estimate)

def estimate_tokens(text: str) -> int:
    # Your code here
    pass

Test with your Salesforce SOQL queries to estimate API costs.


EXERCISE 2: Embedding Similarity Search
---------------------------------------
Create a simple semantic search using embeddings:

documents = [
    "How to create a new Account in Salesforce",
    "Lead conversion process and best practices",
    "Opportunity pipeline management guide",
    "Setting up Einstein Analytics dashboards",
    "Apex trigger best practices for bulk operations"
]

query = "I need help with sales pipeline"

# Find the most relevant document
# (Use OpenAI or Anthropic embeddings API, or simplified cosine similarity)


EXERCISE 3: Prompt Engineering
------------------------------
Create prompts for these Salesforce tasks:
1. Generate SOQL query from natural language
2. Explain Apex code to a non-developer
3. Suggest fields for a custom object based on requirements
4. Review a Flow for best practices


EXERCISE 4: Add a New Tool to Your Server
-----------------------------------------
Add a tool to your Express server that:
1. Searches for duplicate leads by email
2. Takes email as input
3. Returns matching leads with similarity score

Update both tool definition and execution handler.


EXERCISE 5: Multi-turn Context
------------------------------
Modify your chat endpoint to maintain context better:
1. Summarize long conversations
2. Extract key facts mentioned
3. Use system prompt to maintain context
""")


# ============================================================
# 🏆 INTERVIEW QUESTIONS
# ============================================================
print("\n" + "="*60)
print("🏆 INTERVIEW QUESTIONS")
print("="*60)

print("""
1. What is a Large Language Model?
   → Neural network trained on text to predict next token
   → Emerges with language understanding and reasoning abilities

2. What is the difference between GPT and BERT?
   → GPT: Decoder-only, autoregressive, generates text
   → BERT: Encoder-only, bidirectional, understands text

3. What are embeddings and why are they useful?
   → Dense vector representations of text
   → Capture semantic meaning, enable similarity search

4. Explain the concept of "temperature" in LLMs.
   → Controls randomness in output
   → 0 = deterministic, 1 = creative

5. What is the context window?
   → Maximum tokens model can process at once
   → Claude: 100K-200K, GPT-4: 8K-128K

6. What is prompt engineering?
   → Crafting inputs to get desired outputs
   → Includes examples, format specification, reasoning

7. What is chain-of-thought prompting?
   → Asking model to show reasoning steps
   → Improves accuracy on complex tasks

8. What is fine-tuning vs prompt engineering?
   → Fine-tuning: Train model on specific data
   → Prompt engineering: Craft better inputs

9. How do you handle long documents that exceed context?
   → Chunking, summarization, RAG

10. What are the limitations of LLMs?
    → Hallucination, knowledge cutoff, reasoning limits
    → No real-time data, can be manipulated
""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 GENAI FUNDAMENTALS COMPLETE!")
print("="*60)
print("""
You now understand:
✅ How LLMs work (Transformers, attention)
✅ Tokens and embeddings
✅ Using the Anthropic API
✅ Prompt engineering best practices
✅ Model parameters (temperature, max_tokens)
✅ How your MCP server integrates with Claude

NEXT: Move to:
• 02_langchain_basics.py - Framework for AI applications
• 03_tool_use_deep_dive.py - Advanced function calling
• Then: RAG Systems (the most in-demand skill!)
""")
