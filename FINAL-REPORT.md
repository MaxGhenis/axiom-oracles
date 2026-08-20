# Executable tier reconciliation final report

## Outcome

PR #461 now treats the two executable producers as different evidence tiers,
not competing implementations. The branch was rebased onto current `main` at
`dd4ec472acd711c6481c381c20bcce034f3ced6b`.

The shared receipt contract is `axiom_oracles.executable_receipt.v2` with a
mandatory `tier`. Consumer policy requires exact tier equality: a source
reproduction can never satisfy a release-receipt requirement.

Colorado SNAP no longer carries attested executable prose. Its published
artifact makes `release_receipt` mandatory, so the generated certificate is
computed-false until an authenticated receipt and Sigstore bundle are produced
by the governed workflow and its workflow SHA is separately allowlisted. No
receipt, bundle, or verdict was fabricated in this branch.

## Tier definitions

### `source_reproduction`

This tier archives an exact RuleSpec commit, compiles from source with the
configured engine binary, hashes the temporary compiled artifacts, and replays
committed cases. It proves reproducibility in that configured source-build
environment.

It is valid only when the program has no published artifact. A configured
engine checksum can identify a developer binary, so this tier does not claim
that a released engine loaded or ran published bytes.

### `release_receipt`

This tier is required wherever a published artifact exists. It downloads the
released engine asset, proves the asset checksum is the selected member of the
committed release manifest, downloads the published program manifest and
artifact, verifies their hashes, executes those exact bytes by the public
stranger path, checks exact JSON types and golden values, and authenticates the
completed receipt's exact bytes through the isolated OIDC signing job.

This is the tier that caught failures hidden by source or developer paths:
engine v0.1.0 could not load the published artifacts, and the hosted API
returned `226.5` while the released stranger path returned the statutory
whole-dollar `226`.

## Denmark registry verification

The governed artifact registries were checked before classifying DK:

- the live `rulespec-us` publisher builds the `programs/` registry; at
  `c55778119c0dd208a5ea3366092a17d0b0392c8b` its entries are US-only and
  include no DK program;
- live `rulespec-dk` at
  `9a9469edbbc4829847698cd0adf218771120b9cd` has neither a `programs/` nor an
  `artifacts/` registry and has no program-artifact publication workflow; and
- the archived `axiom-programs` artifact registry contains only `uk/`.

Therefore DK has no published program artifact in the governed registry
today. Its current executable premise is honestly `source_reproduction`:
`scripts/executable_reproduction.py` archives that exact RuleSpec commit,
compiles two composed programs into a temporary directory with the configured
engine, and replays ten cases. It records hashes but publishes none of those
compiled bytes. If a DK artifact is published, consumer policy must move to
`release_receipt` and reject the existing source receipt.

## Shared schema and consumer policy

The coordination surface for this PR and the parallel #427 rebase is
`certificates/executable/receipt.schema.json`. Its raw SHA-256 is:

```text
4035fb618468a9c1bca4da0d39fd06912c969c7903e501f19b15551c92bf0ae2
```

The schema is an exact `oneOf` discriminated union:

- common identity: `schema`, `tier`, `program`, and a tier-specific `engine`;
- source body: generator/period, RuleSpec identity, source reports, newly
  compiled artifact hashes, replayed cases, and derived summary;
- release body: released-engine identity, published-artifact identity, golden
  input and typed outputs, exactly nine stranger-path commands, timestamp, and
  workflow provenance.

The CO executable manifest hash-binds those schema bytes and owns
`required_tier: release_receipt`. `scripts/certify.py` independently owns the
same required tier plus receipt/manifest paths, golden-input hash, and exact
expected outputs. DK's registry requires `source_reproduction`. Accepted tier
is emitted only after validation; rejected evidence records the required
policy without falsely labeling the receipt. Existing NZ and tariff producers
retain their legacy schemas until separately migrated.

The shared envelope does not replace deeper producer validation. DK still
re-derives source, engine-pin, compilation, and case claims. The release
validator still re-derives release-manifest membership, published-artifact and
fixture hashes, exact commands and outputs, workflow allowlisting, and the
Sigstore-authenticated exact receipt bytes.

## Release fail-closed boundary

The original sign-only design remains intact:

1. `produce` has `permissions: {}`, fetches the exact public source SHA without
   credentials, accepts no engine/artifact/manifest override, rejects
   credential-bearing environments, and runs only on Linux x86_64.
2. It downloads the selected release and artifact over HTTPS, verifies both
   shell and Python SHA-256 checks, checks the exact engine version, and records
   the fixed nine-command stranger path with zero exit codes and the raw input
   hash.
3. `sign` alone receives `id-token: write` and `attestations: write`. It receives
   only the completed receipt, runs no repository or engine code, re-checks the
   v2 schema, `release_receipt` tier, and immutable run fields, then attests the
   exact receipt bytes.
4. Consumption requires the receipt and bundle together, a byte-pinned public
   Sigstore root, exact certificate/workflow/source/run fields, hosted-runner
   identity, transparency timestamp, one signed subject, and the signed receipt
   digest. Missing or malformed evidence computes false.

## Requested mutants

All three requested cases are explicit and fail closed:

- the real committed DK `source_reproduction` receipt at the CO
  release-required consumer is rejected by tier policy;
- a release receipt whose engine checksum is not the selected member of
  `engine-releases.json` is rejected; and
- deleting `tier` from either producer's receipt is rejected.

Additional coverage rejects schema-byte drift, consumer attempts to weaken the
manifest's tier, cross-tier field smuggling, a developer-engine command,
receipt mutation after signing, wrong golden types/values, malformed or copied
provenance, path escapes, duplicate keys, non-finite values, and missing trust
assets.

## Generated certificate state

- `dk/boerne-og-ungeydelse`: executable computed true at
  `source_reproduction`; the certificate remains certified yes.
- `us-co/snap`: executable computed false at required tier
  `release_receipt`; the stable blocker is
  `executable: receipt: file does not exist`. Its separate exercise premise is
  also incomplete, so certification remains unavailable.
- NZ and tariff certificate semantics are unchanged apart from regenerated
  tier-aware explanatory text.

## Verification

- Consolidated tier-focused battery: **106 passed**.
- Certification-mutant battery: **210 passed**.
- Full repository suite: **2,940 passed, 73 skipped, 2 failed** in 26m06s.
  Neither failure touches this branch's changed surface:
  - `test_dashboard_loader.py::test_loader_equivalence` could not resolve the
    npm registry when `npx` tried to fetch esbuild. Running the test's exact
    bundle and comparison with the cached esbuild binary passed with
    `EQUIVALENT: true` and zero legacy leftovers.
  - `test_entitledto_report.py::test_pe_reference_reproduces_from_policyengine`
    found the globally installed optional `policyengine-uk 2.75.3`, whose model
    no longer contains `council_tax_reduction`. The test, generator, adapter,
    and committed reference fixture are byte-identical to `origin/main`.
- `scripts/certify.py --check`: passed.
- `scripts/exercise_census.py --check`: passed.
- Ruff, targeted Python compilation, actionlint, schema-pin comparison, JSON
  parsing, and `git diff --check`: passed.
- Independent final schema/requirements and security audits found no
  implementation blocker or release-receipt bypass. They separately reran the
  tier and fail-closed mutant surfaces.

## Publication and handoff

The local reconciliation is complete on
`autogo/executable-producer-rebuild`, but publication is externally blocked.
Two exact guarded pushes failed before authentication because terminal Git
could not resolve `github.com`. The connected GitHub interface then returned
`user cancelled MCP tool call` for both a harmless blob capability probe and
the authorized PR-description update. Neither connector attempt created an
object or changed PR metadata.

A final read confirmed PR #461 remains open, draft, unmerged, and unchanged at
remote head `f4ffd1b2d349757dac88ead1b0adc86d0b4ea865`. The rebased local history
cannot be published through either available transport in this environment.
A maintainer can publish it from this exact worktree with the same lease guard:

```bash
git push \
  --force-with-lease=refs/heads/autogo/executable-producer-rebuild:f4ffd1b2d349757dac88ead1b0adc86d0b4ea865 \
  origin HEAD:refs/heads/autogo/executable-producer-rebuild
```

The PR description should then be replaced with the tier definitions, DK
registry result, shared-schema contract, requested mutants, and test totals in
this report. The PR must remain unmerged because the new workflow still
requires the repository's cross-family signing/CI review and maintainer
approval.

After the workflow lands unchanged on `main`, a maintainer must dispatch it,
download the exact receipt/bundle pair, verify the attestation and run metadata,
copy both files byte-for-byte to their declared paths, separately allowlist
only the authenticated workflow SHA, and regenerate certificates. No
maintainer sets the executable verdict directly.
