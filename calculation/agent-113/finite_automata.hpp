#pragma once
// Exact epsilon-free finite automata. Caps throw; they never imply emptiness
// or language equivalence. Labels are arbitrary uint32_t symbols (including 0).
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <deque>
#include <limits>
#include <map>
#include <ostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace a113fa {
using State = uint32_t;
using Label = uint32_t;
constexpr State absent = std::numeric_limits<State>::max();

// Nonnegative exact integers suffice for word-count DP. Avoid an optional
// Boost dependency: base-10^9 limbs support addition, equality and printing.
class Integer {
  static constexpr uint64_t radix = 1000000000;
  std::vector<uint32_t> digits;
public:
  Integer(uint64_t n = 0) {
    while (n) { digits.push_back(static_cast<uint32_t>(n % radix)); n /= radix; }
  }
  Integer& operator+=(const Integer& other) {
    const size_t n = std::max(digits.size(),other.digits.size());
    digits.resize(n,0);
    uint64_t carry = 0;
    for (size_t i = 0; i < n; ++i) {
      uint64_t total = static_cast<uint64_t>(digits[i]) + carry;
      if (i < other.digits.size()) total += other.digits[i];
      digits[i] = static_cast<uint32_t>(total % radix); carry = total / radix;
    }
    if (carry) digits.push_back(static_cast<uint32_t>(carry));
    return *this;
  }
  std::string str() const {
    if (digits.empty()) return "0";
    std::string out = std::to_string(digits.back());
    for (size_t i = digits.size()-1; i > 0; --i) {
      std::string part = std::to_string(digits[i-1]);
      out.append(9-part.size(),'0'); out += part;
    }
    return out;
  }
  friend bool operator==(const Integer& a,const Integer& b) { return a.digits == b.digits; }
  friend bool operator!=(const Integer& a,const Integer& b) { return !(a==b); }
  friend Integer operator<<(Integer value,size_t bits) {
    while (bits--) value += value;
    return value;
  }
  friend std::ostream& operator<<(std::ostream& out,const Integer& value) { return out << value.str(); }
};

struct LimitReached : std::runtime_error {
  explicit LimitReached(const std::string& s) : std::runtime_error(s) {}
};
struct Limits {
  size_t max_states = 200000;
  size_t max_edges = 5000000;
  uint64_t max_operations = 100000000;
  double seconds = 60;
};
struct Budget {
  Limits limits;
  uint64_t operations = 0;
  size_t peak_states = 0, peak_edges = 0;
  std::chrono::steady_clock::time_point started;
  explicit Budget(Limits lim = {}) : limits(lim), started(std::chrono::steady_clock::now()) {
    if (!limits.max_states || !limits.max_operations || !std::isfinite(limits.seconds) ||
        limits.seconds <= 0 || limits.seconds > 1800)
      throw std::invalid_argument("invalid automaton resource limits");
  }
  void check_time() const {
    if (std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count() >= limits.seconds)
      throw LimitReached("automaton wall-time budget");
  }
  void tick(uint64_t n = 1) {
    if (n > limits.max_operations-operations) throw LimitReached("automaton operation cap");
    uint64_t before = operations;
    operations += n;
    if ((before >> 10) != (operations >> 10)) check_time();
  }
  void observe(size_t states, size_t edges) {
    check_time();
    peak_states = std::max(peak_states, states);
    peak_edges = std::max(peak_edges, edges);
    if (states > limits.max_states || states >= absent) throw LimitReached("automaton state cap");
    if (edges > limits.max_edges) throw LimitReached("automaton edge cap");
  }
};

struct Edge {
  Label label;
  State to;
  bool operator==(const Edge& other) const { return label == other.label && to == other.to; }
  bool operator<(const Edge& other) const {
    return label != other.label ? label < other.label : to < other.to;
  }
};

struct NFA {
  std::vector<std::vector<Edge>> edges;
  std::vector<State> initial;
  std::vector<uint8_t> final;
  State add_state(bool accepting = false) {
    if (edges.size() >= absent) throw LimitReached("NFA index capacity");
    State q = static_cast<State>(edges.size());
    edges.emplace_back(); final.push_back(accepting); return q;
  }
  void add_initial(State q) {
    if (q >= edges.size()) throw std::invalid_argument("invalid initial state");
    initial.push_back(q);
  }
  void add_edge(State from, Label label, State to) {
    if (from >= edges.size() || to >= edges.size()) throw std::invalid_argument("invalid NFA edge");
    edges[from].push_back({label,to});
  }
  size_t size() const { return edges.size(); }
  size_t edge_count() const {
    size_t n = 0; for (const auto& row : edges) n += row.size(); return n;
  }
};

struct DFA {
  std::vector<std::vector<Edge>> edges;
  State initial = 0;
  std::vector<uint8_t> final;
  State add_state(bool accepting = false) {
    if (edges.size() >= absent) throw LimitReached("DFA index capacity");
    State q = static_cast<State>(edges.size());
    edges.emplace_back(); final.push_back(accepting); return q;
  }
  void add_edge(State from, Label label, State to) {
    if (from >= edges.size() || to >= edges.size()) throw std::invalid_argument("invalid DFA edge");
    for (const Edge& old : edges[from])
      if (old.label == label) throw std::invalid_argument("duplicate DFA label");
    edges[from].push_back({label,to});
  }
  size_t size() const { return edges.size(); }
  size_t edge_count() const {
    size_t n = 0; for (const auto& row : edges) n += row.size(); return n;
  }
  bool operator==(const DFA& other) const {
    return initial == other.initial && final == other.final && edges == other.edges;
  }
  bool operator!=(const DFA& other) const { return !(*this == other); }
};

inline DFA empty_dfa() { DFA a; a.add_state(false); return a; }
inline NFA as_nfa(const DFA& a) {
  NFA n; n.edges = a.edges; n.final = a.final;
  if (!a.edges.empty()) n.initial.push_back(a.initial);
  return n;
}

inline void validate(const NFA& a, Budget& budget) {
  if (a.final.size() != a.size()) throw std::invalid_argument("NFA final-vector size");
  size_t edge_total = 0;
  for (State q : a.initial) {
    budget.tick(); if (q >= a.size()) throw std::invalid_argument("NFA initial index");
  }
  for (size_t q = 0; q < a.size(); ++q) {
    budget.tick();
    if (a.final[q] > 1) throw std::invalid_argument("NFA final bit");
    for (const Edge& e : a.edges[q]) {
      budget.tick();
      if (e.to >= a.size()) throw std::invalid_argument("NFA target index");
      ++edge_total;
    }
  }
  budget.observe(a.size(), edge_total);
}
inline void validate(const DFA& a, Budget& budget) {
  if (a.size() == 0 || a.initial >= a.size() || a.final.size() != a.size())
    throw std::invalid_argument("DFA shape/initial index");
  size_t edge_total = 0;
  for (size_t q = 0; q < a.size(); ++q) {
    budget.tick();
    if (a.final[q] > 1) throw std::invalid_argument("DFA final bit");
    std::unordered_set<Label> labels;
    for (const Edge& e : a.edges[q]) {
      budget.tick();
      if (e.to >= a.size() || !labels.insert(e.label).second)
        throw std::invalid_argument("invalid or nondeterministic DFA edge");
      ++edge_total;
    }
  }
  budget.observe(a.size(), edge_total);
}

// Keep exactly states lying on a path from an initial to a final state.
// Empty language is an empty NFA: no nodes, no initial states, no edges.
inline NFA trim(const NFA& a, Budget& budget) {
  validate(a,budget);
  const size_t n = a.size();
  std::vector<uint8_t> reachable(n,0), useful(n,0);
  std::vector<std::vector<State>> reverse(n);
  for (State q = 0; q < n; ++q)
    for (const Edge& e : a.edges[q]) { budget.tick(); reverse[e.to].push_back(q); }
  std::deque<State> queue;
  for (State q : a.initial) if (!reachable[q]) { reachable[q] = 1; queue.push_back(q); }
  while (!queue.empty()) {
    State q = queue.front(); queue.pop_front();
    for (const Edge& e : a.edges[q]) {
      budget.tick(); if (!reachable[e.to]) { reachable[e.to] = 1; queue.push_back(e.to); }
    }
  }
  for (State q = 0; q < n; ++q) if (a.final[q]) { useful[q] = 1; queue.push_back(q); }
  while (!queue.empty()) {
    State q = queue.front(); queue.pop_front();
    for (State pred : reverse[q]) {
      budget.tick(); if (!useful[pred]) { useful[pred] = 1; queue.push_back(pred); }
    }
  }
  NFA out; std::vector<State> map(n,absent);
  for (State q = 0; q < n; ++q)
    if (reachable[q] && useful[q]) map[q] = out.add_state(a.final[q]);
  for (State q : a.initial) if (map[q] != absent) out.initial.push_back(map[q]);
  std::sort(out.initial.begin(),out.initial.end());
  out.initial.erase(std::unique(out.initial.begin(),out.initial.end()),out.initial.end());
  size_t edge_total = 0;
  for (State q = 0; q < n; ++q) if (map[q] != absent) {
    auto& row = out.edges[map[q]];
    for (const Edge& e : a.edges[q]) {
      budget.tick(); if (map[e.to] != absent) row.push_back({e.label,map[e.to]});
    }
    std::sort(row.begin(),row.end(),[&](const Edge& x,const Edge& y){budget.tick();return x<y;});
    row.erase(std::unique(row.begin(),row.end()),row.end());
    edge_total += row.size();
  }
  budget.observe(out.size(),edge_total);
  return out;
}

struct VectorHash {
  template<class T> size_t operator()(const std::vector<T>& values) const {
    uint64_t h = 0x9e3779b97f4a7c15ULL;
    for (T value : values) h ^= static_cast<uint64_t>(value)+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);
    return static_cast<size_t>(h);
  }
};

// Ordinary subset construction. Missing transitions lead to an implicit,
// nonaccepting sink, which is never materialized.
inline DFA determinize(const NFA& a, Budget& budget) {
  validate(a,budget);
  if (a.initial.empty()) { budget.observe(1,0); return empty_dfa(); }
  DFA out;
  std::vector<std::vector<State>> subsets;
  std::unordered_map<std::vector<State>,State,VectorHash> ids;
  size_t edge_total = 0;
  auto intern = [&](std::vector<State> set) -> State {
    std::sort(set.begin(),set.end(),[&](State x,State y){budget.tick();return x<y;});
    set.erase(std::unique(set.begin(),set.end()),set.end());
    auto found = ids.find(set); if (found != ids.end()) return found->second;
    budget.observe(out.size()+1,edge_total);
    bool accepting = false;
    for (State q : set) { budget.tick(); accepting |= a.final[q] != 0; }
    State id = out.add_state(accepting);
    subsets.push_back(set); ids.emplace(std::move(set),id); return id;
  };
  out.initial = intern(a.initial);
  for (State q = 0; q < subsets.size(); ++q) {
    std::map<Label,std::vector<State>> images;
    // intern() may reallocate subsets, so finish reading this subset first.
    for (State original : subsets[q])
      for (const Edge& e : a.edges[original]) { budget.tick(); images[e.label].push_back(e.to); }
    for (auto& image : images) {
      State dest = intern(std::move(image.second));
      out.edges[q].push_back({image.first,dest});
      budget.observe(out.size(),++edge_total);
    }
  }
  budget.check_time(); return out;
}

// Reachable BFS numbering with outgoing labels in increasing order is a
// canonical serialization of a rooted deterministic labelled graph.
inline DFA canonicalize(const DFA& a, Budget& budget) {
  validate(a,budget);
  DFA out; std::vector<State> ids(a.size(),absent), queue;
  ids[a.initial] = out.add_state(a.final[a.initial]); queue.push_back(a.initial);
  size_t edge_total = 0;
  for (size_t i = 0; i < queue.size(); ++i) {
    State original = queue[i], here = ids[original];
    auto row = a.edges[original];
    std::sort(row.begin(),row.end(),[&](const Edge& x,const Edge& y){budget.tick();return x<y;});
    for (const Edge& e : row) {
      budget.tick();
      if (ids[e.to] == absent) { ids[e.to] = out.add_state(a.final[e.to]); queue.push_back(e.to); }
      out.edges[here].push_back({e.label,ids[e.to]});
      budget.observe(out.size(),++edge_total);
    }
  }
  budget.check_time(); return out;
}

// Sparse Moore refinement after removing empty right-languages. No full
// alphabet-by-state sink table is needed: every retained edge has a nonempty
// right-language, so presence of its label is itself language-observable.
inline DFA minimize(const DFA& a, Budget& budget) {
  validate(a,budget);
  NFA kept = trim(as_nfa(a),budget);
  if (kept.initial.empty()) { budget.observe(1,0); return empty_dfa(); }
  DFA clean; clean.edges = std::move(kept.edges); clean.final = std::move(kept.final);
  clean.initial = kept.initial.front();
  const size_t n = clean.size();
  std::vector<State> block(n);
  for (size_t q = 0; q < n; ++q) block[q] = clean.final[q];
  State groups = 0;
  while (true) {
    std::unordered_map<std::vector<uint64_t>,State,VectorHash> signatures;
    std::vector<State> next(n);
    groups = 0;
    for (State q = 0; q < n; ++q) {
      budget.tick();
      std::vector<uint64_t> key; key.reserve(clean.edges[q].size()+1);
      key.push_back(clean.final[q]);
      for (const Edge& e : clean.edges[q]) {
        budget.tick(); key.push_back((static_cast<uint64_t>(e.label)<<32)|block[e.to]);
      }
      auto found = signatures.find(key);
      if (found == signatures.end()) { next[q] = groups; signatures.emplace(std::move(key),groups++); }
      else next[q] = found->second;
    }
    if (next == block) break;
    block.swap(next);
  }
  DFA quotient; std::vector<State> representative(groups,absent);
  for (State i = 0; i < groups; ++i) quotient.add_state(false);
  for (State q = 0; q < n; ++q) if (representative[block[q]] == absent) representative[block[q]] = q;
  for (State i = 0; i < groups; ++i) {
    State q = representative[i]; quotient.final[i] = clean.final[q];
    for (const Edge& e : clean.edges[q]) { budget.tick(); quotient.edges[i].push_back({e.label,block[e.to]}); }
  }
  quotient.initial = block[clean.initial];
  return canonicalize(quotient,budget);
}

inline bool accepts(const NFA& a, const std::vector<Label>& word) {
  if (a.final.size() != a.size()) throw std::invalid_argument("NFA final-vector size");
  std::vector<State> frontier = a.initial;
  for (Label label : word) {
    std::vector<State> next;
    for (State q : frontier) {
      if (q >= a.size()) throw std::invalid_argument("NFA state index");
      for (const Edge& e : a.edges[q]) if (e.label == label) next.push_back(e.to);
    }
    std::sort(next.begin(),next.end()); next.erase(std::unique(next.begin(),next.end()),next.end());
    frontier.swap(next);
  }
  for (State q : frontier) {
    if (q >= a.size()) throw std::invalid_argument("NFA state index");
    if (a.final[q]) return true;
  }
  return false;
}
inline bool accepts(const DFA& a, const std::vector<Label>& word) {
  if (a.initial >= a.size() || a.final.size() != a.size()) throw std::invalid_argument("DFA shape");
  State q = a.initial;
  for (Label label : word) {
    State next = absent;
    for (const Edge& e : a.edges[q]) if (e.label == label) {
      if (next != absent) throw std::invalid_argument("nondeterministic DFA label");
      next = e.to;
    }
    if (next == absent) return false;
    if (next >= a.size()) throw std::invalid_argument("DFA target index");
    q = next;
  }
  return a.final[q] != 0;
}

// Exact synchronized product including implicit rejecting sinks. A completed
// false result exhibits a final/nonfinal mismatch; a cap throws instead.
inline bool equivalent(const DFA& a, const DFA& b, Budget& budget) {
  validate(a,budget); validate(b,budget);
  auto encode = [](State x,State y) { return (static_cast<uint64_t>(x)<<32)|y; };
  std::vector<std::pair<State,State>> queue{{a.initial,b.initial}};
  std::unordered_set<uint64_t> seen{encode(a.initial,b.initial)};
  size_t edge_total = 0;
  for (size_t i = 0; i < queue.size(); ++i) {
    auto [x,y] = queue[i]; budget.tick();
    if ((x != absent && a.final[x]) != (y != absent && b.final[y])) return false;
    std::map<Label,std::pair<State,State>> next;
    if (x != absent) for (const Edge& e : a.edges[x]) { budget.tick(); next[e.label] = {e.to,absent}; }
    if (y != absent) for (const Edge& e : b.edges[y]) {
      budget.tick(); auto found = next.find(e.label);
      if (found == next.end()) next[e.label] = {absent,e.to}; else found->second.second = e.to;
    }
    for (const auto& edge : next) {
      budget.tick(); ++edge_total;
      auto pair = edge.second;
      if (seen.insert(encode(pair.first,pair.second)).second) queue.push_back(pair);
      budget.observe(seen.size(),edge_total);
    }
  }
  budget.check_time(); return true;
}

// Each DFA path spells one unique word; NFA path counts must not be used here.
inline Integer count_words(const DFA& a, size_t length, Budget& budget) {
  validate(a,budget);
  std::vector<Integer> counts(a.size()), next(a.size()); counts[a.initial] = 1;
  for (size_t i = 0; i < length; ++i) {
    budget.check_time(); std::fill(next.begin(),next.end(),Integer(0));
    for (State q = 0; q < a.size(); ++q) if (counts[q] != 0)
      for (const Edge& e : a.edges[q]) { budget.tick(); next[e.to] += counts[q]; }
    counts.swap(next);
  }
  Integer total = 0;
  for (State q = 0; q < a.size(); ++q) { budget.tick(); if (a.final[q]) total += counts[q]; }
  budget.check_time(); return total;
}
} // namespace a113fa
