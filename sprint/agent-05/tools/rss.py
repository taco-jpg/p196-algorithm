"""Run a command; print wall time and peak RSS of children (like /usr/bin/time -v)."""
import sys, subprocess, resource, time
t = time.time(); r = subprocess.run(sys.argv[1:]); w = time.time() - t
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(f"[rss.py] exit {r.returncode} wall {w:.1f}s user {ru.ru_utime:.1f}s maxrss {ru.ru_maxrss/1024:.0f} MB", file=sys.stderr)
sys.exit(r.returncode)
