#ifndef AGENT116_EXTERIOR_REGULAR_WITNESS_HPP
#define AGENT116_EXTERIOR_REGULAR_WITNESS_HPP

// Invert a sequence of exact cyclic block images to recover full B words.
// This header is generic over the caller's DFA, block relation and budget.
// It should be included at file scope; concrete DFA types need not exist yet.
//
// Each inverse problem fixes one original coefficient for the WHOLE temporal
// word. Dynamic-programming states are (input DFA state,current coefficient)
// at a particular output-letter position. Intermediate accepting input states
// are expanded normally; acceptance requires both input finality and closure
// to the original coefficient only after consuming the complete output word.
// FIRST positivity is requested only while inverting the first spatial image.
//
// The recovered words retain their common neutral-padded width. Direct replay
// checks every carry and literal equality F(B_t)=B_{t+1} ++ h^{g_t}, h=base-1.
// These are exterior witnesses only, without a center or Lychrel assertion.
// Resource limits propagate the caller's budget exception. A missing preimage
// or a failed replay is a logic error, never a negative mathematical result.

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace agent116::witness {

using Letter = std::uint64_t;

struct Witness {
    std::vector<std::vector<unsigned>> B;
    std::string e, g; // the complete repeated temporal streams
    unsigned width = 0;
    unsigned repetitions = 0;
    std::vector<unsigned> u; // equal to the actual overflow bits for padded B
    bool initial_word_replay = false;
    bool direct_word_replay = false;
    std::uint64_t inverse_dp_states = 0; // cumulative work, including failed trials
    std::uint64_t inverse_initial_trials = 0;
    std::size_t maximum_inverse_dp_states = 0;
};

namespace detail {

inline void require(bool condition, const char* explanation) {
    if (!condition) throw std::logic_error(explanation);
}

inline std::size_t product(std::size_t a, std::size_t b) {
    if (b && a > std::numeric_limits<std::size_t>::max() / b)
        throw std::overflow_error("witness size arithmetic overflow");
    return a * b;
}

template<class Symbol>
Letter encode(Symbol symbol) {
    return (Letter(symbol.phase) << 32) | symbol.cfg;
}

struct Pair {
    std::size_t input_state;
    unsigned coefficient;
    bool operator==(const Pair& other) const {
        return input_state == other.input_state && coefficient == other.coefficient;
    }
};
struct PairHash {
    std::size_t operator()(const Pair& pair) const noexcept {
        return pair.input_state * std::size_t(0x9e3779b97f4a7c15ULL)
               ^ (std::size_t(pair.coefficient) * 65537U);
    }
};

constexpr std::size_t no_parent = std::numeric_limits<std::size_t>::max();
struct Record {
    Pair state;
    std::size_t parent = no_parent;
    Letter input_letter = 0;
    std::array<unsigned char, 5> coefficients{};
    unsigned char length = 0;
};
struct Inverse {
    std::vector<Letter> input_word;
    std::vector<unsigned> column;
};

template<class DFA, class Relation, class Budget>
Inverse invert(const DFA& automaton, const std::vector<Letter>& output_word,
               bool first, Relation& relation, unsigned base, Budget& budget,
               Witness& statistics) {
    require(!output_word.empty(), "cannot invert an empty temporal word");
    require(!automaton.nodes.empty() && automaton.start < automaton.nodes.size(),
            "invalid input DFA for witness reconstruction");
    const unsigned maximum = 2 * (base - 1);
    for (unsigned initial = first ? 1 : 0; initial <= maximum; ++initial) {
        budget.check();
        ++statistics.inverse_initial_trials;
        std::vector<Record> records;
        std::vector<std::size_t> frontier;
        budget.states(1, true);
        records.push_back({{automaton.start, initial}, no_parent, 0, {}, 0});
        frontier.push_back(0);
        ++statistics.inverse_dp_states;
        statistics.maximum_inverse_dp_states = std::max<std::size_t>(
            statistics.maximum_inverse_dp_states, 1);

        for (std::size_t position = 0; position < output_word.size(); ++position) {
            budget.check();
            std::unordered_map<Pair, std::size_t, PairHash> following_index;
            std::vector<std::size_t> following;
            const Letter output = output_word[position];
            for (const auto previous : frontier) {
                // Copy: pushing descendants may relocate the record vector.
                const Record source = records[previous];
                require(source.state.input_state < automaton.nodes.size(),
                        "witness DP reached an invalid input DFA state");
                for (const auto& edge : automaton.nodes[source.state.input_state].edges) {
                    budget.tick();
                    const Letter input = edge.symbol;
                    if ((input >> 32) != (output >> 32)) continue;
                    auto& generator = relation.generator(input);
                    const auto spec = generator.spec();
                    require(spec.length >= 1 && spec.length <= 5,
                            "witness block length outside supported range");
                    auto local = generator.initial_symbol();
                    local.phase = static_cast<std::uint16_t>(input >> 32);
                    local.cfg = static_cast<std::uint32_t>(input);
                    for (const auto& tile : generator.tiles(local, source.state.coefficient, first)) {
                        budget.tick();
                        if (encode(tile.output) != output) continue;
                        const Pair target{edge.to, tile.ending};
                        require(target.input_state < automaton.nodes.size() &&
                                target.coefficient <= maximum,
                                "invalid local witness successor");
                        if (following_index.find(target) != following_index.end()) continue;
                        budget.states(records.size() + 1, true);
                        Record next;
                        next.state = target;
                        next.parent = previous;
                        next.input_letter = input;
                        next.length = spec.length;
                        for (unsigned j = 0; j < spec.length; ++j)
                            next.coefficients[j] = tile.coefficients[j];
                        const auto id = records.size();
                        records.push_back(next);
                        following_index.emplace(target, id);
                        following.push_back(id);
                        ++statistics.inverse_dp_states;
                        statistics.maximum_inverse_dp_states = std::max(
                            statistics.maximum_inverse_dp_states, records.size());
                    }
                }
            }
            frontier.swap(following);
            if (frontier.empty()) break;
        }

        for (const auto ending : frontier) {
            const auto& state = records[ending].state;
            if (state.coefficient != initial || !automaton.nodes[state.input_state].final)
                continue;
            Inverse recovered;
            recovered.input_word.resize(output_word.size());
            std::vector<Record> chosen(output_word.size());
            auto current = ending;
            for (std::size_t position = output_word.size(); position > 0; --position) {
                budget.tick();
                require(current < records.size() && records[current].parent != no_parent,
                        "witness predecessor chain ended too early");
                const auto& item = records[current];
                chosen[position - 1] = item;
                recovered.input_word[position - 1] = item.input_letter;
                current = item.parent;
            }
            require(current == 0 && records[current].state.coefficient == initial,
                    "witness predecessor chain did not return to its initial record");
            unsigned entering = initial;
            for (const auto& item : chosen) {
                require(item.length > 0 && item.coefficients[0] == entering,
                        "local witness input coefficient mismatch");
                for (unsigned j = 0; j < item.length; ++j) {
                    const unsigned coefficient = item.coefficients[j];
                    require(coefficient <= maximum && (!first || coefficient > 0),
                            "local witness violates the coefficient bounds or FIRST");
                    recovered.column.push_back(coefficient);
                }
                entering = item.state.coefficient;
            }
            require(entering == initial, "whole-word coefficient closure failed");
            return recovered;
        }
    }
    throw std::logic_error("accepted target word has no cyclic-image preimage");
}

inline std::pair<std::vector<unsigned>, unsigned>
normalize(unsigned base, const std::vector<unsigned>& word, unsigned carry) {
    std::vector<unsigned> digits;
    digits.reserve(word.size());
    for (const auto coefficient : word) {
        const auto total = coefficient + carry;
        digits.push_back(total % base);
        carry = total / base;
    }
    return {std::move(digits), carry};
}

template<class Budget>
void replay(Witness& witness, unsigned base, Budget& budget) {
    const auto phases = witness.B.size();
    require(phases > 0 && witness.e.size() == phases && witness.g.size() == phases,
            "witness temporal dimensions disagree");
    witness.u.reserve(phases);
    for (std::size_t t = 0; t < phases; ++t) {
        budget.check();
        const auto& word = witness.B[t];
        require(word.size() == witness.width && !word.empty() && word.front() > 0,
                "recovered exterior width or head is invalid");
        for (const auto coefficient : word) {
            budget.tick();
            require(coefficient <= 2 * (base - 1), "recovered exterior coefficient out of range");
        }
        auto low = normalize(base, word, 0);
        std::vector<unsigned> reversed(word.rbegin(), word.rend());
        require(low.second <= 1, "nonbinary recovered exterior carry");
        auto high = normalize(base, reversed, 1 - low.second);
        require(low.second == unsigned(witness.e[t] - '0') &&
                high.second == unsigned(witness.g[t] - '0'),
                "recovered exterior carry stream differs from its target");
        std::reverse(high.first.begin(), high.first.end());
        if (high.second) {
            low.first.push_back((base - 1) * (1 - low.second));
            high.first.insert(high.first.begin(), 1);
        }
        require(low.first.size() == high.first.size(), "exterior raw summand width mismatch");
        std::vector<unsigned> raw;
        raw.reserve(low.first.size());
        for (std::size_t j = 0; j < low.first.size(); ++j) {
            budget.tick();
            raw.push_back(low.first[j] + high.first[j]);
        }
        auto expected = witness.B[(t + 1) % phases];
        expected.insert(expected.end(), high.second, base - 1);
        require(raw == expected, "padded exterior literal successor replay failed");
        witness.u.push_back(high.second);
    }
    witness.direct_word_replay = true;
}

} // namespace detail

template<class History, class Relation, class Budget>
Witness reconstruct(const History& history, const std::vector<Letter>& terminal_unit,
                    unsigned repetitions, unsigned depth, Relation& relation,
                    unsigned base, const std::string& e, const std::string& g,
                    Budget& budget) {
    detail::require(base >= 2 && base <= 32 && repetitions > 0 && depth > 0,
                    "invalid witness reconstruction parameters");
    detail::require(history.size() >= depth && !terminal_unit.empty(),
                    "missing spatial history or terminal block word");
    detail::require(!g.empty() && g.front() == '1' && e.size() == g.size() &&
                    g.find_first_not_of("01") == std::string::npos &&
                    e.find_first_not_of("01") == std::string::npos,
                    "invalid witness target driver");
    const auto phases = detail::product(g.size(), repetitions);
    const auto letters = detail::product(terminal_unit.size(), repetitions);
    // Limit the output certificate itself as well as every retained DP history.
    budget.states(detail::product(phases, depth), true);
    budget.states(letters, true);
    std::vector<Letter> initial_unit;
    std::size_t phase = 0;
    for (const auto symbol : terminal_unit) {
        budget.tick();
        auto& generator = relation.generator(symbol);
        const auto spec = generator.spec();
        detail::require(generator.base() == base && spec.phase == phase &&
                        spec.length > 0 && phase + spec.length <= g.size(),
                        "terminal block types do not partition the target driver");
        detail::require(g[phase] == '1', "target block does not start with overflow");
        unsigned e_mask = 0;
        for (unsigned j = 0; j < spec.length; ++j) {
            detail::require(j == 0 || g[phase + j] == '0', "overflow occurs inside a target block");
            e_mask |= unsigned(e[phase + j] - '0') << j;
        }
        detail::require(detail::encode(generator.terminal_symbol(e_mask)) == symbol,
                        "terminal symbol does not encode the supplied E word");
        initial_unit.push_back(detail::encode(generator.initial_symbol()));
        phase += spec.length;
    }
    detail::require(phase == g.size(), "terminal block word omits temporal phases");

    Witness witness;
    witness.width = depth;
    witness.repetitions = repetitions;
    witness.B.assign(phases, std::vector<unsigned>(depth));
    std::vector<Letter> current;
    current.reserve(letters);
    witness.e.reserve(phases);
    witness.g.reserve(phases);
    for (unsigned repeat = 0; repeat < repetitions; ++repeat) {
        current.insert(current.end(), terminal_unit.begin(), terminal_unit.end());
        witness.e += e;
        witness.g += g;
    }
    for (unsigned spatial = depth; spatial > 0; --spatial) {
        budget.check();
        auto inverse = detail::invert(history[spatial - 1], current, spatial == 1,
                                      relation, base, budget, witness);
        detail::require(inverse.column.size() == phases && inverse.input_word.size() == letters,
                        "inverse image changed the temporal dimensions");
        for (std::size_t t = 0; t < phases; ++t)
            witness.B[t][spatial - 1] = inverse.column[t];
        current = std::move(inverse.input_word);
    }
    for (std::size_t j = 0; j < current.size(); ++j) {
        budget.tick();
        detail::require(current[j] == initial_unit[j % initial_unit.size()],
                        "recovered layer zero is not the initial boundary word repeated k times");
    }
    witness.initial_word_replay = true;
    detail::replay(witness, base, budget);
    return witness;
}

} // namespace agent116::witness

#endif // AGENT116_EXTERIOR_REGULAR_WITNESS_HPP
