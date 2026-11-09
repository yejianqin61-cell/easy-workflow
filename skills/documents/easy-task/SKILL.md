---
name: easy-task
description: >-
  Use to write the task briefs for one phase of a plan, as a handoff contract for a separate (often
  cheaper) model to implement. Stops before any code: easy-implement does the coding. Triggers on
  写task文档, 任务文档, 任务简报, 子任务, 拆任务, 写给低级模型去编码, write task briefs, task doc,
  handoff brief. Reached from easy-plan; hands off to easy-implement.
---

# Easy task

**A task ends in a commit — but this skill stops before the first line of code.** It writes the brief,
and the brief is the whole contract handed to whoever implements it. `easy-implement` does the coding,
and it may run on a cheaper model than the one writing here.

That split is the point. The strong model holds the context and makes the calls. It writes briefs dense
enough that a weaker model can execute them without a judgement call of its own. Every decision this
skill leaves open, the implementer has to invent. And the implementer is the party least equipped to
make it.

Write the whole batch first, then hand off. The batch is one phase: every task in it, and nothing from
the next one. `easy-plan` caps a phase at three to seven tasks, so that is three to seven briefs. The
batch is a gate: no code is written, by anyone, until every brief in the phase exists.

A phase holding more than seven tasks is two phases. Do not write twenty-five briefs: cut the phases
again, or take one phase and leave the rest of the plan for the next batch.

Read [references/readability-law.md](references/readability-law.md) before writing. Its twelve clauses
hold here.

## Output

Ask once: **Markdown, or a single-file HTML report?** For a batch of briefs, Markdown is nearly always
the answer. For the report, finish the Markdown first, then call the Skill tool with "easy-report".

## Write for the implementer

The reader is not you, and is likely less capable than you. Four rules follow, and they are the reason
this skill is split from the act:

- **Pin every decision with its location.** "The lock is server-side (ADR 0007)", not "the lock is
  server-side". A decision with no source gets re-litigated by whoever reads it next.
- **Give exact commands, not descriptions.** `npm test -- src/auth`, not "run the auth tests". A weaker
  model should never have to guess the invocation.
- **Every expected value comes from an independent source**, never from reading the code. A weaker model
  cannot tell a tautological test from a real one, so the brief must hand it the real one.
- **Name the stop triggers.** Where the task might snag, say so, and say that the implementer stops and
  escalates rather than guessing.

A brief that assumes the reader will "figure it out" has handed the hardest part to the least-equipped
party.

## Parts 1 to 4: the brief

One document per task, and one screen each. Four parts, and no others. A brief that runs past a screen
is carrying a fact that belongs in the code, or a second task.

### 1. Where this task sits

Three lines: the phase it belongs to with that phase's goal, what this task moves, and its edges. Name
what must be true before it starts, and what waits on it.

Codes travel with their names here as everywhere: `Phase 2 An admin can unlock`, `R-3 Let an admin
unlock a user`.

### 2. What the developer needs to know

Five blocks, each with a budget. This part decides whether the task lands: a fact written here goes
stale, and a path does not.

| Block | Write | Budget |
|---|---|---|
| **Read first** | 3 to 5 entries, `path — the question it answers` | 3 to 5 lines |
| **Settled** | the decisions this task must not reopen, each with where it lives | ≤4 lines |
| **Edges and seam** | the seam `easy-plan` named, what it touches, what it leaves alone | ≤3 lines |
| **Run** | the exact test command and typecheck command for this task | ≤3 lines |
| **Unknowns** | where it will probably snag, and the trigger to stop and escalate | ≤3 lines |

A path without a question is noise. These are entry points, not an inventory. Give the three to five
places a person handing this over would name. Then let the implementer expand the list by searching from
them.

The seam is the plan's. Restate it here, and add none: a brief that picks its own seam has reopened a
decision the plan closed.

### 3. The workflow

Numbered steps for this task alone. One action per step, and each step says what it produces. Five to
eight steps is normal. Step one is always **read part 2 and restate the task in one line**. That
restatement is what the reading was for, and the implementer's first chance to catch a brief that is
wrong.

### 4. The test cases

A table, and no test code:

| Case | Input | Expected | Seam |
|---|---|---|---|
| 1 | two failed logins | the user can still log in | `login()` |

The expected value comes from somewhere independent: a known-good literal, a worked example, the plan. An
expectation that recomputes what the code does passes by construction, and can never disagree with it.

Five cases is usually enough. The tests themselves are written red-first by `easy-implement`, one case at
a time.

<task-brief>

## 1. Where this task sits

- **Phase 1 A lock that actually locks**, whose goal is that a locked user cannot log in.
- **This task moves R-1 Lock out after 3 failed logins** into place: the counter reads and writes real
  data.
- **Starts after**: nothing. **Waits on it**: `Clear the deadline and keep the count`.

## 2. What the developer needs to know

**Read first**

- `src/auth/login.ts` — where the login path branches today, and where a refusal fits.
- `src/auth/failedAttempts.ts` — the threshold, the counting rule, and who reads them.
- `docs/adr/0007-session-storage.md` — why the session record exists, so the lock does not duplicate it.

**Settled**

- The lock is server-side. The plan refused a client-side check.
- The counter belongs to the user, not to the session.
- The threshold comes from the constant, and not from configuration yet.

**Edges and seam**

- Touches `src/auth`. Leaves the admin surface alone.
- Seam: the existing `login()` entry point, and no new seam.

**Run**

- `npm test -- src/auth`, then `npm run typecheck`.

**Unknowns**

- Whether two failures can interleave and lose a count. If the read and the write cannot be made atomic
  here, stop and escalate.

## 3. The workflow

1. Read the three files above, then restate this task in one line.
2. Write the failing test for case 1, at the `login()` seam.
3. Count the failure, and write the deadline at the threshold. Run the test.
4. Add cases 2 and 3, red first, then green.
5. Run `npm test -- src/auth`, then `npm run typecheck`.
6. Commit.

## 4. The test cases

| Case | Input | Expected | Seam |
|---|---|---|---|
| 1 | two failed logins | the user can still log in | `login()` |
| 2 | three failed logins | the third returns the lock error | `login()` |
| 3 | three failures, then the right password | still the lock error | `login()` |

</task-brief>

## Process

Three steps. Each ends on a check you can make.

### 1. Write the whole batch

One brief per task in the phase, using the template above. If the phase has no plan yet, call the Skill
tool with "easy-plan" first.

**Done when** every task in the phase has a brief, and every brief fits its budgets.

### 2. Gate on self-sufficiency

Write no code. Read each brief as if you were a model with no memory of this conversation and no access
to the strong model that wrote it. A brief passes only if it can be executed from its own four parts. That means
every decision pinned, every command exact, every expected value independent, every snag given a stop
trigger.

**Done when** the batch is complete and every brief passes that cold read.

### 3. Hand off

Deliver the briefs to `easy-implement`, or to the implementer model directly. This skill writes no code
and lands no commit.

**Done when** the briefs are delivered, and nothing in them waits on a fact only you hold.

## Stop and ask

Stop, and ask the user, before handing off when any of these holds:

- A task needs a decision the plan did not make.
- The plan's seam does not exist, or sits lower than the plan claimed. Fixing the brief here is cheaper
  than discovering it mid-implementation.
- A test case cannot get an expected value from an independent source.
- The phase is larger than seven tasks and will not cut cleanly.

## Anti-patterns

- Writing any code. That is `easy-implement`'s job, and starting it here defeats the split.
- A brief written as paragraphs of prose. Blocks, and lines.
- A read-first list with no questions attached. That is an inventory, not a handoff.
- A decision stated with no location, so the implementer re-opens it.
- A command described rather than written out.
- A test whose expected value recomputes what the code does.
- A snag named with no instruction to stop, so the implementer guesses past it.
- Fewer than three or more than seven briefs in one batch.
