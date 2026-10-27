// External verifier: supplied DFA is untrusted. Arithmetic rows are derived
// here, and all three obligations use direct finite products, not a minimizer.
#include "exterior_invariant.hpp"
#include <chrono>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>

namespace agent111_exterior {
using namespace a111x;

static uint64_t integer(const std::string& token) {
  if (token.empty()) throw std::invalid_argument("missing integer");
  uint64_t value = 0;
  for (char c : token) {
    if (c < '0' || c > '9') throw std::invalid_argument("integer must contain decimal digits only");
    unsigned digit = static_cast<unsigned>(c - '0');
    if (value > (UINT64_MAX - digit) / 10) throw std::invalid_argument("integer overflow");
    value = 10 * value + digit;
  }
  return value;
}
static std::string token(std::istream& input) {
  std::string value;
  if (!(input >> value)) throw std::invalid_argument("truncated invariant input");
  return value;
}
static void expect(std::istream& input, const char* expected) {
  if (token(input) != expected) throw std::invalid_argument(std::string("expected token ") + expected);
}
static uint64_t number(std::istream& input) { return integer(token(input)); }

struct Model {
  int base = 0;
  uint32_t period = 0;
  std::string e, g;
  DFA invariant;
  size_t transitions = 0;

  Symbol encode(uint32_t phase, int l, int h, int y) const {
    return uint64_t(phase) * (4 * base) + l * (2 * base) + h * base + y;
  }
  void validate_symbol(Symbol symbol) const {
    uint64_t phase = symbol / (4 * base);
    int y = symbol % base;
    if (phase >= period || (g[phase] == '0' && y != 0))
      throw std::invalid_argument("symbol outside typed exterior alphabet");
  }
  Word root() const {
    Word result;
    for (uint32_t t = 0; t < period; ++t) {
      int overflow = g[t] - '0'; result.push_back(encode(t, 0, overflow, overflow));
    }
    return result;
  }
  Word terminal() const {
    Word result;
    for (uint32_t t = 0; t < period; ++t) {
      int carry = e[t] - '0';
      result.push_back(encode(t, carry, 1 - carry, g[t] == '1' ? (base - 1) * carry : 0));
    }
    return result;
  }
};

static Model read_model(std::istream& input, const Limits& limits) {
  expect(input, "P196_EXTERIOR_INVARIANT"); expect(input, "1");
  Model model;
  expect(input, "base"); uint64_t base = number(input);
  if (base < 2 || base > 62) throw std::invalid_argument("supported base is 2..62");
  model.base = static_cast<int>(base);
  expect(input, "period"); uint64_t period = number(input);
  if (!period || period >= UINT32_MAX - 1) throw std::invalid_argument("period outside supported integer domain");
  if (period + 1 > limits.states) throw Limit("root DFA state cap");
  model.period = static_cast<uint32_t>(period);
  expect(input, "e"); model.e = token(input);
  expect(input, "g"); model.g = token(input);
  for (const auto* stream : {&model.e, &model.g})
    if (stream->size() != period || stream->find_first_not_of("01") != std::string::npos)
      throw std::invalid_argument("e/g must be binary strings of the declared period");
  if (model.g.find('1') == std::string::npos)
    throw std::invalid_argument("zero-overflow unit is outside the positive-FIRST scope");
  expect(input, "states"); uint64_t states = number(input);
  if (!states || states >= UINT32_MAX) throw std::invalid_argument("DFA state count outside integer domain");
  if (states > limits.states) throw Limit("input DFA state cap");
  model.invariant.nodes.resize(static_cast<size_t>(states));
  expect(input, "start"); uint64_t start = number(input);
  if (start >= states) throw std::invalid_argument("start outside DFA states");
  model.invariant.start = static_cast<State>(start);
  expect(input, "accept"); uint64_t accepting = number(input);
  if (accepting > states) throw std::invalid_argument("accepting count exceeds states");
  for (uint64_t i = 0; i < accepting; ++i) {
    uint64_t state = number(input);
    if (state >= states || model.invariant.nodes[state].accept)
      throw std::invalid_argument("invalid or duplicate accepting state");
    model.invariant.nodes[state].accept = true;
  }
  expect(input, "transitions"); uint64_t edges = number(input);
  if (edges > limits.edges) throw Limit("input DFA edge cap");
  model.transitions = static_cast<size_t>(edges);
  for (uint64_t i = 0; i < edges; ++i) {
    uint64_t from = number(input), symbol = number(input), to = number(input);
    if (from >= states || to >= states) throw std::invalid_argument("transition endpoint outside DFA");
    model.validate_symbol(symbol);
    model.invariant.nodes[from].edges.push_back({symbol, static_cast<State>(to)});
  }
  expect(input, "end");
  std::string trailing;
  if (input >> trailing) throw std::invalid_argument("unexpected trailing input");
  for (auto& node : model.invariant.nodes) {
    std::sort(node.edges.begin(), node.edges.end());
    for (size_t i = 1; i < node.edges.size(); ++i)
      if (node.edges[i - 1].first == node.edges[i].first)
        throw std::invalid_argument("duplicate or conflicting deterministic label");
  }
  return model;
}

// Independent scalar arithmetic. Rows are never read from the candidate.
// x is the current temporal coefficient; h is the next high-side carry.
// The returned x_next is matched to the following row's x, including wrap.
struct Arithmetic {
  const Model& model;
  bool first;
  std::unordered_map<Symbol, std::vector<Row>> cache;
  Arithmetic(const Model& m, bool initial) : model(m), first(initial) {}
  const std::vector<Row>& rows(Symbol symbol) {
    auto old = cache.find(symbol);
    if (old != cache.end()) return old->second;
    model.validate_symbol(symbol);
    int b = model.base;
    uint32_t phase = static_cast<uint32_t>(symbol / (4 * b));
    int within = symbol % (4 * b);
    int l_old = within / (2 * b), h_old = (within / b) % 2, y_old = within % b;
    std::vector<Row> result;
    for (int x = first ? 1 : 0; x <= 2 * b - 2; ++x) {
      int l_new = (x + l_old) / b, left_digit = (x + l_old) % b;
      for (int h_new = 0; h_new <= 1; ++h_new) {
        if ((x + h_new) / b != h_old) continue;
        int right_digit = (x + h_new) % b;
        int next_x = left_digit + (model.g[phase] == '1' ? y_old : right_digit);
        int next_y = model.g[phase] == '1' ? right_digit : 0;
        result.push_back({x, model.encode(phase, l_new, h_new, next_y), next_x});
      }
    }
    return cache.emplace(symbol, std::move(result)).first->second;
  }
};

// Reverse the OLD/NEW symbol relation, preserving the incoming/outgoing
// temporal coefficient ports. Reversing those ports would be a different
// transducer. Every valid old symbol of the requested phase is enumerated.
struct ReverseArithmetic {
  const Model& model;
  Arithmetic forward;
  std::vector<uint8_t> complete;
  std::unordered_map<Symbol, std::vector<Row>> cache;
  explicit ReverseArithmetic(const Model& m) : model(m), forward(m, false), complete(m.period, 0) {}
  const std::vector<Row>& rows(Symbol symbol) {
    model.validate_symbol(symbol);
    uint32_t phase = static_cast<uint32_t>(symbol / (4 * model.base));
    if (!complete[phase]) {
      int last_y = model.g[phase] == '1' ? model.base - 1 : 0;
      for (int l = 0; l <= 1; ++l) for (int h = 0; h <= 1; ++h)
        for (int y = 0; y <= last_y; ++y) {
          Symbol old = model.encode(phase, l, h, y);
          for (const Row& row : forward.rows(old))
            cache[row.output].push_back({row.incoming, old, row.outgoing});
        }
      complete[phase] = 1;
    }
    return cache[symbol];
  }
};

static void word_json(const Word& word) {
  std::cout << '[';
  for (size_t i = 0; i < word.size(); ++i) std::cout << (i ? "," : "") << word[i];
  std::cout << ']';
}
static void result_line(const char* obligation, const Result& result, bool backward = false) {
  std::cout << "OBLIGATION name=" << obligation << " status=" << (result.ok ? "proved" : "failed")
            << " product_states=" << result.stats.states << " product_edges=" << result.stats.edges
            << " work=" << result.stats.work << " direction=" << (backward ? "backward" : "forward") << '\n';
  if (!result.ok) {
    std::cout << "COUNTEREXAMPLE obligation=" << obligation << " word=";
    word_json(result.word); std::cout << " input="; word_json(result.input); std::cout << " rows=[";
    for (size_t i = 0; i < result.rows.size(); ++i) {
      const Row& row = result.rows[i];
      std::cout << (i ? "," : "") << '[' << row.incoming << ',' << row.output << ',' << row.outgoing << ']';
    }
    std::cout << "]\n";
  }
  std::cout.flush();
}
template<class Table>
static void replay_image_counterexample(const DFA& source, const DFA& target,
                                       Table& arithmetic, const Result& result, bool intersection = false) {
  if (result.ok) return;
  size_t size = result.word.size();
  if (!size || result.input.size() != size || result.rows.size() != size ||
      !accepts(source, result.input) || accepts(target, result.word) != intersection)
    throw std::logic_error("invalid product counterexample language endpoints");
  for (size_t i = 0; i < size; ++i) {
    const auto& choices = arithmetic.rows(result.input[i]);
    if (result.rows[i].output != result.word[i] ||
        result.rows[i].outgoing != result.rows[(i + 1) % size].incoming ||
        std::find(choices.begin(), choices.end(), result.rows[i]) == choices.end())
      throw std::logic_error("invalid product counterexample cyclic rows");
  }
}

int main(int argc, char** argv) {
  Limits limits;
  bool backward = false;
  try {
    if (argc < 2) throw std::invalid_argument("usage: exterior_invariant INPUT [-backward -states-cap N -edges-cap N -work-cap N]");
    for (int i = 2; i < argc; ++i) {
      std::string option = argv[i];
      if (option == "-backward") {
        if (backward) throw std::invalid_argument("duplicate -backward");
        backward = true; continue;
      }
      if (option != "-states-cap" && option != "-edges-cap" && option != "-work-cap")
        throw std::invalid_argument("unknown verifier option");
      if (++i == argc) throw std::invalid_argument("missing verifier limit");
      uint64_t value = integer(argv[i]);
      if (!value) throw std::invalid_argument("verifier limits must be positive");
      if (option == "-states-cap") {
        if (value >= UINT32_MAX) throw std::invalid_argument("state cap exceeds state identifier domain");
        limits.states = static_cast<size_t>(value);
      } else if (option == "-edges-cap") limits.edges = static_cast<size_t>(value);
      else limits.work = value;
    }
    std::ifstream file;
    std::istream* input = &std::cin;
    if (std::string(argv[1]) != "-") {
      file.open(argv[1]);
      if (!file) throw std::invalid_argument("cannot open invariant input");
      input = &file;
    }
    Model model = read_model(*input, limits);
    DFA root = positive_powers(model.root()), terminal = positive_powers(model.terminal());
    std::cout << "EXTERIOR_INPUT base=" << model.base << " period=" << model.period
              << " states=" << model.invariant.nodes.size() << " transitions=" << model.transitions
              << " scope=positive_unit_repetitions arithmetic=derived_directly direction="
              << (backward ? "backward" : "forward") << '\n';
    auto started = std::chrono::steady_clock::now();

    if (backward) {
      Result terminal_subset = included(terminal, model.invariant, limits);
      if (!terminal_subset.ok && (!accepts(terminal, terminal_subset.word) || accepts(model.invariant, terminal_subset.word)))
        throw std::logic_error("invalid terminal-inclusion counterexample");
      result_line("TERMINAL", terminal_subset, true);
      if (!terminal_subset.ok) {
        std::cout << "REJECTED_INVARIANT obligation=TERMINAL direction=backward interpretation=language_counterexample\n";
        return 1;
      }
      ReverseArithmetic reverse_rows(model);
      Result predecessor = cyclic_image_included(model.invariant, model.invariant,
          [&](Symbol s) -> const std::vector<Row>& { return reverse_rows.rows(s); }, limits);
      replay_image_counterexample(model.invariant, model.invariant, reverse_rows, predecessor);
      result_line("PREDECESSOR", predecessor, true);
      if (!predecessor.ok) {
        std::cout << "REJECTED_INVARIANT obligation=PREDECESSOR direction=backward interpretation=language_counterexample\n";
        return 1;
      }
      Arithmetic positive_rows(model, true);
      Result first_disjoint = cyclic_image_disjoint(root, model.invariant,
          [&](Symbol s) -> const std::vector<Row>& { return positive_rows.rows(s); }, limits);
      replay_image_counterexample(root, model.invariant, positive_rows, first_disjoint, true);
      result_line("FIRST_DISJOINT", first_disjoint, true);
      if (!first_disjoint.ok) {
        std::cout << "REJECTED_INVARIANT obligation=FIRST_DISJOINT direction=backward interpretation=not_an_actual_B_witness\n";
        return 1;
      }
      double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
      std::cout << "VALID_INVARIANT direction=backward terminal_subset=proved predecessor_closed=proved first_disjoint=proved"
                << " scope=all_positive_unit_repetitions sec=" << seconds << '\n';
      return 0;
    }

    Arithmetic first_rows(model, true);
    Result first = cyclic_image_included(root, model.invariant,
        [&](Symbol s) -> const std::vector<Row>& { return first_rows.rows(s); }, limits);
    replay_image_counterexample(root, model.invariant, first_rows, first);
    result_line("FIRST", first);
    if (!first.ok) {
      std::cout << "REJECTED_INVARIANT obligation=FIRST direction=forward interpretation=language_counterexample\n"; return 1;
    }

    Arithmetic generic_rows(model, false);
    Result generic = cyclic_image_included(model.invariant, model.invariant,
        [&](Symbol s) -> const std::vector<Row>& { return generic_rows.rows(s); }, limits);
    replay_image_counterexample(model.invariant, model.invariant, generic_rows, generic);
    result_line("GENERIC", generic);
    if (!generic.ok) {
      std::cout << "REJECTED_INVARIANT obligation=GENERIC direction=forward interpretation=language_counterexample\n"; return 1;
    }

    Result disjunction = disjoint(terminal, model.invariant, limits);
    if (!disjunction.ok && (!accepts(terminal, disjunction.word) || !accepts(model.invariant, disjunction.word)))
      throw std::logic_error("invalid terminal intersection counterexample");
    result_line("TERMINAL", disjunction);
    if (!disjunction.ok) {
      std::cout << "REJECTED_INVARIANT obligation=TERMINAL direction=forward interpretation=not_an_actual_B_witness\n"; return 1;
    }
    double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    std::cout << "VALID_INVARIANT first_subset=proved generic_closed=proved terminal_disjoint=proved"
              << " scope=all_positive_unit_repetitions direction=forward sec=" << seconds << '\n';
    return 0;
  } catch (const Limit& error) {
    std::cerr << "UNDECIDED: direction=" << (backward ? "backward" : "forward") << ' ' << error.what() << '\n'; return 3;
  } catch (const std::bad_alloc&) {
    std::cerr << "UNDECIDED: direction=" << (backward ? "backward" : "forward") << " allocation limit\n"; return 3;
  } catch (const std::invalid_argument& error) {
    std::cerr << "INVALID_OR_UNSUPPORTED: direction=" << (backward ? "backward" : "forward") << ' ' << error.what() << '\n'; return 2;
  } catch (const std::exception& error) {
    std::cerr << "VERIFIER_ERROR: direction=" << (backward ? "backward" : "forward") << ' ' << error.what() << '\n'; return 4;
  }
}
} // namespace agent111_exterior

int main(int argc, char** argv) { return agent111_exterior::main(argc, argv); }
