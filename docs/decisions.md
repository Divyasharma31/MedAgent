# Architecture Decisions — v0.3 Approved

**Divya Sharma · MP2026CSE97**
**Approved version:** v0.3
**Approval date:** 2026-11-06

This file records the decisions approved in ARCHITECTURE_v0.3.md (§17).
It is the reference point for why each implementation choice was made.
Any deviation from these decisions must be discussed and re-approved before code is written.

---

## Approved decisions (§17)

### 1. Stack and architecture choices (carried from v0.1/v0.2)
- **Backend:** FastAPI + Uvicorn (not Flask)
- **Orchestration:** LangGraph (not bare chains)
- **Vector store:** ChromaDB + Sentence Transformers (not FAISS)
- **Database:** SQLAlchemy + SQLite (dev) / PostgreSQL (prod) + Alembic migrations from day one
- **Frontend:** React + TypeScript + Tailwind CSS + Vite
- **Testing:** pytest + httpx
- **LLM abstraction:** `LLMProvider` protocol; real provider chosen after §16.1 is resolved

### 2. Two-stage risk assessment
- Stage 1: deterministic keyword/regex scan on raw text, before any LLM call.
- Stage 2: structured assessment on symptom-agent output, using the full rule file.
- Final level = max(Stage 1, Stage 2). Stage 2 never lowers a Stage 1 level.

### 3. Typed segments (§4A)
- F1 generator returns typed JSON segments, not free prose.
- `generated` segments are restricted to connector phrases and clarifying questions from a fixed library.
- No free text is allowed outside evidence-backed segments.
- F2 validator checks structure deterministically; NLI/LLM semantic check is a later optional ablation.

### 4. Structural validator v1 (§3F)
- F2 is deterministic in v1: schema, reference existence, provenance rules, source status, escalation consistency, secondary pattern checks.
- Known limit: v1 does not verify semantic support; measured by manual sampling in §14.

### 5. Rule governance (§12A)
- Rules are `draft` → `sourced` → `clinically_reviewed` → `retired`.
- Only `sourced` and `clinically_reviewed` rules run in the engine.
- Each rule requires: id, condition, severity, source_id, passage_ref, status, reviewer, review_date, version, positive test, near-miss test.
- If no qualified reviewer is found, every rule stays `sourced`; the report states this plainly.

### 6. Source approval gates (§11)
- Nothing is ingested before its `sources` row shows `approved` for the intended use.
- Four checks required: licence/terms, authority, currency, intended use.
- Indian sources used first; international sources fill gaps and are labelled with country and publisher.

### 7. Research design (§14)
- Two arms: (1) baseline LLM+RAG; (2) proposed multi-agent RAG with safety validation.
- Held identical: LLM model/version/temperature/max_tokens, KB snapshot, embedding model, chunking, top-k, test cases, run conditions.
- Baseline: top-k on raw query + one prompt; no router, rules, segments or validator.
- Metrics: routing accuracy, P@K, R@K, MRR, provenance coverage, invalid-reference rate, uncited medical claim rate, unsafe-response rate, red-flag detection, latency.

### 8. Stage 1 documented as limited early escalation aid (§3C)
- English-only v1; documented false-negative/false-positive test sets.
- Persistent emergency-help line in the UI on every screen, independent of the scan.
- Stage 1 miss means only "no early flag", never "person is safe". No answer may imply safety.

### 9. `generated` segments restricted to fixed library (§4A)
- Connectors: short, non-clinical, hand-written.
- Clarifying questions: fixed slot list (duration, severity, age, current medicines, other symptoms), phrased as questions only.
- F2 checks the ID and that text equals library text with only extracted entity names filled in.
- No reliance on regex to prove a segment is non-medical.

### 10. Privacy policy (§12B)
- Synthetic data by default; no real identifiable health data to free-tier LLMs.
- Requests blocked on detected obvious identifiers (phone, email, long digit strings).
- Provider data register at `docs/provider_data_flow.md`.
- Log redaction and input de-identification are separate, imperfect controls.

### 11. Emergency path independence (§12C)
- Emergency bypass: Stage 1 `emergency` → predetermined template, no LLM/Chroma/generator/validator/DB/LangGraph.
- Allowed dependencies: Python stdlib, rule file, template file (both loaded and validated at startup).
- Service refuses to start if either is missing or invalid.
- Static UI fallback if backend is unreachable.
- Templates predetermined for India (pending confirmation), verified from official government sources.

### 12. Scope frozen
- Five agents (A–E) + LangGraph + RAG + research comparison.
- No new agents, technologies, or scope changes without explicit re-approval.

### 13. Phase gating
- One phase at a time; stop for review after each.
- Phase 0 began after v0.3 approval.
- Phase 1 begins only after Phase 0 review and approval.

---

## Open decisions (§16 — not yet resolved)

| # | Decision | Blocking what |
|---|----------|--------------|
| 1 | Real LLM provider (which one; free-tier data-use terms) | Real provider adapters; provider data register entry |
| 2 | Final approved sources after licence/authority/currency/use checks | Phase 1 (knowledge base) |
| 3 | Qualified clinical reviewer for red-flag rules and emergency template wording | Phase 3 |
| 4 | Deployment region confirmation (assumed India) and emergency number verification | Phase 3 |
| 5 | Languages: English only for v1 (Hindi/Hinglish needs separate effort) | Phase 3 |
| 6 | Embedding model (chosen by retrieval test) | Phase 1 |
| 7 | Evaluation set size and rating method | Phase 6 |
| 8 | Deployment target and timeline | Phase 7 |
| 9 | Whether "usability" needs a user test (consent handling if so) | Phase 7 |

