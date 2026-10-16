"""Replay two frozen exact-arithmetic bundles without modifying their sources."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent
PASS = HERE.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
specs = [
    ('absorbing_core', PASS / 'seam_persistence/followup_absorbing_core',
     'check_absorbing_core.py', ['absorbing_core_results.json', 'absorbing_core_controls.json.gz']),
    ('periodic_bulk', PASS / 'periodic_bulk_followup',
     'verify_periodic.py', ['periodic_verification.json', 'ordinary_trajectories.json.gz']),
]
for label, source, script, outputs in specs:
    files = [p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    frozen = {str(p.relative_to(source)): sha(p) for p in files}
    replay = HERE / (label + '_replay')
    replay.mkdir(exist_ok=True)
    for name in frozen:
        target = replay / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    started = time.monotonic()
    result = subprocess.run([sys.executable, '-B', script], cwd=replay,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                            text=True, capture_output=True)
    log = result.stdout + result.stderr
    (HERE / (label + '_recheck.log')).write_text(log)
    assert result.returncode == 0, log
    reproduced = {}
    for name in outputs:
        assert sha(replay / name) == sha(source / name), name
        reproduced[name] = sha(replay / name)
    assert frozen == {name: sha(source / name) for name in frozen}
    scope = ({
        'absorbing_core': 'Written all-width maximal0/18-run ancestry and no-merging proof reviewed, including singletons, endpoints, new births and5ell extinction of one ancestry. Central18 erosion credited as prior work. Exact finite controls reproduced; no whole-orbit extinction claim.',
        'periodic_bulk': 'Written all-exponent guard-period lemma and cycle criterion reviewed. Exact finite phase graphs and all saved whole-word controls reproduced. Necessary16-step loop is unlifted; all11path-capped whole-word probes remain UNKNOWN.',
    })[label]
    receipt = {'status': 'PASS', 'source_directory': str(source.relative_to(PASS)),
               'source_sha256': frozen, 'script': script,
               'reproduced_outputs': reproduced, 'seconds': time.monotonic() - started,
               'written_proof_review_scope': scope,
               'no_source_files_mutated': True,
               'excluded_duplicate_infrastructure': [replay.name + '/'],
               'decimal_lychrel_existence_proved': False}
    (HERE / (label + '_review.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'bundle': label, 'status': 'PASS', 'files': len(frozen),
                     'reproduced_outputs': reproduced}), flush=True)
