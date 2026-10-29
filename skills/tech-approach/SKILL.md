---
name: tech-approach
description: Turn client meeting notes into a technical approach — the problem, open questions, two solution scenarios sized to the client (from connecting their existing tools with n8n up to a full build), trade-offs and a recommendation. Use when the user pastes meeting notes, a call transcript, or a feature/problem discussion and wants to know how to build or solve it.
argument-hint: "[paste meeting notes, or a path to a notes file]"
---

# Technical approach from meeting notes

The user pastes meeting notes (or gives a file path) and wants a technical plan they can act on or bring back to their team. The notes are usually from a **client** meeting. They are early in their career with AI tooling, so be clear and concrete, and explain jargon briefly the first time it appears.

## Size the solution to the client

Not every client needs a new project. Often the best answer is to connect the tools the client already uses. Treat the solution as a ladder and start at the lowest rung that solves the problem:

1. **Connect what they have**: install n8n and automate between the client's existing tools (CRM, spreadsheets, email, forms, ERP…). No custom app, no database of our own.
2. **Add a light layer**: n8n plus a small piece of ours, such as a Supabase table to store or combine data, a simple dashboard, or a form.
3. **Build a product**: a full Supabase + Next.js app, with n8n for integrations. Only when the client needs their own interface, users and logins, or logic their tools can't handle.

The two scenarios should sit on **different rungs**, usually the lightest one that works and one rung up. Say clearly what the bigger option gets the client that the lighter one doesn't, so the choice comes down to value, not to what's more interesting to build. Never jump to rung 3 without saying why rungs 1–2 aren't enough.

## Time is the main constraint

The team often won't have much time, so treat delivery time as a first-class factor, not a footnote:

- **Find the deadline.** Pull it from the notes. If there isn't one, make "when does the client need this?" an open question and assume it's soon.
- **Estimate in working days** for each scenario, and give **time to first result**: how soon the client sees something working.
- **When time is tight, recommend the faster scenario** even if it's less complete, and say so plainly.
- **Plan to grow, not rebuild.** Where possible, set up the lighter scenario so it can become the bigger one later (e.g. n8n writes to a Supabase table that a future dashboard can read). Point out when an option would have to be thrown away to upgrade.
- **Keep the write-up short.** The user's reading time counts too.

## Our stack

The team already uses these. Build scenarios on them by default:

- **n8n**: workflows, automations, integrations with third-party APIs, scheduled jobs, webhooks
- **Supabase**: backend (auth, storage, edge functions, realtime, row-level security)
- **Postgres**: database (through Supabase)
- **Next.js**: front-end
- **Docker**: containers

How to use it:
- At rung 1 the client's own tools do most of the work and n8n is the only part of our stack involved. That's fine.
- At least one scenario should use only this stack plus the client's existing tools. Say which part of the stack does what (e.g. "n8n handles the email sync, Supabase stores the result, Next.js shows it").
- Choose between n8n and code on purpose: n8n for glue between services and anything non-developers may need to change; Supabase edge functions or Next.js server code for core logic that needs tests, versioning or low latency.
- Use Supabase built-ins (auth, RLS, storage, realtime) before adding a separate service for the same job.
- Only bring in a new tool when the stack clearly can't do the job well. Flag it as **new to the stack** and say what it would cost the team to adopt (learning, hosting, price).
- Not yet known: hosting/cloud provider, CI/CD, team size. If the approach depends on one of these, list it under open questions.

## Steps

1. **Read the input.** If `$ARGUMENTS` is a file path, read that file. If it's empty, ask the user to paste the notes.
2. **Ground it in the code.** If the current directory is a code repository and the notes relate to it, look at the relevant parts (stack, existing patterns, similar features) before proposing anything. Base the scenarios on what's actually there, not on a generic stack.
3. **Don't invent requirements.** If the notes leave out something that changes the approach (scale, deadline, budget, who maintains it), list it under open questions and state the assumption you're making.
4. **Write the response** in the format below.

## Output format

### The problem
2–4 sentences: what needs to be built or solved, and for whom. Pull out any hard constraints mentioned (tech already chosen, budget).

**Deadline:** the date or timeframe from the notes, or "not stated".

**Client's current tools:** list the tools the client already uses, as mentioned in the notes. If the notes don't say, make "what tools do they use today?" the first open question, since it decides whether rung 1 is possible.

### Open questions & assumptions
Bullets. Mark each as **ask the team** or **assumed: …**. Only include ones that would change the approach.

### Scenario A — <short name> *(rung N)*
- **Approach:** how it works, in a few sentences.
- **Tools / tech:** specific libraries, services or patterns, with one line each on why.
- **Steps:** a rough build order (3–7 steps).
- **Pros / cons:** honest trade-offs.
- **Time:** effort in working days, and time to first result.
- **Risk:** the main thing that could go wrong or slow it down.

### Scenario B — <short name> *(rung N)*
Same structure, on a different rung from A. Add **What it adds over A:** what the client gains for the extra cost. Skip B only if the problem clearly fits one rung, and say why.

### Recommendation
Pick one and say why in 2–3 sentences, tied to the deadline and other constraints from the notes. Say what would make you switch to the other. If the lighter scenario can grow into the bigger one, suggest starting light and upgrading later.

### Next steps
3–5 concrete actions the user can take this week, including the questions to bring back to the team.

## Guidelines
- Prefer the simplest approach that meets the stated needs, and call out over-engineering.
- Name real, current tools. Search the web if a tool choice depends on recent pricing or features.
- Keep it scannable. The user may forward it, so it should make sense without the original notes.
- At the end, offer in one line to save the result as a Markdown file or a shareable doc.
