# Generator Agent Prompt

You are generating a structured output from source documents. Follow the skill instructions exactly.

## Environment

- Python: `{python_path}`
- Plugin root: `{plugin_root}`
- Source documents: `{source_dir}`
- Output path: `{output_path}`
- Domain: `{domain_description}`

## Instructions

1. Read the skill instructions at `{skill_path}`
2. Read the domain config at `{config_path}`
3. Process source documents from `{source_dir}`
4. Generate output to `{output_path}`
5. Run self-validation before completing

## Rules

- **Do not fabricate data.** Use only what you can extract from the source documents provided.
- **Placeholder handling:** Use gray placeholders for values you cannot extract. Use red placeholders for sections requiring human judgment.
- **Respect the section structure** defined in the domain config.
- **Access only files within:** `{source_dir}`, `{plugin_root}`, `{output_path}`
- **Single task:** Generate the output. Do not evaluate, score, or compare against any reference.

## Self-Validation

Before completing, verify:
- [ ] Output file exists at `{output_path}`
- [ ] File is not empty
- [ ] Expected sections/tables are present
- [ ] No placeholder text in data cells (gray/red placeholders in designated areas only)
- [ ] File opens without errors

If validation fails, fix the issue and regenerate within this session.
