# decimal_frontier — base-10 certificate searches (2026-10-27)

This folder holds the code and write-ups behind
[reports/REPORT_DECIMAL_FRONTIER.md](../../reports/REPORT_DECIMAL_FRONTIER.md). All of it is computation or paper
argument; none of it is a Lean result. It contains no decimal certificate.

| folder | contents | main write-up |
| --- | --- | --- |
| `exterior_census/` | `bx` exact exterior engine (`src/bx.cpp`), first-coordinate NFA enumerator (`src/fc_enum.cpp`), census drivers, Studio package | `EXTERIOR.md`, `STUDIO_JOBS.md` |
| `theory/` | density theorem, mod (b−1) charge law, independent checks of PRs #411/#404/#399 | `THEORY.md` |
| `lattice_formats/` | generalized (lattice / absorbing band) exterior engines `bauto3`, backward cones, BDD engine, multi-band step `gt.py`; base-9 candidate JSON; decimal p=8 lattice data | `FORMATS.md` |
| `lattice_kinks/` | exact window map and SAT search for centres of the decimal p=8 lattice | `KINK.md`, `STUDIO_JOBS.md` |
| `hybrid_centres/` | neutral exterior + absorbing core: exact step, transfer/SAT searches | `HYBRID.md` |
| `orbits/` | orbit regularity census, base-10 statistics vs null models, template lifetimes | `ORBITS.md` |

Scripts were written on a 2-core research machine, so many contain absolute paths under `/home/claude/research/`
and expect sibling files that are not committed (raw databases, logs). The `STUDIO_JOBS.md` files explain how to
rebuild the inputs. In particular, `exterior_census/STUDIO_JOBS.md` expects the per-word database
(`out/db/b10_p*.jsonl`, about 33 MB). It was not committed because it is a computation record; the owner has a
copy.
