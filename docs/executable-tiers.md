# Executable evidence tiers

Executable receipts share the schema `axiom_oracles.executable_receipt.v2` and
carry one required top-level `tier`. The consumer, not the receipt, declares
the `required_tier`; validation is exact equality, so the weaker tier can never
authorize the stronger claim.

## `source_reproduction`

`source_reproduction` archives a named RuleSpec commit, compiles from that
source with a configured engine binary, and replays committed cases. It binds
the source, configured engine checksum, generated artifact hashes, inputs, and
reproduced values. It proves that those sources can be rebuilt and replayed in
that configured environment.

This tier is valid only for a program with no published program artifact. It
does not prove that a stranger downloaded the published bytes, that the engine
was a released binary rather than a developer build with a configured digest,
or that the published artifact loads on that release.

## `release_receipt`

`release_receipt` is required wherever a published artifact exists. Its
stranger path downloads the engine release asset, proves its checksum is a
member of the governed release manifest, downloads the published program
manifest and artifact, verifies their hashes, runs those exact bytes, compares
strictly typed golden outputs, and signs only the completed receipt in an
isolated OIDC job. Consumption authenticates the receipt's exact bytes and
workflow provenance through its Sigstore bundle.

This is the tier that exposed two failures hidden by source or developer-path
testing: engine v0.1.0 could not load the published artifacts, and the hosted
API returned `226.5` while the released stranger path returned the statutory
whole-dollar `226`. A source rebuild is useful evidence, but it cannot answer
either release question.

## Denmark today

The current executable premise for `dk/boerne-og-ungeydelse` is honestly
`source_reproduction`. On 2026-08-20 the governed artifact registry was checked
before making this statement:

- the live `rulespec-us` publisher builds its `programs/` registry, whose
  entries are US-only and contain no DK program;
- live `rulespec-dk` at
  `9a9469edbbc4829847698cd0adf218771120b9cd` has neither a `programs/` nor an
  `artifacts/` registry and has no program-artifact publication workflow; and
- the archived `axiom-programs` artifact registry contains only `uk/`.

Accordingly, DK has no published artifact in the governed registry today.
`scripts/executable_reproduction.py` archives that exact DK RuleSpec commit,
compiles two composed programs into a temporary directory with the configured
engine, and replays ten cases. It records hashes but publishes none of those
compiled bytes. If a DK artifact is published later, consumer policy must move
to `required_tier: release_receipt`; the current source receipt must then be
rejected until the released binary and published artifact pass the stranger
path.

## Shared schema and policy

The machine-readable discriminated union lives at
`certificates/executable/receipt.schema.json`. Both tiers require `schema`,
`tier`, `program`, and an engine block, then select different exact bodies:

- `source_reproduction` carries source/rulespec identity, source reports,
  newly compiled artifact hashes, replayed cases, and a derived summary.
- `release_receipt` carries released-engine identity, published-artifact
  identity, golden fixtures and typed outputs, the exact command transcript,
  timestamp, and authenticated workflow provenance.

A missing `tier` is invalid. A `source_reproduction` receipt is invalid when
policy requires `release_receipt`. For the release tier, an engine checksum
that is not the selected release-manifest member is invalid even if every
other receipt field is internally consistent.
