# Requirement Quality Defect Taxonomy

This taxonomy defines the first silver-label setup for BAI4. The unit of
analysis is a short requirement-like text: issue statement, feature
description, or generated acceptance criterion.

## Defect Types

| Label | Meaning | Typical evidence |
| --- | --- | --- |
| `ambiguous_term` | The text uses vague wording that can be interpreted in several ways. | correctly, properly, appropriate, robust, user-friendly, as expected, etc. |
| `missing_actor` | The actor or system subject responsible for the behavior is not clear. | no user, admin, system, API, service, component, client, server, model, or module subject |
| `missing_trigger` | The event or condition that starts the behavior is absent. | no when, if, after, before, on, during, once, while, given |
| `missing_expected_outcome` | The observable result is not stated. | no should, must, return, display, show, create, update, reject, error, save, send |
| `missing_constraint` | Required limit, condition, or boundary is underspecified. | no input, format, permission, time, state, config, status, threshold, edge case, error condition |
| `not_testable` | The text cannot be verified directly by a test or review. | no observable assertion, output, response, UI state, file, metric, exception, or persisted change |
| `overly_broad_requirement` | The statement asks for a large goal without decomposed behavior. | improve, enhance, support, handle, optimize, refactor, complete, all/everything with little detail |
| `inconsistent_condition` | The text contains conflicting conditions or incompatible expected outcomes. | contradictory modal verbs, explicit conflict, both enable and disable the same behavior |
| `unsupported_external_assumption` | The text relies on external facts not present in the input. | assumes hidden APIs, product policy, third-party behavior, UI screens, or user roles not stated |

## Label Levels

The initial dataset uses silver labels:

- `gold_label_source=rule_seeded`: defect labels produced by deterministic
  heuristics over the text.
- `gold_label_source=synthetic_injected`: clean acceptance criteria from BAI1
  with one controlled defect injected.
- `gold_label_source=human_review`: reserved for later manual annotation.

Silver labels are suitable for pilot model screening and prompt comparison.
They should not be claimed as final human ground truth in the manuscript.

## Detection Output Contract

Models must return JSON only:

```json
{
  "has_defect": true,
  "defects": [
    {
      "type": "ambiguous_term",
      "severity": "minor",
      "span": "properly",
      "explanation": "The term does not define observable behavior."
    }
  ],
  "overall_quality": "needs_revision",
  "rewrite": "A clearer, testable version of the requirement."
}
```

Allowed severities: `minor`, `major`, `critical`.

