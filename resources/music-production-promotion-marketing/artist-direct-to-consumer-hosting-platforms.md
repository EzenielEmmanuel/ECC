# Music Production, Promotion & Marketing Applications
## Direct-to-Consumer Artist Platforms and Hosting — Research Registry
Date: 2026-10-22
Status: Research candidates; not deployed, integrated, or security-audited.

### Goal
Build a self-managed, white-label ecosystem for artists, musicians, producers and labels: artist sites, digital music and beat sales, merchandise, fan subscriptions, promotion, analytics, distribution and royalty accounting. Evaluate interoperability with ORIS Workshop, KEYS, ORIZE'N and Registry of Royalties. Preserve independent ownership of application code and branding while initially renting server infrastructure.

### Reference: StreetNoise
- Main website: https://www.streetnoisemerch.com/musichub
- Specialized music hub: https://music.streetnoisemerch.com/
- Apparent public site builder: Wix-linked assets; verify independently.
- Separate music application includes artist-facing music commerce and entertainment functions; underlying host, server provider, database and complete stack are **unverified**. PHP-style routes alone do not identify a hosting company.
- Follow-up: inspect publicly available DNS/CNAME, HTTP headers and technology signatures without invasive probing; compare merchant and creator terms.

### Candidates
| Candidate | URL | Primary fit | Due diligence |
|---|---|---|---|
| Mirlo | https://mirlo.space/ ; https://docs.mirlo.space/ | Open-source music commerce, artist support, storefronts | Verify license, deployment requirements, API stability, multi-tenant suitability, Stripe Connect limitations and Jamaica payment options |
| Faircamp | https://simonrepp.com/faircamp/ | Lightweight self-hosted individual artist music websites | Verify automation and scalable multi-artist provisioning |
| Funkwhale | https://www.funkwhale.audio/ | Self-hosted streaming, libraries and community | Verify licenses, streaming rights, scale and integration |
| WooCommerce | https://woocommerce.com/ | Downloads, merchandise, general commerce | Evaluate WordPress multi-vendor extensions, security and transaction accounting |
| Crate | https://github.com/thecrateapp/crate | Self-hosted music library/playback candidate | Verify repository status, license and commercial suitability |
| Wix | https://www.wix.com/ | Benchmark for artist website builder | Proprietary; not a self-hostable core |
| Shopify | https://www.shopify.com/ | Commerce benchmark | Proprietary; not a self-hostable core |

### Proposed modular architecture
1. Artist-facing React/Next.js storefronts and custom domains.
2. Backend API, identity, artist/label workspaces and role-based access.
3. PostgreSQL and S3-compatible audio/artwork storage, secure download delivery.
4. Music sales, merchandise, subscriptions, payouts and payment reconciliation.
5. Marketing tools: mailing lists, fan CRM, campaigns, analytics, events and promotional links.
6. Rights metadata and royalty accounting integrations with Registry of Royalties.
7. Distribution service integration subject to contracts and platform permissions.
8. ORIS-assisted design, operations and automation under explicit authorization.
9. Container-based deployment, monitoring, backups, data export and security.

### Suggested phased evaluation
- Phase 1: verify upstream repositories, licensing, maintenance and security; test StreetNoise public technology signals.
- Phase 2: isolated proof-of-concept of Mirlo with sample non-copyrighted music; evaluate Faircamp for artist microsites.
- Phase 3: custom branded frontend and API integrations, with payment/payout feasibility in Jamaica resolved before commerce launch.
- Phase 4: limited artist pilot; test tenancy isolation, copyright compliance, payouts, support, backups and operational costs.
- Phase 5: expand to managed artist hosting and additional modules only after production-readiness review.

### Guardrails
- No claim that StreetNoise's backend host has been identified.
- No claim that candidate systems are already integrated or that they can all be combined without engineering.
- Check open-source licenses, trademarks, data protection, content licensing, artist contracts and payment-provider jurisdictional support.
- Prefer low-cost cloud VPS initially; self-managed software is not the same as owning physical hosting infrastructure.
