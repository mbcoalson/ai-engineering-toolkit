# AI Engineering Toolkit

Practical patterns for applying AI to engineering workflows without mistaking a plausible answer for a validated one.

This repository is an ongoing collection of tools, frameworks, and skills for building AI-assisted technical workflows that can be inspected, tested, and improved. It is not a production platform or a claim that an AI system can replace engineering judgment.

## Start here

### [Engineering Eval Harnesses](engineering-eval-harnesses/)

A Claude Code skill and template set for evaluating structured outputs such as documents, spreadsheets, and JSON. The core pattern separates generation from evaluation:

```text
Generator → deterministic scorer → independent analysis → bounded iteration
```

Use it when a workflow needs more than a persuasive demo: a known-good reference, explicit scoring criteria, inspectable state, and a stopping condition.

The harness is designed around a few working principles:

1. **LLMs are probabilistic. Test them like it.** One successful run is not validation.
2. **Make what you can deterministic.** Use code and explicit checks before asking a model to reason.
3. **Separate generation from evaluation.** The system producing work should not be its only judge.
4. **Keep humans responsible for consequential assumptions.** A harness can expose uncertainty; it cannot make a decision accountable.

## Status and boundaries

This is an active, evolving project. The included material is a framework and set of templates—not a substitute for domain validation, professional review, security assessment, or production-readiness testing. Individual workflows must define their own data boundaries, evidence sources, and acceptance criteria.

The current harness is built as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code), but the evaluation approach is intended to be useful across model providers and agent frameworks.

## Repository guide

- [`engineering-eval-harnesses/`](engineering-eval-harnesses/) — skill, templates, guidance, and an audit report structure
- [`engineering-eval-harnesses/README.md`](engineering-eval-harnesses/README.md) — what the harness contains and how to begin
- [`engineering-eval-harnesses/best-practices.md`](engineering-eval-harnesses/best-practices.md) — curated principles and sources

## About

Built by [Mat Coalson](https://mbcoalson.com), a building energy engineer exploring AI tools for rigorous technical work.
