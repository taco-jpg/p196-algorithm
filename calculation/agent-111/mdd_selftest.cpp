// Independent finite-set oracle for the Agent 111 exact MDD image engine.
// Build: c++ -O2 -std=c++17 calculation/agent-111/mdd_selftest.cpp -o /tmp/a111_mdd_test
// Run: /tmp/a111_mdd_test [random_cases=2500]
// No center arithmetic or MDD image internals are reproduced here: the oracle
// enumerates every input tuple and every tuple of local relation choices.
#include "mdd.hpp"
#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Label = uint32_t;
using Tuple = std::vector<Label>;
using FiniteSet = std::set<Tuple>;
using Rows = std::map<Label, std::vector<a111::Choice>>;
using Relations = std::vector<Rows>;

struct Counts {
  uint64_t union_cases = 0, image_cases = 0, correlated_inputs = 0;
  uint64_t raw_choice_tuples = 0, image_tuples = 0, duplicate_rows = 0;
  uint64_t nonempty_images = 0, empty_images = 0, guard_cases = 0;
};

static void require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

static Label encode(size_t segment, uint32_t y, int next_c) {
  require(y < 4 && next_c >= -1 && next_c <= 2, "bad synthetic local symbol");
  return Label(100 * segment + 4 * y + uint32_t(next_c + 1));
}

static const std::vector<a111::Choice>& row(const Relations& r, size_t s, Label x) {
  static const std::vector<a111::Choice> empty;
  const auto it = r.at(s).find(x);
  return it == r[s].end() ? empty : it->second;
}

// Complete explicit image. Output coordinate s receives the c symbol selected
// at coordinate s+1, cyclically. The input frontier can have any correlations.
static FiniteSet explicit_image(const FiniteSet& input, const Relations& r, Counts& count) {
  FiniteSet output;
  const size_t n = r.size();
  require(n > 0, "empty synthetic variable set");
  std::vector<a111::Choice> selected(n);
  for (const Tuple& w : input) {
    require(w.size() == n, "synthetic tuple arity mismatch");
    std::function<void(size_t)> visit = [&](size_t s) {
      if (s == n) {
        Tuple next(n);
        for (size_t i = 0; i < n; ++i)
          next[i] = encode(i, selected[i].y, selected[(i + 1) % n].c);
        output.insert(std::move(next));
        ++count.raw_choice_tuples;
        return;
      }
      for (const auto& choice : row(r, s, w[s])) {
        selected[s] = choice;
        visit(s + 1);
      }
    };
    visit(0);
  }
  return output;
}

static std::vector<Tuple> tuples(const FiniteSet& s) {
  return {s.begin(), s.end()};
}

static FiniteSet enumerate(a111::MDD& mdd, a111::MDD::Id root, size_t n) {
  const auto words = mdd.enumerate(root, 1000000);
  FiniteSet found(words.begin(), words.end());
  require(found.size() == words.size(), "MDD enumerator emitted duplicate tuples");
  for (const auto& w : found) require(w.size() == n, "MDD enumerator lost a level");
  return found;
}

static bool correlated(const FiniteSet& s, size_t n) {
  if (s.empty()) return false;
  uint64_t product = 1;
  for (size_t j = 0; j < n; ++j) {
    std::set<Label> marginal;
    for (const auto& w : s) marginal.insert(w[j]);
    product *= marginal.size();
  }
  return product != s.size();
}

static a111::MDD::Id check_image(a111::MDD& mdd, a111::MDD::Id input_root,
                                 const FiniteSet& input, const Relations& r,
                                 Counts& count, FiniteSet* expected_out = nullptr) {
  const auto local = [&](size_t s, Label x) -> const std::vector<a111::Choice>& {
    return row(r, s, x);
  };
  const FiniteSet expected = explicit_image(input, r, count);
  const auto actual_root = a111::cyclic_image(mdd, input_root, local, encode, 10000000);
  require(enumerate(mdd, actual_root, r.size()) == expected,
          "cyclic MDD image differs from complete explicit finite-set image");
  require(actual_root == mdd.from_tuples(tuples(expected)),
          "equal image languages have different canonical roots");
  ++count.image_cases;
  count.image_tuples += expected.size();
  if (expected.empty()) ++count.empty_images; else ++count.nonempty_images;
  if (correlated(input, r.size())) ++count.correlated_inputs;
  if (expected_out) *expected_out = expected;
  return actual_root;
}

static void union_fixture(Counts& count) {
  a111::MDD mdd(3);
  auto a = mdd.make(2, {{10, 1}});
  auto b = mdd.make(2, {{11, 1}});
  auto left = mdd.make(1, {{7, a}});
  auto right = mdd.make(1, {{7, b}});
  // Repeated labels require a recursive union of their suffix languages.
  auto root = mdd.make(0, {{2, right}, {99, 0}, {2, left}, {2, left}});
  FiniteSet expected{{2, 7, 10}, {2, 7, 11}};
  require(enumerate(mdd, root, 3) == expected, "duplicate-edge union fixture");
  require(root == mdd.from_tuples(tuples(expected)), "duplicate-edge canonical root");
  require(mdd.unite(0, root) == root && mdd.unite(root, 0) == root,
          "union empty identity");
  require(mdd.unite(root, root) == root, "union idempotence");
  require(mdd.make(0, {{3, 0}, {4, 0}}) == 0, "empty-edge pruning");
  ++count.union_cases;

  a111::MDD wide(2);
  FiniteSet large_labels{{0, std::numeric_limits<Label>::max()},
                        {std::numeric_limits<Label>::max(), 0}};
  require(enumerate(wide, wide.from_tuples(tuples(large_labels)), 2) == large_labels,
          "full uint32 label range was not preserved");
  ++count.union_cases;
}

static void cyclic_fixtures(Counts& count) {
  {
    a111::MDD mdd(1);
    FiniteSet input{{7}};
    Relations r(1);
    r[0][7] = {{2, -1}, {3, 2}, {2, -1}};
    FiniteSet result;
    check_image(mdd, mdd.from_tuples(tuples(input)), input, r, count, &result);
    require(result == FiniteSet{{encode(0, 2, -1)}, {encode(0, 3, 2)}},
            "NS1 incorrectly cross-combined its own c choices");
  }
  {
    a111::MDD mdd(2);
    FiniteSet input{{0, 0}, {1, 1}};
    Relations r(2);
    r[0][0] = {{0, -1}}; r[1][0] = {{1, 0}};
    r[0][1] = {{2, 1}}; r[1][1] = {{3, 2}};
    FiniteSet result;
    check_image(mdd, mdd.from_tuples(tuples(input)), input, r, count, &result);
    FiniteSet expected{{encode(0, 0, 0), encode(1, 1, -1)},
                       {encode(0, 2, 2), encode(1, 3, 1)}};
    require(result == expected, "NS2 next-c or correlated-input fixture");
  }
  {
    a111::MDD mdd(2);
    FiniteSet input{{0, 1}, {1, 0}};
    Relations r(2);
    // Same y, different c, and same c, different y: neither may be projected
    // away before cyclic neighboring c values have been attached.
    r[0][0] = {{0, -1}, {0, 1}, {2, 1}, {0, -1}};
    r[0][1] = {{1, 2}, {1, -1}};
    r[1][0] = {{3, 0}, {2, 0}};
    r[1][1] = {{1, 2}, {3, -1}, {1, 2}};
    check_image(mdd, mdd.from_tuples(tuples(input)), input, r, count);
    // Same input root, changed relation: cached images cannot survive a layer
    // change unless the actual transition relation is part of the cache key.
    r[0][0].clear(); r[1][0].clear();
    FiniteSet result;
    check_image(mdd, mdd.from_tuples(tuples(input)), input, r, count, &result);
    require(result.empty(), "stale image cache across changed local relations");
  }
}

static FiniteSet random_set(std::mt19937_64& rng, size_t n, bool diagonal) {
  if (diagonal && n >= 2) return {Tuple(n, 0), Tuple(n, 1)};
  FiniteSet result;
  const size_t attempts = rng() % 25;
  for (size_t k = 0; k < attempts; ++k) {
    Tuple w(n);
    for (auto& x : w) x = Label(rng() % 3);
    result.insert(std::move(w));
  }
  return result;
}

static Relations random_relations(std::mt19937_64& rng, const FiniteSet& inputs,
                                  size_t n, Counts& count) {
  Relations r(n);
  for (size_t s = 0; s < n; ++s) {
    std::set<Label> domain;
    for (const auto& w : inputs) domain.insert(w[s]);
    for (Label x : domain) {
      const unsigned k = unsigned(rng() % 4);
      auto& choices = r[s][x];
      for (unsigned j = 0; j < k; ++j)
        choices.push_back({uint32_t(rng() % 4), int(rng() % 4) - 1});
      if (!choices.empty() && rng() % 3 == 0) {
        choices.push_back(choices.front());
        ++count.duplicate_rows;
      }
    }
  }
  return r;
}

static void random_case(std::mt19937_64& rng, size_t index, Counts& count) {
  const size_t n = 1 + index % 6;
  FiniteSet a = random_set(rng, n, index % 4 == 0);
  FiniteSet b = random_set(rng, n, false);
  a111::MDD mdd(n);
  const auto ar = mdd.from_tuples(tuples(a));
  const auto br = mdd.from_tuples(tuples(b));
  FiniteSet united = a;
  united.insert(b.begin(), b.end());
  auto ur = mdd.unite(ar, br);
  require(enumerate(mdd, ur, n) == united, "random union differs from std::set union");
  require(ur == mdd.unite(br, ar), "canonical union not commutative");
  require(ur == mdd.from_tuples(tuples(united)), "union canonical root mismatch");
  require(ar == mdd.unite(ar, ar), "random idempotent union");
  auto shuffled = tuples(united);
  if (!shuffled.empty()) shuffled.push_back(shuffled.front());
  std::shuffle(shuffled.begin(), shuffled.end(), rng);
  require(ur == mdd.from_tuples(shuffled), "construction-order/duplicate dependence");
  ++count.union_cases;

  auto r1 = random_relations(rng, a, n, count);
  FiniteSet output1;
  auto image1 = check_image(mdd, ar, a, r1, count, &output1);
  FiniteSet next_domain = a;
  next_domain.insert(output1.begin(), output1.end());
  auto r2 = random_relations(rng, next_domain, n, count);
  check_image(mdd, ar, a, r2, count);
  if (n <= 4 && output1.size() <= 2000)
    check_image(mdd, image1, output1, r2, count);
}

static void guard_fixtures(Counts& count) {
  bool threw = false;
  try {
    a111::MDD tiny(6, 3);
    tiny.singleton({1, 2, 3, 4, 5, 6});
  } catch (const std::exception& e) {
    require(std::string(e.what()).find("cap") != std::string::npos,
            std::string("unexpected node-limit exception: ") + e.what());
    threw = true;
  }
  require(threw, "node cap silently returned a mathematical answer");
  ++count.guard_cases;

  a111::MDD mdd(6);
  FiniteSet input{Tuple(6, 0), Tuple(6, 1)};
  Relations r(6);
  for (size_t s = 0; s < 6; ++s)
    for (Label x : {Label(0), Label(1)})
      r[s][x] = {{0, -1}, {1, 0}, {2, 1}};
  auto root = mdd.from_tuples(tuples(input));
  check_image(mdd, root, input, r, count);
  auto local = [&](size_t s, Label x) -> const std::vector<a111::Choice>& {
    return row(r, s, x);
  };
  a111::MDD fresh(6);
  auto fresh_root = fresh.from_tuples(tuples(input));
  threw = false;
  try { (void)a111::cyclic_image(fresh, fresh_root, local, encode, 1); }
  catch (const std::exception& e) {
    require(std::string(e.what()).find("cap") != std::string::npos,
            std::string("unexpected work-limit exception: ") + e.what());
    threw = true;
  }
  require(threw, "work cap silently returned a mathematical answer");
  ++count.guard_cases;
}

int main(int argc, char** argv) {
  try {
    unsigned cases = 2500;
    if (argc > 2) throw std::runtime_error("usage: mdd_selftest [random_cases]");
    if (argc == 2) {
      std::string arg = argv[1];
      require(!arg.empty() && arg.find_first_not_of("0123456789") == std::string::npos,
              "random_cases must be a positive integer");
      const auto value = std::stoull(arg);
      require(value > 0 && value <= 10000, "random_cases must be in 1..10000");
      cases = unsigned(value);
    }
    Counts count;
    union_fixture(count);
    cyclic_fixtures(count);
    std::mt19937_64 rng(111);
    for (unsigned i = 0; i < cases; ++i) random_case(rng, i, count);
    guard_fixtures(count);
    require(count.empty_images > 0 && count.nonempty_images > 0,
            "image corpus lacks an empty or nonempty case");
    std::cout << "MDD_FINITE_SET_CONTROLS PASS random_cases=" << cases
              << " union_cases=" << count.union_cases
              << " image_cases=" << count.image_cases
              << " correlated_inputs=" << count.correlated_inputs
              << " raw_local_choice_tuples=" << count.raw_choice_tuples
              << " image_tuples=" << count.image_tuples
              << " duplicate_rows=" << count.duplicate_rows
              << " empty_images=" << count.empty_images
              << " nonempty_images=" << count.nonempty_images
              << " guard_cases=" << count.guard_cases << '\n';
    return 0;
  } catch (const std::exception& e) {
    std::cerr << "MDD_FINITE_SET_CONTROLS FAIL " << e.what() << '\n';
    return 1;
  }
}
