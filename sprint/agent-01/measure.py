"""Run a command and report wall time and peak RSS of the child (Linux/macOS).
Usage: python3 measure.py <cmd> [args...]"""
import resource, subprocess, sys, time, platform
t = time.time()
r = subprocess.run(sys.argv[1:])
wall = time.time() - t
ru = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
mb = ru / 1024 if platform.system() == 'Linux' else ru / (1024 * 1024)
print(f'[measure] exit={r.returncode} wall={wall:.1f}s peakRSS={mb:.0f}MB', file=sys.stderr)
sys.exit(r.returncode)
