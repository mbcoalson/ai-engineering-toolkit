"""
Deterministic Scorer Template
==============================
Compares a generated output against a known-good reference.
Produces structured JSON scores across multiple dimensions.

IMPORTANT: No AI in the scoring path. The same input must always produce
the same score. This makes regression detection reliable. An LLM scorer
introduces variance that makes "pipeline got worse" indistinguishable
from "scorer scored differently."

Usage:
    python scorer_{domain}.py <generated_path> <reference_path> [--output score_report.json]

Customize:
    1. Replace {domain} in the filename
    2. Implement load_generated() and load_reference() for your output format
    3. Implement each score_* function for your dimensions
    4. Update DIMENSIONS with your scoring config
    5. Set weights and hard-fail thresholds
"""

import json
import sys
from pathlib import Path

# --- Configuration ---
# Mirror your harness-config.yaml dimensions here.
DIMENSIONS = {
    "data_accuracy": {
        "weight": 0.40,
        "target": 0.95,
        "hard_fail_threshold": 0.70,  # Below this = automatic pipeline fail
        "description": "Cell-by-cell data comparison against reference"
    },
    "content_completeness": {
        "weight": 0.30,
        "target": 0.90,
        "hard_fail_threshold": None,
        "description": "All expected sections/tables present with content"
    },
    "structural_fidelity": {
        "weight": 0.20,
        "target": 0.85,
        "hard_fail_threshold": None,
        "description": "Heading hierarchy, table placement, formatting"
    },
    # Add dimensions as needed. Keep each focused: one dimension, one concern.
}


# --- Loaders ---
# Customize these for your output format.

def load_generated(path: Path) -> dict:
    """Parse the generated output into a structured dict for comparison.

    Examples by format:
        DOCX: python-docx -> {sections: [...], tables: [...]}
        XLSX: openpyxl -> {sheets: {name: [[cell_values]]}}
        JSON: json.load directly
        PDF:  pymupdf/pdfplumber -> extracted text + tables
    """
    raise NotImplementedError("Implement for your output format")


def load_reference(path: Path) -> dict:
    """Parse the reference output into the same structure as load_generated.

    Must produce an identical schema so dimension scorers can compare
    field-by-field.
    """
    raise NotImplementedError("Implement for your output format")


# --- Dimension Scorers ---
# Each returns a float 0-100. Higher is better.

def score_data_accuracy(generated: dict, reference: dict) -> float:
    """Compare data values cell-by-cell or field-by-field.

    Consider:
        - Numeric tolerance (e.g., within 0.1%)
        - String normalization (whitespace, casing)
        - Missing vs. extra fields
    """
    raise NotImplementedError("Implement data accuracy scoring")


def score_content_completeness(generated: dict, reference: dict) -> float:
    """Check that all expected sections/tables/fields are present.

    Consider:
        - Required sections present
        - No placeholder text remaining in data cells
        - Expected number of rows/entries
    """
    raise NotImplementedError("Implement content completeness scoring")


def score_structural_fidelity(generated: dict, reference: dict) -> float:
    """Compare document structure: headings, table placement, formatting.

    Consider:
        - Heading hierarchy matches
        - Tables appear in correct sections
        - Column headers match
        - Merged cells, styles (if relevant)
    """
    raise NotImplementedError("Implement structural fidelity scoring")


# --- Composite ---

SCORER_MAP = {
    "data_accuracy": score_data_accuracy,
    "content_completeness": score_content_completeness,
    "structural_fidelity": score_structural_fidelity,
}


def compute_composite(scores: dict) -> tuple[float, bool]:
    """Weighted average with hard-fail checking.

    Returns:
        (composite_score, passed) — passed is False if any dimension
        is below its hard_fail_threshold.
    """
    composite = 0.0
    passed = True

    for dim_name, config in DIMENSIONS.items():
        score = scores.get(dim_name, 0.0)
        composite += score * config["weight"]

        if config.get("hard_fail_threshold") is not None:
            if score < config["hard_fail_threshold"]:
                passed = False

    return composite, passed


# --- Diff Summary ---

def generate_diff_summary(generated: dict, reference: dict, scores: dict) -> str:
    """Human-readable markdown summarizing the gaps.

    This goes to the Analyzer agent. Sort by impact so the Analyzer
    targets the highest-value fix first.
    """
    lines = ["# Diff Summary\n"]

    for dim_name, score in sorted(scores.items(), key=lambda x: x[1]):
        config = DIMENSIONS.get(dim_name, {})
        target = config.get("target", 0.0)
        gap = target * 100 - score
        if gap > 0:
            lines.append(f"## {dim_name} (score: {score:.1f}, target: {target*100:.1f}, gap: {gap:.1f})")
            lines.append(f"_{config.get('description', '')}_\n")
            # TODO: Add specific gap details here
            lines.append("")

    if not any("##" in line for line in lines):
        lines.append("All dimensions at or above target. No gaps to report.")

    return "\n".join(lines)


# --- Main ---

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <generated_path> <reference_path> [--output report.json]")
        sys.exit(1)

    generated_path = Path(sys.argv[1])
    reference_path = Path(sys.argv[2])

    output_path = Path("score_report.json")
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    # Load
    generated = load_generated(generated_path)
    reference = load_reference(reference_path)

    # Score each dimension
    scores = {}
    for dim_name, scorer_fn in SCORER_MAP.items():
        scores[dim_name] = scorer_fn(generated, reference)

    # Composite
    composite, passed = compute_composite(scores)

    # Diff summary
    diff_summary = generate_diff_summary(generated, reference, scores)

    # Build report
    report = {
        "composite": round(composite, 2),
        "passed": passed,
        "dimensions": {
            name: {
                "score": round(scores[name], 2),
                "target": DIMENSIONS[name]["target"] * 100,
                "weight": DIMENSIONS[name]["weight"],
                "gap": round(DIMENSIONS[name]["target"] * 100 - scores[name], 2)
            }
            for name in DIMENSIONS
        }
    }

    # Write outputs
    output_path.write_text(json.dumps(report, indent=2))
    Path("diff_summary.md").write_text(diff_summary)

    # Console output
    print(f"\nComposite: {composite:.1f} ({'PASS' if passed else 'FAIL'})")
    for name, data in report["dimensions"].items():
        status = "OK" if data["gap"] <= 0 else f"gap: {data['gap']:.1f}"
        print(f"  {name}: {data['score']:.1f} / {data['target']:.1f} ({status})")


if __name__ == "__main__":
    main()
