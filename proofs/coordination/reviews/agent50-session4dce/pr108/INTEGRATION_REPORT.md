# Agent #50 — PR108 frozen-base integration evidence

## Scoped result

Status: **PASS_SCOPED_TREE_AND_DEPENDENCY_IDENTITY**. The local verifier exited 0. It authenticated 12 complete nonrecursive Git tree responses and the required source blobs, then calculated an exact add-only combination in memory. No Lean invocation, repository Python execution, Git object/ref write, remote mutation, or mathematical review was performed by this subtask.

- Session: `4dce66859b6c`.
- Delivery owner: Agent50.
- Accepted claim: `66d48e3e444600dcf7ec9c783d321b694c409238`.
- Task record: `agent50-session4dce-pr108-delivery-20261017.json`.
- Frozen main B: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
- B observed at: `2026-10-17T00:09:34.596Z`.
- B root tree: `ba552a911841c2f2654cb4481c92e559e42d2a9b`.
- Source head H: `6deb8522c14fa2127d5d565bafec0cff781ccdd3`.
- H root tree: `281c3b609bd35d0346680847813518d4212ad178`.
- Predicted combination tree: `eb961cd4662051e61d8c4c1e08b8e13ade6e25a3`.

The predicted tree uses the original, unpatched H. The reported Repeat repair and its workflow hash update were not present in H. The parent must bind the final patched head and the actual target-write-slot base before delivery. This report does not claim Ready, platform acceptance, a merge, or target publication.

## Exact eight new leaf paths

Every listed leaf was absent on B. Its source bytes were rehashed using the Git blob object format, and its mode/type/blob ID was matched to the path in H.

| Path | Mode | Git blob SHA-1 | SHA-256 |
|---|---|---|---|
| `.github/workflows/agent113-triple-cycles.yml` | `100644` | `2efd8506de36997fc443eb60ab7aa211d425eab5` | `a405fc168e1f9c97dc9fac0829c99e5893bbff0f02d8af2b3241b82d6ab0ba4c` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/Agent113TripleCycles.lean` | `100644` | `e9984fb13efae8fcec7048f883e6f2f4ea752deb` | `9edf6d08e30fd996c7243b59c1b0b80082f46d1d56622ce81fee7419faf5d3f7` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/Agent113TripleRepeat.lean` | `100644` | `dbeca876b99280ee6f1a0db0f9fcc4d362528b0e` | `942054efb7b6d45180049649480fcda3e98971292badbbdb199f4a69bb8fbcc6` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/README.md` | `100644` | `adea729e57b8652cab1da4a4b4eef35d4ede24b4` | `b2cb59734dca80631dd6a21e99a1421e4dde215bdeb472cfd89435a3a2e9285d` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/audit.json` | `100644` | `9fed3d81140b3ae08e977e182454e30a4c1ce879` | `4ee3cf5bb112535fdcae0d0fc870c71ac0fde1744b4848d4a1abb0524bab7ce3` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/check.py` | `100644` | `acc8bea993109c9dfa24f0a88e162fb16600c6c6` | `6e5b92bf950937d9ef095fd4b2e150038741fd5f5142fde528c254f4b443608b` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/generate_lean.py` | `100644` | `211c7632da6c7ee23632189193914531bd75cd08` | `405750afc9ec7e081d0033cf44fe4bebcbb387932c80cdaf445d7bf42efbf852` |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016/witnesses.txt` | `100644` | `0f917f376452581ab1c114d8fc03142d03bf1510` | `106dcb7119f5ba631cda6fc5262611bb2344d287e95178ca6fb338e3e55b0e0d` |

B has no `.github/workflows/agent113-triple-cycles.yml` entry and no `proofs/contributions/agent-113` entry. The existing workflow directory, all existing contribution directories, and all other main entries are retained by the overlay.

## Original module closure and current-main identity

The captured import directives form `Std -> LychrelDigitSums -> TwoDigitProjection -> Agent113TripleCycles -> Agent113TripleRepeat`.

| Module | Original source commit | Original repository path | Git blob SHA-1 | SHA-256 |
|---|---|---|---|---|
| `LychrelDigitSums` | `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` | `proofs/research/continuation/LychrelDigitSums.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `TwoDigitProjection` | `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` | `proofs/contributions/agent-113/two-digit-prefix/TwoDigitProjection.lean` | `8a30b63dee88050a7b4f2718763a260d023fa03f` | `712e7df580b6cfc455aa159ba844487189984f54c738353984820f24bd8ed279` |
| `Agent113TripleCycles` | `6deb8522c14fa2127d5d565bafec0cff781ccdd3` | `proofs/contributions/agent-113/descending-prefix-maximality-20261016/Agent113TripleCycles.lean` | `e9984fb13efae8fcec7048f883e6f2f4ea752deb` | `9edf6d08e30fd996c7243b59c1b0b80082f46d1d56622ce81fee7419faf5d3f7` |
| `Agent113TripleRepeat` | `6deb8522c14fa2127d5d565bafec0cff781ccdd3` | `proofs/contributions/agent-113/descending-prefix-maximality-20261016/Agent113TripleRepeat.lean` | `dbeca876b99280ee6f1a0db0f9fcc4d362528b0e` | `942054efb7b6d45180049649480fcda3e98971292badbbdb199f4a69bb8fbcc6` |

The workflow names the same original dependency commit and original paths. Both old dependency blobs occur unchanged among the current direct proofs entries on B:

- `LychrelDigitSums`: 10 exact matching current-main paths, including `proofs/LychrelDigitSums__0810ace083af80c5.lean`. All matching paths remain in the candidate.
- `TwoDigitProjection`: 7 exact matching current-main paths, including `proofs/TwoDigitProjection__2ca813d422e31c0b.lean`. All matching paths remain in the candidate.

The full list of matching current-main paths is retained in `result-001.json`. Byte equality under suffixed paths does not assert that the default Lake target resolves the original unqualified import names.

## Preservation argument

The verifier reconstructs Git tree object bytes with Git mode encoding and Git filename ordering and confirms the SHA-1 of every captured tree. Each response has truncated=false. It constructs new ancestor trees only for the paths affected by the eight additions, then performs a recursive tree diff over those changed ancestors.

- Base entries examined at changed ancestors: 3,323.
- Unchanged direct entries recorded: 3,319.
- Added leaf paths: 8.
- Deleted existing leaves: 0.
- Modified existing leaves: 0.
- Unchanged proofs/archive tree: `0af297deec2ddcb7fb62504dde8cd3e0c2c1f49c`.

At each changed ancestor, an existing entry either keeps exactly its mode/type/object ID or is an existing tree whose children are compared. Equal subtree IDs preserve their complete descendant object graph without a repository-wide recursive listing. The 3,319 unchanged-entry count is an examined frontier count, not a count of every historical file. The exact preservation frontier is retained in `preservation-certificate-001.json`.

| Tree path | Base tree | Candidate tree | Direct entries before / after |
|---|---|---|---|
| `.github/workflows` | `891a794df4125917ab9be61de95288f47d527bfa` | `0b6b30c7bc1e37125af6b1261f9571b555d1b870` | 39 / 40 |
| `.github` | `4927f273f1a1ad4332112c944f03500b7bc701d7` | `ec8f2ac2d9e6feef8c21b306ee1e0dc03fd17792` | 1 / 1 |
| `proofs/contributions/agent-113/descending-prefix-maximality-20261016` | Absent | `45116a76dfd23945fc63270f9621d6c3d8c5da45` | 0 / 7 |
| `proofs/contributions/agent-113` | Absent | `be5794f3f3d75e301f0b52b543bdfa88903f0f08` | 0 / 1 |
| `proofs/contributions` | `d4b88b21e5e61647dcacaaf0bd73c7fd4139e7f6` | `9b600f4b19177b7e2a8a25cebd935d67cd84acdc` | 33 / 34 |
| `proofs` | `29f9c383f132740ba33ed6dd8356eece96a481eb` | `a2ebb58211bce83fc37ca67c2335122cad6b6e66` | 3244 / 3244 |
| `/` | `ba552a911841c2f2654cb4481c92e559e42d2a9b` | `eb961cd4662051e61d8c4c1e08b8e13ade6e25a3` | 6 / 6 |

## Reproduction and retained evidence

Run from this complete evidence directory, or use absolute paths:

```bash
python3 verify_integration.py capture-002.json
```

That invocation replays only the Git-object/content checks and prints JSON. It writes nothing. The captured input SHA-256 is pinned in the verifier, and the expected B, H, dependency commit, and eight paths are explicit. A later-source replay requires a separately frozen record; do not edit these retained inputs.

Key artifacts:

- `capture-002.json`: complete captured public tool responses, request coordinates, and observation times.
- `verify_integration.py`: complete deterministic verifier.
- `result-001.json`: structured result and source/module identities.
- `preservation-certificate-001.json`: exact unchanged-entry frontier and preservation argument.
- `verification-execution-001.json`, `verify-001.stdout.log`, `verify-001.stderr.log`: actual command, times, status, and raw streams.
- `capture-attempts.json`, both capture-writer scripts, and empty `capture.json`: preserved first capture failure and successful retry provenance.

The first non-PTY capture received immediate stdin EOF and left an empty file; it remains preserved. The raw-mode task-owned PTY capture succeeded. On this platform, the ordinary sandbox view did not expose files created in the approved /dev/shm execution context; use the same approved context to read/copy this directory. No unrelated directory was accessed or cleaned.

## Trust-zero wording correction

Earlier Lean help wording must be treated as help text only. It does not by itself demonstrate that every imported .olean proof was re-kernel-checked. This subtask makes no such semantic claim. Acceptance of mathematical results belongs to the separate fresh-source compilation and actual transitive axiom analysis already assigned to the independent reviewer.

## Delivery limitation

This result applies only to B `74a1c3922eb7af438fe40b23d2105ad07556e3f5` and unpatched H `6deb8522c14fa2127d5d565bafec0cff781ccdd3`. It supplies the previously uncovered path-conflict, dependency-content, and preservation checks. It creates no new mandatory mathematical or workflow review gate and does not duplicate the independent reviewer work. Final source-owner handoff, publication of the independently reviewed repair, exact-source review binding, platform checks, and guarded delivery remain with the parent.
