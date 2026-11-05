# Source Register

**Divya Sharma · MP2026CSE97**

> This register records every knowledge source considered for the system.
> A source must reach `approved` status before any content is ingested,
> chunked, embedded, or cited. See §11 of ARCHITECTURE_v0.3.md for the
> approval gate process.

## Column definitions

| Column | Meaning |
|--------|---------|
| `id` | Unique source identifier (used in `chunks` and `rules` tables) |
| `name` | Short human-readable name |
| `publisher` | Publishing body |
| `url` | Canonical URL |
| `tier` | `india-primary` \| `india-secondary` \| `international` |
| `intended_use` | `answer_content` \| `rule_authority` \| `drug_info` \| `eval_only` \| `reference_only` |
| `status` | `candidate` → `checking` → `approved` \| `rejected` |
| `licence_checked` | Date the terms page was read (not from secondary reports) |
| `authority_checked` | Date the publisher identity was confirmed |
| `currency_checked` | Publication/review date noted |
| `extraction_checked` | Date text extractability was confirmed |
| `approved_by` | Divya Sharma (self; clinician review is separate — see §12A) |
| `approved_on` | Approval date |
| `notes` | Anything that matters for use or re-check |

---

## Candidates (Phase 0 — none approved yet)

All rows start as `candidate`. The first task in parallel with Phase 0 is to
open each official site, read the terms page, and move each row to `checking`.
No code depends on this table until Phase 1.

| id | name | publisher | url | tier | intended_use | status | licence_checked | notes |
|----|------|-----------|-----|------|--------------|--------|-----------------|-------|
| SRC-001 | CDSCO drug regulatory information | Central Drugs Standard Control Organisation | https://cdsco.gov.in | india-primary | drug_info | candidate | — | Check SUGAM portal terms; do not use until verified (§11). |
| SRC-002 | National Health Portal | Ministry of Health and Family Welfare | https://www.nhp.gov.in | india-primary | answer_content | candidate | — | Check which pages are public information and whether a licence statement exists. |
| SRC-003 | National List of Essential Medicines (NLEM) | Ministry of Health and Family Welfare | https://nhsrcindia.org/national-list-essential-medicines | india-primary | drug_info | candidate | — | A list only; not dosing or warning content. Confirm current edition. |
| SRC-004 | ICMR clinical guidelines | Indian Council of Medical Research | https://www.icmr.gov.in | india-primary | rule_authority | candidate | — | Clinician-oriented; prescribing content must stay out of answers. Check licence. |
| SRC-005 | Indian Pharmacopoeia Commission / PvPI safety alerts | IPC / Pharmacovigilance Programme of India | https://ipc.gov.in | india-primary | drug_info | candidate | — | Confirm what is published and the terms. |
| SRC-006 | NCDC disease-specific guidelines | National Centre for Disease Control | https://ncdc.gov.in | india-secondary | answer_content | candidate | — | Select by pilot topic list (not yet fixed). |
| SRC-007 | data.gov.in datasets | Government of India | https://data.gov.in | india-secondary | reference_only | candidate | — | GODL-India licence applies only to datasets published under it; check each dataset individually. |
| SRC-008 | MedlinePlus patient information | U.S. National Library of Medicine | https://medlineplus.gov | international | answer_content | candidate | — | Gap-filler where Indian material is missing; label passages with country and publisher. |
| SRC-009 | WHO fact sheets | World Health Organization | https://www.who.int/news-room/fact-sheets | international | answer_content | candidate | — | Check terms. |
| SRC-010 | CDC health topics | U.S. Centers for Disease Control and Prevention | https://www.cdc.gov | international | answer_content | candidate | — | Check terms. |
| SRC-011 | NHS health information | National Health Service (UK) | https://www.nhs.uk | international | answer_content | candidate | — | Check terms. |
| SRC-012 | DailyMed drug labels | U.S. National Library of Medicine | https://dailymed.nlm.nih.gov | international | drug_info | candidate | — | US labels; brand names and indications may differ from India — label clearly. |
| SRC-013 | openFDA drug data | U.S. Food and Drug Administration | https://open.fda.gov | international | drug_info | candidate | — | US labels; same caveat as DailyMed. |

---

> **Note:** No source is approved. No content is ingested. This register is
> updated as each official terms page is read (a parallel, non-code task).
> Phase 1 cannot start until at least the Phase 1 sources reach `approved`.

