#!/usr/bin/env python3
"""Fresh, kernel-only build of Agent110's complete certificate budget chain."""
import argparse
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--lean', required=True)
p.add_argument('--build', required=True, help='new, nonexistent build directory')
p.add_argument('--evidence', required=True, help='new, nonexistent evidence directory')
a = p.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[3]
checker = here.parent / 'review' / 'independent_rebuild.py'
cmd = [sys.executable, str(checker), '--repo', str(repo), '--lean', a.lean,
       '--build', a.build, '--evidence', a.evidence]
for name in ['CertificateAccounting', 'CertificateCharge', 'CertificateCarryBudget',
             'CertificatePhases', 'CertificateConsequences', 'CertificatePrefix',
             'CertificateSaturation', 'CertificateChecked', 'All']:
    cmd.extend(['--source', str((here / (name + '.lean')).relative_to(repo))])
subprocess.run(cmd, check=True)
