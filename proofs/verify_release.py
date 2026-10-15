"""Check release byte identity and completeness, not mathematical truth."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    # A passing subset manifest is not complete publication verification.
    listed = [line.split('  ', 1)[1] for line in (ROOT/'MANIFEST.sha256').read_text().splitlines()]
    assert len(listed) == len(set(listed)), 'Duplicate manifest path'
    for name in listed:
        path = ROOT/name
        assert not Path(name).is_absolute() and path.resolve().is_relative_to(ROOT.resolve()), 'Unsafe manifest path'
        assert not path.is_symlink(), 'Manifest symlink: '+name
    import subprocess
    probe = subprocess.run(['git','rev-parse','--show-toplevel'],cwd=ROOT,capture_output=True,text=True)
    if probe.returncode == 0 and Path(probe.stdout.strip()).resolve() == ROOT.parent.resolve():
        tracked = subprocess.check_output(['git','ls-files','-z','--','proofs/'],cwd=ROOT.parent).decode().split('\0')
        expected = {name[len('proofs/'):] for name in tracked if name and name != 'proofs/MANIFEST.sha256'}
        coverage_source = 'git-index'
    else:
        expected = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.sha256' and '__pycache__' not in p.parts and p.suffix not in {'.olean','.ilean','.pyc','.o','.so'}}
        coverage_source = 'export-tree-excluding-reproducible-compiled-products'
    assert set(listed) == expected, {'unlisted': sorted(expected-set(listed)), 'unavailable': sorted(set(listed)-expected)}
    count = 0
    published_lean_sources = []
    for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = ROOT/name
        assert path.is_file(), 'Missing published file: '+name
        assert sha(path)==expected, 'Changed published file: '+name
        if path.suffix == '.lean':
            published_lean_sources.append(path)
        count += 1
    original = json.loads((ROOT/'INVENTORY.json').read_text())
    kept = [r for r in original if r['publication']=='retained']
    for record in kept:
        path = ROOT/record['published_path']
        assert path.stat().st_size==record['bytes'], record['source_path']
        assert sha(path)==record['sha256'], record['source_path']
    # Published sources can also live in agent-specific directories. Use the
    # verified manifest, so local caches or untracked build copies cannot
    # accidentally satisfy this source-presence check.
    sources = published_lean_sources
    names = {p.stem for p in sources}
    imports = 0
    for path in sources:
        for module in re.findall(r'^import\s+(\S+)', path.read_text(), re.M):
            # These roots are shipped with the pinned official Lean toolchain.
            # Lean is used by imported meta-level audit modules, not vendored
            # project source; all other module names still require a source.
            # The retained official CollectAxioms source reference imports
            # these two official modules. Their installed and imported-object
            # hashes match the pinned release archive (Agent104's
            # release-integration/standard-library-imports.json). This is a
            # narrow source-presence exemption, not trust in new local theorems.
            # Existing Agent13 real-weights sources use exactly these external
            # Mathlib modules, pinned to c44e0c8ee63ca166450922a373c7409c5d26b00b
            # in their README/check.py and independent Agent104 review. This is
            # source-presence classification only, not a new proof acceptance.
            external_mathlib = {
                'Mathlib.Data.Real.Sqrt',
                'Mathlib.Algebra.Order.BigOperators.Group.Finset',
                'Mathlib.Tactic.Linarith', 'Mathlib.Tactic.NormNum'}
            assert module in {'Std', 'Init', 'Lean', 'Lean.Elab.Tactic.Omega',
                              'Lean.MonadEnv', 'Lean.Util.FoldConsts'} or module in external_mathlib or module in names, (str(path),module)
            imports += 1
    print(json.dumps({'status':'PASS','manifest_files':count,
                     'unchanged_original_files':len(kept),
                     'lean_source_files':len(sources),'lean_imports':imports,
                     'mathematical_proof_check':False,'complete_publication_coverage':True,'coverage_source':coverage_source},indent=2))

if __name__=='__main__': main()
