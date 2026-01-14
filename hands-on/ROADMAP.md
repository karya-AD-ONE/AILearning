# 🚀 AI ENGINEERING HANDS-ON CURRICULUM
## Complete 2-Month Fast-Track Learning Path

**Goal:** Transition from Salesforce Developer/Architect to Advanced AI Engineer  
**Approach:** 100% Hands-on, Build-First Learning  
**Starting Point:** You already have working MCP server + API + LWC integration!

---

## 📊 YOUR CURRENT PROGRESS

### ✅ Already Completed (From Previous Work)
- [x] MCP Server with Salesforce integration
- [x] Express API Server with Claude tool calling
- [x] LWC Chat component deployed
- [x] Basic agentic workflow (Lead Qualification Agent)
- [x] End-to-end AI + Salesforce integration

### 🔴 Gaps to Fill
- [ ] Python fundamentals for AI
- [ ] ML/Data Science basics
- [ ] Deep GenAI understanding
- [ ] RAG Systems
- [ ] Advanced Agentic AI
- [ ] Production deployment

---

## 📚 MODULE STRUCTURE

```
hands-on/
│
├── 01-python-essentials/           ⏱️ 2-3 hours
│   ├── 01_python_for_js_devs.py    ✅ Created
│   ├── 02_numpy_pandas_basics.py   ✅ Created
│   └── 03_first_ml_model.py        ✅ Created
│
├── 02-genai-fundamentals/          ⏱️ 3-4 hours
│   ├── 01_how_llms_work.py         ✅ Created
│   ├── 02_langchain_basics.py      📝 Coming next
│   └── 03_tool_use_deep_dive.py    📝 Coming next
│
├── 03-rag-systems/                 ⏱️ 4-6 hours
│   ├── 01_rag_fundamentals.py      ✅ Created
│   ├── 02_advanced_rag.py          📝 Coming next
│   └── 03_salesforce_rag.py        📝 Coming next
│
├── 04-agentic-ai/                  ⏱️ 4-6 hours
│   ├── 01_agent_fundamentals.py    📝 Coming next
│   ├── 02_langchain_agents.py      📝 Coming next
│   ├── 03_multi_agent_systems.py   📝 Coming next
│   └── 04_crewai_tutorial.py       📝 Coming next
│
├── 05-mcp-advanced/                ⏱️ 2-3 hours
│   ├── 01_mcp_deep_dive.py         📝 Coming next
│   └── 02_rag_mcp_server.py        📝 Coming next
│
└── 06-capstone-project/            ⏱️ 8-10 hours
    └── salesforce_ai_platform/     📝 Final project
```

---

## 🗓️ 8-WEEK SCHEDULE

### WEEK 1-2: FOUNDATIONS
| Day | Module | Time | Status |
|-----|--------|------|--------|
| 1 | Python for JS Devs | 1h | ⬜ |
| 2 | NumPy & Pandas | 1.5h | ⬜ |
| 3 | First ML Model | 1.5h | ⬜ |
| 4 | How LLMs Work | 1.5h | ⬜ |
| 5 | LangChain Basics | 2h | ⬜ |
| 6-7 | Review + Exercises | 2h | ⬜ |

### WEEK 3-4: RAG SYSTEMS (CRITICAL!)
| Day | Module | Time | Status |
|-----|--------|------|--------|
| 8 | RAG Fundamentals | 2h | ⬜ |
| 9 | Vector Databases | 2h | ⬜ |
| 10 | Advanced RAG | 2h | ⬜ |
| 11-12 | Salesforce RAG Project | 4h | ⬜ |
| 13-14 | RAG Evaluation + Polish | 3h | ⬜ |

### WEEK 5-6: AGENTIC AI
| Day | Module | Time | Status |
|-----|--------|------|--------|
| 15 | Agent Fundamentals | 2h | ⬜ |
| 16 | LangChain Agents | 2h | ⬜ |
| 17 | Multi-Agent Systems | 2h | ⬜ |
| 18 | CrewAI Tutorial | 2h | ⬜ |
| 19-21 | Salesforce Agent Project | 5h | ⬜ |

### WEEK 7: ADVANCED TOPICS
| Day | Module | Time | Status |
|-----|--------|------|--------|
| 22 | MCP Deep Dive | 2h | ⬜ |
| 23 | RAG + MCP Integration | 2h | ⬜ |
| 24-25 | Production Deployment | 3h | ⬜ |

### WEEK 8: CAPSTONE + INTERVIEW PREP
| Day | Activity | Time | Status |
|-----|----------|------|--------|
| 26-28 | Capstone Project | 10h | ⬜ |
| 29 | Portfolio Polish | 2h | ⬜ |
| 30 | Interview Prep | 2h | ⬜ |

---

## 🛠️ SETUP REQUIREMENTS

### Python Environment
```bash
cd /Users/arshdave/Documents/VS\ Code\ Workspace/GitRepoCloned/AILearning/AILearning
source venv/bin/activate
pip install numpy pandas scikit-learn
pip install anthropic openai tiktoken
pip install chromadb sentence-transformers
pip install langchain langchain-anthropic
pip install crewai
```

### API Keys Needed
```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"  # Optional
```

### Verify Setup
```bash
python3 -c "import numpy; import pandas; import anthropic; print('✅ Setup complete!')"
```

---

## 🎯 LEARNING APPROACH

### For Each Module:
1. **Run the file first** - See it work
2. **Read the code** - Understand what's happening
3. **Do the exercises** - Hands-on practice
4. **Build the project** - Apply learning
5. **Answer interview questions** - Validate understanding

### Daily Routine:
```
1 hour AM: New module
30 min: Exercises
30 min: Connect to Salesforce project
```

---

## 📈 SUCCESS METRICS

### Week 2 Checkpoint:
- [ ] Can explain how LLMs work
- [ ] Built first ML model
- [ ] Made API calls to Claude

### Week 4 Checkpoint:
- [ ] Built working RAG system
- [ ] Integrated with Salesforce data
- [ ] Can answer RAG interview questions

### Week 6 Checkpoint:
- [ ] Built multi-agent system
- [ ] Integrated agents with Salesforce
- [ ] Can design complex AI workflows

### Week 8 Final:
- [ ] Capstone project complete
- [ ] Portfolio ready
- [ ] Can answer 50+ AI interview questions

---

## 🔗 QUICK COMMANDS

### Run Any Module:
```bash
cd /Users/arshdave/Documents/VS\ Code\ Workspace/GitRepoCloned/AILearning/AILearning
source venv/bin/activate
python3 hands-on/01-python-essentials/01_python_for_js_devs.py
```

### Start Your API Server:
```bash
cd ~/salesforce-ai-api
node index.js
```

### Git Commit Progress:
```bash
git add .
git commit -m "Complete: Module X - Topic Y"
git push
```

---

## 📚 INTERVIEW PREP TOPICS

Each module includes interview questions. Master these:

1. **ML Basics:** Supervised vs unsupervised, overfitting, evaluation metrics
2. **LLMs:** Transformers, attention, embeddings, tokens
3. **Prompt Engineering:** Best practices, few-shot, chain-of-thought
4. **RAG:** Pipeline, chunking, vector DBs, evaluation
5. **Agents:** Tool use, planning, multi-agent systems
6. **Production:** Deployment, monitoring, scaling

---

## 🚀 START HERE

**Your first command:**
```bash
cd /Users/arshdave/Documents/VS\ Code\ Workspace/GitRepoCloned/AILearning/AILearning
source venv/bin/activate
python3 hands-on/01-python-essentials/01_python_for_js_devs.py
```

Let's go! 🎯
