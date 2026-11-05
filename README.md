# Agentic Healthcare CDSS

**Divya Sharma · MP2026CSE97**

> ⚠️ **This system is not a substitute for professional medical advice, diagnosis, or treatment.**
> Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.

---

## Project scope

An Agentic Clinical Decision Support System (CDSS) built as an academic prototype
for a research comparison between conventional LLM+RAG and an orchestrated
multi-agent RAG approach with structured safety validation.

## Important notices

- **Synthetic data only.** No real personal health information is used in
  development or evaluation. The system explicitly blocks requests that contain
  obvious personal identifiers.
- **Not for clinical use.** This is a university research prototype. Emergency
  escalation templates are predetermined and must be verified by a qualified
  reviewer before any real deployment.
- **English only (v1).** Hindi, Hinglish, and other languages are out of scope
  for the initial version.

## Architecture

See `ARCHITECTURE_v0.3.md` for the full architecture design (approved v0.3).
Phase 0 implements foundations only — no medical content, no rules, no sources.

## Phase status

| Phase | Description | Status |
|-------|-------------|--------|
| **0** | Foundations: repo, config, LLMProvider, /health, tests | ✅ In progress |
| 1 | Knowledge base and retrieval | 🔒 Awaiting approval |
| 2 | Core graph, typed segments, Stage 1, first chat | 🔒 Awaiting approval |
| 3 | Rules, templates, emergency path, safety suite | 🔒 Awaiting approval |
| 4 | Medication and document agents | 🔒 Awaiting approval |
| 5 | Frontend | 🔒 Awaiting approval |
| 6 | Evaluation | 🔒 Awaiting approval |
| 7 | Hardening and write-up | 🔒 Awaiting approval |

## Quick start (Phase 0)

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 2. Install backend dependencies
cd backend
pip install -e ".[dev]"

# 3. Copy and configure environment
cp .env.example .env
# Edit .env as needed (LLM_PROVIDER=fake for Phase 0)

# 4. Run the server
uvicorn app.main:app --reload

# 5. Run tests
pytest
```

## Stack

- **Backend:** FastAPI, Uvicorn, Pydantic v2, Python 3.11+
- **Orchestration:** LangGraph (Phase 2+)
- **Vector store:** ChromaDB + Sentence Transformers (Phase 1+)
- **Database:** SQLAlchemy + SQLite (dev) / PostgreSQL (prod) + Alembic (Phase 2+)
- **Frontend:** React + TypeScript + Tailwind CSS + Vite (Phase 5+)
- **Testing:** pytest, httpx

## Repository layout

```
backend/         FastAPI application and all backend logic
frontend/        React UI (placeholder until Phase 5)
docs/            Architecture decisions, source register, provider data flow
ARCHITECTURE_v0.3.md   Single source of truth for design decisions
```

