// Agent 118: exact regular languages of correlated, cyclic segment frontiers.
// P=24 supplies THREE TYPES of unchanged local tables.  The accepted words have
// arbitrarily many ABC blocks; occurrences of a type need not choose equal lids.
// A label (type,lid) retains the entire local configuration and outgoing Z value.
#define main original_center_main118
#include "cauto118_core.hpp"
#undef main
#include <array>
#include <deque>
#include <limits>

namespace REG118 {
using Id = uint32_t;
using Label = uint64_t;
using Arc = pair<Label, Id>;
using U128 = unsigned __int128;
constexpr Id DEAD = UINT32_MAX;
constexpr U128 MAXCOUNT = ~U128(0);

struct Budget {
  uint64_t states = 200000, edges = 3000000, operations = 100000000;
  uint64_t used = 0, peakStates = 0, peakEdges = 0;
  void tick(uint64_t n = 1) {
    if (n > operations || used > operations - n) undecided118("regular_operation_cap");
    used += n;
  }
  void state(size_t n) {
    tick();
    if (n > states || n >= DEAD) undecided118("regular_state_cap");
    peakStates = max(peakStates, uint64_t(n));
  }
  void edge(uint64_t n) {
    tick();
    if (n > edges) undecided118("regular_edge_cap");
    peakEdges = max(peakEdges, n);
  }
};

struct State { bool accept = false; vector<Arc> arcs; };
struct DFA { vector<State> q; Id start = 0; };
struct NFA { vector<State> q; vector<Id> starts; };
template<class T> struct VectorHash {
  size_t operator()(const vector<T>& x) const {
    uint64_t h = 0x9e3779b97f4a7c15ULL;
    for (T a : x) h = mix64(h ^ uint64_t(a));
    return h;
  }
};

Label label(int type, Id lid) {
  if (type < 0 || type >= 3) undecided118("regular_bad_type");
  return (uint64_t(type) << 32) | lid;
}
int typeOf(Label a) {
  if ((a >> 32) >= 3) undecided118("regular_bad_label");
  return a >> 32;
}
Id lidOf(Label a) { return uint32_t(a); }
uint64_t edgeCount(const vector<State>& q) {
  uint64_t n = 0; for (const State& s : q) n += s.arcs.size(); return n;
}
DFA emptyDfa(Budget& b_) { b_.state(1); DFA out; out.q.emplace_back(); return out; }

vector<uint8_t> coreachable(const vector<State>& q, Budget& budget) {
  vector<vector<Id>> reverseEdges(q.size());
  vector<uint8_t> live(q.size(), 0); vector<Id> queue;
  for (size_t i = 0; i < q.size(); ++i) {
    budget.tick();
    if (q[i].accept) { live[i] = 1; queue.push_back(i); }
    for (Arc a : q[i].arcs) {
      budget.tick();
      if (a.second >= q.size()) undecided118("regular_bad_target");
      reverseEdges[a.second].push_back(i);
    }
  }
  for (size_t k = 0; k < queue.size(); ++k) for (Id p : reverseEdges[queue[k]]) {
    budget.tick();
    if (!live[p]) { live[p] = 1; queue.push_back(p); }
  }
  return live;
}

// Only states without an actual path to acceptance are removed. Nonaccepting live
// states are NOT treated as the rejecting sink during partition refinement.
NFA trimNfa(const NFA& in, Budget& budget) {
  vector<uint8_t> live = coreachable(in.q, budget);
  vector<Id> renumber(in.q.size(), DEAD); NFA out;
  for (size_t i = 0; i < in.q.size(); ++i) if (live[i]) {
    budget.state(out.q.size() + 1); renumber[i] = out.q.size();
    out.q.push_back({in.q[i].accept, {}});
  }
  for (Id q : in.starts) {
    if (q >= in.q.size()) undecided118("regular_bad_start");
    if (live[q]) out.starts.push_back(renumber[q]);
  }
  uint64_t edges = 0;
  for (size_t i = 0; i < in.q.size(); ++i) if (live[i])
    for (Arc a : in.q[i].arcs) if (live[a.second]) {
      budget.edge(++edges); out.q[renumber[i]].arcs.push_back({a.first, renumber[a.second]});
    }
  return out;
}

DFA trimDfa(const DFA& in, Budget& budget) {
  if (in.q.empty() || in.start >= in.q.size()) undecided118("regular_bad_dfa_start");
  vector<uint8_t> live = coreachable(in.q, budget);
  if (!live[in.start]) return emptyDfa(budget);
  vector<Id> renumber(in.q.size(), DEAD), queue{in.start};
  renumber[in.start] = 0; DFA out; budget.state(1);
  out.q.push_back({in.q[in.start].accept, {}}); uint64_t edges = 0;
  for (size_t k = 0; k < queue.size(); ++k) {
    Id old = queue[k]; vector<Arc> arcs;
    for (Arc a : in.q[old].arcs) if (live[a.second]) {
      if (renumber[a.second] == DEAD) {
        budget.state(out.q.size() + 1); renumber[a.second] = out.q.size();
        queue.push_back(a.second); out.q.push_back({in.q[a.second].accept, {}});
      }
      budget.edge(++edges); arcs.push_back({a.first, renumber[a.second]});
    }
    out.q[k].arcs = std::move(arcs);
  }
  return out;
}

// Verify the subset construction independently from its map-of-vectors builder.
// Every start, accepting flag, label, and complete target union is checked.
void verifySubsets(const NFA& in, const DFA& out,
                   const vector<vector<Id>>& subsets, Budget& budget) {
  if (subsets.size() != out.q.size() || out.start != 0)
    undecided118("regular_subset_shape_mismatch");
  vector<Id> initial = in.starts;
  sort(initial.begin(), initial.end()); initial.erase(unique(initial.begin(), initial.end()), initial.end());
  if (subsets[0] != initial) undecided118("regular_subset_start_mismatch");
  for (size_t i = 0; i < subsets.size(); ++i) {
    bool accepting = false; vector<Arc> all;
    for (Id q : subsets[i]) {
      budget.tick();
      if (q >= in.q.size()) undecided118("regular_subset_member_mismatch");
      accepting = accepting || in.q[q].accept;
      all.insert(all.end(), in.q[q].arcs.begin(), in.q[q].arcs.end());
      budget.tick(in.q[q].arcs.size());
    }
    if (accepting != out.q[i].accept) undecided118("regular_subset_accept_mismatch");
    sort(all.begin(), all.end()); all.erase(unique(all.begin(), all.end()), all.end());
    size_t arc = 0;
    for (size_t k = 0; k < all.size();) {
      Label a = all[k].first; vector<Id> targets;
      while (k < all.size() && all[k].first == a) { targets.push_back(all[k++].second); budget.tick(); }
      if (arc >= out.q[i].arcs.size() || out.q[i].arcs[arc].first != a)
        undecided118("regular_subset_label_mismatch");
      Id target = out.q[i].arcs[arc++].second;
      if (target >= subsets.size() || subsets[target] != targets)
        undecided118("regular_subset_target_mismatch");
    }
    if (arc != out.q[i].arcs.size()) undecided118("regular_subset_extra_arc");
  }
}

DFA determinize(const NFA& in, Budget& budget) {
  if (in.starts.empty()) return emptyDfa(budget);
  DFA out; vector<vector<Id>> subsets;
  unordered_map<vector<Id>, Id, VectorHash<Id>> known;
  auto intern = [&](vector<Id> set) -> Id {
    budget.tick(set.size() + 1);
    sort(set.begin(), set.end()); set.erase(unique(set.begin(), set.end()), set.end());
    if (set.empty()) undecided118("regular_empty_subset_edge");
    auto it = known.find(set); if (it != known.end()) return it->second;
    budget.state(out.q.size() + 1); Id id = out.q.size(); bool accepting = false;
    for (Id q : set) {
      if (q >= in.q.size()) undecided118("regular_bad_subset_member");
      accepting = accepting || in.q[q].accept;
    }
    out.q.push_back({accepting, {}}); subsets.push_back(set); known.emplace(std::move(set), id);
    return id;
  };
  out.start = intern(in.starts); uint64_t edges = 0;
  for (size_t i = 0; i < out.q.size(); ++i) {
    // intern() can reallocate both vectors; retain no references across it.
    const vector<Id> input = subsets[i]; map<Label, vector<Id>> moves;
    for (Id q : input) for (Arc a : in.q[q].arcs) { budget.tick(); moves[a.first].push_back(a.second); }
    vector<Arc> arcs;
    for (auto& move : moves) {
      Id target = intern(std::move(move.second)); budget.edge(++edges);
      arcs.push_back({move.first, target});
    }
    out.q[i].arcs = std::move(arcs);
  }
  verifySubsets(in, out, subsets, budget);
  return out;
}

DFA minimize(const DFA& input, Budget& budget) {
  DFA in = trimDfa(input, budget);
  vector<Id> classes(in.q.size()); bool yes = false, no = false;
  for (const State& q : in.q) { yes = yes || q.accept; no = no || !q.accept; }
  Id nclass = yes && no ? 2 : 1;
  for (size_t i = 0; i < in.q.size(); ++i) classes[i] = yes && no && in.q[i].accept ? 1 : 0;
  while (true) {
    unordered_map<vector<uint64_t>, Id, VectorHash<uint64_t>> signatures;
    vector<Id> next(in.q.size());
    for (size_t i = 0; i < in.q.size(); ++i) {
      // Including the previous block makes refinement monotone.  Sparse absence
      // denotes the true dead sink; every live transition remains in the key.
      vector<uint64_t> key{classes[i], uint64_t(in.q[i].accept)};
      for (Arc a : in.q[i].arcs) { budget.tick(); key.push_back(a.first); key.push_back(classes[a.second]); }
      budget.tick(); auto found = signatures.find(key);
      if (found == signatures.end()) {
        budget.state(signatures.size() + 1); Id id = signatures.size();
        signatures.emplace(std::move(key), id); next[i] = id;
      } else next[i] = found->second;
    }
    Id count = signatures.size();
    if (count < nclass) undecided118("regular_nonmonotone_refinement");
    classes.swap(next);
    if (count == nclass) break;
    nclass = count;
  }
  vector<Id> representative(nclass, DEAD); DFA quotient; quotient.q.resize(nclass);
  budget.state(nclass); uint64_t edges = 0;
  for (size_t i = 0; i < in.q.size(); ++i) if (representative[classes[i]] == DEAD) {
    representative[classes[i]] = i; State& q = quotient.q[classes[i]];
    q.accept = in.q[i].accept;
    for (Arc a : in.q[i].arcs) { budget.edge(++edges); q.arcs.push_back({a.first, classes[a.second]}); }
  }
  quotient.start = classes[in.start];
  // Exact quotient homomorphism, including absent transitions.  This verifies
  // language preservation even if a future change makes refinement nonminimal.
  for (size_t i = 0; i < in.q.size(); ++i) {
    budget.tick(); const State& x = in.q[i]; const State& y = quotient.q[classes[i]];
    if (x.accept != y.accept || x.arcs.size() != y.arcs.size())
      undecided118("regular_quotient_shape_mismatch");
    for (size_t k = 0; k < x.arcs.size(); ++k) {
      budget.tick();
      if (x.arcs[k].first != y.arcs[k].first || classes[x.arcs[k].second] != y.arcs[k].second)
        undecided118("regular_quotient_target_mismatch");
    }
  }
  return trimDfa(quotient, budget);  // sorted-label BFS gives a canonical start
}

bool equivalent(const DFA& a, const DFA& c, Budget& budget,
                vector<Label>& difference, bool& acceptsLeft) {
  vector<pair<Id, Id>> pending; unordered_set<uint64_t> seen;
  vector<Id> parents; vector<Label> incoming;
  auto add = [&](Id x, Id y, Id parent, Label letter) {
    uint64_t key = (uint64_t(x) << 32) | y;
    if (seen.insert(key).second) {
      budget.state(pending.size() + 1); pending.push_back({x, y});
      parents.push_back(parent); incoming.push_back(letter);
    }
  };
  difference.clear(); add(a.start, c.start, DEAD, 0); const vector<Arc> empty;
  for (size_t k = 0; k < pending.size(); ++k) {
    budget.tick(); Id x = pending[k].first, y = pending[k].second;
    if ((x != DEAD && a.q[x].accept) != (y != DEAD && c.q[y].accept)) {
      acceptsLeft = x != DEAD && a.q[x].accept;
      for (Id p = k; parents[p] != DEAD; p = parents[p]) difference.push_back(incoming[p]);
      reverse(difference.begin(), difference.end()); return false;
    }
    const vector<Arc>& left = x == DEAD ? empty : a.q[x].arcs;
    const vector<Arc>& right = y == DEAD ? empty : c.q[y].arcs;
    size_t i = 0, j = 0;
    while (i < left.size() || j < right.size()) {
      budget.tick();
      if (j == right.size() || (i < left.size() && left[i].first < right[j].first)) {
        add(left[i].second, DEAD, k, left[i].first); ++i;
      } else if (i == left.size() || right[j].first < left[i].first) {
        add(DEAD, right[j].second, k, right[j].first); ++j;
      } else { add(left[i].second, right[j].second, k, left[i].first); ++i; ++j; }
    }
  }
  return true;
}

struct ImageStats { size_t nfa = 0, live = 0, dfaRaw = 0; uint64_t nfaEdges = 0; };
struct Product { Id old; int required, first; };
struct Image {
  Fast& fast; Budget& budget; const DFA& input; int layer; bool generic, prune;
  unordered_map<Label, vector<OutE>> localCache;
  Image(Fast& f, Budget& b_, const DFA& d, int j, bool g_, bool p)
    : fast(f), budget(b_), input(d), layer(j), generic(g_), prune(p) {}
  const vector<OutE>& local(int type, Id lid) {
    Label key = label(type, lid); auto found = localCache.find(key);
    if (found != localCache.end()) return found->second;
    if (lid >= fast.sg[type].lidInfo.size()) undecided118("regular_unknown_local_id");
    SigTab* sig = fast.sigFor(type, layer, generic);
    if (lid >= sig->ent.size() || sig->ent[lid].start == UNSET) { budget.tick(); fast.fill(type, sig, lid); }
    Ent entry = sig->ent[lid]; const SegState& s = fast.sg[type];
    if (s.cfg.size() > budget.states || s.lidInfo.size() > budget.states)
      undecided118("regular_local_state_cap");
    if (s.pool.size() > budget.edges) undecided118("regular_local_pool_cap");
    if (uint64_t(entry.start) + entry.cnt > s.pool.size()) undecided118("regular_bad_local_entry");
    budget.tick(uint64_t(entry.cnt) + 1); vector<OutE> copy;
    copy.reserve(entry.cnt);
    for (uint32_t i = 0; i < entry.cnt; ++i) copy.push_back(s.pool[size_t(entry.start) + i]);
    return localCache.emplace(key, std::move(copy)).first->second;
  }
  DFA run(ImageStats& stats) {
    if (input.q[input.start].accept) undecided118("regular_empty_input_word");
    NFA nfa; vector<Product> products; unordered_map<uint64_t, Id> known;
    vector<uint32_t> carryMasks(input.q.size(), UINT32_MAX);
    auto possible = [&](Id old, int required, int first) -> bool {
      if (!prune) return true;
      if (input.q[old].accept && required == first) return true;
      if (carryMasks[old] == UINT32_MAX) {
        uint32_t mask = 0;
        for (Arc a : input.q[old].arcs) for (OutE choice : local(typeOf(a.first), lidOf(a.first))) {
          budget.tick();
          if (choice.c < -1 || choice.c > 18) undecided118("regular_local_carry_range");
          mask |= uint32_t(1) << (choice.c + 1);
        }
        carryMasks[old] = mask;
      }
      return carryMasks[old] & (uint32_t(1) << (required + 1));
    };
    auto intern = [&](Id old, int required, int first) -> Id {
      budget.tick();
      if (old >= input.q.size() || required < -1 || required > 2 * b - 2 || first < -1 || first > 2 * b - 2)
        undecided118("regular_bad_product_state");
      uint64_t key = (uint64_t(old) << 16) | (uint64_t(required + 1) << 8) | uint64_t(first + 1);
      auto found = known.find(key); if (found != known.end()) return found->second;
      budget.state(nfa.q.size() + 1); Id id = nfa.q.size(); known.emplace(key, id);
      products.push_back({old, required, first});
      nfa.q.push_back({input.q[old].accept && required == first, {}}); return id;
    };
    for (int first = -1; first <= 2 * b - 2; ++first) if (possible(input.start, first, first))
      nfa.starts.push_back(intern(input.start, first, first));
    uint64_t edges = 0;
    for (size_t k = 0; k < nfa.q.size(); ++k) {
      Product p = products[k]; vector<Arc> arcs;
      for (Arc a : input.q[p.old].arcs) {
        budget.tick(); int type = typeOf(a.first);
        const vector<OutE>& choices = local(type, lidOf(a.first));
        for (OutE choice : choices) if (choice.c == p.required) {
          // Every edge guesses freely, INCLUDING edges reaching an accepting
          // ABC boundary.  Only stopping requires required==first.  Forcing
          // closure at intermediate C edges would lose genuine subharmonics.
          for (int next = -1; next <= 2 * b - 2; ++next) {
            budget.tick();
            // Exact local dead-state elimination: a nonaccepting product state
            // with no outgoing local option cannot lie on any accepted path.
            // Accepting states may still continue with a nonclosing carry.
            if (!possible(a.second, next, p.first)) continue;
            Id target = intern(a.second, next, p.first);
            Id lid = fast.getLid(type, choice.yid, next);
            if (fast.sg[type].lidInfo.size() > budget.states) undecided118("regular_local_state_cap");
            budget.edge(++edges); arcs.push_back({label(type, lid), target});
          }
        }
      }
      sort(arcs.begin(), arcs.end()); arcs.erase(unique(arcs.begin(), arcs.end()), arcs.end());
      nfa.q[k].arcs = std::move(arcs);
    }
    stats.nfa = nfa.q.size(); stats.nfaEdges = edgeCount(nfa.q);
    NFA live = trimNfa(nfa, budget); stats.live = live.q.size();
    // Release product storage before determinization, which can be the largest
    // stage.  The local ID/configuration pools remain append-only throughout.
    nfa = NFA(); products.clear(); products.shrink_to_fit(); known.clear(); known.rehash(0);
    DFA dfa = determinize(live, budget); stats.dfaRaw = dfa.q.size();
    return minimize(dfa, budget);
  }
};

struct Count { U128 value = 0; bool exact = true; };
void plus(Count& to, const Count& from) {
  if (!to.exact || !from.exact || to.value > MAXCOUNT - from.value) { to.value = MAXCOUNT; to.exact = false; }
  else to.value += from.value;
}
string decimal(U128 n) {
  if (!n) return "0"; string out;
  while (n) { out.push_back('0' + n % 10); n /= 10; }
  reverse(out.begin(), out.end()); return out;
}
array<Count, 3> counts(const DFA& dfa, Budget& budget) {
  vector<Count> current(dfa.q.size()); current[dfa.start].value = 1;
  array<Count, 3> result;
  for (int len = 1; len <= 9; ++len) {
    vector<Count> next(dfa.q.size());
    for (size_t q = 0; q < dfa.q.size(); ++q) if (current[q].value)
      for (Arc a : dfa.q[q].arcs) { budget.tick(); plus(next[a.second], current[q]); }
    current.swap(next);
    if (len % 3 == 0) for (size_t q = 0; q < dfa.q.size(); ++q) if (dfa.q[q].accept) plus(result[len / 3 - 1], current[q]);
  }
  return result;
}

using Row = array<Id, 3>;
void decodeVisit(const DFA& dfa, Id q, int depth, Row& prefix,
                 const vector<vector<Count>>& suffix, vector<Row>& rows, Budget& budget) {
  if (depth == 3) { if (dfa.q[q].accept) rows.push_back(prefix); return; }
  for (Arc a : dfa.q[q].arcs) if (suffix[2 - depth][a.second].value) {
    budget.tick();
    if (typeOf(a.first) != depth) undecided118("regular_phase_order_mismatch");
    prefix[depth] = lidOf(a.first); decodeVisit(dfa, a.second, depth + 1, prefix, suffix, rows, budget);
  }
}
vector<Row> decodeThree(const DFA& dfa, uint64_t cap, Budget& budget) {
  vector<vector<Count>> suffix(4, vector<Count>(dfa.q.size()));
  for (size_t q = 0; q < dfa.q.size(); ++q) suffix[0][q].value = dfa.q[q].accept;
  for (int len = 1; len <= 3; ++len) for (size_t q = 0; q < dfa.q.size(); ++q)
    for (Arc a : dfa.q[q].arcs) { budget.tick(); plus(suffix[len][q], suffix[len - 1][a.second]); }
  Count count = suffix[3][dfa.start];
  if (!count.exact || count.value > cap) undecided118("regular_comparison_decode_cap");
  vector<Row> rows; rows.reserve(size_t(count.value)); Row prefix{};
  decodeVisit(dfa, dfa.start, 0, prefix, suffix, rows, budget);
  if (rows.size() != count.value) undecided118("regular_decode_count_mismatch");
  return rows;
}

struct Engine {
  Budget budget; Fast fast; int layers = 7; bool compare = false, prune = true;
  uint64_t comparisons = 0, compareCap = 1000000;
  vector<vector<int>> typeTimes;
  Engine() : fast(1000000) {}
  void init() {
    b = 10; P = 24; es_ = "101010010101101010010101"; gs_ = "100010001000100010001000";
    const string vs = "000010000000100000001000";
    e.clear(); g.clear(); v.clear();
    for (char x : es_) e.push_back(x - '0');
    for (char x : gs_) g.push_back(x - '0');
    for (char x : vs) v.push_back(x - '0');
    if (!setup_instance(2 * (layers + 8)) || nseg != 3 || noV) undecided118("regular_driver_setup");
    typeTimes = order;
    for (int s = 0; s < 3; ++s) {
      if (order[s].size() != 8) undecided118("regular_type_length");
      for (int k = 0; k < 8; ++k) if (order[s][k] != (8 * s + 5 + k) % 24)
        undecided118("regular_type_alignment");
    }
    fast.cap = compareCap; g_cap = compareCap; fast.init(order);
  }
  DFA initial() {
    vector<Id> local = fast.startState(); DFA out; budget.state(4); out.q.resize(4);
    out.q[0].arcs = {{label(0, local[0]), 1}};
    out.q[1].arcs = {{label(1, local[1]), 2}};
    out.q[2].arcs = {{label(2, local[2]), 3}};
    out.q[3].accept = true; out.q[3].arcs = out.q[0].arcs;
    budget.edge(4); return out;  // (sA sB sC)^+, never the empty word
  }
  void compareStep(const DFA& in, const DFA& out, int j, bool generic) {
    vector<Row> before = decodeThree(in, compareCap, budget);
    vector<Row> after = decodeThree(out, compareCap, budget);
    vector<Id> flat; flat.reserve(before.size() * 3);
    for (const Row& row : before) flat.insert(flat.end(), row.begin(), row.end());
    StateSet explicitOut;
    if (!fast.step(flat, j, generic, explicitOut)) undecided118("regular_explicit_comparison_cap");
    budget.tick(explicitOut.data.size() + flat.size() + 1);
    vector<Row> expected; expected.reserve(explicitOut.n);
    for (size_t i = 0; i < explicitOut.data.size(); i += 3)
      expected.push_back({explicitOut.data[i], explicitOut.data[i + 1], explicitOut.data[i + 2]});
    sort(expected.begin(), expected.end());
    if (expected != after) undecided118("REGULAR_EXPLICIT_FRONTIER_MISMATCH");
    ++comparisons;
    printf("REG_COMPARE j=%d generic=%d input=%zu output=%zu comparisons=%llu\n", j, int(generic),
           before.size(), after.size(), (unsigned long long)comparisons); fflush(stdout);
  }
  DFA step(const DFA& in, int j, bool generic, ImageStats& stats) {
    DFA out = Image(fast, budget, in, j, generic, prune).run(stats);
    if (compare) compareStep(in, out, j, generic);
    return out;
  }
  void diagnostic(int j, const DFA& dfa, const ImageStats& stats) {
    auto n = counts(dfa, budget);
    printf("REG_LAYER j=%d nfa=%zu nfa_live=%zu nfa_edges=%llu dfa_raw=%zu dfa=%zu edges=%llu "
           "counts3=%s counts6=%s counts9=%s counts_exact=%d ops=%llu comparisons=%llu\n", j,
           stats.nfa, stats.live, (unsigned long long)stats.nfaEdges, stats.dfaRaw, dfa.q.size(),
           (unsigned long long)edgeCount(dfa.q), decimal(n[0].value).c_str(), decimal(n[1].value).c_str(),
           decimal(n[2].value).c_str(), int(n[0].exact && n[1].exact && n[2].exact),
           (unsigned long long)budget.used, (unsigned long long)comparisons); fflush(stdout);
  }
  void prepareTail(int width, int q) {
    if (!setup_instance(width) || order != typeTimes || nseg != 3 || noV ||
        *min_element(J.begin(), J.end()) - 1 != q || Jall != q + 2)
      undecided118("regular_tail_profile_mismatch");
    const vector<uint8_t> odd0{T_LODD,T_LODD,T_LODD,T_LODD,T_LEVEN,T_LEVEN,T_LEVEN,T_LEVEN};
    const vector<uint8_t> odd1{T_INZ,T_INZ,T_INZ,T_INZ,T_INZ,T_INZ,T_INZ,T_INP};
    const vector<uint8_t> even0{T_LEVEN,T_LEVEN,T_LEVEN,T_LEVEN,T_GEN,T_GEN,T_GEN,T_GEN};
    const vector<uint8_t> even1{T_INZ,T_INZ,T_INZ,T_INP,T_LODD,T_LODD,T_LODD,T_LODD};
    for (int s = 0; s < 3; ++s) {
      for (int k = 0; k < 8; ++k) if (m[typeTimes[s][k]] != width + int(k >= 4))
        undecided118("regular_length_offset_mismatch");
      SigTab* a = fast.sigFor(s, q, false); SigTab* c = fast.sigFor(s, q + 1, false);
      if (a->types != (width % 2 ? odd0 : even0) || c->types != (width % 2 ? odd1 : even1) ||
          a->j0 != (q == 0) || c->j0)
        undecided118("regular_tail_signature_mismatch");
    }
  }
  vector<Label> acceptedWord(const DFA& dfa) {
    vector<Id> parent(dfa.q.size(), DEAD); vector<Label> via(dfa.q.size());
    vector<Id> queue{dfa.start}; parent[dfa.start] = dfa.start; Id last = DEAD;
    for (size_t k = 0; k < queue.size(); ++k) {
      Id q = queue[k]; budget.tick();
      if (dfa.q[q].accept) { last = q; break; }
      for (Arc a : dfa.q[q].arcs) if (parent[a.second] == DEAD) {
        budget.tick(); parent[a.second] = q; via[a.second] = a.first; queue.push_back(a.second);
      }
    }
    if (last == DEAD) return {};
    vector<Label> word;
    while (last != dfa.start) { word.push_back(via[last]); last = parent[last]; }
    reverse(word.begin(), word.end()); return word;
  }
  void potential(const DFA& dfa, int width) {
    vector<Label> word = acceptedWord(dfa);
    if (word.empty() || word.size() % 3) undecided118("regular_bad_potential_word");
    printf("REG_WORD length=%zu symbols=", word.size());
    for (size_t i = 0; i < word.size(); ++i) {
      if (typeOf(word[i]) != int(i % 3)) undecided118("regular_potential_phase_mismatch");
      printf("%s%d:%u", i ? "," : "", typeOf(word[i]), lidOf(word[i]));
    }
    printf("\n"); set<Label> alphabet(word.begin(), word.end());
    for (Label a : alphabet) {
      const SegState& s = fast.sg[typeOf(a)]; auto info = s.lidInfo[lidOf(a)]; const string& cfg = s.cfg[info.first];
      printf("REG_LABEL type=%d lid=%u z=%d cfg=", typeOf(a), lidOf(a), int(info.second));
      for (size_t k = 0; k < cfg.size(); ++k) printf("%s%u", k ? "," : "", unsigned(uint8_t(cfg[k])));
      printf("\n");
    }
    printf("REG_DONE status=potential_center scope=accepted_temporal_word period=%zu width=%d "
           "ops=%llu comparisons=%llu\n", word.size() * 8, width,
           (unsigned long long)budget.used, (unsigned long long)comparisons); fflush(stdout);
  }
  void distinction(int j, const vector<Label>& word, bool acceptsLeft) {
    printf("REG_DIFFERENCE left=%d right=%d word_length=%zu temporal_period=%zu accepts=%s symbols=",
           j, j + 1, word.size(), word.size() * 8, acceptsLeft ? "left" : "right");
    // Each symbol is type:lid:Z:hex(raw l,r,Rd+1 triples).  It is meaningful
    // independently of local interning order, not merely a transient ID dump.
    for (size_t i = 0; i < word.size(); ++i) {
      int type = typeOf(word[i]); Id lid = lidOf(word[i]);
      const SegState& s = fast.sg[type]; auto info = s.lidInfo[lid]; const string& cfg = s.cfg[info.first];
      printf("%s%d:%u:%d:", i ? "," : "", type, lid, int(info.second));
      for (uint8_t x : cfg) printf("%02x", unsigned(x));
    }
    printf("\n"); fflush(stdout);
  }
  void run() {
    init(); vector<DFA> frontiers; frontiers.push_back(initial());
    printf("REG_INIT base=10 temporal_unit=24 types=3 repetitions=positive_arbitrary prune=%d\n", int(prune));
    diagnostic(0, frontiers[0], ImageStats()); int fixed = -1;
    for (int j = 0; j < layers; ++j) {
      ImageStats stats; DFA next = step(frontiers.back(), j, true, stats);
      diagnostic(j + 1, next, stats);
      if (j >= 1) {
        vector<Label> difference; bool acceptsLeft = false;
        if (equivalent(frontiers.back(), next, budget, difference, acceptsLeft)) { fixed = j; break; }
        distinction(j, difference, acceptsLeft);
      }
      frontiers.push_back(std::move(next));
    }
    if (fixed < 1) undecided118("regular_fixedpoint_not_detected");
    printf("REG_FIXED fixed_at=%d method=exact_dfa_product\n", fixed); fflush(stdout);
    int tailChecks = 0;
    for (int q = 0; q <= fixed; ++q) for (int parity = 1; parity <= 2; ++parity) {
      int width = 2 * q + parity; prepareTail(width, q); ImageStats firstStats, secondStats;
      DFA first = step(frontiers[q], q, false, firstStats);
      DFA last = step(first, q + 1, false, secondStats); ++tailChecks;
      bool empty = last.q.size() == 1 && !last.q[0].accept && last.q[0].arcs.empty();
      printf("REG_TAIL width=%d generic=%d empty=%d first_nfa=%zu first_dfa=%zu last_nfa=%zu last_dfa=%zu "
             "ops=%llu comparisons=%llu\n", width, q, int(empty), firstStats.nfa, first.q.size(),
             secondStats.nfa, last.q.size(), (unsigned long long)budget.used, (unsigned long long)comparisons);
      fflush(stdout);
      if (!empty) { potential(last, width); return; }
    }
    printf("REG_DONE status=none scope=all_repetitions_all_widths fixed_at=%d tail_checks=%d "
           "peak_states=%llu peak_edges=%llu ops=%llu comparisons=%llu\n", fixed, tailChecks,
           (unsigned long long)budget.peakStates, (unsigned long long)budget.peakEdges,
           (unsigned long long)budget.used, (unsigned long long)comparisons); fflush(stdout);
  }
};

int main118(int argc, char** argv) {
  Engine engine; set<string> seen;
  for (int i = 1; i < argc; ++i) {
    string flag = argv[i];
    if (!seen.insert(flag).second) undecided118("duplicate_regular_option");
    auto value = [&]() -> uint64_t {
      if (++i >= argc) undecided118("missing_regular_option_value");
      long long n = number118(argv[i]); if (n < 1) undecided118("nonpositive_regular_limit"); return n;
    };
    if (flag == "--layers") { uint64_t n = value(); if (n > 1000) undecided118("unsupported_regular_layers"); engine.layers = n; }
    else if (flag == "--states") { engine.budget.states = value(); if (engine.budget.states > 10000000) undecided118("unsupported_regular_states"); }
    else if (flag == "--edges") { engine.budget.edges = value(); if (engine.budget.edges > 100000000) undecided118("unsupported_regular_edges"); }
    else if (flag == "--ops") engine.budget.operations = value();
    else if (flag == "--compare-cap") { engine.compareCap = value(); if (engine.compareCap > 10000000) undecided118("unsupported_regular_compare_cap"); }
    else if (flag == "--compare") engine.compare = true;
    else if (flag == "--no-prune") engine.prune = false;
    else undecided118("unsupported_regular_option");
  }
  engine.run(); return 0;
}
}  // namespace REG118

int main(int argc, char** argv) {
  try { return REG118::main118(argc, argv); }
  catch (const exception& error) { fprintf(stderr, "UNDECIDED %s\n", error.what()); return 2; }
  catch (...) { fprintf(stderr, "UNDECIDED unexpected_exception\n"); return 2; }
}
