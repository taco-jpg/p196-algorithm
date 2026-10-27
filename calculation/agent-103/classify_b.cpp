// Agent 103: explicit terminal status around the existing exact B transfer.
// Arithmetic is reused, not copied; this adds bounded resource handling and
// complete accepting-stream enumeration. A negative requires an empty frontier.
#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#endif
#define main upstream_bauto_main
#include "../neutral_band/structure/bauto.cpp"
#undef main
#if defined(__GNUC__)
#pragma GCC diagnostic pop
#endif
#include <map>
#include <stdexcept>

int main(int argc, char **argv) {
  if (argc < 2 || argc > 4) {
    fprintf(stderr, "usage: classify_b G [state_cap=2000000] [seconds=30]\n");
    return 2;
  }
  std::string gs = argv[1];
  if (gs.empty() || gs.size() > 24 || gs.find_first_not_of("01") != std::string::npos) {
    fprintf(stderr, "unsupported overflow word\n"); return 2;
  }
  uint64_t cap = argc > 2 ? std::stoull(argv[2]) : 2000000;
  double seconds = argc > 3 ? std::stod(argv[3]) : 30.0;
  if (cap < 1 || seconds <= 0) return 2;
  b = 10; p = gs.size(); ydig = 4; g.clear(); Gidx.clear();
  for (int t=0; t<p; ++t) {
    g.push_back(gs[t]-'0'); if (g[t]) Gidx.push_back(t);
  }
  const int ng = Gidx.size();
  if (2*p+4*ng > 128) return 2;
  int ys[64]; std::fill(ys, ys+ng, 1);
  u64 hm=0; for(int t=0;t<p;++t) hm |= (u64)g[t]<<t;
  K128 start=pack(0,hm,ys,ng);
  std::unordered_set<K128,KH> seen;
  std::vector<K128> frontier{start}, next;
  std::map<std::string,int> accepts;
  uint64_t arcs=0; int depth=0; bool first=true;
  // The first-column marker is separate from regular states. Even if the
  // starting interface recurs later, its unrestricted transitions are visited.
  const auto began=std::chrono::steady_clock::now();
  std::string status="EXHAUSTED";
  while(!frontier.empty()) {
    next.clear();
    for(auto s:frontier) {
      u64 L,H; int Y[64]; unpack(s,L,H,Y,ng);
      if(accepting(L,H,Y,ng)) {
        std::string es;
        for(int t=0;t<p;++t) es += char('0'+((L>>t)&1));
        if(!accepts.count(es)) accepts[es]=depth;
      }
      transitions(L,H,Y,ng,first,[&](u64 L2,u64 H2,int *Y2,int *,int *) {
        ++arcs;
        K128 target=pack(L2,H2,Y2,ng);
        if(seen.insert(target).second) next.push_back(target);
      });
      if(seen.size()+1>cap) { status="CAPPED"; break; }
      if(std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()>seconds) {
        status="TIMEOUT"; break;
      }
    }
    if(status!="EXHAUSTED") break;
    frontier.swap(next); ++depth; first=false;
  }
  double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
  printf("{\"g\":\"%s\",\"status\":\"%s\",\"states\":%zu,\"depth\":%d,\"arcs\":%llu,\"seconds\":%.6f,\"accepted\":[",
         gs.c_str(),status.c_str(),seen.size()+1,depth,(unsigned long long)arcs,elapsed);
  bool comma=false;
  for(auto &kv:accepts) {
    printf("%s{\"e\":\"%s\",\"width\":%d}",comma?",":"",kv.first.c_str(),kv.second); comma=true;
  }
  printf("]}\n");
  return status=="EXHAUSTED" ? 0 : 3;
}
