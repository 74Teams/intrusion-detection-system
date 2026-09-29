---
description: Emergency hotfix process for production bugs.
---

# Hotfix Workflow

This workflow guides the rapid resolution of critical production bugs with minimal downtime, following a structured triage → fix → deploy pipeline.

## Phase 1: Triage & Assessment

**Goal**: Quickly identify the root cause, assess impact, and define the scope of the fix.

1.  **Bug Report Analysis**: [Senior QC](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-qc/SKILL.md) reproduces the issue, captures logs/screenshots, and documents the exact steps to reproduce.
2.  **Impact Assessment**: [Senior Product Owner](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-po/SKILL.md) evaluates user impact, affected features, and priority level (P0/P1).
3.  **Data Validation**: [Senior Data Analyst](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-data-analyst/SKILL.md) checks error rate dashboards, affected user segments, and data integrity.

## Phase 2: Root Cause Analysis

**Goal**: Pinpoint the exact source of the bug and determine the safest fix strategy.

1.  **Backend Investigation**: [Senior Backend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-backend/SKILL.md) debugs API, database queries, and server-side logic.
2.  **Frontend Investigation**: [Senior Frontend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-frontend/SKILL.md) inspects UI rendering, client-side state, and network calls.
3.  **Root Cause Documentation**: Document the root cause, affected code paths, and the chosen fix strategy before proceeding.

## Phase 3: Fix Implementation

**Goal**: Implement the minimal, targeted fix without introducing regressions.

1.  **Create Hotfix Branch**: Branch from `main` (or production tag). Naming convention: `hotfix/<issue-id>-<short-description>`.
2.  **Apply Fix**: The responsible developer ([Senior Backend](.agents/skills/senior-backend/SKILL.md) or [Senior Frontend](.agents/skills/senior-frontend/SKILL.md)) implements the narrowest possible change to resolve the issue.
3.  **Write Regression Test**: [Senior QC](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-qc/SKILL.md) writes a test case that specifically covers the bug scenario to prevent recurrence.

## Phase 4: Validation & Deploy

**Goal**: Verify the fix resolves the issue without side effects, then deploy to production.

1.  **Smoke Testing**: [Senior QC](.agents/skills/senior-qc/SKILL.md) runs targeted test suite on affected area + critical path regression tests.
2.  **Code Review**: Peer review focusing on scope (no unrelated changes), correctness, and potential side effects.
3.  **Deploy to Production**: Deploy the hotfix branch directly to production.
4.  **Post-Deploy Monitoring**: [Senior Data Analyst](.agents/skills/senior-data-analyst/SKILL.md) monitors error rates and key metrics for 30 minutes post-deploy.
5.  **Merge Back**: Merge the hotfix branch back into `develop` to keep branches in sync.

## Phase 5: Post-Mortem

**Goal**: Learn from the incident to prevent future occurrences.

1.  **Incident Report**: [Senior Product Owner](.agents/skills/senior-po/SKILL.md) documents timeline, impact, root cause, fix, and preventive actions.
2.  **Process Improvement**: Identify gaps in testing, monitoring, or code review that allowed the bug to reach production.
