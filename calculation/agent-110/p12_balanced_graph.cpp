// Agent 110: exact center return graph for the documented decimal p12 stream.
// No B witness, decimal certificate, or Lean claim is made by this program.
//
// E=101010010101, G=100010001000; repeat twice, with trims at phases 4,12,20.
// Start at phase 4, immediately before an overflow+trim. The source has width W
// 和 endpoints 9. State ID encodes half(D) in C=[9]++D++[9]:
//        id = sum(D[j]*19^j, j=0..ceil((W-2)/2)-1).
// D is reflected to complete its palindrome; the least power stores D[0].
// Every state is included. No residue or odd-middle-coefficient filter is used.
//
// Build: g++ -O3 -std=c++17 -Wall -Wextra -pedantic p12_balanced_graph.cpp -o p12_graph
// Run:   p12_graph W [--seconds 1500]
// Probe: p12_graph --map W   (stdin IDs; stdout contains exactly "ID NEXT")
// NEXT=-1 means that the specified 24-step legal return fails.

#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <exception>
#include <iostream>
#include <limits>
#include <new>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
using Clock = std::chrono::steady_clock;
constexpr uint32_t NONE = std::numeric_limits<uint32_t>::max();
constexpr int PERIOD = 24;
constexpr int MAX_WIDTH = 14;
constexpr uint64_t MEMORY_LIMIT = 1000000000ULL;
constexpr char ES[] = "101010010101";
constexpr char GS[] = "100010001000";

struct Word {
    std::array<uint8_t, MAX_WIDTH + 2> digit{};
    int size = 0;
};

struct Counts {
    uint64_t evaluated = 0;
    uint64_t initial_flip_valid = 0;
    uint64_t step_attempts = 0;
    uint64_t valid_steps = 0;
    uint64_t completed_24_steps = 0;
    uint64_t return_edges = 0;
    uint64_t carry_failures = 0;
    uint64_t trim_failures = 0;
    uint64_t shape_failures = 0;
    uint64_t finished = 0;
    uint64_t max_path = 0;
    std::vector<std::pair<uint32_t, uint32_t>> edge_examples;
};

struct Context {
    int width;
    int half;
    uint32_t states;
    std::array<int, PERIOD> e{}, g{}, v{};
    std::array<int, PERIOD + 1> length{};
    Clock::time_point started = Clock::now();
    double seconds;

    Context(int W, double limit) : width(W), half((W - 1) / 2), states(1), seconds(limit) {
        if (W < 2 || W > MAX_WIDTH)
            throw std::invalid_argument("supported widths are 2..14");
        uint64_t n = 1;
        for (int i = 0; i < half; ++i) n *= 19;
        // Successors 4N + distances 4N + colors N + a reserved path 4N.
        if (n >= NONE || 13 * n + 16000000ULL > MEMORY_LIMIT)
            throw std::invalid_argument("state or memory budget exceeded");
        states = static_cast<uint32_t>(n);
        length[0] = W;
        for (int t = 0; t < PERIOD; ++t) {
            int original_phase = (t + 4) % PERIOD;
            e[t] = ES[original_phase % 12] - '0';
            g[t] = GS[original_phase % 12] - '0';
            v[t] = original_phase == 4 || original_phase == 12 || original_phase == 20;
            length[t + 1] = length[t] + g[t] - 2 * v[t];
            if (length[t + 1] < W - 1 || length[t + 1] > W)
                throw std::logic_error("invalid balanced width profile");
        }
        if (length[PERIOD] != W || !g[0] || !v[0])
            throw std::logic_error("invalid cyclic starting phase");
    }

    double elapsed() const {
        return std::chrono::duration<double>(Clock::now() - started).count();
    }
    bool timed_out() const { return elapsed() >= seconds; }
};

Word decode(const Context& c, uint32_t id) {
    Word word;
    word.size = c.width;
    word.digit[0] = word.digit[c.width - 1] = 9;
    for (int j = 0; j < c.half; ++j) {
        uint8_t d = static_cast<uint8_t>(id % 19);
        id /= 19;
        word.digit[j + 1] = word.digit[c.width - 2 - j] = d;
    }
    return word;
}

uint32_t encode(const Context& c, const Word& word) {
    if (word.size != c.width || word.digit[0] != 9 || word.digit[c.width - 1] != 9)
        return NONE;
    uint32_t id = 0, power = 1;
    for (int j = 0; j < word.size; ++j) {
        if (word.digit[j] > 18 || word.digit[j] != word.digit[word.size - 1 - j])
            return NONE;
    }
    for (int j = 0; j < c.half; ++j) {
        id += static_cast<uint32_t>(word.digit[j + 1]) * power;
        power *= 19;
    }
    return id < c.states ? id : NONE;
}

enum class Failure { none, carry, trim, shape };

Failure step(const Context& c, int phase, Word& word) {
    if (word.size != c.length[phase] || word.size < 1 || word.size > MAX_WIDTH)
        return Failure::shape;
    std::array<uint8_t, MAX_WIDTH + 2> digits{}, raw{};
    int carry = c.e[phase];
    for (int j = 0; j < word.size; ++j) {
        if (word.digit[j] > 18) return Failure::shape;
        int sum = word.digit[j] + carry;
        digits[j] = static_cast<uint8_t>(sum % 10);
        carry = sum / 10;
    }
    if (carry != 1 - c.e[phase]) return Failure::carry;
    int size = word.size;
    if (c.g[phase]) digits[size++] = static_cast<uint8_t>(9 * c.e[phase]);
    for (int j = 0; j < size; ++j)
        raw[j] = static_cast<uint8_t>(digits[j] + digits[size - 1 - j]);
    int trim = c.v[phase];
    if (trim && (size < 3 || raw[0] != 9 || raw[size - 1] != 9))
        return Failure::trim;
    int result_size = size - 2 * trim;
    if (result_size != c.length[phase + 1] || result_size < 1 || result_size > MAX_WIDTH)
        return Failure::shape;
    word.size = result_size;
    for (int j = 0; j < result_size; ++j) word.digit[j] = raw[j + trim];
    return Failure::none;
}

uint32_t next_state(const Context& c, uint32_t id, Counts* counts = nullptr) {
    Word word = decode(c, id);
    for (int t = 0; t < PERIOD; ++t) {
        if (counts) ++counts->step_attempts;
        Failure failure = step(c, t, word);
        if (failure != Failure::none) {
            if (counts) {
                if (failure == Failure::carry) ++counts->carry_failures;
                else if (failure == Failure::trim) ++counts->trim_failures;
                else ++counts->shape_failures;
            }
            return NONE;
        }
        if (counts) {
            ++counts->valid_steps;
            // At this prescribed source, endpoints 9 force the first trim
            // automatically once the carry flips; these counts coincide.
            if (t == 0) ++counts->initial_flip_valid;
        }
    }
    if (counts) ++counts->completed_24_steps;
    uint32_t result = encode(c, word);
    if (result == NONE && counts) ++counts->shape_failures;
    return result;
}

void summary(const Context& c, const Counts& n, const char* status, const char* reason,
             int cycles, bool complete) {
    std::cout << "{\"status\":\"" << status << "\",\"reason\":\"" << reason
              << "\",\"width\":" << c.width << ",\"states\":" << c.states
              << ",\"evaluated_states\":" << n.evaluated
              << ",\"initial_flip_valid\":" << n.initial_flip_valid
              << ",\"step_attempts\":" << n.step_attempts
              << ",\"valid_steps\":" << n.valid_steps
              << ",\"completed_24_steps\":" << n.completed_24_steps
              << ",\"valid_return_edges\":" << n.return_edges
              << ",\"carry_failures\":" << n.carry_failures
              << ",\"trim_failures\":" << n.trim_failures
              << ",\"shape_failures\":" << n.shape_failures
              << ",\"finished_states\":" << n.finished
              << ",\"max_path_edges\":" << n.max_path
              << ",\"cycles_found\":" << cycles
              << ",\"cycle_scan_complete\":" << (complete ? "true" : "false")
              << ",\"edge_examples\":[";
    for (size_t i = 0; i < n.edge_examples.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << '[' << n.edge_examples[i].first << ',' << n.edge_examples[i].second << ']';
    }
    std::cout << "],\"seconds\":" << c.elapsed() << "}\n";
    std::cout.flush();
}

void print_word(const Word& word) {
    std::cout << '[';
    for (int j = 0; j < word.size; ++j) {
        if (j) std::cout << ',';
        std::cout << static_cast<int>(word.digit[j]);
    }
    std::cout << ']';
}

void print_cycle(const Context& c, const std::vector<uint32_t>& path, size_t first) {
    uint64_t count = path.size() - first;
    // Recheck every return before announcing the center-cycle witness.
    for (size_t j = first; j < path.size(); ++j) {
        uint32_t expected = j + 1 == path.size() ? path[first] : path[j + 1];
        if (next_state(c, path[j]) != expected)
            throw std::logic_error("cycle replay failed");
    }
    std::cout << "{\"type\":\"center_cycle\",\"graph_nodes\":" << count
              << ",\"center_period\":" << count * PERIOD << "}\n";
    uint64_t edge = 0;
    for (size_t j = first; j < path.size(); ++j) {
        Word word = decode(c, path[j]);
        for (int t = 0; t < PERIOD; ++t) {
            Word source = word;
            if (step(c, t, word) != Failure::none)
                throw std::logic_error("center-edge replay failed");
            std::cout << "{\"type\":\"center_edge\",\"edge\":" << edge++
                      << ",\"phase12\":" << (t + 4) % 12
                      << ",\"e\":" << c.e[t] << ",\"g\":" << c.g[t]
                      << ",\"v\":" << c.v[t] << ",\"C\":";
            print_word(source);
            std::cout << ",\"C2\":";
            print_word(word);
            std::cout << "}\n";
        }
    }
    std::cout.flush();
}

int graph(Context& c) {
    Counts n;
    try {
        std::vector<uint32_t> next(c.states, NONE);
        for (uint32_t id = 0; id < c.states; ++id) {
            if ((id & 4095U) == 0 && c.timed_out()) {
                summary(c, n, "UNDECIDED", "wall_time", 0, false);
                return 2;
            }
            next[id] = next_state(c, id, &n);
            ++n.evaluated;
            if (next[id] != NONE) {
                ++n.return_edges;
                if (n.edge_examples.size() < 16) n.edge_examples.emplace_back(id, next[id]);
            }
        }
        if (n.return_edges == 0) {
            n.finished = c.states;
            summary(c, n, "NO_CENTER_CYCLE", "exhausted", 0, true);
            return 0;
        }
        std::vector<uint8_t> color(c.states, 0);
        std::vector<uint32_t> distance(c.states, 0), path;
        path.reserve(c.states);
        uint64_t traversal = 0;
        for (uint32_t initial = 0; initial < c.states; ++initial) {
            if (color[initial]) continue;
            path.clear();
            uint32_t current = initial;
            while (current != NONE && color[current] == 0) {
                if ((traversal++ & 16383ULL) == 0 && c.timed_out()) {
                    summary(c, n, "UNDECIDED", "wall_time", 0, false);
                    return 2;
                }
                color[current] = 1;
                path.push_back(current);
                current = next[current];
            }
            if (current != NONE && color[current] == 1) {
                auto position = std::find(path.begin(), path.end(), current);
                if (position == path.end()) throw std::logic_error("active path mismatch");
                size_t first = static_cast<size_t>(position - path.begin());
                print_cycle(c, path, first);
                summary(c, n, "CENTER_CYCLE", "first_cycle_only", 1, false);
                return 0;
            }
            for (auto it = path.rbegin(); it != path.rend(); ++it) {
                uint32_t id = *it;
                distance[id] = next[id] == NONE ? 0 : distance[next[id]] + 1;
                n.max_path = std::max<uint64_t>(n.max_path, distance[id]);
                color[id] = 2;
                ++n.finished;
            }
        }
        if (n.finished != c.states) throw std::logic_error("incomplete graph traversal");
        summary(c, n, "NO_CENTER_CYCLE", "exhausted", 0, true);
        return 0;
    } catch (const std::bad_alloc&) {
        summary(c, n, "UNDECIDED", "allocation_failed", 0, false);
        return 2;
    }
}

uint64_t unsigned_number(const std::string& token) {
    uint64_t value = 0;
    auto parsed = std::from_chars(token.data(), token.data() + token.size(), value);
    if (parsed.ec != std::errc() || parsed.ptr != token.data() + token.size())
        throw std::invalid_argument("invalid nonnegative integer");
    return value;
}

int map_states(const Context& c) {
    std::string token;
    uint64_t count = 0;
    while (std::cin >> token) {
        uint64_t id = unsigned_number(token);
        if (id >= c.states) throw std::invalid_argument("state ID exceeds the selected width domain");
        if ((count++ & 1023ULL) == 0 && c.timed_out()) {
            std::cerr << "UNDECIDED: wall time limit\n";
            return 2;
        }
        uint32_t target = next_state(c, static_cast<uint32_t>(id));
        std::cout << id << ' ';
        if (target == NONE) std::cout << -1;
        else std::cout << target;
        std::cout << '\n';
    }
    return 0;
}
}  // namespace

int main(int argc, char** argv) {
    bool map = argc >= 2 && std::string(argv[1]) == "--map";
    try {
        int first = map ? 2 : 1;
        if (argc != first + 1 && argc != first + 3)
            throw std::invalid_argument("usage: p12_graph [--map] W [--seconds 1..1500]");
        uint64_t requested = unsigned_number(argv[first]);
        if (requested < 2 || requested > MAX_WIDTH)
            throw std::invalid_argument("supported widths are 2..14");
        uint64_t seconds = 1500;
        if (argc == first + 3) {
            if (std::string(argv[first + 1]) != "--seconds")
                throw std::invalid_argument("expected --seconds");
            seconds = unsigned_number(argv[first + 2]);
            if (seconds == 0 || seconds > 1500)
                throw std::invalid_argument("wall time budget must be 1..1500 seconds");
        }
        Context context(static_cast<int>(requested), static_cast<double>(seconds));
        return map ? map_states(context) : graph(context);
    } catch (const std::exception& error) {
        std::cerr << "UNDECIDED: " << error.what() << '\n';
        if (!map) std::cout << "{\"status\":\"UNDECIDED\",\"reason\":\"invalid_input_or_internal_error\"}\n";
        return 2;
    }
}
