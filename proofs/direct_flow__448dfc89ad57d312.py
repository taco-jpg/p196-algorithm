"""Direct universal carry-tile synthesis with finite seed-path flow.

The allowed grammar may branch. Separate selected tiles encode just one
finite seed path (and may contain irrelevant disconnected cycles). All
universal safety and closure clauses are the archived exact Horn clauses.
No orbit or word-length sampling is used to certify a candidate.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

import z3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "main_existence_attempt" / "invariant"))

import creative_regular_invariant as arithmetic
from persist_spacetime_tile_grammar import composed_tiles
from persist_spacetime_weighted import FS, FE, TS, TERMS, NW, history_path, safety_graph, trim
from tile_closure import closure_tiles, unsafe, image_tiles
from grammar_cegis import accepted_path


def save(path, result):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n")
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(prior_path=None):
    started = time.monotonic()
    solver = z3.SolverFor("QF_FD")
    solver.set(phase="always_false")
    allowed = [z3.Bool(f"allowed_{k}") for k in range(NW)]
    selected = [z3.Bool(f"seed_{k}") for k in range(NW)]
    solver.add(*[z3.Implies(selected[k], allowed[k]) for k in range(NW)])

    # Exact archived safety product; it monitors the output folded word.
    safety_states, initial, safety_edges, safety_terms = trim(safety_graph())
    reachable = [z3.Bool(f"safe_reach_{i}") for i in range(len(safety_states))]
    solver.add(*[reachable[i] for i in initial])
    for u, v, cost in safety_edges:
        k, = cost
        assert cost[k] == -1
        solver.add(z3.Implies(z3.And(reachable[u], allowed[k]), reachable[v]))
    for u, cost in safety_terms:
        k, = cost
        solver.add(z3.Not(z3.And(reachable[u], allowed[k])))

    # Exact archived universal Horn closure, including extra terminal pairs.
    states, edges, terms = composed_tiles()
    good = [z3.Bool(f"closed_good_{i}") for i in range(len(states))]
    bad = [z3.Bool(f"closed_bad_{i}") for i in range(len(states))]
    solver.add(*good[:4])
    for u, v, a, b in edges:
        solver.add(z3.Implies(z3.And(good[u], allowed[a], allowed[b]), good[v]))
        solver.add(z3.Implies(z3.And(good[u], allowed[a], z3.Not(allowed[b])), bad[v]))
        solver.add(z3.Implies(z3.And(bad[u], allowed[a]), bad[v]))
    for u, a, extra, b in terms:
        solver.add(z3.Not(z3.And(bad[u], allowed[a])))
        required = allowed[b] if extra is None else z3.And(allowed[extra], allowed[b])
        solver.add(z3.Implies(z3.And(good[u], allowed[a]), required))

    # Native cardinality seed flow. These restrictions are NOT imposed on
    # the allowed grammar, whose language remains unrestricted in length.
    incoming = [[] for _ in FS]
    outgoing = [[] for _ in FS]
    terminal_choices = []
    for k, (u, q, o, v) in enumerate(FE):
        assert v not in (0, 1)
        outgoing[u].append(selected[k])
        incoming[v].append(selected[k])
    for (u, c), (extra, oc, k) in TERMS.items():
        outgoing[u].append(selected[k])
        terminal_choices.append(selected[k])
    assert not incoming[0] and not incoming[1]
    solver.add(z3.PbEq([(x, 1) for x in outgoing[0] + outgoing[1]], 1))
    solver.add(z3.PbEq([(x, 1) for x in terminal_choices], 1))
    for u in range(2, len(FS)):
        if len(incoming[u]) > 1:
            solver.add(z3.AtMost(*incoming[u], 1))
        if len(outgoing[u]) > 1:
            solver.add(z3.AtMost(*outgoing[u], 1))
        solver.add(z3.Or(incoming[u]) == z3.Or(outgoing[u]))

    prior_audit = None
    if prior_path is not None:
        replay_start = time.monotonic()
        raw = prior_path.read_bytes()
        prior = json.loads(raw)
        cores = prior["clauses"]
        seen = set()
        for index, core in enumerate(cores):
            assert core and len(core) == len(set(core))
            assert all(type(k) is int and 0 <= k < NW for k in core)
            key = tuple(sorted(core))
            assert key not in seen
            seen.add(key)
            assert not closure_tiles(core)[0], ("invalid prior core", index, core)
            # The unsafe least closure proves that no safe closed allowed
            # language can contain this entire core, independently of flow.
            solver.add(z3.Or([z3.Not(allowed[k]) for k in core]))
        prior_audit = dict(path=str(prior_path), sha256=hashlib.sha256(raw).hexdigest(),
                           clauses=len(cores), all_replayed_unsafe=True,
                           seconds=time.monotonic() - replay_start)

    metadata = dict(encoding="direct_universal_horn_with_separate_seed_flow",
                    solver="Z3 QF_FD", phase="always_false", z3_version=z3.get_version_string(),
                    fst_states=len(FS), tiles=NW, safety_states=len(safety_states),
                    safety_edges=len(safety_edges), safety_terminals=len(safety_terms),
                    composition_states=len(states), composition_edges=len(edges),
                    composition_terminals=len(terms), prior_audit=prior_audit,
                    assertions=len(solver.assertions()), build_seconds=time.monotonic() - started,
                    scope_shortest_seed_max_edges=44, scope_shortest_seed_max_digit_positions=89)
    return solver, allowed, selected, metadata


def audit_candidate(allowed, selected):
    assert selected <= allowed
    incoming = [0] * len(FS)
    outgoing = [0] * len(FS)
    terminal_count = 0
    for k, (u, q, o, v) in enumerate(FE):
        if k in selected:
            incoming[v] += 1
            outgoing[u] += 1
    for (u, c), (extra, oc, k) in TERMS.items():
        if k in selected:
            outgoing[u] += 1
            terminal_count += 1
    assert incoming[0] == incoming[1] == 0
    assert outgoing[0] + outgoing[1] == 1 and terminal_count == 1
    for u in range(2, len(FS)):
        assert incoming[u] <= 1 and outgoing[u] <= 1
        assert bool(incoming[u]) == bool(outgoing[u])

    path, raw_word = accepted_path(selected)
    word = (tuple(raw_word[0]), raw_word[1])
    assert arithmetic.valid(word)
    assert path == history_path(word)
    assert set(path) <= allowed
    assert len(path) == len(set(path))
    assert not unsafe(allowed)
    image = image_tiles(allowed)
    assert image <= allowed

    pairs, center = word
    digits = ([max(q - 9, 0) for q in pairs]
              + ([] if center is None else [center // 2])
              + [min(q, 9) for q in pairs[::-1]])
    assert digits and digits[-1] > 0 and all(0 <= d <= 9 for d in digits)
    n = sum(d * 10 ** i for i, d in enumerate(digits))
    n1 = n + int(str(n)[::-1])
    n2 = n1 + int(str(n1)[::-1])

    def encode(value):
        ds = tuple(map(int, str(value)[::-1]))
        return arithmetic.fold(tuple(a + b for a, b in zip(ds, ds[::-1])))

    assert encode(n) == word
    expected = encode(n1)
    assert arithmetic.qstep(word) == expected
    assert arithmetic.trans(word) == [expected]
    assert set(history_path(expected)) <= allowed
    assert not arithmetic.bad(expected)
    assert str(n2) != str(n2)[::-1]
    return dict(canonical_finite_word=[list(pairs), center], seed_path=path,
                realization=str(n), first_step=str(n1), lychrel_candidate=str(n2),
                witness_shift=2, independent_safety_check=True,
                independent_image_closure_check=True, image_tiles=len(image),
                finite_path_check=True, canonical_realization_check=True,
                candidate_nonpalindromic=True)


def run(seconds, prior_path):
    started = time.monotonic()
    solver, allowed_vars, selected_vars, metadata = build(prior_path)
    result = dict(metadata, status="running", requested_solver_seconds=seconds,
                  infinite_existence_proved=False)
    result["source_sha256"] = {
        str(p.relative_to(ROOT)): digest(p) for p in [
            Path(__file__), ROOT / "research/persist_spacetime_tile_grammar.py",
            ROOT / "research/persist_spacetime_weighted.py",
            ROOT / "research/creative_regular_direct.py",
            ROOT / "research/creative_regular_invariant.py",
            ROOT / "main_existence_attempt/invariant/tile_closure.py"]}
    save(HERE / "direct_flow_status.json", result)
    print(json.dumps(result), flush=True)
    solver.set(timeout=max(1, int(seconds * 1000)))
    solve_start = time.monotonic()
    status = solver.check()
    result.update(status=str(status), solver_seconds=time.monotonic() - solve_start,
                  total_seconds=time.monotonic() - started)
    if status == z3.sat:
        model = solver.model()
        allowed = {k for k, x in enumerate(allowed_vars)
                   if z3.is_true(model.eval(x, model_completion=True))}
        selected = {k for k, x in enumerate(selected_vars)
                    if z3.is_true(model.eval(x, model_completion=True))}
        result.update(allowed_tiles=sorted(allowed), selected_tiles=sorted(selected))
        try:
            result["candidate_audit"] = audit_candidate(allowed, selected)
            result["status"] = "candidate_verified_by_exact_python_graph_checks"
        except Exception as error:
            result["status"] = "candidate_audit_failed"
            result["audit_error"] = repr(error)
            save(HERE / "direct_flow_result.json", result)
            raise
    elif status == z3.unknown:
        result["reason"] = solver.reason_unknown()
    elif status == z3.unsat:
        result["unsat_scope"] = "one-tile carry-history grammar with nonempty finite accepted language"
        result["unsat_independently_formalized"] = False
    result["statistics"] = str(solver.statistics())
    save(HERE / "direct_flow_result.json", result)
    save(HERE / "direct_flow_status.json", result)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("allowed_tiles", "selected_tiles", "source_sha256", "statistics")},
                     indent=2), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--prior", type=Path)
    options = parser.parse_args()
    run(options.seconds, options.prior)
