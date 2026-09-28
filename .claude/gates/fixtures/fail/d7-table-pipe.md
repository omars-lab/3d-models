# Fixture: D7 must fire on a table row with an unescaped pipe in backticks

Asserted FAIL fixture for rule D7 (render). A pipe splits a table cell even
inside a code span, so this row has three cells under a two-cell header and
loses its last one (docs/research/pattern-outline-dsl-surface-survey.md had one).

| System | Word for the body outline |
|---|---|
| bikar | evaluator error vocabulary `'outline' | 'profile'` |

Expected: exactly one finding, `D7 (render)`.
