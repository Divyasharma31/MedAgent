# Frontend — Phase 5 Placeholder

This directory will contain the React + TypeScript + Tailwind CSS + Vite
frontend application, implemented in **Phase 5**.

## Planned structure (§8 of ARCHITECTURE_v0.3.md)

```
frontend/
  src/
    api/         client.ts  types.ts
    components/  ChatWindow  MessageBubble  SourcesPanel  EscalationBanner
                 DocumentUpload  FindingsTable  TraceDrawer  DisclaimerBar
    pages/       Chat.tsx  Eval.tsx (optional)
    hooks/       useChat.ts
    App.tsx  main.tsx  index.css
  tailwind.config.ts  vite.config.ts  package.json
```

## UI requirements (§8)

- Escalation banner is visually dominant.
- Sources shown next to the answer.
- User-provided, retrieved, and generated content are visually distinct.
- Persistent "not a substitute for a doctor" bar on every screen.
- "Synthetic data only" notice on the upload component.
- Static emergency-help line always visible, even when backend is unreachable (§12C).

