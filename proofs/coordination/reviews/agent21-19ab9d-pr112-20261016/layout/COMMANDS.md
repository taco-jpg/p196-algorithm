# Executed source-layout checks: exact commands and retained outputs

Agent #21 / session 19ab9d430efc / PR112.

Evidence classification: STATIC_SOURCE_CHECK_ONLY. These checks were executed during the preceding read-only layout assessment. All five recorded commands exited 0. No command below was re-executed for this preservation task, and no Lean compilation or axiom audit was performed.

The exact command strings are transcribed from the recorded tool calls. The two long command payloads contain the original in-memory UTF-8 source inputs and proposed registry. Those payloads were reconstructed for preservation using the original serialized field order and the same immutable PR112 source blobs; this is preservation, not a new verification run. The proposal-status metadata added to PROPOSED_SCOPED_BUILD.json was not present in the earlier static-check input and is therefore not inserted into the historical command.

## Original commit versus current/archive/source-map bytes

Execution output chunk: `31c272`. Exit code: `0`.

```bash
python3 -B - <<'PY'
import pathlib,json,hashlib,subprocess,re
root=pathlib.Path('/workspace/scratch/8b5152316f75/p196-agent4'); d=json.loads((root/'proofs/SOURCE_MAP.json').read_bytes())
names=['ArithmeticCRT','DigitPools','ModularSpan','ModulusSplit','OuterBlock','PairWeights','PalindromeDigits','PeriodExistence','ResidueOrbit','Saturation','Lychrel196Research']
for n in names+['check']:
 key='proofs/research/Lychrel196Research.lean' if n=='Lychrel196Research' else f'proofs/contributions/agent-111/exact-length-residues/{n}.'+('py' if n=='check' else 'lean')
 m=d['paths'][key]; b=subprocess.check_output(['git','-C',str(root),'show','c3192d5bf2962298bcb2bb209a0947f657e8a7e5:'+key]); c=(root/m['current']).read_bytes(); a=(root/m['preserved']).read_bytes()
 print(json.dumps({'module':n,'original_commit':'c3192d5bf2962298bcb2bb209a0947f657e8a7e5','sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),'equals_current':b==c,'equals_archive':b==a,'equals_source_map':hashlib.sha256(b).hexdigest()==m['sha256']}))
PY
```

Complete substantive output:

```text
{"module": "ArithmeticCRT", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5", "git_blob": "2722c6cf788605260eace42a86b3c0069ba0dce6", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "DigitPools", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec", "git_blob": "c8e8f00d28c9e0630488e2e17218f909f5bc4534", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "ModularSpan", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754", "git_blob": "13c65527cb65dd199325a4c3b11c35e1474dcc58", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "ModulusSplit", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f", "git_blob": "88b6f05e3346650dec35017f31b3a2721e8ddb15", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "OuterBlock", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705", "git_blob": "57b7dfa5a6e24f3d5097cd0031dd7c986b9f2ff4", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "PairWeights", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae", "git_blob": "345cb5dce73ee99bbbb2a65ae6840370de18cf21", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "PalindromeDigits", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f", "git_blob": "d60da8781a92943d9c4281002aaca13b403c4f67", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "PeriodExistence", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd", "git_blob": "15a20afe499c1a54583a6c384c967049b523fcab", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "ResidueOrbit", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6", "git_blob": "98de673674512414f38182eded9b2a01c47ce4b6", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "Saturation", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0", "git_blob": "d09021588e3fc9c3c456d4276762613c30a68be1", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "Lychrel196Research", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c", "git_blob": "c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506", "equals_current": true, "equals_archive": true, "equals_source_map": true}
{"module": "check", "original_commit": "c3192d5bf2962298bcb2bb209a0947f657e8a7e5", "sha256": "9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af", "git_blob": "4759deab8d954c5d347fa761aeb073f01e209e35", "equals_current": true, "equals_archive": true, "equals_source_map": true}
```

## New source SHA-256 and Git blob checks

Execution output chunk: `92384f`. Exit code: `0`.

```bash
python3 -B - <<'PY'
import json,hashlib,re
files=json.loads("[{\"content\":\"import Saturation\\n\\n/-!\\nAgent #111: unbounded width-dependent decimal suffix congruence obstruction.\\n\\nFor any sufficiently long exact decimal width L, allow a modulus 10^(k L)\\nthat can grow exponentially with L, but with k L <= (L-4)/2.\\nThe original decimal orbit and exact-length saturation proofs are imported\\nunchanged. This does not prove that any particular orbit hits a palindrome.\\n-/\\n\\nnamespace Agent111.GrowingSuffix\\n\\nopen Lychrel196 DecimalDigits ExactLengthResidues\\n\\n/-- At any specified width L with 1 <= k and 2*k+4 <= L, every residue\\ncompatible with a true palindrome has a same-width palindrome modulo 10^k.\\nThis specializes the *existing* arbitrary-modulus theorem at u=10^k,\\nq=1, r=1; no unproved arithmetic assumption remains. -/\\ntheorem powerTen_saturation (k : Nat) (hk : 1 <= k) :\\n    SaturationAbove (10 ^ k) (2*k+4) := by\\n  apply saturation_of_split (10 ^ k) k (10 ^ k) 1 1 hk\\n  · exact Nat.pow_pos (by decide)\\n  · decide\\n  · simp\\n  · exact ⟨1, by simp⟩\\n  · simp\\n  · decide\\n  · simp\\n\\n/-- If the suffix modulus is a power of ten with exponent at most almost\\nhalf the available width, forward closure forces *some member of the set*\\nto be an ordinary decimal palindrome. The orbit used to transfer membership\\nis not claimed to contain that palindrome. -/\\ntheorem variable_powerTen_closed_set_contains_palindrome\\n    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)\\n    (hwidth : ∀ L, B <= L -> 1 <= k L ∧ 2*(k L)+4 <= L)\\n    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  obtain ⟨n, hn, hnS⟩ := hne\\n  obtain ⟨t, d, L, _, _, hc, hL, h11, h10⟩ :=\\n    AstraModular.large_width_compatible_state n (max B 6) hn\\n  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL\\n  have hk : 1 <= k L := (hwidth L hLB).1\\n  have hbound : 2*(k L)+4 <= L := (hwidth L hLB).2\\n  have hcompatible : Compatible (10 ^ (k L)) L (orbit n t) := by\\n    constructor\\n    · intro h\\n      exact h10 h.2\\n    · intro _\\n      exact Nat.dvd_trans (Nat.gcd_dvd_right (10 ^ (k L)) 11) h11\\n  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=\\n    (powerTen_saturation (k L) hk) L hbound (orbit n t) hcompatible\\n  have hmem : ∀ j, S (orbit n j) := by\\n    intro j\\n    induction j with\\n    | zero => exact hnS\\n    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih\\n  refine ⟨p, hp, ?_, hpal⟩\\n  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)\\n\\n/-- An explicit unbounded schedule: at width L>=6, membership depends\\nonly on the last floor((L-4)/2) decimal digits, plus the exact width.\\nNo fixed modulus can replace this schedule for all large L. -/\\ntheorem half_width_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop)\\n    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ ((L - 4) / 2)) = m % (10 ^ ((L - 4) / 2)) ->\\n      (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  apply variable_powerTen_closed_set_contains_palindrome\\n    S (fun L => (L - 4) / 2) 6\\n  · intro L hL\\n    constructor <;> omega\\n  · exact hsat\\n  · exact hne\\n  · exact hclosed\\n\\nend Agent111.GrowingSuffix\\n\\n#print axioms Agent111.GrowingSuffix.powerTen_saturation\\n#print axioms Agent111.GrowingSuffix.variable_powerTen_closed_set_contains_palindrome\\n#print axioms Agent111.GrowingSuffix.half_width_suffix_closed_set_contains_palindrome\\n\",\"blob\":\"aa7ed6bf0675d2fdd6bbcd7f689f64039ff7b8cc\",\"module\":\"GrowingSuffix\"},{\"content\":\"import GrowingSuffix\\n\\n/-! Ordinary decimal palindrome realization with a prescribed low-order half.\\nThe modulus 10^k is allowed up to k=floor(L/2), without the 4-digit\\npadding required by general arbitrary-modulus residue saturation. -/\\n\\nnamespace Agent111.GrowingSuffix\\n\\nopen Lychrel196 DecimalDigits ExactLengthResidues\\n\\n/-- Every positive-width decimal residue whose units digit is nonzero can\\nbe completed to an ordinary positive palindrome of exact width L, whenever\\n2*k<=L. We reuse the *checked* original constructive realization with\\nempty inner digit pools, not a search over finite examples. -/\\ntheorem palindrome_with_given_suffix (n k L : Nat)\\n    (hk : 0 < k) (hL : 2 * k <= L) (hunit : ¬ 10 ∣ n) :\\n    ∃ P e, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧\\n      P % (10 ^ k) = n % (10 ^ k) := by\\n  let A := n % (10 ^ k)\\n  have hA : A < 10 ^ k := Nat.mod_lt n (Nat.pow_pos (by decide))\\n  have hten : 10 ∣ 10 ^ k := ten_dvd_pow k (by omega)\\n  have hA0 : A % 10 ≠ 0 := by\\n    change n % (10 ^ k) % 10 ≠ 0\\n    rw [Nat.mod_mod_of_dvd n hten]\\n    intro hzero\\n    exact hunit (Nat.dvd_of_mod_eq_zero hzero)\\n  have hlow : LowerPositions k L ([] : List Nat) := by\\n    intro i hi\\n    simp at hi\\n  obtain ⟨P, e, hc, hp, hmod, _⟩ :=\\n    two_pool_realization A k L (10 ^ k) 1 0 0 ([] : List Nat) ([] : List Nat)\\n      hk hL hA hA0 (⟨1, by simp⟩) (by simp) hlow (by simp) (by simp)\\n  have hPpos : 0 < P := by\\n    rw [← hc.2.2.2]\\n    exact value_positive e L hc.1 hc.2.2.1\\n  refine ⟨P, e, hPpos, hc, hp, ?_⟩\\n  simpa only [A, Nat.mod_mod] using hmod\\n\\n/-- Every eventually exact-width, trailing-k(L)-digit saturated, nonempty\\npositive reverse-add forward-closed set has a positive palindrome, even if\\nk(L) grows without any uniform bound, provided 2*k(L)<=L. -/\\ntheorem variable_half_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)\\n    (hwidth : ∀ L, B <= L -> 0 < k L ∧ 2*(k L) <= L)\\n    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  obtain ⟨n, hn, hnS⟩ := hne\\n  obtain ⟨t, d, L, _, _, hc, hL, _, h10⟩ :=\\n    AstraModular.large_width_compatible_state n (max B 6) hn\\n  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL\\n  have hk : 0 < k L := (hwidth L hLB).1\\n  have hbound : 2 * (k L) <= L := (hwidth L hLB).2\\n  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=\\n    palindrome_with_given_suffix (orbit n t) (k L) L hk hbound h10\\n  have hmem : ∀ j, S (orbit n j) := by\\n    intro j\\n    induction j with\\n    | zero => exact hnS\\n    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih\\n  refine ⟨p, hp, ?_, hpal⟩\\n  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)\\n\\n/-- The entire low half may be retained: at every exact width L>=6,\\nS depends only on L and n mod 10^(floor(L/2)). This unbounded modulus\\nis strictly stronger than the previous (L-4)/2 exponent. -/\\ntheorem exact_half_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop)\\n    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (L / 2)) = m % (10 ^ (L / 2)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  apply variable_half_suffix_closed_set_contains_palindrome\\n    S (fun L => L / 2) 6\\n  · intro L hL\\n    constructor <;> omega\\n  · exact hsat\\n  · exact hne\\n  · exact hclosed\\n\\nend Agent111.GrowingSuffix\\n\\n#print axioms Agent111.GrowingSuffix.palindrome_with_given_suffix\\n#print axioms Agent111.GrowingSuffix.variable_half_suffix_closed_set_contains_palindrome\\n#print axioms Agent111.GrowingSuffix.exact_half_suffix_closed_set_contains_palindrome\\n\",\"blob\":\"cd2bf60a3b3e0c5718574aa5a5bdaff9d04d46ec\",\"module\":\"SharpSuffix\"}]")
for f in files:
 b=f['content'].encode(); calculated=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(); assert calculated==f['blob']
 print(json.dumps({'module':f['module'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':calculated,'imports':re.findall(r'^import (.+)$',f['content'],re.M)}))
PY
```

Complete substantive output:

```text
{"module": "GrowingSuffix", "bytes": 3660, "sha256": "910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a", "git_blob": "aa7ed6bf0675d2fdd6bbcd7f689f64039ff7b8cc", "imports": ["Saturation"]}
{"module": "SharpSuffix", "bytes": 3943, "sha256": "8f26f160d90b363a4e89728bc2470bde12bac5e751c89e97dacbc9e59bfa1c1c", "git_blob": "cd2bf60a3b3e0c5718574aa5a5bdaff9d04d46ec", "imports": ["GrowingSuffix"]}
```

## Verifier, manifest and source-map identities

Execution output chunk: `5b9000`. Exit code: `0`.

```bash
python3 -B - <<'PY'
from pathlib import Path
import hashlib,json
root=Path('/workspace/scratch/8b5152316f75/p196-agent4')
for n in ['proofs/verify_project__214bf7673efe116b.py','proofs/MANIFEST.sha256','proofs/SOURCE_MAP.json']:
 b=(root/n).read_bytes();print(n,len(b),hashlib.sha256(b).hexdigest(),hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest())
m=json.loads((root/'proofs/SOURCE_MAP.json').read_bytes())['paths']; lines=(root/'proofs/MANIFEST.sha256').read_text().splitlines()
keys={v['current'] for k,v in m.items() if (k.endswith('.lean') and k.startswith('proofs/contributions/agent-111/exact-length-residues/') and k.count('/')==4) or k=='proofs/research/Lychrel196Research.lean'}
for line in lines:
 if any(line.endswith(' '+k) or line.endswith(' '+k.removeprefix('proofs/')) for k in keys if k): print(line)
PY
```

Complete substantive output:

```text
proofs/verify_project__214bf7673efe116b.py 14531 c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a 21131b03dfa516eb19a0a7a4df4f2a41020d4db1
proofs/MANIFEST.sha256 1334622 5fac9a5de4a537e91c847fe739594ded47c22460d1e5286db62f7ed5a5adf74d 7371435c20a38b134d5d530bf2619d074cd35378
proofs/SOURCE_MAP.json 4396780 f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba e5f8d27bf09f50f8b9756bf91dff02e992aa4a32
```

## Full static source and import closure check

Execution output chunk: `b16060`. Exit code: `0`.

```bash
python3 -B - <<'PY'
import ast,json,hashlib,re
from pathlib import Path
root=Path('/workspace/scratch/8b5152316f75/p196-agent4')
data=json.loads("{\"registry\":{\"schema_version\":1,\"agent\":\"Agent #21\",\"title\":\"PR112 scoped original-source binding to the current repository layout\",\"source_binding\":{\"source_head\":\"01ecb6aa6bc555335ff6cb628d08e84133888307\",\"target_base\":\"160ea9e84016f8f98625fcfd0d879536a0dd5799\",\"original_dependency_commit\":\"c3192d5bf2962298bcb2bb209a0947f657e8a7e5\",\"archive_root\":\"2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5\",\"source_map_sha256\":\"f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba\",\"source_map_git_blob\":\"e5f8d27bf09f50f8b9756bf91dff02e992aa4a32\",\"scope\":\"Source identity and import mapping only; no fresh Lean verification is claimed by this record.\"},\"toolchain\":{\"release\":\"4.19.0\",\"commit_prefix\":\"6caaee842e94\",\"allowed_axioms\":[\"propext\",\"Classical.choice\",\"Quot.sound\"],\"compiler_arguments\":[\"-j1\",\"-DElab.async=false\"],\"release_tar_sha256\":\"6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe\"},\"catalogue_complete\":false,\"catalogue_blockers\":[{\"id\":\"SCOPED_PR112_REGISTRY\",\"status\":\"OUT_OF_SCOPE\",\"description\":\"This registry describes only the original thirteen-module PR112 closure; it does not claim repository-wide accepted-scope coverage.\"}],\"projects\":{\"agent111-growing-tenpower-suffix\":{\"scope\":\"Original ordinary-decimal semantics; palindrome realization and conditional palindrome membership in sufficiently suffix-saturated, positive nonempty reverse-add forward-closed sets. No actual orbit-hit or 196 conclusion.\",\"roots\":[\"SharpSuffix\"],\"modules\":{\"OuterBlock\":{\"path\":\"proofs/OuterBlock__f3eeca89d7075870.lean\",\"sha256\":\"bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705\",\"git_blob\":\"57b7dfa5a6e24f3d5097cd0031dd7c986b9f2ff4\",\"imports\":[\"Std\"]},\"ModulusSplit\":{\"path\":\"proofs/ModulusSplit__508a004fdcababff.lean\",\"sha256\":\"b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f\",\"git_blob\":\"88b6f05e3346650dec35017f31b3a2721e8ddb15\",\"imports\":[\"OuterBlock\"]},\"PeriodExistence\":{\"path\":\"proofs/PeriodExistence__95d4d6b8d7cc42d4.lean\",\"sha256\":\"e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd\",\"git_blob\":\"15a20afe499c1a54583a6c384c967049b523fcab\",\"imports\":[\"Std\"]},\"ModularSpan\":{\"path\":\"proofs/ModularSpan__03f58c6453a7d3cc.lean\",\"sha256\":\"1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754\",\"git_blob\":\"13c65527cb65dd199325a4c3b11c35e1474dcc58\",\"imports\":[\"Std\"]},\"ArithmeticCRT\":{\"path\":\"proofs/ArithmeticCRT__1fcf44d7abb07924.lean\",\"sha256\":\"c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5\",\"git_blob\":\"2722c6cf788605260eace42a86b3c0069ba0dce6\",\"imports\":[\"ModularSpan\"]},\"Lychrel196Research\":{\"path\":\"proofs/Lychrel196Research__c696e0ea3db39d92.lean\",\"sha256\":\"f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c\",\"git_blob\":\"c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506\",\"imports\":[\"Std\"]},\"PalindromeDigits\":{\"path\":\"proofs/PalindromeDigits__2c76cffae2ea7218.lean\",\"sha256\":\"323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f\",\"git_blob\":\"d60da8781a92943d9c4281002aaca13b403c4f67\",\"imports\":[\"Lychrel196Research\"]},\"PairWeights\":{\"path\":\"proofs/PairWeights__e065d83279cdd12a.lean\",\"sha256\":\"8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae\",\"git_blob\":\"345cb5dce73ee99bbbb2a65ae6840370de18cf21\",\"imports\":[\"Std\"]},\"DigitPools\":{\"path\":\"proofs/DigitPools__35519b17610b4240.lean\",\"sha256\":\"40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec\",\"git_blob\":\"c8e8f00d28c9e0630488e2e17218f909f5bc4534\",\"imports\":[\"PalindromeDigits\",\"PairWeights\"]},\"ResidueOrbit\":{\"path\":\"proofs/ResidueOrbit__d8f2f960ab0bad2b.lean\",\"sha256\":\"989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6\",\"git_blob\":\"98de673674512414f38182eded9b2a01c47ce4b6\",\"imports\":[\"Lychrel196Research\"]},\"Saturation\":{\"path\":\"proofs/Saturation__759aae5707b26af4.lean\",\"sha256\":\"a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0\",\"git_blob\":\"d09021588e3fc9c3c456d4276762613c30a68be1\",\"imports\":[\"ModulusSplit\",\"PeriodExistence\",\"ArithmeticCRT\",\"DigitPools\",\"ResidueOrbit\"]},\"GrowingSuffix\":{\"path\":\"proofs/contributions/agent-111/growing-tenpower-suffix-20261016/GrowingSuffix.lean\",\"sha256\":\"910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a\",\"git_blob\":\"aa7ed6bf0675d2fdd6bbcd7f689f64039ff7b8cc\",\"imports\":[\"Saturation\"]},\"SharpSuffix\":{\"path\":\"proofs/contributions/agent-111/growing-tenpower-suffix-20261016/SharpSuffix.lean\",\"sha256\":\"8f26f160d90b363a4e89728bc2470bde12bac5e751c89e97dacbc9e59bfa1c1c\",\"git_blob\":\"cd2bf60a3b3e0c5718574aa5a5bdaff9d04d46ec\",\"imports\":[\"GrowingSuffix\"]}},\"historical_originals_unchanged\":true}},\"claims\":[{\"id\":\"growing-suffix\",\"project\":\"agent111-growing-tenpower-suffix\",\"module\":\"GrowingSuffix\",\"endpoints\":[\"Agent111.GrowingSuffix.powerTen_saturation\",\"Agent111.GrowingSuffix.variable_powerTen_closed_set_contains_palindrome\",\"Agent111.GrowingSuffix.half_width_suffix_closed_set_contains_palindrome\"]},{\"id\":\"sharp-half-suffix\",\"project\":\"agent111-growing-tenpower-suffix\",\"module\":\"SharpSuffix\",\"endpoints\":[\"Agent111.GrowingSuffix.palindrome_with_given_suffix\",\"Agent111.GrowingSuffix.variable_half_suffix_closed_set_contains_palindrome\",\"Agent111.GrowingSuffix.exact_half_suffix_closed_set_contains_palindrome\"]}]},\"new_files\":[{\"module\":\"GrowingSuffix\",\"content\":\"import Saturation\\n\\n/-!\\nAgent #111: unbounded width-dependent decimal suffix congruence obstruction.\\n\\nFor any sufficiently long exact decimal width L, allow a modulus 10^(k L)\\nthat can grow exponentially with L, but with k L <= (L-4)/2.\\nThe original decimal orbit and exact-length saturation proofs are imported\\nunchanged. This does not prove that any particular orbit hits a palindrome.\\n-/\\n\\nnamespace Agent111.GrowingSuffix\\n\\nopen Lychrel196 DecimalDigits ExactLengthResidues\\n\\n/-- At any specified width L with 1 <= k and 2*k+4 <= L, every residue\\ncompatible with a true palindrome has a same-width palindrome modulo 10^k.\\nThis specializes the *existing* arbitrary-modulus theorem at u=10^k,\\nq=1, r=1; no unproved arithmetic assumption remains. -/\\ntheorem powerTen_saturation (k : Nat) (hk : 1 <= k) :\\n    SaturationAbove (10 ^ k) (2*k+4) := by\\n  apply saturation_of_split (10 ^ k) k (10 ^ k) 1 1 hk\\n  · exact Nat.pow_pos (by decide)\\n  · decide\\n  · simp\\n  · exact ⟨1, by simp⟩\\n  · simp\\n  · decide\\n  · simp\\n\\n/-- If the suffix modulus is a power of ten with exponent at most almost\\nhalf the available width, forward closure forces *some member of the set*\\nto be an ordinary decimal palindrome. The orbit used to transfer membership\\nis not claimed to contain that palindrome. -/\\ntheorem variable_powerTen_closed_set_contains_palindrome\\n    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)\\n    (hwidth : ∀ L, B <= L -> 1 <= k L ∧ 2*(k L)+4 <= L)\\n    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  obtain ⟨n, hn, hnS⟩ := hne\\n  obtain ⟨t, d, L, _, _, hc, hL, h11, h10⟩ :=\\n    AstraModular.large_width_compatible_state n (max B 6) hn\\n  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL\\n  have hk : 1 <= k L := (hwidth L hLB).1\\n  have hbound : 2*(k L)+4 <= L := (hwidth L hLB).2\\n  have hcompatible : Compatible (10 ^ (k L)) L (orbit n t) := by\\n    constructor\\n    · intro h\\n      exact h10 h.2\\n    · intro _\\n      exact Nat.dvd_trans (Nat.gcd_dvd_right (10 ^ (k L)) 11) h11\\n  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=\\n    (powerTen_saturation (k L) hk) L hbound (orbit n t) hcompatible\\n  have hmem : ∀ j, S (orbit n j) := by\\n    intro j\\n    induction j with\\n    | zero => exact hnS\\n    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih\\n  refine ⟨p, hp, ?_, hpal⟩\\n  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)\\n\\n/-- An explicit unbounded schedule: at width L>=6, membership depends\\nonly on the last floor((L-4)/2) decimal digits, plus the exact width.\\nNo fixed modulus can replace this schedule for all large L. -/\\ntheorem half_width_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop)\\n    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ ((L - 4) / 2)) = m % (10 ^ ((L - 4) / 2)) ->\\n      (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  apply variable_powerTen_closed_set_contains_palindrome\\n    S (fun L => (L - 4) / 2) 6\\n  · intro L hL\\n    constructor <;> omega\\n  · exact hsat\\n  · exact hne\\n  · exact hclosed\\n\\nend Agent111.GrowingSuffix\\n\\n#print axioms Agent111.GrowingSuffix.powerTen_saturation\\n#print axioms Agent111.GrowingSuffix.variable_powerTen_closed_set_contains_palindrome\\n#print axioms Agent111.GrowingSuffix.half_width_suffix_closed_set_contains_palindrome\\n\"},{\"module\":\"SharpSuffix\",\"content\":\"import GrowingSuffix\\n\\n/-! Ordinary decimal palindrome realization with a prescribed low-order half.\\nThe modulus 10^k is allowed up to k=floor(L/2), without the 4-digit\\npadding required by general arbitrary-modulus residue saturation. -/\\n\\nnamespace Agent111.GrowingSuffix\\n\\nopen Lychrel196 DecimalDigits ExactLengthResidues\\n\\n/-- Every positive-width decimal residue whose units digit is nonzero can\\nbe completed to an ordinary positive palindrome of exact width L, whenever\\n2*k<=L. We reuse the *checked* original constructive realization with\\nempty inner digit pools, not a search over finite examples. -/\\ntheorem palindrome_with_given_suffix (n k L : Nat)\\n    (hk : 0 < k) (hL : 2 * k <= L) (hunit : ¬ 10 ∣ n) :\\n    ∃ P e, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧\\n      P % (10 ^ k) = n % (10 ^ k) := by\\n  let A := n % (10 ^ k)\\n  have hA : A < 10 ^ k := Nat.mod_lt n (Nat.pow_pos (by decide))\\n  have hten : 10 ∣ 10 ^ k := ten_dvd_pow k (by omega)\\n  have hA0 : A % 10 ≠ 0 := by\\n    change n % (10 ^ k) % 10 ≠ 0\\n    rw [Nat.mod_mod_of_dvd n hten]\\n    intro hzero\\n    exact hunit (Nat.dvd_of_mod_eq_zero hzero)\\n  have hlow : LowerPositions k L ([] : List Nat) := by\\n    intro i hi\\n    simp at hi\\n  obtain ⟨P, e, hc, hp, hmod, _⟩ :=\\n    two_pool_realization A k L (10 ^ k) 1 0 0 ([] : List Nat) ([] : List Nat)\\n      hk hL hA hA0 (⟨1, by simp⟩) (by simp) hlow (by simp) (by simp)\\n  have hPpos : 0 < P := by\\n    rw [← hc.2.2.2]\\n    exact value_positive e L hc.1 hc.2.2.1\\n  refine ⟨P, e, hPpos, hc, hp, ?_⟩\\n  simpa only [A, Nat.mod_mod] using hmod\\n\\n/-- Every eventually exact-width, trailing-k(L)-digit saturated, nonempty\\npositive reverse-add forward-closed set has a positive palindrome, even if\\nk(L) grows without any uniform bound, provided 2*k(L)<=L. -/\\ntheorem variable_half_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)\\n    (hwidth : ∀ L, B <= L -> 0 < k L ∧ 2*(k L) <= L)\\n    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  obtain ⟨n, hn, hnS⟩ := hne\\n  obtain ⟨t, d, L, _, _, hc, hL, _, h10⟩ :=\\n    AstraModular.large_width_compatible_state n (max B 6) hn\\n  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL\\n  have hk : 0 < k L := (hwidth L hLB).1\\n  have hbound : 2 * (k L) <= L := (hwidth L hLB).2\\n  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=\\n    palindrome_with_given_suffix (orbit n t) (k L) L hk hbound h10\\n  have hmem : ∀ j, S (orbit n j) := by\\n    intro j\\n    induction j with\\n    | zero => exact hnS\\n    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih\\n  refine ⟨p, hp, ?_, hpal⟩\\n  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)\\n\\n/-- The entire low half may be retained: at every exact width L>=6,\\nS depends only on L and n mod 10^(floor(L/2)). This unbounded modulus\\nis strictly stronger than the previous (L-4)/2 exponent. -/\\ntheorem exact_half_suffix_closed_set_contains_palindrome\\n    (S : Nat -> Prop)\\n    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),\\n      Canonical n d L -> Canonical m e L ->\\n      n % (10 ^ (L / 2)) = m % (10 ^ (L / 2)) -> (S n ↔ S m))\\n    (hne : ∃ n, 0 < n ∧ S n)\\n    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :\\n    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by\\n  apply variable_half_suffix_closed_set_contains_palindrome\\n    S (fun L => L / 2) 6\\n  · intro L hL\\n    constructor <;> omega\\n  · exact hsat\\n  · exact hne\\n  · exact hclosed\\n\\nend Agent111.GrowingSuffix\\n\\n#print axioms Agent111.GrowingSuffix.palindrome_with_given_suffix\\n#print axioms Agent111.GrowingSuffix.variable_half_suffix_closed_set_contains_palindrome\\n#print axioms Agent111.GrowingSuffix.exact_half_suffix_closed_set_contains_palindrome\\n\"}]}")
v=(root/'proofs/verify_project__214bf7673efe116b.py').read_bytes()
assert hashlib.sha1(f'blob {len(v)}\0'.encode()+v).hexdigest()=='21131b03dfa516eb19a0a7a4df4f2a41020d4db1'
tree=ast.parse(v)
fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='code_only')
ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<inspected-code-only>','exec'),ns)
news={x['module']:x['content'].encode() for x in data['new_files']}
records=data['registry']['projects']['agent111-growing-tenpower-suffix']['modules']; order=[];seen=set();active=set()
for name,rec in records.items():
 b=news[name] if name in news else (root/rec['path']).read_bytes()
 assert hashlib.sha256(b).hexdigest()==rec['sha256'],name
 assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==rec['git_blob'],name
 code=ns['code_only'](b.decode()); deps=[d for ln in re.findall(r'^\s*import\s+([^\n]+)',code,re.M) for d in ln.split()]
 assert deps==rec['imports'],(name,deps)
 assert not re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])",code),name
 print('SOURCE_IDENTITY_AND_IMPORTS_PASS',name,rec['git_blob'],rec['sha256'])
def visit(name):
 if name=='Std': return
 assert name in records,name
 assert name not in active,name
 if name in seen:return
 active.add(name)
 for dep in records[name]['imports']:visit(dep)
 active.remove(name);seen.add(name);order.append(name)
visit('SharpSuffix');assert seen==set(records)
print('CLOSURE_PASS',len(order),json.dumps(order))
print('LEAN_COMPILATION_NOT_RUN; AXIOM_AUDIT_NOT_RUN; STATIC_SOURCE_CHECK_ONLY')
PY
```

Complete substantive output:

```text
SOURCE_IDENTITY_AND_IMPORTS_PASS OuterBlock 57b7dfa5a6e24f3d5097cd0031dd7c986b9f2ff4 bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705
SOURCE_IDENTITY_AND_IMPORTS_PASS ModulusSplit 88b6f05e3346650dec35017f31b3a2721e8ddb15 b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f
SOURCE_IDENTITY_AND_IMPORTS_PASS PeriodExistence 15a20afe499c1a54583a6c384c967049b523fcab e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd
SOURCE_IDENTITY_AND_IMPORTS_PASS ModularSpan 13c65527cb65dd199325a4c3b11c35e1474dcc58 1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754
SOURCE_IDENTITY_AND_IMPORTS_PASS ArithmeticCRT 2722c6cf788605260eace42a86b3c0069ba0dce6 c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5
SOURCE_IDENTITY_AND_IMPORTS_PASS Lychrel196Research c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506 f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c
SOURCE_IDENTITY_AND_IMPORTS_PASS PalindromeDigits d60da8781a92943d9c4281002aaca13b403c4f67 323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f
SOURCE_IDENTITY_AND_IMPORTS_PASS PairWeights 345cb5dce73ee99bbbb2a65ae6840370de18cf21 8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae
SOURCE_IDENTITY_AND_IMPORTS_PASS DigitPools c8e8f00d28c9e0630488e2e17218f909f5bc4534 40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec
SOURCE_IDENTITY_AND_IMPORTS_PASS ResidueOrbit 98de673674512414f38182eded9b2a01c47ce4b6 989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6
SOURCE_IDENTITY_AND_IMPORTS_PASS Saturation d09021588e3fc9c3c456d4276762613c30a68be1 a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0
SOURCE_IDENTITY_AND_IMPORTS_PASS GrowingSuffix aa7ed6bf0675d2fdd6bbcd7f689f64039ff7b8cc 910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a
SOURCE_IDENTITY_AND_IMPORTS_PASS SharpSuffix cd2bf60a3b3e0c5718574aa5a5bdaff9d04d46ec 8f26f160d90b363a4e89728bc2470bde12bac5e751c89e97dacbc9e59bfa1c1c
CLOSURE_PASS 13 ["OuterBlock", "ModulusSplit", "PeriodExistence", "ModularSpan", "ArithmeticCRT", "Lychrel196Research", "PalindromeDigits", "PairWeights", "DigitPools", "ResidueOrbit", "Saturation", "GrowingSuffix", "SharpSuffix"]
LEAN_COMPILATION_NOT_RUN; AXIOM_AUDIT_NOT_RUN; STATIC_SOURCE_CHECK_ONLY
```

## Historical manifest binding

Execution output chunk: `b20d42`. Exit code: `0`.

```bash
python3 -B - <<'PY'
from pathlib import Path
import hashlib,json
root=Path('/workspace/scratch/8b5152316f75/p196-agent4'); b=(root/'proofs/MANIFEST.sha256').read_bytes(); assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()=='7371435c20a38b134d5d530bf2619d074cd35378'
manifest={line.split('  ',1)[1]:line.split('  ',1)[0] for line in b.decode().splitlines() if '  ' in line};d=json.loads((root/'proofs/SOURCE_MAP.json').read_bytes())['paths']
names=['ArithmeticCRT','DigitPools','ModularSpan','ModulusSplit','OuterBlock','PairWeights','PalindromeDigits','PeriodExistence','ResidueOrbit','Saturation','Lychrel196Research']
for n in names:
 key='proofs/research/Lychrel196Research.lean' if n=='Lychrel196Research' else f'proofs/contributions/agent-111/exact-length-residues/{n}.lean'
 assert manifest[key.removeprefix('proofs/')]==d[key]['sha256'];print('HISTORICAL_MANIFEST_PASS',n,manifest[key.removeprefix('proofs/')])
print('MANIFEST_USES_ORIGINAL_PATHS; SOURCE_MAP_BINDS_RELOCATED_CURRENT_PATHS')
PY
```

Complete substantive output:

```text
HISTORICAL_MANIFEST_PASS ArithmeticCRT c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5
HISTORICAL_MANIFEST_PASS DigitPools 40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec
HISTORICAL_MANIFEST_PASS ModularSpan 1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754
HISTORICAL_MANIFEST_PASS ModulusSplit b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f
HISTORICAL_MANIFEST_PASS OuterBlock bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705
HISTORICAL_MANIFEST_PASS PairWeights 8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae
HISTORICAL_MANIFEST_PASS PalindromeDigits 323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f
HISTORICAL_MANIFEST_PASS PeriodExistence e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd
HISTORICAL_MANIFEST_PASS ResidueOrbit 989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6
HISTORICAL_MANIFEST_PASS Saturation a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0
HISTORICAL_MANIFEST_PASS Lychrel196Research f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c
MANIFEST_USES_ORIGINAL_PATHS; SOURCE_MAP_BINDS_RELOCATED_CURRENT_PATHS
```

## Read-only remote binding

The original assessment read main commit 160ea9e84016f8f98625fcfd0d879536a0dd5799 and its nonrecursive proofs tree c205bb5910259415e010c6366b455ca850dffbfb (2682 entries, truncated=false). For each of the eleven original Lean dependencies, the target flattened-file blob, archived-file blob, source-map oid, and locally recomputed Git blob were identical. The source-map and manifest local bytes were independently authenticated against their remote target blobs. These observations bind the older local checkout's relevant bytes to the inspected target; the older checkout head was not treated as the target head.

Remote read endpoints used:

- https://api.github.com/repos/taco-jpg/p196-algorithm/git/ref/heads/main
- https://api.github.com/repos/taco-jpg/p196-algorithm/git/trees/c205bb5910259415e010c6366b455ca850dffbfb
- https://api.github.com/repos/taco-jpg/p196-algorithm/contents/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-111/exact-length-residues?ref=160ea9e84016f8f98625fcfd0d879536a0dd5799
- https://api.github.com/repos/taco-jpg/p196-algorithm/contents/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research?ref=160ea9e84016f8f98625fcfd0d879536a0dd5799

A preliminary recursive root-tree read failed with Transport closed. It was replaced by the complete nonrecursive proofs-tree read; no inference of absence or conflict was drawn from the transport failure.
