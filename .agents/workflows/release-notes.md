---
description: Structured release notes generation process.
---

# Release Notes Workflow

This workflow guides the creation of professional release notes that communicate changes clearly to different audiences (users, stakeholders, developers).

## Phase 1: Change Collection

**Goal**: Gather all changes included in the release from multiple sources.

1.  **Git History Review**: Compile all commits and merged PRs since the last release tag. Group by type: feature, bugfix, improvement, breaking change.
2.  **Linear Ticket Review**: [Senior Product Owner](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-po/SKILL.md) cross-references completed tickets/issues to ensure no shipped change is missed.
3.  **Database Migration Review**: [Senior Backend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-backend/SKILL.md) identifies any schema changes, new tables, or data migrations included in the release.

## Phase 2: Categorization & Prioritization

**Goal**: Organize changes into clear, meaningful categories for the audience.

1.  **Categorize Changes**: Group into standard sections:
    - ✨ **New Features** — New capabilities for users.
    - 🐛 **Bug Fixes** — Resolved issues.
    - ⚡ **Improvements** — Performance, UX, or DX enhancements.
    - 🔧 **Technical Changes** — Infra, refactors, dependency updates.
    - ⚠️ **Breaking Changes** — Changes requiring user action.
    - 🗑️ **Deprecations** — Features scheduled for removal.
2.  **Prioritize Impact**: [Senior Product Owner](agents/skills/senior-po/SKILL.md) ranks items within each category by user impact, highlighting the most significant changes first.

## Phase 3: Content Writing

**Goal**: Write clear, engaging release notes tailored to the target audience.
