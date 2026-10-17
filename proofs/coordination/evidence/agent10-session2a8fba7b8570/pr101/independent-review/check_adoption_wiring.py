"""Read-only independent adoption wiring checks; no Lean, Git, or generators."""
import collections
import hashlib
import json
from pathlib import Path
import re

ROOT = Path('/workspace/scratch/2a8fba7b8570/agent10-pr101')
ADOPTION = ROOT / 'adoption-001'
OUT = ROOT / 'independent-review'
PROPOSED = ADOPTION / 'proposed-tree'
BASE = ADOPTION / 'base-selection'

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}

def read_json(path):
    return json.loads(path.read_text())

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def lean_code(text):
    # Independently strip nested comments and strings, retaining line boundaries.
    out, pos, depth, string = [], 0, 0, False
    while pos < len(text):
        pair, char = text[pos:pos+2], text[pos]
        if depth:
            if pair == '/-': depth += 1; out.append('  '); pos += 2
            elif pair == '-/': depth -= 1; out.append('  '); pos += 2
            else: out.append('\n' if char == '\n' else ' '); pos += 1
        elif string:
            if char == '\\': out.append('  '); pos += 2
            else:
                string = char != '"'
                out.append('\n' if char == '\n' else ' '); pos += 1
        elif pair == '/-': depth = 1; out.append('  '); pos += 2
        elif pair == '--':
            end = text.find('\n', pos)
            if end < 0: end = len(text)
            out.append(' ' * (end-pos)); pos = end
        elif char == '"': string = True; out.append(' '); pos += 1
        else: out.append(char); pos += 1
    check(not depth and not string, 'Unclosed Lean comment/string')
    return ''.join(out)

sealed_names = ['FINDINGS.md', 'STATIC_AUDIT.json', 'BUILD_AND_REPAIR_SUPPLEMENT.md',
                'BUILD_EVIDENCE_CHECK.json', 'AXIOM_EVIDENCE_CHECK.json']
sealed_before = {name: identity((OUT/name).read_bytes()) for name in sealed_names}
manifest = read_json(ADOPTION/'PATCH_MANIFEST.json')
registry = read_json(PROPOSED/'proofs/Agent1172641.registry.json')
mapping = read_json(PROPOSED/'proofs/Agent1172641.mapping.json')
records = registry['projects']['agent117-2641']['modules']
roots = registry['projects']['agent117-2641']['roots']
changes = {r['path']: r for r in manifest['changed_paths']}
check(len(changes) == len(manifest['changed_paths']) == 103, 'Changed path set')
check(collections.Counter(r['operation'] for r in changes.values()) == {'ADD': 101, 'MODIFY': 2}, 'Operations')
patch = (ADOPTION/'source-adoption.patch').read_bytes()
check(identity(patch)['sha256'] == '67bc0737c2eeb00546c58e1c07be2c25a87a8455b28284749d6f09b33b75f35c', 'Frozen patch')
check(identity(patch)['bytes'] == 1583520, 'Patch length')
check(identity((PROPOSED/'proofs/Agent1172641.registry.json').read_bytes())['sha256'] == '46a5b682a2ad0d6b62959511d342b88495257e7b7ce3b6c672e75bdbe0a27473', 'Frozen registry')

# Parse every complete unified-diff hunk and reconstruct all 103 resulting files
# in memory, including the exact no-final-newline metadata file.
lines = patch.splitlines(keepends=True)
boundaries = [i for i, line in enumerate(lines) if line.startswith(b'diff --git ')] + [len(lines)]
patch_results = []
for start, end in zip(boundaries, boundaries[1:]):
    chunk = lines[start:end]
    header = re.fullmatch(rb'diff --git a/(.+) b/(.+)\n', chunk[0])
    check(header is not None and header[1] == header[2], 'No renames or malformed headers')
    name = header[1].decode(); rec = changes[name]
    old = (BASE/name).read_bytes() if rec['operation'] == 'MODIFY' else b''
    wanted = (PROPOSED/name).read_bytes()
    check(identity(wanted) == rec['after'], 'Manifest after ' + name)
    check((identity(old) if rec['operation'] == 'MODIFY' else None) == rec['before'], 'Manifest before ' + name)
    check(not name.startswith('/') and '..' not in Path(name).parts, 'Safe patch path')
    first_hunk = next(i for i, line in enumerate(chunk) if line.startswith(b'@@ '))
    expected_header = [chunk[0]]
    if rec['operation'] == 'ADD': expected_header.append(b'new file mode 100644\n')
    expected_header.extend([(b'--- a/' + name.encode() + b'\n') if rec['operation'] == 'MODIFY' else b'--- /dev/null\n',
                            b'+++ b/' + name.encode() + b'\n'])
    check(chunk[:first_hunk] == expected_header, 'Exact allowed file header ' + name)
    old_lines = old.splitlines(keepends=True); cursor = 0; output = []
    i = first_hunk
    while i < len(chunk):
        h = re.fullmatch(rb'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n', chunk[i])
        check(h is not None, 'Hunk header ' + name)
        old_start, old_count = int(h[1]), int(h[2] or b'1')
        new_start, new_count = int(h[3]), int(h[4] or b'1')
        old_index = old_start - 1 if old_count else old_start
        check(cursor <= old_index <= len(old_lines), 'Hunk old offset ' + name)
        output.extend(old_lines[cursor:old_index]); cursor = old_index
        check(len(output) == (new_start - 1 if new_count else new_start), 'Hunk new offset ' + name)
        i += 1; old_seen = new_seen = 0
        while i < len(chunk) and not chunk[i].startswith(b'@@ '):
            line = chunk[i]; check(line[:1] in (b' ', b'+', b'-'), 'Hunk body ' + name)
            prefix, value = line[:1], line[1:]; i += 1
            if i < len(chunk) and chunk[i] == b'\\ No newline at end of file\n':
                check(value.endswith(b'\n'), 'No-newline marker position')
                value = value[:-1]; i += 1
            if prefix in (b' ', b'-'):
                check(cursor < len(old_lines) and old_lines[cursor] == value, 'Original hunk bytes ' + name)
                cursor += 1; old_seen += 1
            if prefix in (b' ', b'+'): output.append(value); new_seen += 1
        check((old_seen, new_seen) == (old_count, new_count), 'Hunk line counts ' + name)
    output.extend(old_lines[cursor:]); reconstructed = b''.join(output)
    check(reconstructed == wanted, 'Reconstructed patch result ' + name)
    check((ADOPTION/'patch-application-check'/name).read_bytes() == wanted, 'Retained git-apply result ' + name)
    patch_results.append({'path': name, 'operation': rec['operation'], **identity(wanted)})
check(len(patch_results) == 103 and {r['path'] for r in patch_results} == set(changes), 'Complete patch coverage')

H = read_json(ADOPTION/'inputs/source-head-proofs-tree.json')
B = read_json(ROOT/'source-closure/inputs/mainProofsTree.json')
check(H['sha'] == '7e8f4b3399d7e3998e26fc0d53f898b37943236c' and not H['truncated'], 'H tree')
check(B['sha'] == '29f9c383f132740ba33ed6dd8356eece96a481eb' and not B['truncated'], 'B tree')
hpaths = {'proofs/'+r['path']:r for r in H['tree']}
bpaths = {'proofs/'+r['path']:r for r in B['tree']}
maps = {r['module']:r for r in mapping['modules']}
check(len(maps) == len(records) == 104 and maps.keys() == records.keys(), 'Mapping module set')
check(roots == ['A124117P2641K7Final', 'Agent1172641Targets'], 'Both roots')
module_results, paths, external = [], set(), set()
for module, rec in records.items():
    path = rec['path']; mapped = maps[module]
    check(Path(path).parent == Path('proofs') and path not in paths, 'Unique flat module path ' + module); paths.add(path)
    check(not rec.get('adapter'), 'No source adapters ' + module)
    data = (PROPOSED/path).read_bytes()
    original = ROOT/'execution/strict-build/attempt-002/sources'/f'{module}.lean'
    if module == 'Agent1172641Targets': original = ROOT/'execution/strict-build/repair/Agent1172641Targets.lean'
    check(data == original.read_bytes(), 'Byte identity with qualified source ' + module)
    ident = identity(data)
    check(all(rec[k] == ident[k] == mapped[k] for k in ident), 'Registry/mapping identity ' + module)
    check(mapped['destination'] == path, 'Mapping path ' + module)
    code = lean_code(data.decode())
    deps = [name for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for name in line.split()]
    check(deps == rec['imports'], 'Actual imports ' + module)
    check(not re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", code), 'Existing verifier source screen ' + module)
    external.update(dep for dep in deps if dep not in records)
    reused = mapped['disposition'] == 'REUSE_EXACT_EXISTING_SOURCE'
    if reused:
        check(path not in changes, 'Untouched reused path ' + module)
        check(all(tree[path]['sha'] == ident['git_blob'] and tree[path]['mode'] == '100644' and tree[path]['size'] == len(data) for tree in (hpaths,bpaths)), 'Both H and B reuse ' + module)
        check((BASE/path).read_bytes() == data, 'Selected baseline reuse ' + module)
    else:
        check(path in changes and changes[path]['operation'] == 'ADD', 'Selected added source ' + module)
        check(path not in hpaths and path not in bpaths, 'Added path absent at both H/B ' + module)
    module_results.append({'module': module, 'path': path, 'qualified_source': str(original.relative_to(ROOT)),
                           'disposition': mapped['disposition'], 'imports': deps, **ident})
check(external == {'Std'}, 'External import set')
active, seen, order = set(), set(), []
def visit(module):
    if module not in records: return
    check(module not in active, 'Import cycle')
    if module in seen: return
    active.add(module)
    for dep in records[module]['imports']: visit(dep)
    active.remove(module); seen.add(module); order.append(module)
for root in roots: visit(root)
check(seen == set(records), 'Both roots cover all104')
counts = dict(collections.Counter(r['disposition'] for r in maps.values()))
check(counts == {'REUSE_EXACT_EXISTING_SOURCE':9, 'ADD_EXACT_HISTORICAL_SOURCE':8,
                 'ADD_EXACT_GENERATED_SOURCE':86, 'ADD_FIXED_WIP_DEFINITIONS_WITH_ORIGINAL_PRESERVED':1}, 'Source group counts')
check(registry['schema_version'] == 1 and registry['catalogue_complete'] is False and registry['catalogue_blockers'], 'Scoped incomplete catalogue')
check(registry['toolchain']['allowed_axioms'] == ['propext','Classical.choice','Quot.sound'], 'Helper axiom policy')
check(registry['accepted_global_registry_modified'] is False and all('ACCEPTED_BUILD' not in p for p in changes), 'Default global registry untouched')
check([c['endpoints'] for c in registry['claims']] == [['Agent124.Cert117P2641K7.ancestry_2641'],['Agent124.Cert117P2641K7.no_196_2641']], 'Exact scoped endpoints')
check(all(c['project'] == 'agent117-2641' and c['module'] == 'A124117P2641K7Final' for c in registry['claims']), 'Endpoint project and module')

original_results = []
for rec in manifest['original_nine']:
    name = rec['path']; before = (BASE/name).read_bytes(); after = (PROPOSED/name).read_bytes()
    pinned = ROOT/'source-closure/snapshot/pr101'/name
    check(before == pinned.read_bytes() and identity(before) == {k:rec[k] for k in ('bytes','sha256','git_blob')}, 'Original retained source ' + name)
    if name.endswith('/README.md'):
        check(after.startswith(before) and b'## 2026-10-17 verification and proposed source adoption' in after[len(before):], 'Dated append-only README')
    elif name.endswith('/lean_wip/Agent1172641Targets.lean'):
        check(after.count('«prefix»'.encode()) == 4 and after.replace('«prefix»'.encode(), b'prefix') == before,
              'Four identifier escapes only; historical comment remains unchanged')
        check(after == (PROPOSED/'proofs/Agent1172641Targets.lean').read_bytes(), 'Two fixed WIP copies equal')
    else: check(before == after and name not in changes, 'Unmodified original file ' + name)
    original_results.append({'path':name, 'changed':before != after, 'original':identity(before), 'proposed':identity(after)})
check(sum(r['changed'] for r in original_results) == 2, 'Original nine preservation')
data_results=[]
for rec in mapping['data']:
    data=(PROPOSED/rec['destination']).read_bytes()
    check(data == (ROOT/rec['original_path']).read_bytes(), 'Exact data copy ' + rec['destination'])
    check(identity(data) == {k:rec[k] for k in ('bytes','sha256','git_blob')}, 'Data identity')
    data_results.append({'path':rec['destination'], 'ends_with_newline':data.endswith(b'\n'), **identity(data)})
check((PROPOSED/'proofs/Agent1172641.source-pins.json').read_bytes() == (ROOT/'source-closure/SOURCE_PINS.json').read_bytes(), 'Historical pins preserved verbatim')
helper=(ADOPTION/'inputs/main-verify_project-implementation.py').read_bytes()
check(identity(helper)['sha256'] == 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a' and len(helper)==14531, 'Inspected verifier identity')
check(bpaths['proofs/verify_project__214bf7673efe116b.py']['sha'] == identity(helper)['git_blob'], 'Helper exists at main B')
sealed_after = {name: identity((OUT/name).read_bytes()) for name in sealed_names}
check(sealed_before == sealed_after, 'Earlier independent review files unchanged')
inputs=['source-adoption.patch','PATCH_MANIFEST.json','STRUCTURAL_CHECK.json','ADOPTION_PACKET.md','PACKAGING_DIAGNOSTIC.md',
        'proposed-tree/proofs/Agent1172641.registry.json','proposed-tree/proofs/Agent1172641.mapping.json',
        'proposed-tree/proofs/Agent1172641.md','proposed-tree/proofs/Agent1172641.source-pins.json',
        'inputs/main-verify_project-implementation.py','inputs/source-head-proofs-tree.json']
report={'status':'PASS_EXACT_ADOPTION_WIRING', 'review_scope':'Static full patch/source/registry wiring only; no new compiler, generator, graph or whole-main build.',
        'source_head':registry['source_head'],'comparison_main':registry['comparison_main'],
        'inputs':{str((ADOPTION/p).relative_to(ROOT)):identity((ADOPTION/p).read_bytes()) for p in inputs},
        'source_counts':counts,'module_count':104,'roots':roots,'external_imports':sorted(external),'build_order':order,
        'module_comparisons':module_results,'patch_changed_paths':patch_results,'original_nine':original_results,
        'data_files':data_results,'earlier_sealed_files':sealed_after,
        'all_patch_hunks_reconstructed_in_memory':True,'retained_git_apply_results_match':True,
        'helper_source_only_not_executed':True,'default_registry_untouched':True,'source_pins_verbatim':True,
        'claims':registry['claims'],'script':identity(Path(__file__).read_bytes())}
(OUT/'ADOPTION_WIRING_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'modules':104,'changed_paths':103,'source_counts':counts,
                  'output':'ADOPTION_WIRING_CHECK.json','patch_sha256':identity(patch)['sha256']},indent=2))
