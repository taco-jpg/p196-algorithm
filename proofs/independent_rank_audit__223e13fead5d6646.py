#!/usr/bin/env python3
"""Parse the transparent Lean rank table independently of its generator.

This is a source/data and exhaustive arithmetic audit, not a Lean build.
The separate kernel build remains the authority for the Lean proof terms.
"""

from hashlib import sha256
from pathlib import Path
import gzip
import json
import re
import struct
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parent / '2026-10-14-seven-step-extension-formal'
GRAPH = HERE.parent / '2026-10-14-seven-step-extension'
PREFIXES = ((4, 4, 0), (8, 8, 0), (16, 16, 0), (7, 14, 7),
            (15, 8, 15), (6, 14, 14), (13, 9, 9))
OVERFLOWS = (0, 0, 1, 0, 1, 0, 1)
V = 7 * 19**3


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def step(p, incoming):
    """Direct low/high recurrence transcribed from SixPrefix.step."""
    low, high = [], [0] * 6
    carry = 0
    for a in p:
        carry, digit = divmod(a + carry, 10)
        low.append(digit)
    carry = incoming
    for i in range(5, -1, -1):
        carry, high[i] = divmod(p[i] + carry, 10)
    if carry == 0:
        output = tuple(a + b for a, b in zip(low, high))
    else:
        output = (low[0] + 1,) + tuple(low[i] + high[i-1] for i in range(1, 6))
    return output, carry


def main():
    data_path = FORMAL / 'RankData.lean'
    data = data_path.read_text()
    # Parse each match definition rather than importing the generator.
    definitions = {}
    pattern = re.compile(r'^def (\w+) : ([^\n]+)\n((?:  \| [^\n]+\n)+)', re.M)
    for name, signature, body in pattern.findall(data):
        clauses = re.findall(r'^  \| (\d+|_) => (.+)$', body, re.M)
        assert clauses and clauses[-1][0] == '_'
        keys = [int(key) for key, _ in clauses[:-1]]
        assert keys == list(range(len(keys))), name
        assert name not in definitions
        definitions[name] = (signature, [value for _, value in clauses[:-1]], clauses[-1][1])
    assert set(definitions) == {'phasePrefix', 'phaseOverflow', 'rank'} | {
        name for name in definitions if re.fullmatch(r'(row|table|phase)\d+', name)}
    assert definitions['phasePrefix'][1] == [f'⟨{a}, {b}, {c}⟩' for a, b, c in PREFIXES]
    assert definitions['phasePrefix'][2] == '⟨4, 4, 0⟩'
    assert definitions['phaseOverflow'][1] == list(map(str, OVERFLOWS))
    assert definitions['phaseOverflow'][2] == '0'
    assert definitions['rank'][1] == [f'phase{i}' for i in range(7)]
    assert definitions['rank'][2] == 'fun _ _ _ => 0'
    for name, (_, values, default) in definitions.items():
        if re.fullmatch(r'row\d+', name):
            assert len(values) == 19 and default == '0'
            assert all(value.isdigit() for value in values)
        elif re.fullmatch(r'table\d+', name):
            assert len(values) == 19 and default == 'fun _ => 0'
            assert all(re.fullmatch(r'row\d+', value) and value in definitions for value in values)
        elif re.fullmatch(r'phase\d+', name):
            assert len(values) == 19 and default == 'fun _ _ => 0'
            assert all(re.fullmatch(r'table\d+', value) and value in definitions for value in values)

    def rank(phase, a, b, c):
        phase_name = definitions['rank'][1][phase]
        table_name = definitions[phase_name][1][a]
        row_name = definitions[table_name][1][b]
        return int(definitions[row_name][1][c])

    compressed = GRAPH / 'direct_six_graph.bin.gz'
    assert digest(compressed) == '6b9fc4d21f146b87e1204619511191074797a613f0fb0ddfe64f5dbdaaf124b4'
    binary = gzip.decompress(compressed.read_bytes())
    assert binary[:8] == b'P196DAG1'
    vertices, edge_count = struct.unpack_from('<II', binary, 8)
    assert vertices == V and edge_count == 61731
    assert len(binary) == 16 + 4*V + 9*edge_count
    ranks = struct.unpack_from(f'<{V}I', binary, 16)
    edges = [struct.unpack_from('<IIB', binary, 16 + 4*V + 9*i) for i in range(edge_count)]
    controls_path = GRAPH / 'independent_direct_controls.bin.gz'
    assert digest(controls_path) == 'c1649975b58cac1d279cf1004524f52a3855433c83c9aea9325565c26cd494f2'
    controls = gzip.decompress(controls_path.read_bytes())
    assert controls[:8] == b'P196INT1'
    assert struct.unpack_from('<I', controls, 8)[0] == 2*V
    assert len(controls) == 12 + 14*V
    reconstructed = []
    for vertex in range(V):
        phase, rest = divmod(vertex, 19**3)
        a, rest = divmod(rest, 19**2)
        b, c = divmod(rest, 19)
        assert rank(phase, a, b, c) == ranks[vertex]
        for incoming in (0, 1):
            p, overflow = step(PREFIXES[phase] + (a, b, c), incoming)
            saved = tuple(controls[12 + 7*(2*vertex+incoming):12 + 7*(2*vertex+incoming+1)])
            assert p + (overflow,) == saved
            # These checks rule out every default branch on every legal input,
            # including rejected controls, not just accepted graph edges.
            assert overflow in (0, 1) and all(0 <= x < 19 for x in p)
            target_phase = (phase + 1) % 7
            if p[:3] == PREFIXES[target_phase] and overflow == OVERFLOWS[phase]:
                target = target_phase * 19**3 + p[3]*19**2 + p[4]*19 + p[5]
                reconstructed.append((vertex, target, incoming))
                assert rank(target_phase, *p[3:]) < rank(phase, a, b, c)
    assert reconstructed == edges
    maxima = [max(ranks[t*19**3:(t+1)*19**3]) for t in range(7)]
    assert maxima == [26, 25, 24, 26, 25, 28, 27]

    checks, bounds = [], []
    for phase in range(7):
        source = (FORMAL / f'RankChecks{phase}.lean').read_text()
        found = re.findall(r'theorem check_(\d+)_(\d+) : ∀ b c : Fin 19, ∀ control : Bool,\n    EdgeGood (\d+) (\d+) b.val c.val control := by decide', source)
        assert [(int(p), int(a), int(pp), int(aa)) for p,a,pp,aa in found] == [
            (phase, a, phase, a) for a in range(19)]
        checks.extend((int(p), int(a)) for p,a,_,_ in found)
        found_bounds = re.findall(r'theorem bound_0_(\d+) : ∀ b c : Fin 19,\n    rank 0 (\d+) b.val c.val ≤ 26 := by decide', source)
        assert [(int(a),int(aa)) for a,aa in found_bounds] == ([(a,a) for a in range(19)] if phase == 0 else [])
        bounds.extend(int(a) for a,_ in found_bounds)
    assert checks == [(phase,a) for phase in range(7) for a in range(19)]
    assert bounds == list(range(19))
    certificate = (FORMAL / 'RankCertificate.lean').read_text()
    references = re.findall(r'exact check_(\d+)_(\d+) ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩', certificate)
    assert [(int(p),int(a)) for p,a in references] == checks
    assert re.findall(r'exact bound_0_(\d+) ⟨b, hb⟩ ⟨c, hc⟩', certificate) == list(map(str,range(19)))
    assert (FORMAL/'RankChecks.lean').read_text() == ''.join(f'import RankChecks{i}\n' for i in range(7))

    # A generator regression check is additional to the independent parser.
    with tempfile.TemporaryDirectory(prefix='p196-rank-generation-audit-') as tmp:
        proc = subprocess.run([sys.executable, str(FORMAL/'generate_rank_certificate.py'),
                               '--output', tmp], capture_output=True, text=True, check=True)
        generated = sorted(Path(tmp).glob('*.lean'))
        assert len(generated) == 10
        for path in generated:
            assert path.read_bytes() == (FORMAL/path.name).read_bytes(), path.name
        generation_message = proc.stdout.strip()

    paths = sorted(FORMAL.glob('*.lean')) + [FORMAL/name for name in
        ('generate_rank_certificate.py','verify_rank_certificate.py','check.py')]
    result = dict(status='PASS_SOURCE_TABLE_AND_FINITE_DOMAIN',
        vertices=V, controls=2*V, accepted_edges=edge_count,
        chunks=len(checks), phase0_bound_chunks=len(bounds),
        phase_maxima=maxima, every_legal_transition_stays_in_table_domain=True,
        generator_byte_agreement=True, generation_message=generation_message,
        graph_sha256=digest(compressed), literal_control_sha256=digest(controls_path),
        source_sha256={path.name:digest(path) for path in paths},
        scope='Independent source/data audit only. No Lean compiler invocation; kernel-build status is separately recorded by the formal contribution.')
    (HERE/'independent_rank_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'}))


if __name__ == '__main__':
    main()
