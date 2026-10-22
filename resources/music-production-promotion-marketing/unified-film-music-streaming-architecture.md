# Unified Film & Music Streaming Platform — Architecture Decision
Date: 2026-10-22
Category: Music Production, Promotion & Marketing Applications
Status: APPROVED DIRECTION / DESIGN ONLY — not deployed

## Decision
Use **one shared backend** to control both film and music streaming. Launch a combined responsive web application initially, with the option for multiple independently branded frontends sharing the same backend later.

## Architecture
- **One modular-monolith backend** with clear modules: identity and authorization, creator/label accounts, unified content catalog, metadata, rights/licensing, entitlements, subscriptions, rentals, direct sales, payments, royalties, analytics, administration and APIs.
- **Specialized media processing services:** video upload, encoding/transcoding, adaptive playback and CDN; audio ingestion, transcoding, playlists and playback. Media delivery can scale independently of shared business logic.
- **Storage:** PostgreSQL for operational records; S3-compatible object storage for audio, video and artwork; caching/queue as needed.
- **Frontend:** shared login and creator dashboard; differentiated music and film browsing/player experiences. Separate brands/apps can be added without duplicating backend.
- **ORIS:** optional intelligence and administrative automation, governed by explicit authorization.
- **Registry of Royalties:** future integration for music and film accounting, preserving different rights and payout rules.
- **Security/operations:** creator isolation, least-privilege roles, audit logs, backups, monitoring, media access controls, rate limits and data export.

## Candidate open-source components to evaluate
- MediaCMS — https://github.com/mediacms-io/mediacms — video publishing and management candidate; review AGPL compliance.
- Navidrome — https://github.com/navidrome/navidrome — lightweight audio streaming candidate; assess commercial multi-tenant fit.
- Jellyfin — https://github.com/jellyfin/jellyfin — playback/reference candidate, not turnkey multi-creator commerce.
- Mirlo — https://mirlo.space/ — direct-to-fan music commerce candidate.
All candidates require license, API, security, scalability and integration verification before selection.

## Monetization possibilities
Free/ad-supported streaming, paid subscriptions, music downloads, film rentals/purchases, merchandise, artist fan memberships, and managed branded storefronts. No monetization model is committed for initial launch. Verify rights for streaming, territories, sync/publishing as applicable, payments and payouts, particularly availability in Jamaica.

## First demonstrable milestone
One registered test user signs in, plays a rights-cleared sample song, watches a rights-cleared sample film, and sees both in one account. One creator can upload/manage both through one dashboard. Use non-copyrighted or expressly authorized sample media.

## Development sequence
1. Define data model, identity, unified content/rights records and media-specific modules.
2. Prototype UI and shared API using test data.
3. Test audio/video engines in isolated containers and compare cost/performance.
4. Implement secure storage, media access and operational observability.
5. Add commerce/entitlements and accurate royalty event accounting only after payments/rights review.
6. Small controlled pilot, then expand mobile/TV/live events and multi-brand hosting.

## Rationale
Shared identity, catalog, rights, billing, creator operations and administration reduce duplication and permit multiple products; media-specific pipelines retain performance flexibility. A modular monolith is lower-overhead initially than a fleet of microservices.

Related research: resources/music-production-promotion-marketing/artist-direct-to-consumer-hosting-platforms.md
