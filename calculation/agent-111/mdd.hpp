#ifndef AGENT111_MDD_HPP
#define AGENT111_MDD_HPP

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

namespace a111 {

struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };

class MDD {
public:
  using Id = uint32_t;
  using Label = uint32_t;
  using Edge = std::pair<Label, Id>;
  struct Count { uint64_t value; bool saturated; };

private:
  struct Node {
    size_t level;
    std::vector<Edge> edges;
    Id collision_next;
    Count count;
  };
  size_t variables_, cap_;
  std::deque<Node> nodes_;
  std::unordered_map<uint64_t, Id> unique_;
  std::unordered_map<uint64_t, Id> unions_;

  static uint64_t mix(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
  }

  void valid_id(Id id) const {
    if (id >= nodes_.size()) throw std::logic_error("invalid MDD node id");
  }

  Id intern(size_t level, std::vector<Edge> edges) {
    if (edges.empty()) return 0;
    uint64_t hash = mix(level);
    Count count{0, false};
    for (auto [label, child] : edges) {
      hash = mix(hash ^ (uint64_t(label) << 32) ^ child);
      Count add = nodes_[child].count;
      if (count.saturated || add.saturated || UINT64_MAX - count.value < add.value)
        count = {UINT64_MAX, true};
      else count.value += add.value;
    }
    auto found = unique_.find(hash);
    Id collision = found == unique_.end() ? 0 : found->second;
    for (Id id = collision; id; id = nodes_[id].collision_next)
      if (nodes_[id].level == level && nodes_[id].edges == edges) return id;
    if (nodes_.size() >= cap_ || nodes_.size() >= UINT32_MAX)
      throw Limit("MDD node cap nodes=" + std::to_string(nodes_.size()) +
                  " cap=" + std::to_string(cap_));
    Id id = static_cast<Id>(nodes_.size());
    nodes_.push_back({level, std::move(edges), collision, count});
    unique_[hash] = id;
    return id;
  }

public:
  explicit MDD(size_t variables, size_t node_cap = 2000000)
      : variables_(variables), cap_(node_cap) {
    if (!variables || variables > 64) throw std::invalid_argument("MDD variables must be 1..64");
    if (node_cap < 2) throw Limit("MDD node cap below terminal overhead");
    nodes_.push_back({variables, {}, 0, {0, false}}); // empty, valid at every level
    nodes_.push_back({variables, {}, 0, {1, false}}); // terminal-one, level variables only
  }

  size_t variables() const { return variables_; }
  size_t node_count() const { return nodes_.size(); }
  size_t union_cache_size() const { return unions_.size(); }
  void clear_union_cache() { unions_.clear(); }
  size_t level(Id id) const { valid_id(id); return nodes_[id].level; }
  const std::vector<Edge>& edges(Id id) const { valid_id(id); return nodes_[id].edges; }
  Count count(Id id) const { valid_id(id); return nodes_[id].count; }

  Id unite(Id a, Id b) {
    valid_id(a); valid_id(b);
    if (!a) return b;
    if (!b || a == b) return a;
    if (nodes_[a].level != nodes_[b].level)
      throw std::logic_error("union at unequal MDD levels");
    if (a == 1 || b == 1) throw std::logic_error("terminal/nonterminal union");
    if (a > b) std::swap(a, b);
    uint64_t key = (uint64_t(a) << 32) | b;
    auto found = unions_.find(key);
    if (found != unions_.end()) return found->second;
    const auto& x = nodes_[a].edges;
    const auto& y = nodes_[b].edges;
    std::vector<Edge> out;
    out.reserve(x.size() + y.size());
    size_t i = 0, j = 0;
    while (i < x.size() || j < y.size()) {
      if (j == y.size() || (i < x.size() && x[i].first < y[j].first)) out.push_back(x[i++]);
      else if (i == x.size() || y[j].first < x[i].first) out.push_back(y[j++]);
      else {
        out.push_back({x[i].first, unite(x[i].second, y[j].second)});
        ++i; ++j;
      }
    }
    Id answer = intern(nodes_[a].level, std::move(out));
    unions_[key] = answer;
    return answer;
  }

  Id make(size_t level, std::vector<Edge> edges) {
    if (level >= variables_) throw std::logic_error("nonterminal at terminal level");
    std::sort(edges.begin(), edges.end());
    std::vector<Edge> out;
    for (auto [label, child] : edges) {
      valid_id(child);
      if (!child) continue;
      if (nodes_[child].level != level + 1)
        throw std::logic_error("skipped MDD level");
      if (!out.empty() && out.back().first == label)
        out.back().second = unite(out.back().second, child);
      else out.push_back({label, child});
    }
    return intern(level, std::move(out));
  }

  Id singleton(const std::vector<Label>& tuple) {
    if (tuple.size() != variables_) throw std::logic_error("tuple arity mismatch");
    Id root = 1;
    for (size_t level = variables_; level-- > 0;)
      root = make(level, {{tuple[level], root}});
    return root;
  }

  Id from_tuples(const std::vector<std::vector<Label>>& tuples) {
    Id root = 0;
    for (const auto& tuple : tuples) root = unite(root, singleton(tuple));
    return root;
  }

  std::vector<Label> pick(Id root) const {
    valid_id(root);
    if (!root || level(root) != 0) throw std::logic_error("cannot pick from empty/nonroot MDD");
    std::vector<Label> tuple;
    while (root != 1) {
      const auto& edge = nodes_[root].edges.front();
      tuple.push_back(edge.first); root = edge.second;
    }
    return tuple;
  }

  std::vector<std::vector<Label>> enumerate(Id root, size_t limit = 1000000) const {
    valid_id(root);
    if (root && level(root) != 0) throw std::logic_error("enumeration requires level-zero root");
    std::vector<std::vector<Label>> result;
    std::vector<Label> tuple;
    std::function<void(Id)> visit = [&](Id id) {
      if (!id) return;
      if (id == 1) {
        if (result.size() >= limit) throw Limit("MDD enumeration tuple cap");
        result.push_back(tuple); return;
      }
      for (auto [label, child] : nodes_[id].edges) {
        tuple.push_back(label); visit(child); tuple.pop_back();
      }
    };
    visit(root);
    return result;
  }
};

struct Choice { uint32_t y; int c; };
using Local = std::function<const std::vector<Choice>&(size_t, MDD::Label)>;
using Encode = std::function<MDD::Label(size_t, uint32_t, int)>;

// One segment of look-ahead preserves the full input suffix correlation.
// A fresh memo belongs to this image only: a later layer can have another
// transition signature even when its input root has the same identifier.
inline MDD::Id cyclic_image(MDD& graph, MDD::Id root, const Local& local,
                            const Encode& encode, uint64_t work_cap = 50000000) {
  using Id = MDD::Id;
  struct Key {
    Id node; uint32_t previous_y; int first_c;
    bool operator==(const Key& other) const {
      return node == other.node && previous_y == other.previous_y && first_c == other.first_c;
    }
  };
  struct Hash {
    size_t operator()(const Key& key) const {
      uint64_t h = (uint64_t(key.node) << 32) | key.previous_y;
      return static_cast<size_t>((h ^ (uint64_t(uint32_t(key.first_c)) * 0x9e3779b97f4a7c15ULL)) *
                                 0xbf58476d1ce4e5b9ULL);
    }
  };
  if (!root) return 0;
  if (graph.level(root) != 0) throw std::logic_error("cyclic image requires root level zero");
  std::unordered_map<Key, Id, Hash> memo;
  uint64_t work = 0;
  auto tick = [&] {
    if (work == work_cap) throw Limit("MDD image work cap=" + std::to_string(work_cap));
    ++work;
  };
  std::function<Id(Id, uint32_t, int)> next = [&](Id node, uint32_t previous_y, int first_c) -> Id {
    if (!node) return 0;
    Key key{node, previous_y, first_c};
    auto found = memo.find(key);
    if (found != memo.end()) return found->second;
    tick();
    size_t level = graph.level(node);
    Id answer;
    if (node == 1) {
      answer = graph.make(graph.variables() - 1,
                          {{encode(graph.variables() - 1, previous_y, first_c), 1}});
    } else {
      if (level == 0 || level >= graph.variables()) throw std::logic_error("bad image recursion level");
      std::vector<MDD::Edge> outputs;
      for (auto [input, child] : graph.edges(node)) {
        for (const Choice& row : local(level, input)) {
          tick();
          Id suffix = next(child, row.y, first_c);
          if (suffix) outputs.push_back({encode(level - 1, previous_y, row.c), suffix});
        }
      }
      answer = graph.make(level - 1, std::move(outputs));
    }
    memo.emplace(key, answer);
    return answer;
  };
  Id answer = 0;
  for (auto [input, child] : graph.edges(root)) {
    for (const Choice& row : local(0, input)) {
      tick();
      answer = graph.unite(answer, next(child, row.y, row.c));
    }
  }
  return answer;
}

} // namespace a111
#endif
