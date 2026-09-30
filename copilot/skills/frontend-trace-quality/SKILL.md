---
name: frontend-trace-quality
description: Use when adapting frontend design documents, issue breakdown, meaningful test code, and traceability for a Next.js project while preserving existing templates and agreed specifications.
---

# Frontend Trace Quality

Use this skill when helping with a frontend project that needs to connect design documents, Figma, API assets, tests, and execution evidence without replacing existing templates or agreed specifications.

## Operating Principles

- Preserve the customer's template by default. Propose changes separately with reason, effect, cost, and approval path.
- Separate confirmed constraints, negotiable proposals, and local habits. Cite the source for each.
- Do not invent missing requirements. If a behavior is not defined, mark it as unresolved or propose options for human selection.
- For each project, ask which source governs observed API/IF behavior when design docs, API specifications, generated artifacts, implementation, and runtime observations conflict. Separate observed current behavior from approved requirements and from proposed fixes for bugs or risky behavior.
- Do not claim Automotive SPICE compliance. You may use bidirectional traceability and consistency checks as reference concepts at an appropriate web-project scale.
- Do not treat matching IDs, links, or coverage percentages as proof that the test semantically satisfies the design.
- If docs and code live in sibling repositories under one Codespace/workspace parent, record repo name, path, and commit for every source. Do not assume read access means write permission, and do not commit across repositories unless explicitly asked.

## Workflow

1. Inventory existing assets:
   - customer design template, Markdown screen design documents, Excel test specifications, Figma, OpenAPI, backend routes/handlers/serializers/permissions/exceptions/models, table design, tests, CI, approval rules.
   - docs repo/code repo paths, commits, applicable instructions, and target repo for issues.
   - classify each as source of truth, supporting material, implementation observation, or habit.
   - discover existing IDs, headings, sheet names, columns, merged cells, and test IDs with source and confidence. If extraction is uncertain, say so.

2. Review design documents:
   - check gaps, contradictions, and testability for inputs, display/enabled conditions, transitions, API interaction, communication failure, permissions, async states, empty states, and boundary values.
   - compare against Figma, OpenAPI/backend implementation, existing code, Storybook, and tests when available.
   - separate customer-facing behavior questions from internal design decisions.

3. Identify component and responsibility boundaries:
   - customer-visible behavior stays in the screen design or existing approved template when possible.
   - minimal supplemental notes may record common component, screen, custom hook, and API responsibilities.
   - if responsibility can be split multiple ways, present options with impact; do not choose silently.
   - base component-splitting proposals on existing common components, screens, hooks, Storybook, and tests. Include reuse opportunities, impact, migration cost, and unresolved questions.

4. Break design into issues:
   - draft issues with design source/version, user usage, expected behavior, scope/non-scope, dependencies/contracts, acceptance criteria, test layer, unresolved questions, and completion evidence.
   - do not turn unstated behavior into accepted criteria; stop with a proposal or question.
   - keep end-to-end use-case responsibility visible when splitting issues.
   - when implementation is requested and authorized, use the agreed issue, acceptance criteria, and existing architecture to make scoped code changes in IDE Copilot. Reopen the design decision if ownership or interfaces must change. Do not weaken acceptance criteria to fit the implementation; author/update meaningful tests and retain review evidence.

5. Derive meaningful test intent:
   - start from real usage, user actions, and expected behavior.
   - then add boundary values, error paths, states, permissions, and untested branches.
   - use coverage only as a diagnostic for missing meaningful tests.
   - Vitest for custom hooks, pure functions, and narrow logic contracts.
   - Storybook Interaction for screen states and component/screen combinations.
   - consider integration-style tests that combine the screen and real hooks to verify wiring and user-visible behavior; do not force every logic test into either pure-hook or E2E.
   - Playwright for main flows, transitions, and API-integrated behavior.
   - avoid duplicating every item in every layer.
   - API spies and mocks are acceptable when they verify meaningful payloads, suppressed sends, contracts, or visible results. Avoid tests that only prove a mock was called without checking the contract or outcome.

6. Maintain trace evidence:
   - link design item, document version/location, verification condition, test ID/path, execution result, commit, and evidence status.
   - distinguish candidate links from approved links.
   - flag missing links, missing test files, stale evidence, not-run results, failures, and orphan tests.
   - distinguish evidence that passed under an old requirement but is invalidated by a requirement change from evidence that newly failed when re-run. Preserve old evidence as history and mark it expired or requiring confirmation.
   - if this package's `scripts/trace_check.py` is available in the workspace, it may be used for mechanical trace checks against JSON exports of the trace table, test inventory, and results. Do not treat a clean mechanical check as semantic proof.

7. Escalate for human review:
   - semantic adequacy of expected results.
   - source-of-truth conflicts.
   - customer-facing behavior changes.
   - template changes.
   - unclear API behavior, authorization, side effects, asynchronous behavior, or error handling.
   - whether GitHub Issues may be created in the project repository.

## Outputs

Prefer concise tables:

- asset/source-of-truth inventory.
- design review findings.
- fixed/negotiable/habit classification.
- responsibility boundary candidates.
- component split proposals.
- issue breakdown drafts.
- test-layer assignment.
- trace consistency findings.
- customer approval questions.

When used in an approved Codespace/Copilot environment, read the permitted real documents and code directly instead of asking the user to manually retype IDs, headings, Excel columns, or test structure. If the usage surface or sharing scope is not approved, do not move project content outside that environment; ask for anonymized excerpts or a high-level description instead.
