// Independent exterior-cycle decision by explicit carry tuples.
//
// Derivation from one ordinary column, least significant first:
//   a = low incoming carry, r = required reverse outgoing carry,
//   q = guessed reverse incoming carry, z = previous reverse digit.
// For coefficient x, require (x+q)/base = r. Then
//   x_next = (x+a)%base + (overflow ? z : (x+q)%base),
//   a_next_column = (x+a)/base, r_next_column = q,
//   z_next_column = (x+q)%base on overflow phases.
// Close this coefficient trajectory around the supplied time word.
//
// The initial column has a=0, r=overflow, z=1, and positive coefficients.
// Later columns permit zero. These two modes are deliberately separate.
// A terminal tuple requires a+r=1, z=(base-1)*a on overflow phases.
// Such a tuple admits an infinite neutral tail. A finite B cycle can be
// padded to common width; conversely stripping terminal neutral symbols
// from an accepted common-width witness recovers its literal B cycle.
// Empty B is represented by the positive neutral padding, never by a
// forbidden leading zero. An optional witness is checked independently
// using direct whole-word normalization before it is printed.
//
// No packed integer state keys, depth ceiling, first-coordinate prefilter,
// or dependency on another author's exterior-search implementation.
// EXHAUSTED means the reachable fixed point was completely traversed.
// Resource stops are UNDECIDED; --prefix-width is expressly bounded only.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <new>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
#include <sys/resource.h>

namespace {
constexpr std::size_t max_period = 32;
constexpr std::uint32_t no_parent = std::numeric_limits<std::uint32_t>::max();
using Column = std::array<std::uint32_t, max_period>;
using Clock = std::chrono::steady_clock;

struct State {
    std::array<std::uint8_t, max_period> low{};
    std::array<std::uint8_t, max_period> reverse{};
    Column lag{};
    bool operator==(const State& other) const {
        return low == other.low && reverse == other.reverse && lag == other.lag;
    }
};

struct StateHash {
    std::size_t operator()(const State& state) const noexcept {
        // Hashing combines tuple entries; equality always compares the arrays.
        std::size_t hash = 0xcbf29ce484222325ULL;
        for (std::size_t t = 0; t < max_period; ++t) {
            for (auto value : {std::uint32_t(state.low[t]),
                               std::uint32_t(state.reverse[t]), state.lag[t]}) {
                hash ^= value + 0x9e3779b9U;
                hash *= 0x100000001b3ULL;
                hash ^= hash >> 31;
            }
        }
        return hash;
    }
};

struct Options {
    std::uint32_t base = 0;
    std::string overflow;
    std::uint64_t max_states = 2000000;
    double seconds = 60.0;
    std::uint64_t memory_mib = 4096;
    std::uint32_t prefix_width = 0; // zero means unlimited
    bool witness = false;
};

std::uint64_t natural(const std::string& value) {
    if (value.empty() || value.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument("expected a nonnegative decimal integer");
    std::size_t consumed = 0;
    auto number = std::stoull(value, &consumed);
    if (consumed != value.size()) throw std::invalid_argument("invalid integer");
    return number;
}

Options parse(int argc, char** argv) {
    if (argc < 3) throw std::invalid_argument(
        "usage: exterior_tuple BASE G [--states N] [--seconds S] "
        "[--memory-mib M] [--witness] [--prefix-width N]");
    Options options;
    const auto base = natural(argv[1]);
    if (base < 2 || base > 62) throw std::invalid_argument("base must be 2..62");
    options.base = static_cast<std::uint32_t>(base);
    options.overflow = argv[2];
    if (options.overflow.empty() || options.overflow.size() > max_period ||
        options.overflow.find_first_not_of("01") != std::string::npos)
        throw std::invalid_argument("G must contain 1..32 binary digits");
    for (int argument = 3; argument < argc; ++argument) {
        const std::string flag = argv[argument];
        if (flag == "--witness") { options.witness = true; continue; }
        if (++argument >= argc) throw std::invalid_argument("missing option value");
        const std::string value = argv[argument];
        if (flag == "--states") options.max_states = natural(value);
        else if (flag == "--seconds") {
            std::size_t consumed = 0;
            options.seconds = std::stod(value, &consumed);
            if (consumed != value.size()) throw std::invalid_argument("invalid seconds");
        } else if (flag == "--memory-mib") options.memory_mib = natural(value);
        else if (flag == "--prefix-width") {
            const auto width = natural(value);
            if (width == 0 || width >= no_parent)
                throw std::invalid_argument("prefix width must be 1..4294967294");
            options.prefix_width = static_cast<std::uint32_t>(width);
        } else throw std::invalid_argument("unknown option: " + flag);
    }
    if (options.max_states == 0 || options.max_states >= no_parent)
        throw std::invalid_argument("state budget must be 1..4294967294");
    if (!std::isfinite(options.seconds) || options.seconds <= 0 || options.seconds > 1190)
        throw std::invalid_argument("wall budget must be positive and at most 1190 seconds");
    if (options.memory_mib < 64 || options.memory_mib > 8192)
        throw std::invalid_argument("memory budget must be 64..8192 MiB");
    return options;
}

void set_memory_budget(std::uint64_t mib) {
    struct rlimit current{};
    if (getrlimit(RLIMIT_AS, &current) != 0)
        throw std::runtime_error("could not inspect address-space limit");
    const rlim_t requested = static_cast<rlim_t>(mib * 1024ULL * 1024ULL);
    current.rlim_cur = std::min(current.rlim_max, requested);
    if (setrlimit(RLIMIT_AS, &current) != 0)
        throw std::runtime_error("could not set address-space limit");
}

struct Stop { const char* status; };
struct Node { State state; std::uint32_t width; };
struct Parent { std::uint32_t previous; Column coefficients; };
struct Accepted { std::uint32_t node; std::uint32_t width; };

class Search {
    const Options options;
    const std::size_t period;
    const Clock::time_point start = Clock::now();
    std::unordered_map<State, std::uint32_t, StateHash> index;
    std::vector<Node> nodes;
    std::vector<Parent> parents;
    std::map<std::string, Accepted> accepted;
    std::size_t next_expand = 0;
    std::size_t first_frontier = 0;
    std::uint32_t deepest = 0;
    std::uint64_t temporal_nodes = 0;
    std::uint64_t generated_columns = 0;
    std::uint64_t initial_coefficients = 0;
    bool boundary_complete = false;
    bool partial_expansion = false;
    std::string status = "EXHAUSTED";

    void budget() const {
        if (elapsed() >= options.seconds) throw Stop{"TIMEOUT_UNDECIDED"};
    }

    bool terminal(const State& state) const {
        for (std::size_t t = 0; t < period; ++t) {
            if (state.low[t] + state.reverse[t] != 1) return false;
            if (options.overflow[t] == '1' &&
                state.lag[t] != (options.base - 1) * state.low[t]) return false;
        }
        return true;
    }

    void emit(const State& state, const Column& column,
              std::uint32_t previous, std::uint32_t width) {
        ++generated_columns;
        if (index.find(state) != index.end()) return;
        // The FIRST boundary counts as one state but is not in the interior map.
        if (1 + nodes.size() >= options.max_states) throw Stop{"STATE_CAP_UNDECIDED"};
        const auto id = static_cast<std::uint32_t>(nodes.size());
        nodes.push_back({state, width});
        if (options.witness) parents.push_back({previous, column});
        index.emplace(state, id);
        deepest = std::max(deepest, width);
        if (terminal(state)) {
            std::string e;
            for (std::size_t t = 0; t < period; ++t) e += char('0' + state.low[t]);
            accepted.emplace(e, Accepted{id, width});
        }
    }

    void time_column(const State& source, bool first, std::uint32_t initial,
                     std::size_t t, std::uint32_t coefficient, State& target,
                     Column& column, std::uint32_t previous, std::uint32_t width) {
        if ((++temporal_nodes & 2047U) == 0) budget();
        if (first && coefficient == 0) return;
        const auto low_total = coefficient + source.low[t];
        const auto low_digit = low_total % options.base;
        for (std::uint32_t inward = 0; inward <= 1; ++inward) {
            const auto high_total = coefficient + inward;
            if (high_total / options.base != source.reverse[t]) continue;
            const auto high_digit = high_total % options.base;
            const auto following = low_digit +
                (options.overflow[t] == '1' ? source.lag[t] : high_digit);
            target.low[t] = static_cast<std::uint8_t>(low_total / options.base);
            target.reverse[t] = static_cast<std::uint8_t>(inward);
            target.lag[t] = options.overflow[t] == '1' ? high_digit : 0;
            column[t] = coefficient;
            if (t + 1 == period) {
                if (following == initial) emit(target, column, previous, width);
            } else {
                time_column(source, first, initial, t + 1, following,
                            target, column, previous, width);
            }
        }
    }

    void expand(const State& source, bool first,
                std::uint32_t previous, std::uint32_t width) {
        State target{};
        Column column{};
        for (std::uint32_t coefficient = first ? 1 : 0;
             coefficient <= 2 * options.base - 2; ++coefficient) {
            ++initial_coefficients;
            budget();
            time_column(source, first, coefficient, 0, coefficient,
                        target, column, previous, width);
        }
    }

    std::pair<std::vector<std::uint32_t>, std::uint32_t>
    normalize(const std::vector<std::uint32_t>& word, std::uint32_t carry) const {
        std::vector<std::uint32_t> digits;
        for (auto x : word) {
            const auto total = x + carry;
            digits.push_back(total % options.base);
            carry = total / options.base;
        }
        return {digits, carry};
    }

    std::vector<std::vector<std::uint32_t>> witness(const std::string& e,
                                                   const Accepted& hit) const {
        std::vector<Column> columns;
        auto node = hit.node;
        while (node != no_parent) {
            const auto& link = parents.at(node);
            columns.push_back(link.coefficients);
            node = link.previous;
        }
        std::reverse(columns.begin(), columns.end());
        if (columns.size() != hit.width) throw std::runtime_error("parent width mismatch");
        std::vector<std::vector<std::uint32_t>> words(period);
        for (std::size_t t = 0; t < period; ++t) {
            for (const auto& column : columns) words[t].push_back(column[t]);
            while (!words[t].empty() && words[t].back() == options.base - 1)
                words[t].pop_back();
        }
        for (std::size_t t = 0; t < period; ++t) {
            const auto& word = words[t];
            if (!word.empty() && word.front() == 0)
                throw std::runtime_error("recovered exterior has a zero head");
            auto low = normalize(word, 0);
            auto reversed = word;
            std::reverse(reversed.begin(), reversed.end());
            auto high = normalize(reversed, 1 - low.second);
            if (low.second != std::uint32_t(e[t] - '0') ||
                high.second != std::uint32_t(options.overflow[t] - '0'))
                throw std::runtime_error("recovered exterior carry mismatch");
            std::reverse(high.first.begin(), high.first.end());
            if (high.second) {
                low.first.push_back((options.base - 1) * (1 - low.second));
                high.first.insert(high.first.begin(), 1);
            }
            std::vector<std::uint32_t> actual;
            for (std::size_t j = 0; j < low.first.size(); ++j)
                actual.push_back(low.first[j] + high.first.at(j));
            while (!actual.empty() && actual.back() == options.base - 1) actual.pop_back();
            if (actual != words[(t + 1) % period])
                throw std::runtime_error("recovered exterior successor mismatch");
        }
        return words;
    }

public:
    explicit Search(Options given) : options(std::move(given)), period(options.overflow.size()) {}

    double elapsed() const {
        return std::chrono::duration<double>(Clock::now() - start).count();
    }

    void run() {
        try {
            State boundary{};
            for (std::size_t t = 0; t < period; ++t) {
                boundary.reverse[t] = options.overflow[t] - '0';
                boundary.lag[t] = options.overflow[t] == '1' ? 1 : 0;
            }
            partial_expansion = true;
            expand(boundary, true, no_parent, 1);
            partial_expansion = false;
            boundary_complete = true;
            first_frontier = nodes.size();
            while (next_expand < nodes.size()) {
                budget();
                if (options.prefix_width && nodes[next_expand].width >= options.prefix_width) {
                    status = "BOUNDED_WIDTH_ONLY";
                    break;
                }
                // Copy: adding successor nodes may relocate the vector.
                const Node node = nodes[next_expand];
                partial_expansion = true;
                expand(node.state, false, static_cast<std::uint32_t>(next_expand), node.width + 1);
                partial_expansion = false;
                ++next_expand;
            }
        } catch (const Stop& stop) {
            status = stop.status;
        } catch (const std::bad_alloc&) {
            status = "MEMORY_CAP_UNDECIDED";
            index.clear(); // Release duplicate key storage before reporting.
        }
        if (!boundary_complete) first_frontier = nodes.size();
    }

    void print() const {
        struct rusage usage{};
        getrusage(RUSAGE_SELF, &usage);
#ifdef __APPLE__
        const double rss_mib = usage.ru_maxrss / 1048576.0;
#else
        const double rss_mib = usage.ru_maxrss / 1024.0;
#endif
        std::cout << std::setprecision(9)
            << "{\"base\":" << options.base << ",\"period\":" << period
            << ",\"g\":\"" << options.overflow << "\",\"status\":\"" << status
            << "\",\"complete\":" << (status == "EXHAUSTED" ? "true" : "false")
            << ",\"states\":" << 1 + nodes.size()
            << ",\"state_convention\":\"one FIRST seed plus distinct INTERIOR tuples\""
            << ",\"interior_states\":" << nodes.size()
            << ",\"first_frontier\":" << first_frontier
            << ",\"boundary_expansion_completed\":" << (boundary_complete ? "true" : "false")
            << ",\"processed_interior\":" << next_expand
            << ",\"frontier\":" << nodes.size() - next_expand
            << ",\"partial_expansion\":" << (partial_expansion ? "true" : "false")
            << ",\"max_depth\":" << deepest
            << ",\"generated_columns\":" << generated_columns
            << ",\"temporal_nodes\":" << temporal_nodes
            << ",\"initial_coefficients\":" << initial_coefficients
            << ",\"prefix_width\":" << options.prefix_width
            << ",\"state_budget\":" << options.max_states
            << ",\"wall_budget_seconds\":" << options.seconds
            << ",\"memory_budget_mib\":" << options.memory_mib
            << ",\"peak_rss_mib\":" << rss_mib
            << ",\"elapsed_seconds\":" << elapsed()
            << ",\"accepts\":[";
        bool comma = false;
        for (const auto& entry : accepted) {
            if (comma) std::cout << ',';
            comma = true;
            std::cout << "{\"e\":\"" << entry.first << "\",\"width\":" << entry.second.width;
            if (options.witness) {
                const auto words = witness(entry.first, entry.second);
                std::cout << ",\"B\":[";
                for (std::size_t t = 0; t < words.size(); ++t) {
                    if (t) std::cout << ',';
                    std::cout << '[';
                    for (std::size_t j = 0; j < words[t].size(); ++j) {
                        if (j) std::cout << ',';
                        std::cout << words[t][j];
                    }
                    std::cout << ']';
                }
                std::cout << "],\"direct_word_replay\":true";
            }
            std::cout << '}';
        }
        std::cout << "]}\n";
    }
};
} // namespace

int main(int argc, char** argv) {
    try {
        auto options = parse(argc, argv);
        set_memory_budget(options.memory_mib);
        Search search(std::move(options));
        search.run();
        search.print();
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "exterior_tuple: " << error.what() << '\n';
        return 2;
    }
}
