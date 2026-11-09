---
name: easy-implement
description: >-
  Use to implement a batch of task briefs written by easy-task, one at a time, each ending in its own
  commit. Written to be followed step by step by a lower-tier model: follow the brief, do not improve on
  it, and escalate on ambiguity. Triggers on 执行task, 开工, 按简报编码, 实现这些任务, implement the
  briefs, execute the batch, code the tasks. Reached from easy-task; closes by calling easy-summary.
---

# Easy implement

**A task ends in a commit.** That one sentence sizes the task, names its proof, and decides when it is
finished.

This skill consumes a batch of briefs from `easy-task` and lands them one at a time. It is written to be
followed closely, step by step, because the model running it may be cheaper than the model that wrote
the briefs. **Follow the brief; do not improve on it.** The thinking was done upstream, and the brief is
the record of it.

If there is no batch of briefs yet, stop and call the Skill tool with "easy-task" first. Implementing
without a brief is the exact thing this chain exists to prevent.

Read [references/readability-law.md](references/readability-law.md) before writing the closing summary.

## The brief is the contract

Four rules, and they bind harder the weaker the model running this skill:

- **Do not reopen anything under "Settled".** Those decisions were made by the model that held the
  context. Re-deciding them here, with less context, is how a batch goes wrong quietly.
- **Do not invent a test seam.** Use the one the brief names. If that seam does not exist, stop.
- **Do not change an expected value.** The brief's expected values came from an independent source.
  Recomputing one from your own code makes the test prove nothing.
- **When the brief is ambiguous, wrong, or missing something you need, stop and escalate.** Say which
  brief and which line. Do not guess. A guess here is a decision made by the party least equipped to
  make it.

## The loop

Six steps. Each ends on a check you can make.

### 1. Confirm the batch

Every task in the phase has a brief, and the briefs are complete. If not, call the Skill tool with
"easy-task".

**Done when** the batch is in front of you, whole.

### 2. Take the frontier

Work the tasks whose predecessors are done, one at a time. Any task with nothing left in front of it can
start, which for a linear phase means top to bottom.

**Done when** one task is chosen, and you can say why it is the next one.

### 3. Restate, and check against the brief

Read part 2 of the brief, and restate the task in one line. Compare that restatement to part 1. If they
do not match, the brief has taught you something it did not intend — stop and escalate.

**Done when** the restatement matches part 1, or you have escalated.

### 4. Red, then green

Write one failing test at the seam the brief names, then the least code that passes it. Repeat per case,
in the order the brief lists them. Test only at that seam, and keep the slices vertical: one test, one
implementation, then the next case.

**Done when** every case in part 4 is green, and the tests read as behaviour rather than structure.

### 5. Commit

One commit per intent, in the conventional format. A failing test fixed afterwards earns its own commit,
because the next reader wants to see what broke.

**Done when** the working tree is clean, and a reader can tell from the log what changed and why.

### 6. Next, then close

Take the next frontier task and repeat from step 2. When the last task in the batch is committed, call
the Skill tool with "easy-summary". Produce the batch summary: what changed, what it means, and what is
still open.

**Done when** the summary document exists, and every task in the batch is either committed or named as
unfinished.

## Commits

`type(scope): what changed`, imperative, lowercase type: `feat(auth): count failed logins and lock at
the threshold`.

- One commit per intent. A task usually makes one, and a task holding two intents makes two.
- A fix after a red test is its own commit, `fix(auth): ...`. The test and the fix never share a commit.
- The commit body carries what the reading changed. That is where findings live, because a brief is not
  edited once it is written.

## Stop and escalate

Stop, name the brief and the line, and hand back to whoever wrote the brief when any of these holds. Do
not proceed on a guess:

- Reading part 2 changes the task.
- The seam the brief names does not exist, or sits lower than the brief claimed.
- A case's expected value is missing, or looks wrong against an independent check.
- The task needs a decision the brief did not make.

Escalating is not failure. It is the brief doing its job: catching at the seam the one thing the strong
model could not foresee.

## Anti-patterns

- Coding without the batch of briefs in hand.
- Reopening a decision the brief marked "Settled".
- Inventing a seam the brief did not name.
- Changing an expected value so the test matches the code.
- Guessing past an ambiguity instead of escalating.
- The red test and its fix sharing a commit.
- Finishing the last task without calling `easy-summary`.
