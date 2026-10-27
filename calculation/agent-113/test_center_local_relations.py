#!/usr/bin/env python3
"""Crosscheck the independent invariant checker's arithmetic and tail cache.

The C++ checker is included only in a temporary test wrapper. Its complete
11-phase successor tuples are compared with the separately implemented
chronological Python transfer, including both terminal parities. Generated
sources, binaries and the small depth-one certificate stay in a temporary
directory. This finite regression does not establish the all-k invariant.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from center_reachability import CenterProblem, GEN, _Budget, _Limit

DRIVER = (10, '10100110011', '11100010000', '01000010000')
ORDER = ((2, 3, 4, 5, 6), (7, 8, 9, 10, 0, 1))

WRAPPER = r'''
#define main a113_checker_main
#include @CHECKER@
#undef main
#include <set>
using namespace independent;
using State = std::array<std::array<int,4>,phases>;

static std::array<Letter,2> letters_for(const Checker& c,const State& state) {
  std::array<Letter,2> letters;
  for(int s=0;s<2;++s) {
    letters[s].type=s; letters[s].z=state[c.order[s].back()][3];
    for(int t:c.order[s]) {
      letters[s].cfg.push_back(state[t][0]);
      letters[s].cfg.push_back(state[t][1]);
      letters[s].cfg.push_back(state[t][2]+1);
    }
  }
  return letters;
}

static void local_query(Checker& c,int width,int j,bool first,const State& input) {
  Profile p; if(width) p=c.profile(width,j); else p.fill(generic);
  auto letters=letters_for(c,input);
  std::array<std::vector<Choice>,2> choices;
  for(int s=0;s<2;++s) choices[s]=c.local(letters[s],p,first);
  std::set<State> out;
  for(const Choice& a:choices[0]) for(const Choice& b:choices[1]) {
    State state;
    std::array<const Choice*,2> chosen{&a,&b};
    for(int s=0;s<2;++s) {
      for(size_t i=0;i<c.order[s].size();++i) {
        const std::string& cfg=chosen[s]->cfg;
        state[c.order[s][i]]={static_cast<unsigned char>(cfg[3*i]),
          static_cast<unsigned char>(cfg[3*i+1]),
          static_cast<unsigned char>(cfg[3*i+2])-1,none};
      }
      state[c.order[s].back()][3]=chosen[1-s]->first;
    }
    out.insert(state);
  }
  for(auto kind:p) std::cout<<kind<<' ';
  std::cout<<out.size();
  for(const State& state:out) for(const auto& row:state)
    for(int x:row) std::cout<<' '<<x;
  std::cout<<'\n';
}

static void tail_query(Checker& c,int width,const State& input) {
  auto letters=letters_for(c,input);
  std::array<uint32_t,2> ids;
  for(int s=0;s<2;++s) {
    auto entry=c.labels.emplace(key(letters[s]),c.alphabet.size());
    if(entry.second) c.alphabet.push_back(letters[s]);
    ids[s]=entry.first->second;
  }
  const auto& a=c.tail_relation(ids[0],width);
  const auto& b=c.tail_relation(ids[1],width);
  bool ok=false;
  for(int first=0;first<coeffs;++first) for(int next:a[first])
    if(std::find(b[next].begin(),b[next].end(),first)!=b[next].end()) ok=true;
  std::cout<<(ok?1:0)<<'\n';
}

int main(int argc,char** argv) {
  try {
    if(argc!=4) throw std::invalid_argument("mode certificate seconds required");
    Options o; o.seconds=unsigned_number(argv[3]); o.operations=1000000000;
    o.memory_mib=2048; resources(o); Budget budget(o); Checker checker(budget);
    std::ifstream in(argv[2]); checker.read(in);
    std::string mode=argv[1]; int width,j=0,first=0;
    if(mode!="local" && mode!="tail") throw std::invalid_argument("unknown mode");
    while(std::cin>>width) {
      if(mode=="local") std::cin>>j>>first;
      State state;
      for(auto& row:state) for(int& x:row)
        if(!(std::cin>>x)) throw std::invalid_argument("truncated query");
      if(mode=="local") local_query(checker,width,j,first,state);
      else tail_query(checker,width,state);
    }
    alarm(0); return 0;
  } catch(const Limit& ex) {
    std::cerr<<"UNDECIDED: "<<ex.what()<<'\n'; return 3;
  } catch(const std::bad_alloc&) {
    std::cerr<<"UNDECIDED: memory_limit\n"; return 3;
  } catch(const std::exception& ex) {
    std::cerr<<ex.what()<<'\n'; return 1;
  }
}
'''


class Undecided(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run(command, seconds, data=None):
    try:
        result = subprocess.run(command, input=data, text=True, capture_output=True,
                                timeout=seconds+5)
    except subprocess.TimeoutExpired as exc:
        raise Undecided(f'timeout: {command[0]}') from exc
    if result.returncode == 3:
        raise Undecided(result.stderr[-300:] or result.stdout[-300:])
    require(result.returncode == 0,
            f'command failed ({result.returncode}): {command[0]}: {result.stderr[-500:]}')
    return result.stdout


def query_line(prefix, state):
    return ' '.join(map(str, [*prefix, *(x for row in state for x in row)]))+'\n'


def local_checks(problem, binary, certificate, seconds):
    budget = _Budget(50000, seconds)
    queries, expected, sizes = [], [], []
    front = {problem.start}
    for depth in range(6):
        following = set()
        for state in sorted(front):
            targets = set(problem._transfer(state, (GEN,)*11, depth == 0, budget))
            queries.append(query_line((0, depth, int(depth == 0)), state))
            expected.append(((GEN,)*11, targets))
            following.update(targets)
        front = following
        sizes.append(len(front))
    generic_queries = len(queries)
    require(sizes == [35, 83, 243, 563, 755, 755], 'independent generic fixtures changed')
    for width in range(1, 5):
        front = {problem.start}
        for j, profile in enumerate(problem._profiles(problem._lengths(width))):
            following = set()
            for state in sorted(front):
                targets = set(problem._transfer(state, profile, j == 0, budget))
                queries.append(query_line((width, j, int(j == 0)), state))
                expected.append((profile, targets))
                following.update(targets)
            front = following
        require(not front, f'unexpected finite positive width {width}')
    output = run([str(binary), 'local', str(certificate), str(seconds)], seconds, ''.join(queries))
    lines = output.splitlines()
    require(len(lines) == len(queries), 'wrong number of local results')
    matched = 0
    for i, (line, (profile, targets)) in enumerate(zip(lines, expected)):
        values = list(map(int, line.split()))
        require(len(values) >= 12 and tuple(values[:11]) == profile, f'profile mismatch at query {i}')
        count, raw = values[11], values[12:]
        require(len(raw) == count*44, f'malformed local result {i}')
        actual = {tuple(tuple(raw[pos+4*t:pos+4*t+4]) for t in range(11))
                  for pos in range(0, len(raw), 44)}
        require(len(actual) == count and actual == targets, f'complete successor mismatch at query {i}')
        matched += count
    print(json.dumps(dict(status='PASS', test='local_relations', generic_sizes=sizes,
                          generic_queries=generic_queries, tail_queries=len(queries)-generic_queries,
                          local_relation_calls=2*len(queries), matched_successor_states=matched),
                     sort_keys=True), flush=True)


def read_alphabet(text):
    tokens = iter(text.split())
    require(next(tokens) == 'A113REG1', 'wrong certificate format')
    require((int(next(tokens)), int(next(tokens))) == (10, 11), 'wrong base or period')
    require(tuple(next(tokens) for _ in range(3)) == DRIVER[1:], 'wrong certificate driver')
    require(int(next(tokens)) == 2, 'wrong number of segment types')
    count = int(next(tokens))
    for times in ORDER:
        require(int(next(tokens)) == len(times), 'wrong segment length')
        require(tuple(int(next(tokens)) for _ in times) == times, 'wrong chronology')
    letters = [[], []]
    for _ in range(count):
        kind, z = int(next(tokens)), int(next(tokens))
        require(kind in (0, 1), 'wrong symbol type')
        cfg = tuple(tuple(int(next(tokens)) for _ in range(3)) for _ in ORDER[kind])
        letters[kind].append((z, cfg))
    return letters


def tail_checks(problem, binary, certificate, seconds):
    budget = _Budget(50000, seconds)
    profiles = {w: list(problem._profiles(problem._lengths(w)))[int(w > 2):] for w in range(1, 5)}
    queries = [(1, problem.start), (2, problem.start)]
    front = {problem.start}
    for depth in range(1, 6):
        front = problem._advance(front, (GEN,)*11, depth == 1, budget)
        queries.extend((w, state) for w in (3, 4) for state in sorted(front))
    actual_count = len(queries)
    # These arbitrary cuts exercise acceptance of both parity tails; they are
    # deliberately not claimed to be reachable center-cycle cuts.
    for carry, digit in ((0, 0), (1, 9)):
        state = tuple((carry, carry, digit if problem.g[t] else -1,
                       2*digit if problem.v[t] else -1) for t in range(11))
        queries.extend((w, state) for w in (3, 4))
    letters = read_alphabet(certificate.read_text())
    for a in letters[0]:
        for b in letters[1]:
            state = [None]*11
            for kind, (z, cfg) in enumerate((a, b)):
                for phase, row in zip(ORDER[kind], cfg):
                    state[phase] = (*row, -1)
                state[ORDER[kind][-1]] = (*state[ORDER[kind][-1]][:3], z)
            queries.extend((w, tuple(state)) for w in (3, 4))
    data = ''.join(query_line((width,), state) for width, state in queries)
    output = run([str(binary), 'tail', str(certificate), str(seconds)], seconds, data)
    answers = list(map(int, output.split()))
    require(len(answers) == len(queries) and all(x in (0, 1) for x in answers), 'bad cached-tail results')
    cache = {}
    selected = {(w, a): 0 for w in (3, 4) for a in (0, 1)}
    pools = dict(selected)
    matched = 0
    for i, ((width, state), answer) in enumerate(zip(queries, answers)):
        if i >= actual_count:
            pools[(width, answer)] += 1
            if selected[(width, answer)] >= 30:
                continue
            selected[(width, answer)] += 1
        key = width, state
        if key not in cache:
            out = {state}
            for j, profile in enumerate(profiles[width]):
                out = problem._advance(out, profile, width <= 2 and j == 0, budget)
            cache[key] = bool(out)
        require(answer == cache[key], f'cached-tail composition mismatch at query {i}, width {width}')
        if i < actual_count:
            require(not answer, 'unexpected reachable positive terminal cut')
        matched += 1
    require(selected[(3, 1)] >= 2 and selected[(4, 1)] >= 2, 'missing positive parity controls')
    print(json.dumps(dict(status='PASS', test='cached_tail_relations', actual_queries=actual_count,
                          unique_oracle_cases=len(cache), total_matched=matched,
                          synthetic_class_counts={str(k): v for k, v in pools.items()},
                          checked_synthetic={str(k): v for k, v in selected.items()}),
                     sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--checker-source', type=Path,
                        default=Path(__file__).with_name('check_regular_invariant.cpp'))
    parser.add_argument('--cxx', default='g++')
    parser.add_argument('--seconds', type=int, default=120)
    args = parser.parse_args()
    require(1 <= args.seconds <= 1800, 'seconds must be in 1..1800')
    with tempfile.TemporaryDirectory(prefix='a113-local-relations-') as directory:
        directory = Path(directory)
        certificate = directory/'depth1.txt'
        command = [str(args.engine.resolve()), *map(str, DRIVER), '--text-depth', '1', '--depth', '1',
                   '--states', '1000000', '--edges', '20000000', '--ops', '1000000000',
                   '--seconds', str(args.seconds)]
        certificate.write_text(run(command, args.seconds))
        source, binary = directory/'probe.cpp', directory/'probe'
        source.write_text(WRAPPER.replace('@CHECKER@', json.dumps(str(args.checker_source.resolve()))))
        run([args.cxx, '-std=c++17', '-O2', str(source), '-o', str(binary)], 60)
        problem = CenterProblem(*DRIVER)
        local_checks(problem, binary, certificate, args.seconds)
        tail_checks(problem, binary, certificate, args.seconds)
    print('LOCAL RELATION TESTS PASSED; finite checks do not establish the all-k invariant')


if __name__ == '__main__':
    try:
        main()
    except (Undecided, _Limit, MemoryError, RecursionError) as exc:
        print(f'UNDECIDED: {exc}', file=sys.stderr)
        raise SystemExit(3)
    except (AssertionError, RuntimeError, ValueError, OSError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
