# Computed executable evidence

Tiered executable receipts use `axiom_oracles.executable_receipt.v2`; see
[`docs/executable-tiers.md`](../../docs/executable-tiers.md). The DK receipt is
`source_reproduction`: its producer recompiles from the exact RuleSpec commit
and replays the committed cases, but does not claim that those temporary bytes
are a published artifact. A program certificate accepts a receipt only through
the producer and consumer-owned tier policy named in `scripts/certify.py`; the
producer must re-derive its `executable` Boolean.

The NZ and tariff reproduction receipts retain their producer-specific legacy
schemas until they are migrated to the shared tier envelope.

The NZ receipt commits the exact 703,295-byte comparison composition whose
SHA-256 was recorded by the original harness. Its request set is the 19 engine
calls made while evaluating the
`single_parent_three_children_area1_rent` scenario at weekly wages 0 and 740.
Those calls cover all 19 requested RuleSpec output roots and support 22 of the
1,976 comparison cells: the 11 program-view columns at each selected wage.

`python scripts/nz_executable_reproduction.py --check` is hermetic and is the
CI gate: it verifies all committed bytes and re-derives the transcript/golden
matches. `--check --live` is the stronger local integration gate. It requires
the pinned RuleSpec checkout and macOS engine binary, recompiles the composition
byte-for-byte, executes every request, and byte-compares the fresh transcript.
The release binary is not portable to the Linux CI runner, so CI does not
perform that final engine invocation; it does verify the artifact, request,
golden-output, and transcript digests produced by the live gate.
