# Fixture: D6 and D7 stay quiet on spans and tables that render

Asserted PASS fixture for rules D6 and D7 (render).

A span that sits on one line: `bikar render --piece Coaster --format stl --check`.
A double-backtick span holding a backtick: `` a ` inside ``. A span opened at
the start of a line after a wrap:
`23 compared, 0 failed, 17 skipped/extra` closes on its own line.

```
A fence is code, so an unbalanced ` here is not a span.
```

| System | Word for the body outline |
|---|---|
| bikar | evaluator error vocabulary `'outline' \| 'profile'` |
| OpenSCAD | `offset`, `projection` |

Expected: zero findings.
