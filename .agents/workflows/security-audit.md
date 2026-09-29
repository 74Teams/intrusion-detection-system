---
description: Security audit and RLS policy verification.
---

# Security Audit Workflow

This workflow ensures the application remains secure, focusing on Supabase RLS and sensitive data handling.

## Phase 1: Policy Review

**Goal**: Audit current Row Level Security (RLS) and database permissions.

1.  **RLS Audit**: [Senior Backend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-backend/SKILL.md) uses Supabase MCP to list and review every policy.
2.  **Access Scanning**: Verify that sensitive tables (users, private data) are not publicly accessible.
3.  **Context Check**: Review `auth.uid()` usage in policies to ensure proper user isolation.

## Phase 2: Vulnerability Assessment

**Goal**: Identify potential security gaps across the stack.

1.  **Backend Analysis**: Check for direct database access bypasses or weak business logic guards.
2.  **Frontend Analysis**: [Senior Frontend](.agents/skills/senior-frontend/SKILL.md) audits for XSS, CSRF, and improper storage of JWTs/Tokens.
3.  **Data Leak Check**: [Senior Data Analyst](.agents/skills/senior-data-analyst/SKILL.md) reviews logs to ensure no PII is being exposed.

## Phase 3: Hardening & Remediation

**Goal**: Implement fixes and stricter security controls.

1.  **Policy Hardening**: Apply more restrictive RLS policies where gaps were found.
2.  **Encryption**: Ensure sensitive fields are encrypted at rest if required.
3.  **Middleware Guards**: Implement additional authentication/authorization checks in Next.js middleware.

## Phase 4: Verification & Compliance

**Goal**: Validate that security measures are effective.

1.  **Role-Based Testing**: [Senior QC](.agents/skills/senior-qc/SKILL.md) tests the app using various user roles (Admin, Member, Guest) to verify isolation.
2.  **Penetration Test**: Simulated attacks on identified weak points.
3.  **Security Sign-off**: [Master Agent](.agents/master/rules.md) approves the security updates.
