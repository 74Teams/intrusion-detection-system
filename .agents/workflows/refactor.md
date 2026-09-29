---
description: Code cleanup and technical debt reduction.
---

# Refactor Workflow

This workflow focuses on improving the internal structure of the code without changing its external behavior.

## Phase 1: Analysis & Scoping

**Goal**: Identify technical debt and define the boundaries of the refactor.

1.  **Code Audit**: [Senior Backend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-backend/SKILL.md) and [Senior Frontend](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-frontend/SKILL.md) identify "hotspots" (complex code, duplicate logic, slow queries).
2.  **Risk Assessment**: [Senior Product Owner](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-po/SKILL.md) assesses potential impact on existing features.
3.  **Refactor Plan**: [Master Agent](file:///Users/truongtritin/Github/tuhocproductv2/.agents/master/core.md) defines the specific modules to be refactored and sets "Done" criteria.

## Phase 2: Implementation

**Goal**: Execute the refactoring while maintaining all existing functionality.

1.  **Branch Creation**: Create a `refactor/` branch derived from the latest stable code.
2.  **Modular Cleanup**:
    - **Backend**: Refactor database queries, API logic, or domain models.
    - **Frontend**: Improve component hierarchy, hooks, or state management.
3.  **Unit Testing**: Ensure existing tests pass and add new ones for refactored logic.

## Phase 3: Validation & Performance

**Goal**: Ensure no regressions were introduced and performance has improved.

1.  **Regression Testing**: [Senior QC](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-qc/SKILL.md) runs full suite of manual and automated tests.
2.  **Performance Audit**: [Senior Data Analyst](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-data-analyst/SKILL.md) compares execution times (API/Frontend) before and after.
3.  **UI/UX Review**: [Senior UI/UX Designer](file:///Users/truongtritin/Github/tuhocproductv2/.agents/skills/senior-uiux/SKILL.md) ensures no visual regressions.

## Phase 4: Sign-off & Merge

**Goal**: Final review and integration into the main branch.

1.  **Internal Review**: Cross-role peer review (FE reviews BE logic, etc.).
2.  **Final Approval**: [Master Agent](file:///Users/truongtritin/Github/tuhocproductv2/.agents/master/rules.md) signs off on the refactor.
3.  **Merge**: Integrate into `main`/`develop` and monitor for any immediate issues.
