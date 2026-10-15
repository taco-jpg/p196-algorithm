#!/usr/bin/env python3
"""Agent #115: run COPIES of the original generate_scalar_data.py (main+models) and
generate_checks.py (main+checks), patched only by literal string substitutions
(hierarchy 'scalar'->'broader', ids 16..30 renumbered by -16, module/namespace names,
job count 16->15), with `array` replaced by the v2 chunked `array`. Output to OUTDIR.
usage: python3 -I patch_orig_data_checks.py ORIG_DIR V2_GENERATOR CERT OUTDIR
"""
import sys, types, importlib.util
from pathlib import Path
orig_dir, v2_path, cert, out = map(Path, sys.argv[1:5])

def sub(src, old, new, count=1):
    assert src.count(old) == count, (old, src.count(old)); return src.replace(old, new)

# v2 array/tree: load only those two function definitions from the v2 file text
v2src = v2_path.read_text()
start = v2src.index('def tree('); end = v2src.index('def main():')
v2ns = {'CHUNK': 256}; assert v2src.count('CHUNK = 256') == 1
exec(v2src[start:end], v2ns)

d = (orig_dir / 'generate_scalar_data.py').read_text()
d = sub(d, "SOURCE = HERE.parent / '2026-10-14-component-specific-bound/component_certificates.json.gz'", f'SOURCE = Path({str(cert)!r})')
d = sub(d, "j['hierarchy'] == 'scalar'", "j['hierarchy'] == 'broader'")
d = sub(d, "assert [j['id'] for j in jobs] == list(range(16))", "assert [j['id'] for j in jobs] == list(range(16, 31))")
d = sub(d, "child = result[link['child_job']]", "child = result[link['child_job']-16]")
d = sub(d, "parent=p['job']['id']", "parent=p['job']['id']-16")
d = sub(d, "ScalarJobData", "BroaderJobData", 4)
d = sub(d, "'import RankRows", "'import RankRows")
d = sub(d, "s='import JobCatalog", "s='import BJobCatalog")
d = sub(d, "args.output/'JobCatalog.lean'", "args.output/'BJobCatalog.lean'")
d = sub(d, "f'JobData{identity}.lean'", "f'BJobData{identity}.lean'")
d = sub(d, 'then {link["child_job"]+1} else', 'then {link["child_job"]-16+1} else')
d = sub(d, "assert all(0 <= j < 16 for j in args.jobs)", "assert all(0 <= j < 15 for j in args.jobs)")
dm = types.ModuleType('generate_scalar_data'); dm.__file__ = str(out / 'gsd.py')
exec(compile(d, 'patched_generate_scalar_data', 'exec'), dm.__dict__)
dm.array = v2ns['array']   # v2 representation, same as v2 main does (original.array = array)

c = (orig_dir / 'generate_checks.py').read_text()
c = sub(c, 'import generate_scalar_data as data_source', 'data_source = DATA_SOURCE')
c = sub(c, "f'import JobData{identity}", "f'import BJobData{identity}")
c = sub(c, "f'import JobData{p}", "f'import BJobData{p}")
c = sub(c, "ScalarJobData", "BroaderJobData", 2)
c = sub(c, "f'JobChecks{identity}.lean'", "f'BJobChecks{identity}.lean'")
c = sub(c, "default=list(range(16))", "default=list(range(15))")
out.mkdir(parents=True, exist_ok=True)
(out / 'patched_generate_scalar_data.py.txt').write_text(d)
(out / 'patched_generate_checks.py.txt').write_text(c)
jobs = [str(i) for i in range(15)]
sys.argv = ['gsd', '--jobs', *jobs, '--output', str(out)]; dm.main()
cns = {'__name__': 'x', '__file__': str(out / 'gc.py'), 'DATA_SOURCE': dm}
exec(compile(c, 'patched_generate_checks', 'exec'), cns)
sys.argv = ['gc', '--output', str(out)]; cns['main']()
