#ifndef AGENT111_EXTERIOR_INVARIANT_HPP
#define AGENT111_EXTERIOR_INVARIANT_HPP

// Exact finite-product inclusion checks. No determinization or minimization.
#include <algorithm>
#include <cstdint>
#include <deque>
#include <functional>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace a111x {
using Symbol = uint64_t;
using State = uint32_t;
using Word = std::vector<Symbol>;
struct DNode { bool accept = false; std::vector<std::pair<Symbol, State>> edges; };
struct DFA { std::vector<DNode> nodes; State start = 0; };
struct NNode {
  bool accept = false;
  std::vector<std::pair<Symbol, State>> edges;
  std::vector<State> epsilon;
};
struct NFA { std::vector<NNode> nodes; std::vector<State> starts; };
struct Row { int32_t incoming; Symbol output; int32_t outgoing; };
inline bool operator==(const Row& a, const Row& b) {
  return a.incoming == b.incoming && a.output == b.output && a.outgoing == b.outgoing;
}
using Relation = std::function<const std::vector<Row>&(Symbol)>;
struct Limits { size_t states = 1000000, edges = 10000000; uint64_t work = 100000000; };
struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };
struct Stats { size_t states = 0, edges = 0; uint64_t work = 0; };
struct Result {
  bool ok = true;
  Word word, input;
  std::vector<Row> rows;
  Stats stats;
};

namespace detail {
constexpr State absent = UINT32_MAX;
struct Budget {
  Limits limits;
  Stats stats;
  explicit Budget(Limits l) : limits(l) {}
  void tick(uint64_t n = 1) {
    if (n > limits.work - stats.work) throw Limit("exterior work cap");
    stats.work += n;
  }
  void input_states(size_t n) const {
    if (n > limits.states || n >= UINT32_MAX) throw Limit("exterior state cap");
  }
  void input_edges(size_t n) const {
    if (n > limits.edges) throw Limit("exterior edge cap");
  }
  void state(size_t n) { input_states(n); stats.states = n; }
  void edge() {
    tick();
    if (stats.edges >= limits.edges) throw Limit("exterior edge cap");
    ++stats.edges;
  }
};

inline DFA checked(const DFA& input, Budget& budget) {
  if (input.nodes.empty()) {
    if (input.start) throw std::invalid_argument("nonzero start in empty DFA");
    budget.input_states(1); return DFA{{DNode{}}, 0};
  }
  budget.input_states(input.nodes.size());
  if (input.start >= input.nodes.size()) throw std::invalid_argument("DFA start outside states");
  DFA copy = input; size_t count = 0;
  for (auto& node : copy.nodes) {
    budget.tick();
    std::sort(node.edges.begin(), node.edges.end());
    std::vector<std::pair<Symbol, State>> unique;
    for (auto arc : node.edges) {
      budget.tick(); budget.input_edges(++count);
      if (arc.second >= copy.nodes.size()) throw std::invalid_argument("DFA target outside states");
      if (!unique.empty() && unique.back().first == arc.first) {
        if (unique.back().second != arc.second) throw std::invalid_argument("conflicting DFA arcs");
      } else unique.push_back(arc);
    }
    node.edges = std::move(unique);
  }
  return copy;
}
inline void check_nfa(const NFA& nfa, Budget& budget) {
  budget.input_states(nfa.nodes.size()); size_t count = 0;
  for (State start : nfa.starts)
    if (start >= nfa.nodes.size()) throw std::invalid_argument("NFA start outside states");
  for (const auto& node : nfa.nodes) {
    budget.tick();
    for (auto [label, target] : node.edges) {
      (void)label; budget.tick(); budget.input_edges(++count);
      if (target >= nfa.nodes.size()) throw std::invalid_argument("NFA target outside states");
    }
    for (State target : node.epsilon) {
      budget.tick(); budget.input_edges(++count);
      if (target >= nfa.nodes.size()) throw std::invalid_argument("NFA epsilon target outside states");
    }
  }
}
inline State delta(const DFA& dfa, State state, Symbol symbol) {
  State sink = static_cast<State>(dfa.nodes.size());
  if (state == sink) return sink;
  const auto& edges = dfa.nodes[state].edges;
  auto it = std::lower_bound(edges.begin(), edges.end(), symbol,
      [](const auto& arc, Symbol key) { return arc.first < key; });
  return it == edges.end() || it->first != symbol ? sink : it->second;
}
inline bool final(const DFA& dfa, State state) {
  return state < dfa.nodes.size() && dfa.nodes[state].accept;
}
inline NFA as_nfa(const DFA& dfa) {
  NFA nfa; nfa.starts.push_back(dfa.start); nfa.nodes.resize(dfa.nodes.size());
  for (size_t i = 0; i < dfa.nodes.size(); ++i) {
    nfa.nodes[i].accept = dfa.nodes[i].accept; nfa.nodes[i].edges = dfa.nodes[i].edges;
  }
  return nfa;
}
struct Pair {
  State a, b;
  bool operator==(const Pair& other) const { return a == other.a && b == other.b; }
};
struct PairHash {
  size_t operator()(const Pair& k) const {
    uint64_t x = (uint64_t(k.a) << 32) | k.b;
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL; x ^= x >> 27;
    return static_cast<size_t>(x ^ (x >> 31));
  }
};

// Product with the rejecting/accepting part of a completed partial DFA.
// Epsilon moves have cost zero; all symbol moves cost one. The 0-1 BFS
// therefore returns a shortest WORD, including when epsilon cycles exist.
inline Result product(const NFA& nfa, const DFA& dfa, bool intersection, Budget& budget) {
  struct Record { Pair key; State parent; Symbol label; bool labeled; size_t distance; };
  std::vector<Record> records;
  std::unordered_map<Pair, State, PairHash> ids;
  std::deque<std::pair<State, size_t>> queue;
  auto reach = [&](Pair key, State parent, Symbol label, bool labeled, size_t distance) {
    auto found = ids.find(key); State id;
    if (found == ids.end()) {
      budget.state(records.size() + 1); id = static_cast<State>(records.size());
      records.push_back({key, parent, label, labeled, distance}); ids.emplace(key, id);
    } else {
      id = found->second;
      if (distance >= records[id].distance) return;
      records[id] = {key, parent, label, labeled, distance};
    }
    if (labeled) queue.push_back({id, distance}); else queue.push_front({id, distance});
  };
  for (State start : nfa.starts) reach({start, dfa.start}, absent, 0, false, 0);
  while (!queue.empty()) {
    auto [id, distance] = queue.front(); queue.pop_front();
    if (records[id].distance != distance) continue;
    Record here = records[id]; budget.tick();
    bool target_final = final(dfa, here.key.b);
    if (nfa.nodes[here.key.a].accept && (intersection ? target_final : !target_final)) {
      Result result; result.ok = false;
      for (State at = id; records[at].parent != absent; at = records[at].parent)
        if (records[at].labeled) result.word.push_back(records[at].label);
      std::reverse(result.word.begin(), result.word.end()); result.input = result.word;
      result.stats = budget.stats; return result;
    }
    for (State next : nfa.nodes[here.key.a].epsilon) {
      budget.edge(); reach({next, here.key.b}, id, 0, false, distance);
    }
    for (auto [label, next] : nfa.nodes[here.key.a].edges) {
      budget.edge(); reach({next, delta(dfa, here.key.b, label)}, id, label, true, distance + 1);
    }
  }
  Result result; result.stats = budget.stats; return result;
}
} // namespace detail

inline Result included(const NFA& source, const DFA& target, Limits limits = {}) {
  detail::Budget budget(limits); detail::check_nfa(source, budget);
  DFA dfa = detail::checked(target, budget); return detail::product(source, dfa, false, budget);
}
inline Result included(const DFA& source, const DFA& target, Limits limits = {}) {
  detail::Budget budget(limits); DFA a = detail::checked(source, budget), b = detail::checked(target, budget);
  return detail::product(detail::as_nfa(a), b, false, budget);
}
inline Result disjoint(const NFA& source, const DFA& target, Limits limits = {}) {
  detail::Budget budget(limits); detail::check_nfa(source, budget);
  DFA dfa = detail::checked(target, budget); return detail::product(source, dfa, true, budget);
}
inline Result disjoint(const DFA& source, const DFA& target, Limits limits = {}) {
  detail::Budget budget(limits); DFA a = detail::checked(source, budget), b = detail::checked(target, budget);
  return detail::product(detail::as_nfa(a), b, true, budget);
}
inline bool accepts(const DFA& input, const Word& word) {
  if (input.nodes.empty()) return false;
  if (input.start >= input.nodes.size()) throw std::invalid_argument("DFA start outside states");
  State state = input.start;
  for (Symbol symbol : word) {
    const auto& edges = input.nodes.at(state).edges;
    auto found = std::find_if(edges.begin(), edges.end(), [&](auto arc) { return arc.first == symbol; });
    if (found == edges.end()) return false;
    state = found->second;
  }
  return input.nodes.at(state).accept;
}

inline DFA positive_powers(const Word& word) {
  if (word.empty()) throw std::invalid_argument("empty positive-power unit");
  if (word.size() >= UINT32_MAX - 1) throw Limit("positive-power state cap");
  DFA result; result.nodes.resize(word.size() + 1);
  for (size_t i = 0; i < word.size(); ++i) result.nodes[i].edges.push_back({word[i], State(i + 1)});
  result.nodes.back().accept = true; result.nodes.back().edges.push_back({word.front(), 1});
  return result;
}

// One common accepting junction allows arbitrary mixtures of blocks. The
// fresh start rejects epsilon even if a block returns to the junction.
inline NFA positive_blocks(const std::vector<Word>& blocks) {
  if (blocks.empty()) throw std::invalid_argument("empty positive-block family");
  NFA nfa; nfa.nodes.resize(2); nfa.starts = {0}; nfa.nodes[1].accept = true;
  for (const Word& block : blocks) {
    if (block.empty()) throw std::invalid_argument("empty positive block");
    State current = 0;
    for (size_t i = 0; i < block.size(); ++i) {
      State target = 1;
      if (i + 1 < block.size()) {
        if (nfa.nodes.size() >= UINT32_MAX - 1) throw Limit("positive-block state cap");
        target = static_cast<State>(nfa.nodes.size()); nfa.nodes.push_back(NNode{});
      }
      nfa.nodes[current].edges.push_back({block[i], target});
      if (i == 0) nfa.nodes[1].edges.push_back({block[i], target});
      current = target;
    }
  }
  return nfa;
}

// Image of the nonempty source words under a finite cyclic row relation.
// Product states carry the FIRST and current boundaries without truncation.
// Closing an accepted input prefix does not prevent continuing longer inputs.
inline Result detail_cyclic_product(const DFA& source, const DFA& target,
                                    const Relation& relation, Limits limits, bool intersection) {
  detail::Budget budget(limits);
  DFA old = detail::checked(source, budget), invariant = detail::checked(target, budget);
  struct Key {
    State source, target; int32_t first, current;
    bool operator==(const Key& other) const {
      return source == other.source && target == other.target && first == other.first && current == other.current;
    }
  };
  struct Hash {
    size_t operator()(const Key& key) const {
      uint64_t x = (uint64_t(key.source) << 32) | key.target;
      uint64_t y = (uint64_t(static_cast<uint32_t>(key.first)) << 32) | static_cast<uint32_t>(key.current);
      x ^= y + 0x9e3779b97f4a7c15ULL + (x << 6) + (x >> 2);
      x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL; x ^= x >> 27;
      return static_cast<size_t>(x ^ (x >> 31));
    }
  };
  struct Record { Key key; State parent; Symbol input; Row row; };
  std::vector<Record> records;
  std::unordered_map<Key, State, Hash> ids;
  auto reach = [&](Key key, State parent, Symbol input, Row row) {
    if (ids.count(key)) return;
    budget.state(records.size() + 1);
    State id = static_cast<State>(records.size());
    records.push_back({key, parent, input, row}); ids.emplace(key, id);
  };
  // These initial records have consumed exactly one input/output symbol.
  for (auto [symbol, next] : old.nodes[old.start].edges) {
    for (const Row& row : relation(symbol)) {
      budget.edge();
      reach({next, detail::delta(invariant, invariant.start, row.output), row.incoming, row.outgoing},
            detail::absent, symbol, row);
    }
  }
  for (size_t head = 0; head < records.size(); ++head) {
    Record here = records[head]; budget.tick();
    bool target_final = detail::final(invariant, here.key.target);
    if (old.nodes[here.key.source].accept && here.key.first == here.key.current &&
        (intersection ? target_final : !target_final)) {
      Result result; result.ok = false;
      for (State at = static_cast<State>(head); at != detail::absent; at = records[at].parent) {
        result.input.push_back(records[at].input); result.word.push_back(records[at].row.output);
        result.rows.push_back(records[at].row);
      }
      std::reverse(result.input.begin(), result.input.end());
      std::reverse(result.word.begin(), result.word.end());
      std::reverse(result.rows.begin(), result.rows.end());
      result.stats = budget.stats; return result;
    }
    for (auto [symbol, next] : old.nodes[here.key.source].edges) {
      for (const Row& row : relation(symbol)) {
        budget.tick();
        if (row.incoming != here.key.current) continue;
        budget.edge();
        reach({next, detail::delta(invariant, here.key.target, row.output), here.key.first, row.outgoing},
              static_cast<State>(head), symbol, row);
      }
    }
  }
  Result result; result.stats = budget.stats; return result;
}
inline Result cyclic_image_included(const DFA& source, const DFA& target,
                                    const Relation& relation, Limits limits = {}) {
  return detail_cyclic_product(source, target, relation, limits, false);
}
inline Result cyclic_image_disjoint(const DFA& source, const DFA& target,
                                    const Relation& relation, Limits limits = {}) {
  return detail_cyclic_product(source, target, relation, limits, true);
}
} // namespace a111x
#endif
