# Memory MCP — Candidate Assessment

Reviewed: 2026-10-20.
User supplied name: memory mpc; interpreted provisionally as Memory MCP. Exact project remains unconfirmed because several projects share this name.
Status: Documentation review only; no installation, fork or runtime testing.

## Lightweight candidate
https://github.com/M-Ashrey/memory-mcp
Repository description documents filesystem-backed JSON memory with write/read/search/list/delete tools, keyword retrieval and no embeddings/database requirement. LICENSE inspected: MIT. Potential ORIS use: a small persistent memory service; semantic recall is not established by this design.

## Other distinct candidates
- https://github.com/dwovitz/memory-mcp — PostgreSQL/pgvector structured personal context and hybrid retrieval.
- https://github.com/jayzuccarelli/memory-mcp — Markdown-based shared memory exposed over MCP.
These alternatives were identified from upstream descriptions; their licenses and implementations are not verified here.

## Next evaluation
Confirm the intended repository. Compare against existing ORIS memory plans before adding infrastructure. Test persistence, retrieval accuracy, correction/deletion, project isolation and backup/restore. Cloud operation needs durable storage; do not expose private memories through an unauthenticated public endpoint.
