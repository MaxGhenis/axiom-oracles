VERDICT: REQUEST-CHANGES

# Round-2 blind review: `fed-parity/snap-residual-cleanup`

- Target: `72718c962ce06385be4858b770af6d55b43bc3fa`
- Compared with local `origin/main`:
  `9b889a27432e84804938bd3b374b4f5f7466792e`
- Merge base: `9b889a27432e84804938bd3b374b4f5f7466792e`
- Review date: 2026-07-27
- Risk: high, because a browser-served generated bundle contradicts the
  repaired canonical reports

The three round-1 repairs are substantially present in the canonical configs,
five JSON reports, compact case-explorer chunks, and freshness register.
Version resolution, served-case reconciliation, live counterfactuals, and the
re-merge check all pass.

The exact target is not approvable because the complete writer chain does not
pass. `dashboard/public/data/overview.json` was not regenerated after the five
reports, so the browser still serves the pre-repair SNAP summaries and version
provenance on overview/program surfaces. The branch's committed
`WORKER-REPORT.md` also remains the superseded round-1 narrative and
contradicts the corrected runtime and qualifier evidence.

## Blocking findings

### 1. The primary browser overview bundle is stale

This exact read-only check exits 1:

```text
PYTHONPATH=. <repo-root>/.venv/bin/python \
  scripts/generate_dashboard_overview.py --check

overview.json is stale (report set or sizes changed);
run scripts/generate_dashboard_overview.py
```

The committed and rebuilt bundles each contain the same 214 report keys.
Exactly the five reviewed SNAP objects differ:

| Suite | Committed source bytes | Current source bytes | Stale unexplained | Current unexplained |
| --- | ---: | ---: | ---: | ---: |
| AL | 100,162 | 104,532 | 43 | 23 |
| MA | 420,884 | 413,720 | 49 | 83 |
| NC | 196,037 | 199,879 | 88 | 71 |
| SC | 294,109 | 285,264 | 54 | 106 |
| TN | 127,198 | 133,137 | 68 | 41 |
| **Total** | — | — | **302** | **324** |

Each stale embedded object is semantically equal to the corresponding
`origin/main` report after removing `cases`. The bundle therefore still shows
655 raw rows rather than 656, including SC's old 180 rather than 181. It has no
`engines.versions` for these suites, and its provenance still says
PolicyEngine-US 1.752.2 with no Core version. The rebuilt objects attest
PolicyEngine 4.18.9 / US 1.767.3 / Core 3.30.3 and carry the new disposition
summaries.

This is served data, not an inert cache. `dashboard/src/utils/data.js` accepts
any nonempty `overview.reports` array and then skips canonical per-file
loading. Overview and program pages therefore receive the stale summaries,
versions, and mismatch data. The lazy-loaded household chunks are independently
correct, which creates a split-brain UI rather than mitigating the defect.

Committed overview SHA-256:
`8f1915f826990f1ac18031d448f7886696ca90afd0b9dd92828e4b36f5a003f7`.
In-memory rebuilt SHA-256:
`2900cc22436ad01acbf5b680d2fe5066ef750be4db127b9c248feb9381ee9525`.

### 2. The committed worker report still states superseded evidence

`WORKER-REPORT.md` is not labeled historical and describes itself as the final
branch report, but it was not repaired in round 2:

- line 65 says PolicyEngine Core 3.28.0;
- line 133 cites the superseded TANF artifact hash
  `084db4c17c97c3ab6ed057186b5c6df969737944013069361125499674497f66`;
- lines 157-167 call a six-row minimum-benefit table exhaustive and omit MA
  `ecps-2303`.

The untracked `REPAIR-ROUND2-REPORT.md` supplies the corrected Core 3.30.3
runtime, artifact hash
`0251315e09222289f11e21efc89c5421b84459acaa23bcd1f615828dadcb0b00`,
and seven-row qualifier screen, but that evidence will not ship with the
branch.

There is also a concrete hygiene failure:

```text
WORKER-REPORT.md:3: trailing whitespace.
WORKER-REPORT.md:4: trailing whitespace.
```

`git diff --check origin/main...72718c96` exits 2, contrary to the untracked
repair report's claimed pass.

## Version truth

The five comparison configs explicitly specify Python 3.13 and:

```text
policyengine==4.18.9
policyengine-us==1.767.3
policyengine-core==3.30.3
```

Loading every config through the committed
`scripts/run_comparison.py::_resolve_pe_oracle_pins` independently returned
that exact tuple. A real offline `uv run` using a writable temporary cache
resolved 101 packages and imported, on Python 3.13.9:

```text
policyengine       4.18.9
policyengine-us    1.767.3
policyengine-core  3.30.3
```

The imported `axiom_oracles` code came from this exact review worktree.
PolicyEngine emitted the disclosed warning that the 4.18.9 meta-package's
bundled manifest names US 1.752.2; the explicitly resolved and imported
runtime remained US 1.767.3 / Core 3.30.3.

All five canonical reports have the exact versions in both
`engines.versions` and `provenance.oracle`. All five compact case indexes have
the exact `engines.versions`. None of those ten artifacts contains 1.752.2 or
3.28.0. Seven focused pin and fail-closed attestation tests pass.

Thus the regenerated JSON artifacts pass version truth; the stale served
overview and committed worker narrative do not.

## Served case-explorer parity

Both new semantic checks exit 0, and independent parsing produced:

| Suite | Mismatch rows | Annotated rows | YAML entries | YAML-expanded rows |
| --- | ---: | ---: | ---: | ---: |
| AL | 53 | 30 | 19 | 30 |
| MA | 255 | 172 | 24 | 172 |
| NC | 99 | 28 | 16 | 28 |
| SC | 181 | 75 | 35 | 75 |
| TN | 68 | 27 | 25 | 27 |
| **Total** | **656** | **332** | **119** | **332** |

The five served disposition-explanation files contain exactly the same 119
YAML entries. There are no duplicate, missing, obsolete, value-drifted,
class-drifted, orphaned, or unknown rows/entries and zero silent
classifications.

The categorical rollback identity set is MA 27 households/54 rows plus SC 42
households/84 rows. All 138 keys exist in canonical and served data; canonical
`disposition` and compact served `e` are both physically absent for every key.
The two emitter `--check` commands pass, as do their 10 focused tests.

## Live TANF counterfactual replay

Runtime: Python 3.13.9, PolicyEngine 4.18.9, PolicyEngine-US 1.767.3,
PolicyEngine Core 3.30.3, and SPM Calculator 0.3.1. The pinned 349,048,491-byte
Populace artifact independently hashed to
`16be6338f9d0b3c339883dae59949e995663b64cf145de6728b3dd0f916c5d5f`.

Ten exact households were rerun: one committed pass and one member of the
26-case fail pool in every state.

| State / case | Axiom | Baseline PE | TANF/mo | Zero-TANF PE | Abs. delta | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| AL `ecps-36777` | 785 | 749.274170 | 328.651835 | 789.399170 | 4.399170 | PASS, dispositioned |
| AL `ecps-37187` | 1,421 | 1,364.013184 | 279.929443 | 1,428.963379 | 7.963379 | FAIL, unannotated |
| MA `ecps-2037` | 785 | 450.024129 | 1,009.333252 | 789.399170 | 4.399170 | PASS, dispositioned |
| MA `ecps-2680` | 546 | 273.284749 | 577.498983 | 533.384766 | 12.615234 | FAIL, unannotated |
| NC `ecps-27628` | 546 | 519.659790 | 140.931183 | 549.059814 | 3.059814 | PASS, dispositioned |
| NC `ecps-28003` | 1,421 | 1,409.013184 | 318.233968 | 1,428.963379 | 7.963379 | FAIL, unannotated |
| SC `ecps-28740` | 499 | 395.234782 | 358.618896 | 502.934814 | 3.934814 | PASS, dispositioned |
| SC `ecps-28773` | 714 | 704.379476 | 57.977208 | 721.779460 | 7.779460 | FAIL, unannotated |
| TN `ecps-35320` | 280 | 208.334798 | 253.362386 | 284.234782 | 4.234782 | PASS, dispositioned |
| TN `ecps-35304` | 613 | 410.274129 | 175.702515 | 463.074137 | 149.925863 | FAIL, unannotated |

Every baseline matched its current report exactly. Eligibility remained true
before and after, the state TANF component equaled aggregate TANF, and both
became zero after neutralization. The strict predicate
`abs(zero_tanf_snap - axiom_snap) <= 7` reproduced all five YAML dispositions
and all five sampled failures.

### Lone-minor #9157 signature

Two actual dispositioned cases reproduced the signature:

- AL `ecps-36459`: one age-17 earner with $217,027.52 wages. Imputed K-12
  excluded the wages and produced PE eligibility true / SNAP 296.894979 while
  Axiom returned false / zero. Explicit K-12 false counted the wages, failed
  gross and net tests, and returned false / zero.
- NC `ecps-27147`: one age-15 earner with the same wages. Imputed K-12
  produced PE true / 150.644969 against Axiom false / zero. Explicit K-12
  false again counted wages and returned false / zero.

### Minimum-benefit qualifier

The exact qualifier requires shared eligibility plus Axiom exactly $24 and PE
exactly $23.84 or $23.973597208658855. The complete near-minimum screen is:

| State / case | Axiom | PolicyEngine | Exact qualifier |
| --- | ---: | ---: | --- |
| MA `ecps-2070` | 24 | 44.294978 | No |
| MA `ecps-2303` | 24 | 100.169993 | No |
| NC `ecps-27289` | 24 | 63.494980 | No |
| NC `ecps-27513` | 76 | 23.973597 | No |
| NC `ecps-27882` | 24 | 6.093599 | No |
| NC `ecps-28338` | 151 | 23.973597 | No |
| SC `ecps-28997` | 45 | 23.973597 | No |

All seven are unannotated for this class. The exact qualifier count is zero.

## Chain, re-merge, and containment

Twelve of thirteen CI writer checks pass:

| Writer check | Result |
| --- | --- |
| dispositions | 83 files consistent |
| served cases | 656 rows / 332 annotated / zero silent |
| served explanations | 119 entries / exact YAML parity |
| grids | current |
| boundary suggestions | current |
| affected map | 163 suites / 172 edges |
| vacuous/freshness | 136 configs / 213 suites / 24 surfaces |
| dashboard overview | **FAIL: stale five-report bundle** |
| conformance universes | exit 0 |
| conformance compositions | 23 BE suites current |
| scoreboard | 4 jurisdictions / 3 conformant |
| ratchet | no regression |
| burn-down | 4 series / 49 points |

The universe check left US-PE and UK-PE unverified as a documented no-op
because the available local checkouts are US 1.779.4 versus pinned 1.767.3 and
UK 2.88.52 versus pinned 2.89.2. Independent config/runtime checks above cover
the in-scope SNAP version requirement.

Freshness itself passes. Current `origin/main` is the target's merge base and
ancestor. `git merge-tree --write-tree origin/main 72718c96` returns the
target tree `93784fbbfc5bd1b6b8a0315bbdd78db1bc7c7adf` with no conflict.
Normalized rebuilt and committed freshness SHA-256 both equal
`35036d549706402f6633cac55aa10d11f55faa713f9e24049ec6cc33e561e953`;
all five freshness timestamps equal their canonical report provenance.

The PR-style diff contains 56 paths and no unrelated-suite artifacts:

- 41 requested data paths: five canonical reports, 22 compact case files, five
  YAML dispositions, five served disposition files, freshness, and the
  `us-pe:snap` note plus two generated mirrors;
- 15 supporting paths: five required configs, three repair scripts, four
  tests, one CI gate, and the two mandated branch ledgers/reports.

The `us-pe:snap` registration and both generated mirrors differ only in note
text. It remains in scope and registered to `ca-snap-ecps`; every metric and
status field is unchanged.

The task-scoped test command passes: 364 passed, 3 skipped.

## Required changes

1. Regenerate and commit `dashboard/public/data/overview.json`, then make all
   thirteen writer `--check` commands pass.
2. Update or explicitly supersede the committed `WORKER-REPORT.md`: record Core
   3.30.3, the fresh TANF evidence hash, and the seven-row qualifier screen
   including MA `ecps-2303`.
3. Remove the two trailing-whitespace defects and rerun `git diff --check`.

No change is requested to the five canonical reports, compact case chunks,
disposition selectors, freshness register, or `us-pe:snap` registration based
on this review.

## Sandbox and tooling disclosures

- No remote or GitHub write was made.
- Normal `uv` cache initialization failed at the read-only home cache
  `~/.cache/uv/sdists-v9/.git` with `Operation not permitted`. An offline
  writable cache under `/private/tmp` successfully resolved and imported the
  exact committed pins.
- The counterfactual probe's first offline `uv` attempt could not map the
  cached extracted US 1.767.3 package back to its wheel URL. The replay then
  used the already-extracted exact US/Core distributions ahead of the base
  PolicyEngine 4.18.9 environment and attested distribution versions and
  module paths before calculation.
- A diagnostic `ps` command was sandbox-denied; it was irrelevant to the
  completed calculations.
- `npx gitnexus status` produced no output for 60 seconds and was interrupted.
  No usable graph index or connector was available, so review tracing used the
  exact diff, configs, writers, tests, and browser load path directly.
- All review writes are confined to the disposable review branch under
  `.git/review-worktrees/`; target artifacts were not modified.
