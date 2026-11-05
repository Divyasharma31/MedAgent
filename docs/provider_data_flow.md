# Provider Data Flow Register

**Divya Sharma · MP2026CSE97**

> This register documents what data each external LLM provider receives,
> per §12B of ARCHITECTURE_v0.3.md.
> One row per provider, filled in when that provider is chosen (§16.1).
>
> **Phase 0 status:** `LLM_PROVIDER=fake`. No external calls are made.
> This register has no completed rows yet.

## Privacy policy summary (§12B)

| Control | Protects | What it does | What it does not do |
|---------|---------|--------------|----------------------|
| Log redaction | Data stored in logs and DB | Logs keep hashes, codes, IDs, latencies; obvious identifiers masked | Does not stop data being sent to an LLM provider |
| Input de-identification | Data sent to external providers | Best-effort regex masking of obvious identifiers before any external call | Cannot guarantee anonymity; names, places, dates may still identify a person |

**Standing policy:**
- Development and evaluation use synthetic data only.
- Real identifiable health information is never sent to external free-tier LLM providers.
- If an obvious identifier is detected, the request is blocked (not sent).
- Local-only components (Stage 1 scan, rules, templates, PyMuPDF, Sentence Transformers, ChromaDB, SQLite) send nothing externally.

## Column definitions

| Column | Meaning |
|--------|---------|
| `provider` | Provider name |
| `endpoint_region` | API endpoint and region (e.g. `api.gemini.google.com / us-central1`) |
| `call_types` | Which agent calls use this provider |
| `data_sent` | Categories of data sent (from §12B table) |
| `never_sent` | Categories explicitly excluded |
| `retention_terms` | Provider's stated retention policy (from terms page, with date verified) |
| `training_use_terms` | Whether provider uses data for model training |
| `terms_verified_on` | Date the terms page was read |
| `notes` | Anything else relevant |

---

## Providers

| provider | endpoint_region | call_types | data_sent | never_sent | retention_terms | training_use_terms | terms_verified_on | notes |
|----------|-----------------|------------|-----------|------------|-----------------|-------------------|-------------------|-------|
| fake | local / no network | all (Phase 0 only) | nothing — no external calls | everything | n/a | n/a | n/a | FakeLLM for Phase 0. Replaced when §16.1 is decided. |

---

> When a real provider is chosen, add a row here **before** any real data
> (even synthetic) is sent to it. Free-tier terms on retention and training
> use must be checked; assume anything sent may be stored or read.

