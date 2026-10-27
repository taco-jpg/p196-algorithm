// Agent 118: exact correlated segment frontiers as decision DAGs.
// The temporary header is generated from the pinned, guarded original source.
#define main original_center_main118
#include "cauto118_core.hpp"
#undef main
#include <deque>
#include <limits>

namespace MDD118 {
using Id = uint32_t;
using Arc = pair<uint32_t, Id>;
using U128 = unsigned __int128;
const U128 MAXCOUNT = ~U128(0);

struct Budget {
  uint64_t nodes = 1000000, operations = 200000000, used = 0;
  void tick(uint64_t n = 1) {
    if (n > operations || used > operations - n) undecided118("mdd_operation_cap");
    used += n;
  }
};

struct Node {
  int level;
  vector<Arc> arcs;
  U128 count;
  bool countExact;
};

string decimal(U128 n) {
  if (!n) return "0";
  string out;
  while (n) { out.push_back('0' + n % 10); n /= 10; }
  reverse(out.begin(), out.end()); return out;
}

struct Dag {
  int levels;
  Budget& budget;
  deque<Node> nodes;  // immutable nodes; push_back preserves references
  unordered_map<uint64_t, vector<Id>> unique;
  unordered_map<uint64_t, Id> unions;

  Dag(int n, Budget& b_) : levels(n), budget(b_) {
    nodes.push_back({-1, {}, 0, true});
    nodes.push_back({n, {}, 1, true});
  }
  void memoRoom(size_t size) {
    if (size > budget.nodes * 8) undecided118("mdd_memo_cap");
  }
  Id make(int level, vector<Arc> arcs) {
    budget.tick(arcs.size() + 1);
    arcs.erase(remove_if(arcs.begin(), arcs.end(), [](Arc x) { return x.second == 0; }), arcs.end());
    if (arcs.empty()) return 0;
    if (level < 0 || level >= levels) undecided118("mdd_bad_level");
    uint64_t hash = mix64(level);
    bool first = true; uint32_t prior = 0;
    U128 count = 0; bool exact = true;
    for (Arc a : arcs) {
      if ((!first && a.first <= prior) || a.second >= nodes.size() || nodes[a.second].level != level + 1)
        undecided118("mdd_bad_arc");
      first = false; prior = a.first;
      hash = mix64(hash ^ (uint64_t(a.first) << 32) ^ a.second);
      const Node& child = nodes[a.second];
      if (!child.countExact || count > MAXCOUNT - child.count) { count = MAXCOUNT; exact = false; }
      else count += child.count;
    }
    auto found = unique.find(hash);
    if (found != unique.end()) for (Id id : found->second)
      if (nodes[id].level == level && nodes[id].arcs == arcs) return id;
    if (nodes.size() >= budget.nodes || nodes.size() >= UINT32_MAX) undecided118("mdd_node_cap");
    Id id = nodes.size(); nodes.push_back({level, std::move(arcs), count, exact});
    unique[hash].push_back(id); return id;
  }
  Id unite(Id a, Id c) {
    budget.tick();
    if (!a) return c;
    if (!c || a == c) return a;
    if (a > c) swap(a, c);
    uint64_t key = (uint64_t(a) << 32) | c;
    auto known = unions.find(key); if (known != unions.end()) return known->second;
    const Node& x = nodes[a]; const Node& y = nodes[c];
    if (x.level != y.level || x.level == levels) undecided118("mdd_union_level");
    vector<Arc> out; size_t i = 0, j = 0;
    while (i < x.arcs.size() || j < y.arcs.size()) {
      budget.tick();
      if (j == y.arcs.size() || (i < x.arcs.size() && x.arcs[i].first < y.arcs[j].first)) out.push_back(x.arcs[i++]);
      else if (i == x.arcs.size() || y.arcs[j].first < x.arcs[i].first) out.push_back(y.arcs[j++]);
      else { out.push_back({x.arcs[i].first, unite(x.arcs[i].second, y.arcs[j].second)}); ++i; ++j; }
    }
    Id result = make(x.level, std::move(out));
    memoRoom(unions.size()); unions.emplace(key, result); return result;
  }
  Id singleton(const vector<uint32_t>& tuple) {
    if ((int)tuple.size() != levels) undecided118("mdd_tuple_width");
    Id root = 1;
    for (int level = levels - 1; level >= 0; --level) root = make(level, {{tuple[level], root}});
    return root;
  }
  void decodeRec(Id root, vector<uint32_t>& prefix, vector<uint32_t>& out) const {
    if (!root) return;
    if (root == 1) { out.insert(out.end(), prefix.begin(), prefix.end()); return; }
    for (Arc a : nodes[root].arcs) { prefix.push_back(a.first); decodeRec(a.second, prefix, out); prefix.pop_back(); }
  }
  vector<uint32_t> decode(Id root, uint64_t cap) const {
    const Node& node = nodes[root];
    if (!node.countExact || node.count > cap) undecided118("mdd_compare_decode_cap");
    vector<uint32_t> prefix, out; out.reserve((size_t)node.count * levels);
    decodeRec(root, prefix, out); return out;
  }
};

struct Image {
  Dag& dag; Fast& fast;
  int layer; bool generic;
  unordered_map<uint64_t, vector<OutE>> options;
  unordered_map<uint64_t, Id> memo;
  Image(Dag& d, Fast& f, int j, bool g_) : dag(d), fast(f), layer(j), generic(g_) {}

  const vector<OutE>& local(int segment, uint32_t lid) {
    uint64_t key = (uint64_t(segment) << 32) | lid;
    auto found = options.find(key); if (found != options.end()) return found->second;
    SigTab* signature = fast.sigFor(segment, layer, generic);
    if (lid >= signature->ent.size() || signature->ent[lid].start == UNSET) fast.fill(segment, signature, lid);
    Ent entry = signature->ent[lid];
    // Copy pool entries: later recursive fill calls can reallocate Fast pools.
    vector<OutE> copy;
    copy.reserve(entry.cnt);
    for (uint32_t i = 0; i < entry.cnt; ++i) copy.push_back(fast.sg[segment].pool[(size_t)entry.start + i]);
    dag.budget.tick(copy.size() + 1); dag.memoRoom(options.size());
    return options.emplace(key, std::move(copy)).first->second;
  }
  Id suffix(Id old, int required, int first) {
    dag.budget.tick();
    if (!old) return 0;
    if (old == 1) return required == first ? 1 : 0;
    uint64_t key = (uint64_t(old) << 16) | (uint64_t(required + 1) << 8) | uint64_t(first + 1);
    auto cached = memo.find(key); if (cached != memo.end()) return cached->second;
    const Node& input = dag.nodes[old]; int s = input.level;
    map<uint32_t, Id> arcs;
    for (Arc a : input.arcs) {
      const vector<OutE>& choices = local(s, a.first);
      for (const OutE& choice : choices) if (choice.c == required) {
        int low = s + 1 == dag.levels ? first : -1;
        int high = s + 1 == dag.levels ? first : 2 * b - 2;
        for (int next = low; next <= high; ++next) {
          Id child = suffix(a.second, next, first);
          if (!child) continue;
          uint32_t label = fast.getLid(s, choice.yid, next);
          auto known = arcs.find(label);
          if (known == arcs.end()) arcs.emplace(label, child);
          else known->second = dag.unite(known->second, child);
        }
      }
    }
    Id result = dag.make(s, vector<Arc>(arcs.begin(), arcs.end()));
    dag.memoRoom(memo.size()); memo.emplace(key, result); return result;
  }
  Id run(Id old) {
    Id result = 0;
    for (int first = -1; first <= 2 * b - 2; ++first) result = dag.unite(result, suffix(old, first, first));
    return result;
  }
};

struct Engine {
  Budget budget;
  Fast fast;
  unique_ptr<Dag> dag;
  bool compare = false, witness = false, verbose = true;
  int genericLimit = 120;
  uint64_t comparisons = 0;
  explicit Engine(long cap) : fast(cap) {}
  void init() {
    int Mbig = 2 * (genericLimit + 2 * P + 8);
    if (!setup_instance(Mbig)) undecided118("invalid_length_balance");
    if (nseg < 1 || nseg > MAXNS || noV) undecided118("mdd_requires_positive_trim_segments");
    fast.init(order); dag.reset(new Dag(nseg, budget));
  }
  void diagnostic(int j, Id root, const char* kind) {
    const Node& node = dag->nodes[root];
    printf("MDD_LAYER j=%d kind=%s tuples=%s count_exact=%d nodes=%zu ops=%llu\n", j, kind,
           decimal(node.count).c_str(), int(node.countExact), dag->nodes.size(), (unsigned long long)budget.used);
    fflush(stdout);
  }
  vector<uint32_t> sortedRows(const vector<uint32_t>& flat) {
    int n = dag->levels;
    vector<vector<uint32_t>> rows;
    for (size_t i = 0; i < flat.size(); i += n) rows.emplace_back(flat.begin() + i, flat.begin() + i + n);
    sort(rows.begin(), rows.end());
    vector<uint32_t> out; out.reserve(flat.size());
    for (auto& row : rows) out.insert(out.end(), row.begin(), row.end());
    return out;
  }
  Id step(Id old, int j, bool generic) {
    Id result = Image(*dag, fast, j, generic).run(old);
    if (compare) {
      vector<uint32_t> input = dag->decode(old, g_cap);
      StateSet output;
      if (!fast.step(input, j, generic, output)) undecided118("explicit_comparison_state_cap");
      if (sortedRows(output.data) != dag->decode(result, g_cap)) undecided118("MDD_EXPLICIT_FRONTIER_MISMATCH");
      ++comparisons;
    }
    return result;
  }
  void feasible(const string& pattern, int m0, const char* tag) {
    vector<vector<int>> centers;
    if (witness) get_witness(&fast, m0, centers);
    printf("%s b=%d e=%s g=%s v=%s m0=%d", tag, b, es_.c_str(), gs_.c_str(), pattern.c_str(), m0);
    for (size_t t = 0; t < centers.size(); ++t) {
      printf(" C%zu=[", t);
      for (size_t i = 0; i < centers[t].size(); ++i) printf("%s%d", i ? "," : "", centers[t][i]);
      printf("]");
    }
    printf("\n"); fflush(stdout);
  }
  void finite(const string& pattern, int low, int high) {
    int hits = 0;
    for (int m0 = low; m0 <= high; ++m0) {
      if (!setup_instance(m0)) continue;
      Id current = dag->singleton(fast.startState());
      for (int j = 0; current && j < Jall; ++j) {
        current = step(current, j, false);
        if (verbose) diagnostic(j + 1, current, "finite");
      }
      if (current) { ++hits; feasible(pattern, m0, "FEASIBLE"); }
    }
    printf("MDD_DONE status=%s scope=finite low=%d high=%d hits=%d nodes=%zu ops=%llu comparisons=%llu\n",
           hits ? "hit" : "none", low, high, hits, dag->nodes.size(), (unsigned long long)budget.used, (unsigned long long)comparisons);
  }
  void allLengths(const string& pattern) {
    vector<Id> generic{dag->singleton(fast.startState())};
    int jstar = -1, period = 0;
    for (int j = 0; j < genericLimit; ++j) {
      Id next = step(generic.back(), j, true);
      if (verbose) diagnostic(j + 1, next, "generic");
      if (!next) { jstar = j + 1; period = 1; generic.push_back(next); break; }
      for (int old = (int)generic.size() - 1; old >= 1; --old)
        if (generic[old] == next) { jstar = old; period = generic.size() - old; break; }
      if (jstar >= 0) break;
      generic.push_back(next);
    }
    if (jstar < 0) undecided118("mdd_generic_period_not_detected");
    int mlo = -1;
    for (int width = 1; width < 100000; ++width) {
      if (!setup_instance(width)) continue;
      int j0 = *min_element(J.begin(), J.end()) - 1;
      if (j0 >= jstar && width > 2 * P) { mlo = width; break; }
    }
    if (mlo < 1) undecided118("mdd_all_length_threshold_not_found");
    map<pair<int, int>, bool> memo;
    int hits = 0, classes = 0, tails = 0;
    for (int width = 1; width < mlo + 2 * period; ++width) {
      if (!setup_instance(width)) continue;
      if (width >= mlo) ++classes;
      int j0 = *min_element(J.begin(), J.end()) - 1;
      int index = j0 < jstar ? j0 : jstar + (j0 - jstar) % period;
      pair<int, int> key = {width & 1, index};
      auto known = memo.find(key); bool hit;
      if (known != memo.end()) hit = known->second;
      else {
        ++tails; Id current = generic[index];
        for (int j = j0; current && j < Jall; ++j) current = step(current, j, false);
        hit = current != 0; memo.emplace(key, hit);
      }
      if (hit) { ++hits; feasible(pattern, width, width < mlo ? "FEASIBLE" : "FEASIBLE_CLASS"); }
    }
    printf("MDD_DONE status=%s scope=allm jstar=%d period=%d mlo=%d classes=%d hits=%d tails=%d nodes=%zu ops=%llu comparisons=%llu\n",
           hits ? "hit" : "none", jstar, period, mlo, classes, hits, tails, dag->nodes.size(), (unsigned long long)budget.used, (unsigned long long)comparisons);
  }
};

int run(int argc, char** argv) {
  if (argc < 8) undecided118("usage_center_mdd_b_e_g_mlo_mhi_v_pattern");
  vector<string> forwarded;
  for (int i = 0; i < min(argc, 6); ++i) forwarded.emplace_back(argv[i]);
  Budget budget; bool compare = false, witness = false, allm = false, verbose = true;
  int layers = 120; string pattern; long cap = 1000000;
  for (int i = 6; i < argc; ++i) {
    string flag = argv[i];
    auto value = [&]() -> string { if (++i >= argc) undecided118("missing_mdd_option_value"); return argv[i]; };
    if (flag == "-nodes") { auto x = number118(value()); if (x < 3 || x > 100000000) undecided118("unsupported_mdd_node_cap"); budget.nodes = x; }
    else if (flag == "-ops") { auto x = number118(value()); if (x < 1) undecided118("unsupported_mdd_operation_cap"); budget.operations = x; }
    else if (flag == "-layers") { auto x = number118(value()); if (x < 1 || x > 10000) undecided118("unsupported_generic_layer_limit"); layers = x; }
    else if (flag == "--compare") compare = true;
    else if (flag == "-quiet") verbose = false;
    else if (flag == "-v") { pattern = value(); forwarded.push_back(flag); forwarded.push_back(pattern); }
    else if (flag == "-cap") { string val = value(); cap = number118(val); forwarded.push_back(flag); forwarded.push_back(val); }
    else if (flag == "-w") { witness = true; forwarded.push_back(flag); }
    else if (flag == "-allm") { allm = true; forwarded.push_back(flag); }
    else undecided118("unsupported_mdd_option");
  }
  vector<char*> cargs; for (string& arg : forwarded) cargs.push_back(&arg[0]);
  arguments118(cargs.size(), cargs.data());
  b = number118(argv[1]); es_ = argv[2]; gs_ = argv[3]; P = es_.size();
  e.clear(); g.clear(); v.clear();
  for (int t = 0; t < P; ++t) { e.push_back(es_[t] - '0'); g.push_back(gs_[t] - '0'); v.push_back(pattern[t] - '0'); }
  g_cap = cap; g_wit = witness; g_wlegacy = false;
  Engine engine(cap); engine.budget = budget; engine.compare = compare; engine.witness = witness;
  engine.genericLimit = layers; engine.verbose = verbose; engine.init();
  if (allm) engine.allLengths(pattern);
  else engine.finite(pattern, number118(argv[4]), number118(argv[5]));
  return 0;
}
}  // namespace MDD118

int main(int argc, char** argv) {
  try { return MDD118::run(argc, argv); }
  catch (const exception& error) { fprintf(stderr, "UNDECIDED %s\n", error.what()); return 2; }
  catch (...) { fprintf(stderr, "UNDECIDED unexpected_mdd_exception\n"); return 2; }
}
