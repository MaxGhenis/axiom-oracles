# PROGRESS — PR #468 cross-lane reconciliation

## State

- Branch/worktree: `evidence-validator-land` in
  `/Users/maxghenis/TheAxiomFoundation/_worktrees/evidence-land`.
- Requested operation: finish the `origin/main` reconciliation in place, keep
  the strict evidence layer together with the DK/NZ multi-program and
  oracle-switch machinery, regenerate all certificates and downstream
  artifacts, run every freshness check and the full requested battery, then
  push the branch without merging PR #468.
- Starting checkout: clean at `27e3a51fc`; contrary to the task handoff,
  `MERGE_HEAD` is absent. The tip contains an earlier merge of main at
  `7f4e579b3`, but current `origin/main` is `a33cadea0` and is not an ancestor.
  The current remote-tracking tip will therefore be merged without discarding
  or aborting the prior reconciliation history.
- Reconciliation rules: union both code lanes; prove the certification-mutant
  function-name union in both directions; never hand-edit certificate
  conflicts; preserve and prominently report honest DK/NZ regressions caused
  by strict evidence requirements.
- Final report target:
  `sol-evidence-validator-land-reconciliation-2026-08-15-result.md`.
- Current status: reconciliation is committed and every requested gate is
  green. Publication is externally blocked: terminal transport cannot resolve
  GitHub, and the connected GitHub interface rejected its first blob write.
  The remote branch and PR remain unchanged.

## Done

- Confirmed the requested branch and clean worktree.
- Confirmed there is no active merge metadata and recorded the exact local and
  `origin/main` tips rather than aborting or rewriting any history.
- Started independent read-only audits of `scripts/certify.py`, mutant-test
  function sets, and the repository's canonical regeneration/check pipeline.
- Read `origin/main`'s 1,055-line `scripts/certify.py` end to end before
  resolving it. The result retains CO+DK+seven NZ registry entries, NZ
  report/view and attestation switching, and every strict evidence contract:
  bound/full reference evidence, typed fail-closed report parsing, disposition
  schema/marker agreement, exact report/index byte hashes, per-case evidence,
  and census-to-registry identity. Derived premise modes still override any
  registry-supplied `mode` field.
- Reconciled `tests/test_certification_mutants.py` as the exact name union:
  branch 55 functions, main 41, 23 shared, merged 73. Both parent-to-merged
  differences are empty, and the merged-to-parent-union difference is empty.
- Preserved main's fresh 856-case Colorado QC execution, then used the guarded
  inline-mirror migration and immutable source replay rather than hand edits.
  CO QC now validates `bound/cardinality`; CO ECPS validates `bound/full`.
- Regenerated NZ unified/closure receipts, dispositions, both certified chunk
  indexes, freshness, scoreboard/history, both ratchets, burn-down, overview,
  the exercise census, and every program certificate. Certificate conflicts
  were resolved solely by `scripts/certify.py` output.
- Preserved the honest protocol regressions: CO remains conformant=true and
  certified=unavailable; DK changes from main's conformant=true to false and
  remains certified=unavailable; all seven NZ program views change from
  conformant=true to false and certified=no.
- DK's three legs are `unbound/full`: each lacks a chunk index, disagrees on
  the stored case/report disposition marker, and has a non-object
  `errors_by_engine`. NZ's shared leg is `unbound/none`: the unified report
  lacks a non-negative top-level `case_count`, its stored cases cannot support
  full/cardinality reconciliation, and its chunk index is absent. No strict
  rule was softened and no certificate verdict was edited by hand.
- All canonical checks pass: NZ record/closure, 95 disposition files, both
  immutable Colorado replays and indexes, freshness (223 suites / 34
  executable surfaces), scoreboard (6 jurisdictions / 4 conformant), both
  ratchets, burn-down (6 series / 143 points), overview (224 reports), census,
  and certificates.
- Requested batteries pass: 83/83 certification mutants, 84/84 complete
  evidence cases (the historical 66 expanded by the 18 NZ mutants), and 65/65
  runner/refresh cases in 565.35 seconds.
- Focused Ruff/compile/whitespace checks and the 10-case census/immutable-replay
  support battery pass.
- Created merge commit `0e4d9a840578264bc6e862c4169cd52666d5d312`
  with parents `511cacaa9` and `a33cadea0`; its subject and body explicitly
  document the three-way union and the DK/NZ conformant regressions.
- A normal push failed before authentication with `Could not resolve host:
  github.com`. A connected GitHub Git-data interface is available as the
  publication fallback; PR #468 has not been merged or edited.
- The connected interface confirmed PR #468 is open and unmerged at remote
  head `27e3a51fc`, then rejected the first atomic blob write as
  `user cancelled MCP tool call`. No remote object, ref, or PR state changed.

## Next

- When GitHub terminal transport or connected write authorization is
  available, push `evidence-validator-land`, verify the remote ref, and leave
  PR #468 unmerged.

## Executable producer — 2026-07-29

### State

- Branch: `autogo/executable-producer-rebuild`, based on the locally available
  `origin/main` at `2a1660d` because the network cannot currently resolve
  `github.com`.
- Intended publication ref: `autogo/executable-producer`.
- Phase: implementation, trust-boundary repair, validation, and independent
  re-review complete; publication is blocked by unavailable Git transport and
  connector write access.
- Scope: add a deterministic, sign-only CI producer for executable receipts and
  standalone receipt consumption by the certificate harness.
- Existing workflows, toolchain files, dependency pins, and CODEOWNERS are
  out of scope and must remain unchanged.

### Done

- Read the closure-sprint encoder preamble and repository-level instructions.
- Confirmed the requested local branch/worktree already contained stale,
  incomplete task work; preserved it untouched for read-only review.
- Created this fresh worktree from the latest locally available `origin/main`.
- Read the generated-only certified-node contract, the exact ops stranger-path
  fixture and output bindings, the release/publication machinery, and the
  parked certificate implementation.
- Ported the coherent exercise-census/program-certificate baseline from
  `program-certificate` without importing either parked evidence-validator
  branch (#378/#379).
- Regenerated the census and certificate against this worktree's current main
  data. The expected pre-producer certificate remains attested and red.
- Pinned the full `v0.1.1` release archive checksums, artifact release manifest
  and content hash, byte-identical ops golden request/output bindings, committed
  receipt path, and an initially empty governed workflow-SHA allowlist.
- Added the governed workflow and its only producer path: anonymous release
  downloads, checksum checks, archive extraction, version check, published
  manifest binding, artifact hash check, real engine execution, golden-value
  comparison, receipt emission, signing, and artifact upload.
- Replaced the hand-carried executable attestation with standalone, fail-closed
  receipt validation in `scripts/certify.py`; missing evidence now produces a
  stable computed-false verdict.
- Added constructed receipt and producer tests for checksum, golden-output,
  workflow-provenance, workflow-allowlist, dev-engine, command, input, timestamp,
  and failure-cleanup mutants. Focused result: 61 passed.
- Ran the full repository suite: 2,365 passed and 70 skipped. The sole failure
  was the dashboard loader-equivalence test because its `npx esbuild` subprocess
  attempted a blocked npm download in this fresh worktree; the cached esbuild
  binary remains available for an equivalent direct check.
- Independent receipt and workflow reviews reproduced a release-blocking gap:
  workflow provenance was only self-asserted in the JSON while the generated
  Sigstore bundle was discarded. A hand-authored receipt that copied an
  allowlisted workflow SHA could therefore pass.
- Read the final local `axiom-encode#1192` notary design. Its load-bearing
  boundary is a secretless deterministic execution job followed by a signing
  job that runs no candidate code, with cryptographic authentication required
  at consumption.
- Independent review also found that producer output parsing coerces numeric
  strings and floats to integers. That masks output-type disagreement and must
  be replaced by exact type-and-value comparison.
- Replaced numeric coercion with exact released-engine schema, JSON type, and
  pinned-value checks. Added mutants for numeric strings, floats, scientific
  notation, booleans masquerading as integers, and the wrong typed-value kind.
- Sealed the public producer entry point: `produce()` and `main()` accept no
  repository, manifest, environment, engine, or artifact parameters. Tests use
  private constant monkeypatching rather than a production escape hatch.
- Reran the producer suite after those repairs: 46 passed.
- Audited the apparent ops golden-fixture contradiction. The committed fixture
  on ops `origin/main` has stale `_provenance` prose, but contains the later SSN
  and relation repair; the ops repair branch records that the released pair
  returns the pinned `478 / 226 / holds` tuple. The later minimal audited fixture
  has not landed on ops main and is therefore not silently substituted here.
- Split the workflow into a permission-empty execution job and an isolated
  OIDC signing job that runs no repository or engine code. The execution job
  fetches the public main commit anonymously; the signing job re-checks the
  immutable receipt before signing its exact bytes.
- Retained the Sigstore bundle beside the receipt and pinned a public-good
  trusted root, its raw SHA-256, the immutable GitHub repository ID, workflow
  identity, workflow/source commits, event/ref, and run ID/attempt.
- Made `scripts/certify.py` authenticate the bundle offline through
  `gh attestation verify`, then independently re-check the verified certificate
  fields, hosted-runner identity, transparency timestamp, signed receipt digest,
  release/checksum membership, fixture bytes, commands, and golden values.
- Added adversarial cases for a copied allowlisted SHA without a bundle,
  malformed bundle, post-signature receipt mutation, wrong repository/workflow/
  digest/ref certificate fields, mutated trusted root, and parsed-object byte
  bypass. Added a full-certificate test proving authenticated evidence flips
  only the executable premise and removes its blocker mechanically.
- Expanded the maintainer handoff with exact artifact, verification, immutable
  copy, allowlist, regeneration, and check commands. No verdict is hand-edited.
- A second adversarial pass caught that `gh` treats `--cert-identity` and
  `--signer-workflow` as mutually exclusive. Removed the redundant workflow
  flag, retained the stronger exact certificate identity, and added a smoke
  test that sends the production flag set through the real installed CLI
  parser so mocks cannot hide this failure class.
- Reran all focused executable-receipt tests after the authentication repair:
  84 passed.
- Reran the full repository suite: 2,387 passed and 70 skipped. Its sole
  failure remains the environment-only `npx esbuild` network lookup; no
  task-related test failed.
- Ran the loader test's exact bundle-and-compare sequence with the cached
  esbuild binary: `EQUIVALENT: true`, with zero legacy leftovers.
- Completed three independent adversarial, workflow-governance, and certificate
  integration reviews. All approved the repaired boundary with no viable
  receipt, bundle, certificate, or integration bypass.
- Strengthened the real-`gh` smoke test so it must reach bundle parsing, not
  merely avoid one known mutually-exclusive-flag error. Focused result remains
  84 passed.
- Passed certificate and census regeneration checks, actionlint, Ruff,
  targeted Python compilation, `git diff --check`, and cached wheel/sdist
  builds.
- Wrote and committed `FINAL-REPORT.md` with the design, schema, test evidence,
  and maintainer handoff.
- Attempted both a remote refresh and the exact non-force push to
  `autogo/executable-producer`; both failed because `github.com` could not be
  resolved. Confirmed through the GitHub connector that no branch with that
  name exists.
- Attempted connector-based publication of the exact committed tree. Both the
  tree and single-blob write probes were rejected before creating an object or
  branch, so a draft PR could not be opened.
- Added the exact maintainer push and draft-PR commands, including the required
  title and certified-nodes critical-path reference, to `FINAL-REPORT.md`.

### Next

- A maintainer with GitHub network/write access publishes the exact committed
  tree and opens the documented draft PR; after review and landing, perform the
  evidence-pair and allowlist handoff documented above.

## Executable tier reconciliation — 2026-08-20

### State

- Branch: `autogo/executable-producer-rebuild`; PR #461 remains open, draft,
  and unmerged.
- Rebased onto `origin/main` at
  `dd4ec472acd711c6481c381c20bcce034f3ced6b`.
- Phase: implementation, certificate regeneration, validation, and final
  report complete; guarded branch publication and PR description update
  remain.
- Output report: `FINAL-REPORT.md`.

### Done

- Attempted an explicit `git fetch`; terminal DNS could not resolve GitHub.
  The shared repository's `origin/main` was independently refreshed to the
  2026-08-20 commit above, and that exact local object is the rebase base.
- Preserved current main's multi-program `scripts/certify.py`, DK/NZ/tariff
  computed-producer machinery, generated census, and generated certificates.
- Dropped only the PR's obsolete July census/certificate baseline commits;
  replayed its release contract, permission-empty execution plus isolated OIDC
  signing workflow, sealed producer, Sigstore authentication, and adversarial
  tests.
- Mapped the shared receipt consumers. Current main accepts producer-specific
  executable receipts without a central tier policy; PR #427's parallel
  `certify_nodes.py` expects the stronger published-artifact/released-binary
  contract and must coordinate through the shared schema file only.
- Verified the governed artifact registries contain no published DK program
  artifact: live `rulespec-us` has no DK `programs/` entry; live `rulespec-dk`
  has neither `programs/` nor `artifacts/` and has no publication workflow; the
  archived registry contains only `uk/`. DK's current compile-from-source and
  ten-case replay is therefore honestly `source_reproduction` today.
- Added `certificates/executable/receipt.schema.json` as the exact v2
  discriminated union for `source_reproduction` and `release_receipt`, plus a
  shared fail-closed envelope loader with a raw-byte schema digest.
- Wrote `docs/executable-tiers.md`: source reproduction is allowed only when no
  published artifact exists; release receipt is required when one does, and
  consumer-owned policy—not receipt self-description—selects the tier.
- Added six schema/envelope tests covering both tiers, missing tier, a source
  receipt under release-required policy, and cross-tier field smuggling. All
  six pass; Ruff, Python compilation, JSON parsing, and whitespace checks pass.
- Migrated DK's producer and committed receipt from its producer-specific v1
  shape to shared `axiom_oracles.executable_receipt.v2` with the mandatory
  `source_reproduction` discriminator. Its existing producer validator still
  re-derives every deep source, engine-pin, compiled-artifact, and case claim.
- Added DK-specific mutants proving the real committed source receipt cannot
  satisfy a `release_receipt` policy and that deleting `tier` fails closed.
  The combined schema and DK reproduction battery passes: 13 tests.
- Migrated the CO producer and validator to the shared v2 `release_receipt`
  branch. The committed release contract now owns the required tier and
  hash-binds the raw shared-schema bytes; the isolated signing job re-checks
  both discriminator fields before signing.
- Preserved the release receipt's strict release-manifest engine membership,
  published-artifact binding, exact nine-command transcript, golden byte/type
  checks, and exact-byte Sigstore verification. Added tier, schema-drift, and
  anti-downgrade mutants alongside the existing wrong-engine-checksum mutant.
  The release producer/validator battery passes: 87 tests; actionlint, Ruff,
  Python compilation, schema-pin comparison, and whitespace checks pass.
- Replaced CO SNAP's attested executable prose with a computed
  `release_receipt` consumer. The program registry independently owns the
  tier, receipt/manifest paths, golden-input hash, and exact expected outputs;
  missing or invalid authenticated evidence adds an executable blocker.
- Made DK's registry require `source_reproduction`, retaining the deep DK
  producer validation, while leaving the NZ and tariff legacy producer paths
  unchanged. Accepted tier is emitted only after validation; rejected release
  evidence records the required policy without falsely labeling its tier.
- Added certifier integration coverage for DK/legacy dispatch, missing release
  evidence, a real source receipt at a release-required consumer, absent tier,
  certificate-owned golden values, and a fully authenticated receipt. Six
  focused tests pass. Before regeneration, the 210-test certification-mutant
  battery had only the expected generated-certificate drift and no logic
  failure.
- Regenerated every program certificate from the new registry policy and
  passed `scripts/certify.py --check`. DK now records accepted
  `source_reproduction` evidence and remains certified yes. CO SNAP replaces
  attested executable prose with computed `release_receipt` policy and remains
  honestly false because no receipt/bundle/allowlist evidence pair is
  committed; the stable blocker is `executable: receipt: file does not exist`.
  The 210-test certification-mutant battery now passes after regeneration.
- Passed the consolidated 106-test tier battery plus certificate/census
  freshness, Ruff, Python compilation, actionlint, schema-pin, JSON, and
  whitespace checks.
- Ran the complete repository suite: 2,940 passed and 73 skipped. Its two
  unrelated environment/optional-dependency failures are on files byte-equal
  to main: `npx` could not resolve npm to fetch esbuild, and globally installed
  `policyengine-uk 2.75.3` lacks `council_tax_reduction`. The cached esbuild
  path passed the exact loader-equivalence check (`EQUIVALENT: true`, zero
  leftovers).
- Rewrote `FINAL-REPORT.md` with the tier definitions, DK registry result,
  shared schema and digest, fail-closed boundary, mutant mapping, generated
  state, and exact validation totals.
- Independent final schema/requirements and security audits found no blocker
  and no release-receipt bypass; both rechecked the tier and fail-closed mutant
  surfaces.

### Next

- Force-with-lease push the rebased branch, update PR #461's description,
  verify its remote head/draft/unmerged state, and record publication here.
