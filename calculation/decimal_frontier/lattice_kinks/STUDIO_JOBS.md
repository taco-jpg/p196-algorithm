# STUDIO_JOBS.md (W7) -- jobs for the 32-core Mac Studio.  Single-thread jobs, run many in parallel on separate processes.

Setup: cd w7_kink/code; python3 -m venv ../venv; ../venv/bin/pip install python-sat; g++ -O3 -march=native -o surv surv.cpp (DFS, optional).
Data: ../data/lat0.txt lat1.txt lat2.txt lat_p12m9.txt.

Job family A (lifetime/exclusion, any period): for each lattice L in {lat0, lat2, lat_p12m9}, each o in {0,1,2,3} (0..2 for p12m9), each w in 8..16:
    ../venv/bin/python lifet.py ../data/L.txt w o 2*w     # prints LIFETIME w o = max SAT horizon; UNSAT at lifetime+1 => no kink of any period at that width/class
  A width w is EXCLUDED only when all classes o have finite lifetime.  Measured cost lat0: w=8 ~30 s, w=9 ~40 s per class, growth x2-3 per width unit
  => w=12: ~10-30 min, w=14: ~hours per class.  Expected total for w=8..14 x 4 classes x 3 lattices: ~100-150 core-hours, trivial on 32 cores.
Job family B (periodic orbit search, only if A shows lifetimes > T): sat_kink.py ../data/L.txt w o per T   (T=80, 192, 72; and 160 for 2x period).
Job family C: lifetimes for rec2 need H up to 192 horizon; start lifet.py at H=2*w and it increases until UNSAT.
Any SAT in family B: decode with sat_verify.py's decode(), rebuild the integer from the pair word (lib7.digits_from_pair), replay >= 20,000 plain big-int
reverse-and-add steps checking structure and no palindrome, save JSON, report.
Done criterion for the lattice question at "reachable" width: lifetime L(w) <= 4w+~16 observed; to reach 80 steps need w ~ 17-20 (cost ~x2.5^(20-9) = hopelessly large
for brute force) => the all-width answer needs the theory route (item 2 in KINK.md).
