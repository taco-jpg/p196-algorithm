"""Check release byte identity and completeness, not mathematical truth."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
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
            assert module in {'Std', 'Init', 'Lean', 'Lean.Elab.Tactic.Omega',
                              'Lean.MonadEnv', 'Lean.Util.FoldConsts'} or module in names, (str(path),module)
            imports += 1
    print(json.dumps({'status':'PASS','manifest_files':count,
                     'unchanged_original_files':len(kept),
                     'lean_source_files':len(sources),'lean_imports':imports,
                     'mathematical_proof_check':False},indent=2))

if __name__=='__main__': main()
