# Fixture: D2 must fire on a validator with no worked examples

Asserted FAIL fixture for rule D2 (K6). This reproduces the shape of the
c2-assembly defect: a fit-class validator whose acceptance windows were never
worked through, and which turned out to accept the same gap under two adjacent
classes.

**Validator:** each fit class accepts a diametral gap within its window plus or
minus 0.05 mm, so adjacent fit classes can never overlap.

The claim is stated and never exercised. Expected: exactly one finding,
`D2 (K6)`, naming the missing PASS and FAIL examples.
