#!/usr/bin/env python3
"""Small P48 seam/filter controls for Agent 108's unchanged exterior MDD.

This constructs one synthetic cut transition under the target G48 whose
coefficient trace has x[0]=4, x[24]=8, x[48]=4. Its exact target must be in
the full P48 image, and neither half may be in its separate P24 image.
The input and target cuts are deliberately correlated across the two laps.
They are not asserted reachable from the physical initial cut and are not
an exterior cycle or a candidate certificate.

A separate neutral-terminal fixture uses a carry word changed only in the
second lap. Its matching P48 filter must accept it; the original target E48
must reject it. This tests the matching full48 word and one second-lap
mismatch at phase31, without a whole-width search or a large frontier export.

The fixture arithmetic and packing below are independent of Agent 108's
Python oracle. A temporary C++ translation unit includes the unchanged
production source and exercises its exact Arena.image/predecessor/terminal
methods using history storage. Live collection and positive replay are
covered separately by Agent 108's live-selftest. No production source is
edited. Compilation and checks share an external wall budget; each child
has an address-space limit.

Run from the repository root:
  python3 -O calculation/agent-115/two_lap_mdd_controls.py --seconds 45 --memory-mib 1024
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "calculation/agent-108/exterior_mdd.cpp"
G24 = "110001001000110001001000"
E24 = "010100110100101011001011"
COLUMN = (
    4, 10, 3, 6, 12, 4, 11, 2, 4, 4, 8, 16,
    12, 2, 3, 6, 12, 4, 11, 2, 4, 11, 2, 4,
    8, 10, 3, 6, 12, 4, 11, 2, 4, 4, 8, 16,
    12, 2, 4, 8, 16, 12, 3, 6, 12, 3, 6, 12,
)


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def pack(bits, cut):
    low, high, partners = cut
    starts = [t for t, bit in enumerate(bits) if bit]
    require(starts and starts[0] == 0, "control packing requires an initial overflow")
    require(len(low) == len(high) == len(bits) and len(partners) == len(starts),
            "cut dimensions")
    result = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(bits)
        length = end - start
        lm = sum(low[t] << (t - start) for t in range(start, end))
        hm = sum(high[t] << (t - start) for t in range(start, end))
        result.append(lm + (hm << length) + (partners[i] << (2 * length)))
    return result


def fixture():
    bits = tuple(map(int, G24 * 2))
    period = len(bits)
    require(period == len(COLUMN) == 48 and all(1 <= x <= 18 for x in COLUMN),
            "positive coefficient column")
    high = tuple(x // 10 for x in COLUMN)
    partners = tuple(COLUMN[(t + 1) % period] - COLUMN[t] % 10
                     for t, bit in enumerate(bits) if bit)
    require(all(0 <= value <= 9 for value in partners), "source partner digits")
    source = (tuple(0 for _ in bits), high, partners)
    target = (high, tuple(0 for _ in bits),
              tuple(COLUMN[t] % 10 for t, bit in enumerate(bits) if bit))
    partner_index = 0
    for t, coefficient in enumerate(COLUMN):
        forward_carry, forward_digit = divmod(coefficient + source[0][t], 10)
        reverse_carry, reverse_digit = divmod(coefficient + target[1][t], 10)
        require(forward_carry == target[0][t] and reverse_carry == source[1][t],
                "independent column carry equation")
        other = reverse_digit
        if bits[t]:
            other = source[2][partner_index]
            require(reverse_digit == target[2][partner_index], "output partner equation")
            partner_index += 1
        require(forward_digit + other == COLUMN[(t + 1) % period],
                "independent temporal coefficient equation")
    require(COLUMN[0] != COLUMN[24], "control must fail the midpoint seam")
    require(source[1][:24] != source[1][24:] and target[0][:24] != target[0][24:],
            "control cuts must retain distinct laps")

    wanted_e = E24 * 2
    changed = list(wanted_e)
    changed[31] = str(1 - int(changed[31]))
    changed_e = "".join(changed)
    low = tuple(map(int, changed_e))
    terminal = (low, tuple(1 - x for x in low),
                tuple(9 * low[t] for t, bit in enumerate(bits) if bit))
    require(changed_e[:24] == wanted_e[:24] and changed_e[24:] != wanted_e[24:],
            "terminal control changes only the second lap")
    return bits, source, target, terminal, wanted_e, changed_e


HARNESS = r'''
#define main agent108_original_main
#include ENGINE_INCLUDE
#undef main

static void demand(bool condition,const char *detail){
  if(!condition)throw runtime_error(detail);
}
static bool contains(const Arena &a,Id root,const vector<int>& word){
  for(int symbol:word){
    if(root<2)return false;
    const auto &arcs=a.nodes[root].arcs;
    auto it=lower_bound(arcs.begin(),arcs.end(),Arc{symbol,0});
    if(it==arcs.end()||it->first!=symbol)return false;
    root=it->second;
  }
  return root==1;
}
int main(){
  try{
    string g,e,changed_e;cin>>g>>e>>changed_e;
    Pattern p=pattern(g);
    demand(p.P==48&&p.lengths.size()==16,"wrong P48 layout");
    vector<int> source(16),target(16),column(48),terminal(16);
    for(auto *word:{&source,&target,&column,&terminal})
      for(int &value:*word)demand(bool(cin>>value),"short control input");
    string extra;demand(!(cin>>extra),"extra control input");
    Arena a(p,"",250000,20000000,20);
    Id initial=a.singleton(source),image=a.image(initial,true);
    demand(contains(a,image,target),"P48 finite image excluded known transition");
    auto pred=a.predecessor(initial,target,true);
    demand(pred.first==source&&pred.second==column,"P48 reconstructed column mismatch");
    demand(column[0]==4&&column[24]==8,"midpoint seam control lost");

    Pattern half=pattern(g.substr(0,24));
    for(int start:{0,8}){
      Arena h(half,"",250000,20000000,20);
      vector<int> before(source.begin()+start,source.begin()+start+8);
      vector<int> after(target.begin()+start,target.begin()+start+8);
      Id out=h.image(h.singleton(before),true);
      demand(!contains(h,out,after),"nonclosing P24 half unexpectedly accepted");
    }

    Arena matching(p,changed_e,1000,10000,20);
    Id good=matching.singleton(terminal);
    demand(decimal(matching.nodes[good].accepts)=="1","matching full48 terminal filter rejected");
    demand(matching.accepted_word(good)==terminal,"terminal reconstruction mismatch");
    Arena original(p,e,1000,10000,20);
    Id bad=original.singleton(terminal);
    demand(decimal(original.nodes[bad].accepts)=="0","second-lap carry mismatch ignored");

    cout<<"{\"status\":\"PASSED\",\"storage_mode\":\"history\",\"period\":48,\"blocks\":16,"
        <<"\"finite_image_states\":\""<<decimal(a.nodes[image].count)<<"\","
        <<"\"finite_image_nodes\":"<<a.nodes.size()<<","
        <<"\"finite_image_operations\":"<<a.operations<<","
        <<"\"full_seam\":[4,8,4],\"separate_half_rejections\":2,"
        <<"\"terminal_matching_accepts\":1,\"terminal_second_lap_mismatch_accepts\":0}\n";
    return 0;
  }catch(const Limit &error){
    cerr<<"resource limit: "<<error.reason<<'\n';return 3;
  }catch(const exception &error){
    cerr<<error.what()<<'\n';return 2;
  }
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=45.0)
    parser.add_argument("--memory-mib", type=int, default=1024)
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or not 0 < args.seconds <= 60:
        parser.error("seconds must be positive, finite and at most 60")
    if not 512 <= args.memory_mib <= 2048:
        parser.error("memory-mib must be 512..2048")
    began = time.monotonic()
    deadline = began + args.seconds
    requested = args.memory_mib * 1024 * 1024

    def child_limit():
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        finite = [x for x in (requested, soft, hard) if x != resource.RLIM_INFINITY]
        resource.setrlimit(resource.RLIMIT_AS, (min(finite), hard))

    def run(command, **kwargs):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise subprocess.TimeoutExpired(command, args.seconds)
        return subprocess.run(command, text=True, capture_output=True,
                              timeout=remaining, preexec_fn=child_limit, **kwargs)

    try:
        bits, source, target, terminal, wanted_e, changed_e = fixture()
        data = "\n".join([
            G24 * 2, wanted_e, changed_e,
            " ".join(map(str, pack(bits, source))),
            " ".join(map(str, pack(bits, target))),
            " ".join(map(str, COLUMN)),
            " ".join(map(str, pack(bits, terminal))),
        ]) + "\n"
        with tempfile.TemporaryDirectory(prefix="p196-agent115-p48-control-") as temp:
            source_path = Path(temp) / "control.cpp"
            binary = Path(temp) / "control"
            source_path.write_text(HARNESS.replace("ENGINE_INCLUDE", json.dumps(str(ENGINE))))
            compilation = run([os.environ.get("CXX", "c++"), "-O2", "-std=c++17",
                               str(source_path), "-o", str(binary)])
            require(compilation.returncode == 0, "control compilation failed: " + compilation.stderr[-2000:])
            execution = run([str(binary)], input=data)
            if execution.returncode == 3 or execution.returncode < 0:
                result = {"status": "UNDECIDED", "reason": execution.stderr[-1000:]}
            else:
                require(execution.returncode == 0, "production seam control failed: " + execution.stderr[-2000:])
                result = json.loads(execution.stdout)
        result.update(classification="COMPUTED", engine_sha256=hashlib.sha256(ENGINE.read_bytes()).hexdigest(),
                      changed_terminal_phase=31, independent_column_equations=48,
                      scope="synthetic local P48 image and neutral-terminal controls; no physical B cycle claimed")
    except subprocess.TimeoutExpired:
        result = {"status": "UNDECIDED", "reason": "external wall deadline reached"}
    except (OSError, ValueError, MemoryError) as error:
        result = {"status": "FAILED", "reason": str(error)}
    result["seconds"] = round(time.monotonic() - began, 6)
    result["child_address_space_limit_mib"] = args.memory_mib
    result["child_peak_mib"] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss /
                                     (1024 * 1024 if sys.platform == "darwin" else 1024), 3)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
