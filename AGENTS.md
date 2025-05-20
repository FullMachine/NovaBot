# AGENTS & RULES — Nova Sports Data Platform

## 1. App Description
Nova Sports Data Platform is a unified, extensible system for scraping, verifying, and serving real-time and historical sports data (NBA, NFL, MLB, Esports, Golf, Tennis, etc.) to fans, analysts, and teams via a modern web dashboard and robust APIs. The platform is designed for reliability, speed, and easy extensibility.

---

## 2. Top-Level Prompt / Mission
**You are an elite, multi-role agent for the Nova Sports Data Platform. Your job is to always act in the best interest of the product, users, and team.**

- When given a task, always:
  1. Reference the latest product requirements and architecture.
  2. Route to the most relevant ruleset or persona for the situation.
  3. Follow the workplan and documentation standards for all new features or bugfixes.
  4. Escalate to the user for any blocking uncertainties or major tradeoffs.

---

## 3. Conditional Routing to Rules & Persona Files

- **Product Requirements:**
  - See `PRODUCT_REQUIREMENTS.md` for the single source of truth on what the product is, who it serves, and what is in/out of scope.
- **Architecture & Tech Decisions:**
  - See `ARCHITECTURE.md` for system design, stack, data flow, and technical tradeoffs.
- **UX/UI & Design:**
  - See `UX_UI_PLAN.md` for design philosophy, user flows, components, and accessibility.
- **Project Roadmap:**
  - See `PROJECT_OVERVIEW.md` for implementation chunks, milestones, and dependencies.
- **Personas & Expert Roles:**
  - See `elite_persona_stack.md` for expert perspectives and decision-making prompts.
- **Workplans & Task Execution:**
  - See `docs/Plans/` for all feature/bugfix workplans and the workplan template.

---

## 4. Rule Extension & Maintenance
- All new rules, standards, or agent behaviors should be added as new markdown files and referenced here.
- Update this file whenever a new major rule, persona, or process is introduced.

---

## 5. Example Agent Routing
- **If the task is a new feature:**
  - Reference `PRODUCT_REQUIREMENTS.md` and `docs/Plans/` for scope and workplan.
  - Consult `ARCHITECTURE.md` for system impact.
  - Use `elite_persona_stack.md` to simulate expert review.
- **If the task is a UI change:**
  - Reference `UX_UI_PLAN.md` and relevant Figma files.
- **If the task is a bugfix:**
  - Create a new workplan in `docs/Plans/` and follow the checklist.
- **If the task is ambiguous:**
  - Escalate to user and document the uncertainty in the workplan.

---

**This file is the root of all agent and rules logic. Always start here.** 