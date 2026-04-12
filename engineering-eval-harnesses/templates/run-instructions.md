# Run Instructions (CLAUDE.md Template)

This file is placed in each run directory as CLAUDE.md. It establishes operational boundaries for agents working within the overnight framework.

## Environment

- OS: {operating_system}
- Python: `{python_path}`
- Plugin root: `{plugin_root}`
- Output format: `{output_format}`

## Allowed Modifications

You may ONLY modify files listed here:
{allowed_modifications}

## Forbidden Files

Do NOT modify these files. The orchestrator will reject commits that touch them:
{forbidden_files}

## Agent Rules

1. **Single-purpose invocations.** You are either generating or analyzing, never both.
2. **Tool allowances for sub-agents:** `--allowedTools "Bash,Read,Write,Edit,Glob,Grep"`
3. **No fabricated data.** Use placeholders for values you cannot extract.
4. **Commit every change** with a descriptive message following the format in your prompt.
5. **Read STATE.json** before proceeding — it tells you the current iteration and scores.
6. **Read the change log** — do not re-attempt approaches that have already failed.

## Validation

Before completing any generation task, verify:
- [ ] Output file exists
- [ ] Expected sections/tables are present
- [ ] No formatting errors
- [ ] File opens without corruption

## Domain-Specific Instructions

{domain_specific_instructions}
