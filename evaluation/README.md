# Evaluation set

`cases.json` contains 20 synthetic labeled cases: five defects, five included revisions, five scope changes, and five ambiguous requests. The expected labels are evaluation-only metadata and are deliberately excluded from the payload shown to an agent.

Run the structural validation with:

```powershell
python scripts/run_evaluation.py
```

This validates unique IDs, category balance, non-empty prompts, and label separation. It does not claim that a model has achieved 100% accuracy; model scoring requires running these prompts through a chosen assessor and comparing the returned decisions to the held-out labels.
