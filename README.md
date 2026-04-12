# AI Engineering Toolkit

Tools, frameworks, and skills for applying AI to engineering workflows — with the rigor engineers expect.

## What's Here

### [Engineering Eval Harnesses](engineering-eval-harnesses/)

A framework for building automated evaluation loops that prove AI-powered tools produce correct, reliable output. Based on the principle that LLMs are probabilistic systems and must be tested statistically.

**Core pattern:** Generator agent (produces output) → Deterministic scorer (Python, no AI) → Analyzer agent (diagnoses gaps, patches pipeline) → Orchestrator (loops until threshold met).

Built as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code) but the methodology applies to any LLM-powered tool pipeline.

## Philosophy

1. **LLMs are probabilistic. Test them like it.** One successful run is not validation. Characterize the output distribution.
2. **Make everything deterministic that you can.** Push as much work as possible out of the probabilistic domain before involving the LLM.
3. **Separate generation from evaluation.** The system that creates the output must not be the system that judges it.
4. **Engineering rigor over demo magic.** The first working prototype is 20% of the effort. The harness is the other 80%.

## Author

**Mat Coalson** — Building energy engineer building AI tools for the engineering industry.

- [mbcoalson.com](https://mbcoalson.com)
- [GitHub](https://github.com/mbcoalson)
- [LinkedIn](https://linkedin.com/in/mbcoalson)
