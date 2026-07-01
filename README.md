# Support Ticket Triage

## Overview
Q3 2026 support ticket triage platform for backlog burn-down, intelligent routing, engineering escalation, and SLA management. Supports 50 tickets across 6 customers and 3 products with false backlog detection.

## Problem Statement
Acme Horizon Group Q3 2026 backlog requires systematic triage:
- 50 support tickets (June-July 2026)
- 6 customers (BluePeak, Helio, Meridian, NordForge, UrbanNest, ClearWave)
- 3 products (FlowSphere, SupportPilot, InsightGrid)
- Issue types: SSO token expiration, API 403 errors, invoice disputes, sync failures
- 15-20% false backlog (stale tickets)
- 30-40% requiring engineering escalation

## Key Features
- Intelligent ticket triage (P1/P2/P3 classification)
- Automatic team routing (Engineering, RevOps, Support)
- False backlog detection and quarantine (15-20% stale)
- SLA tracking by priority (P1: 4h, P2: 24h, P3: 48h)
- HAR file workflow automation
- Engineering queue management
- RevOps validation routing
- Weekly burn-down metrics

## Metrics (Q3 2026)
- Total Tickets: 50 (Week 1-6 tracking)
- Customers: 6 (all sample customers from brief)
- Products: 3 (all from brief)
- Issue Categories: SSO tokens, API 403, invoices, sync, diagnostics
- False Backlog: 15-20% of tickets
- Engineering Engagement: 30-40% of tickets
- RevOps Involvement: 25-35% of tickets
- SLA Compliance: 85% met
- Burn-Down Velocity: 2-3 tickets/week

## Issue Types
- SSO Token Expiration (P1): IdP policy changes, all customers affected
- API 403 Errors (P1/P2): Key rotation, scope mismatch, sync failures
- Invoice Disputes (P2): Proration disputes, RevOps review (avg $6.78)
- Sync Failures: Product-specific, engineering escalation
- HAR Requests (P3): Diagnostic file collection

## Triage Workflows
1. HAR Collection: Requested → Received/Pending/Not needed
2. Engineering Triage: ENG-Assist requested → Queued → ENG engaged → Hotfix in progress
3. RevOps Validation: Pending → Joint review → Resolved
4. False Backlog: Age analysis → Quarantine → Actionable backlog improvement

## Technology
- Language: Python, Node.js
- Database: PostgreSQL, Snowflake
- Triage: ML-based classification and routing
- Automation: Engineering/RevOps workflow
- Dashboards: Real-time queue and SLA tracking

## Getting Started
```bash
git clone https://github.com/ACME-Mock-EU/support-ticket-triage.git
cd support-ticket-triage
python main.py
```

## API Endpoints
- GET /tickets - All tickets
- GET /tickets/{id} - Ticket details
- GET /tickets/customer/{name} - Customer tickets
- GET /backlog/burndown - Weekly metrics
- POST /tickets/{id}/triage - Assign triage
- GET /engineering/queue - Escalation queue
- GET /revops/validation - Billing queue
- GET /false-backlog/candidates - Stale tickets

## Timeline
- June 18: Q3 backlog initiated
- July 5: Mid-Q3 review
- July 29: Q3 Week 6 (burn-down in progress)
- August 1: v1.0.0 release

## License
Internal use only - Acme Horizon Group

## Support
support@acmemock02.de | supportpilot@acmemock02.de
