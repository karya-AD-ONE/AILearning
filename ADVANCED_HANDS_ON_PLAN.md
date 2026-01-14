# 🔧 ADVANCED HANDS-ON AI LEARNING PLAN

## Overview

**Goal:** Build coding confidence by writing AI code yourself  
**Prerequisite:** Basic course complete ✅  
**Status:** 🔄 Starting

---

## PHASE A: Code Walkthrough (30 min)

Understand existing project structure before building.

### Session Objectives:
- [ ] Project structure overview (which file does what)
- [ ] Config files vs main programs
- [ ] How files connect to each other
- [ ] Entry points and flow
- [ ] Dependencies and imports

### Files to Review:
```
projects/01-salesforce-rag/
├── rag_system.py        ← Core RAG logic (CLASS)
├── rag_api.py           ← Flask wrapper (ENDPOINTS)
├── index_with_rag.js    ← Express + RAG (MAIN SERVER)
├── knowledge_base.json  ← Data (CONFIG)
└── package.json         ← Node dependencies (CONFIG)
```

---

## PHASE B: Build from Scratch (1-2 hours)

You code, Claude guides only when stuck.

### Mini Project: Simple Q&A RAG
Build a minimal RAG from empty file:
1. Load documents
2. Create embeddings
3. Store in ChromaDB
4. Search function
5. Query with Claude

**Rule:** You type every line. Ask for hints, not code.

---

## PHASE C: Modification Exercises (1 hour)

Hands-on tasks to modify existing code:

| Task | Skill Practiced |
|------|-----------------|
| Add new tool `sf_get_contacts` | Tool definition + handler |
| Change chunk size from 300→500 | Understanding chunking |
| Add new knowledge article | Data management |
| Add logging to agent steps | Debugging skills |
| Create new endpoint `/api/test` | Express routing |

---

## PHASE D: Debugging Practice (30 min)

Claude breaks code → You find and fix:

| Bug Type | What You'll Learn |
|----------|-------------------|
| Missing import | Dependency management |
| Wrong port number | Configuration |
| Typo in tool name | Tool routing |
| API key not set | Environment variables |
| JSON parse error | Data handling |

---

## PHASE E: Combination Track (2-3 hours)

Recommended path:
1. Walkthrough (A) → 30 min
2. Build mini RAG (B) → 1 hour
3. 3 modification tasks (C) → 30 min
4. 3 debugging challenges (D) → 30 min

---

## PHASE F: Advanced Complex Project (4-6 hours)

**Project: Salesforce Deal Intelligence Platform**

Build from scratch combining ALL concepts:

### Features:
1. **Multi-source RAG**
   - Salesforce Knowledge Articles
   - Company policies
   - Competitor intelligence

2. **Advanced Agents**
   - Deal Risk Analyzer
   - Competitor Comparison Agent
   - Win/Loss Pattern Analyzer

3. **Multi-Agent Orchestration**
   - Agents that call other agents
   - Parallel tool execution
   - Human-in-the-loop approvals

4. **Production Features**
   - Error handling & retries
   - Logging & monitoring
   - Rate limiting
   - Caching

### Tech Stack:
- Python (RAG + ML)
- Node.js (API)
- ChromaDB (Vector DB)
- Claude API (LLM)
- Salesforce CLI (Data)

---

## Learning Sequence

```
Week 1: A → B → C → D (Fundamentals)
Week 2: F Part 1 (RAG from scratch)
Week 3: F Part 2 (Agents from scratch)
Week 4: F Part 3 (Integration + Polish)
```

---

## Progress Tracker

| Phase | Status | Date |
|-------|--------|------|
| A - Code Walkthrough | ⬜ Not Started | |
| B - Build from Scratch | ⬜ Not Started | |
| C - Modification Exercises | ⬜ Not Started | |
| D - Debugging Practice | ⬜ Not Started | |
| E - Combination Track | ⬜ Not Started | |
| F - Advanced Project | ⬜ Not Started | |

---

## Rules for Maximum Learning

1. **You type all code** - no copy-paste from Claude
2. **Ask for hints, not solutions** - "What should I look at?" not "Write it for me"
3. **Debug yourself first** - Try 5 min before asking
4. **Explain back** - After each section, explain what you learned
5. **Break things intentionally** - Best way to learn is to fix

---

*Created: January 2025*
*Updated: January 2025*
