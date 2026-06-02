You are evaluating the quality of a software requirement-like statement.

Return JSON only. Do not include markdown fences.
Do not force a defect label when the statement is specific enough to test or review.

Repository or system: {repo}
Source type: {source_type}
Language/domain: {language}
Detection condition: {condition}

Statement:
{statement}

Allowed defect types:
- ambiguous_term
- missing_actor
- missing_trigger
- missing_expected_outcome
- missing_constraint
- not_testable
- overly_broad_requirement
- inconsistent_condition
- unsupported_external_assumption

If the condition is rubric_guided, apply these decision rules:
- Mark ambiguous_term only when the wording prevents a tester from knowing what to verify.
- Mark missing_actor only when neither a user role nor a system/component subject is clear.
- Mark missing_trigger when the event, input, or condition that starts the behavior is absent.
- Mark missing_expected_outcome when no observable result is stated.
- Mark missing_constraint when important boundaries, permissions, formats, states, or error cases are required but absent.
- Mark not_testable when the statement lacks observable behavior that could be checked by a unit, integration, UI, API, or manual test.
- Mark overly_broad_requirement when the statement is a broad goal rather than a bounded behavior.
- Mark inconsistent_condition only for explicit contradiction, not merely missing detail.
- Mark unsupported_external_assumption when the statement relies on facts not present in the text.
- For function specifications, treat a named function as a valid system actor.
- For testing-rule specifications, treat the mutator, checker, or tool as a valid actor.
- For layout-change specifications, treat the page, element, viewport, or layout checker as a valid actor.
- If tests, rules, or mutant descriptions make the expected behavior observable, do not mark not_testable only because the statement is short.

JSON schema:
{
  "has_defect": true,
  "confidence": 0.82,
  "defects": [
    {
      "type": "ambiguous_term",
      "severity": "minor",
      "span": "short copied phrase",
      "confidence": 0.78,
      "explanation": "one sentence"
    }
  ],
  "overall_quality": "acceptable | needs_revision | poor",
  "rewrite": "clearer testable statement, or empty string if no change is needed",
  "needs_human_review": false
}

Confidence rules:
- Use confidence near 0.5 when the statement is underspecified or the defect label is uncertain.
- Use confidence above 0.8 only when the exact span clearly supports the label.
- Set needs_human_review to true when multiple labels are plausible or evidence is weak.
