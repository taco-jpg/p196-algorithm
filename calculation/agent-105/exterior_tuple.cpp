// Agent 105 independent exterior transfer. Explicit carry/digit arrays.
// No packed state key and no depth cutoff. A restricted first column is a
// separate root vertex; only its successors enter the ordinary visited set.
//
// Build: g++ -O3 -std=c++17 -Wall -Wextra -pedantic exterior_tuple.cpp -o exterior_tuple
// Run:   ./exterior_tuple 11100010000 --base 10 --cap 12000000 --seconds 1200 --witness
// Batch: ./exterior_tuple --batch p23-head-survivors.txt --cap 12000000 --seconds 1200
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <sys/resource.h>
#include <unordered_map>
#include <utility>
#include <vector>

constexpr unsigned MAX_PERIOD = 24;
constexpr uint32_t NO_PARENT = std::numeric_limits<uint32_t>::max();

struct State {
    std::array<uint8_t, MAX_PERIOD> left{};
    std::array<uint8_t, MAX_PERIOD> right{};
    std::array<uint8_t, MAX_PERIOD> previous{};
    bool operator==(const State& o) const {
        return left == o.left && right == o.right && previous == o.previous;
    }
};
static_assert(sizeof(State) == 3 * MAX_PERIOD, "unexpected state padding");

struct StateHash {
    size_t operator()(const State& s) const noexcept {
        // Hashing only; the stored key and equality retain every array byte.
        const auto* bytes = reinterpret_cast<const unsigned char*>(&s);
        uint64_t h = 0x8b8b8b8b1234567ULL;
        for (unsigned i = 0; i < sizeof(State); i += 8) {
            uint64_t q;
            std::memcpy(&q, bytes + i, 8);
            q ^= q >> 30;
            q *= 0xbf58476d1ce4e5b9ULL;
            q ^= q >> 27;
            q *= 0x94d049bb133111ebULL;
            q ^= q >> 31;
            h ^= q + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        }
        return static_cast<size_t>(h);
    }
};

struct Node {
    State state;
    uint32_t parent = NO_PARENT;
    uint32_t depth = 0;
    std::array<uint8_t, MAX_PERIOD> column{};
};

struct Acceptance {
    uint32_t depth = 0;
    std::vector<std::vector<unsigned>> exterior;
    std::string e;
    std::vector<unsigned> trims;
};

struct Result {
    std::string status;
    uint64_t states = 0, transitions = 0, work = 0, frontier = 0;
    uint32_t depth = 0;
    double elapsed = 0;
    long rss_kb = 0;
    bool complete = false;
    std::vector<Acceptance> accepted;
};

class Search {
    unsigned p, base, neutral;
    std::array<uint8_t, MAX_PERIOD> overflow{};
    uint64_t cap;
    double seconds;
    bool want_witness, all_accepts;
    using Clock = std::chrono::steady_clock;
    Clock::time_point started;
    std::vector<Node> nodes;
    std::unordered_map<State, uint32_t, StateHash> visited;
    std::vector<uint32_t> current, next;
    Result answer;
    bool stopped = false;
    State source, target;
    std::array<uint8_t, MAX_PERIOD> column{};
    uint32_t parent = 0, next_depth = 0;
    bool first_column = false;

    double elapsed() const {
        return std::chrono::duration<double>(Clock::now() - started).count();
    }
    bool check_time() {
        if (elapsed() > seconds) {
            answer.status = "TIMEOUT";
            stopped = true;
        }
        return stopped;
    }
    bool terminal(const State& s) const {
        for (unsigned t = 0; t < p; ++t) {
            if (s.left[t] + s.right[t] != 1) return false;
            if (overflow[t] && s.previous[t] != neutral * s.left[t]) return false;
        }
        return true;
    }
    void emit() {
        ++answer.transitions;
        // Count all augmented visited vertices, including the special root.
        if (nodes.size() >= cap) {
            if (visited.find(target) != visited.end()) return;
            answer.status = "CAPPED";
            stopped = true;
            return;
        }
        const auto id = static_cast<uint32_t>(nodes.size());
        if (!visited.emplace(target, id).second) return;
        Node n;
        n.state = target;
        n.parent = parent;
        n.depth = next_depth;
        n.column = column;
        nodes.push_back(n);
        next.push_back(id);
        answer.depth = std::max(answer.depth, next_depth);
    }
    void walk(unsigned t, unsigned x, unsigned x0) {
        if (stopped) return;
        if (((++answer.work) & 32767ULL) == 0 && check_time()) return;
        if (x > 2*neutral || (first_column && x == 0)) return;
        column[t] = static_cast<uint8_t>(x);
        const unsigned forward_digit = (x + source.left[t]) % base;
        target.left[t] = static_cast<uint8_t>((x + source.left[t]) / base);
        for (unsigned inward = 0; inward <= 1; ++inward) {
            if ((x + inward) / base != source.right[t]) continue;
            const unsigned backward_digit = (x + inward) % base;
            target.right[t] = static_cast<uint8_t>(inward);
            target.previous[t] = overflow[t] ? static_cast<uint8_t>(backward_digit) : 0;
            const unsigned successor = forward_digit +
                (overflow[t] ? source.previous[t] : backward_digit);
            if (t + 1 == p) {
                if (successor == x0) emit();
            } else {
                walk(t + 1, successor, x0);
            }
            if (stopped) return;
        }
    }
    void expand(uint32_t id, bool first) {
        // Copy before vector insertion; growth cannot invalidate this source.
        source = nodes[id].state;
        target = State{};
        column.fill(0);
        parent = id;
        next_depth = nodes[id].depth + 1;
        first_column = first;
        for (unsigned x = first ? 1 : 0; x <= 2*neutral && !stopped; ++x) {
            walk(0, x, x);
        }
    }
    std::pair<std::vector<unsigned>, unsigned> normalize(
            const std::vector<unsigned>& a, unsigned carry) {
        std::vector<unsigned> d;
        for (unsigned x : a) {
            d.push_back((x + carry) % base);
            carry = (x + carry) / base;
        }
        return {d, carry};
    }
    Acceptance reconstruct(uint32_t id) {
        Acceptance aresult;
        aresult.depth = nodes[id].depth;
        std::vector<uint32_t> path;
        for (uint32_t u = id; nodes[u].parent != NO_PARENT; u = nodes[u].parent)
            path.push_back(u);
        std::reverse(path.begin(), path.end());
        aresult.exterior.assign(p, {});
        for (uint32_t u : path)
            for (unsigned t = 0; t < p; ++t)
                aresult.exterior[t].push_back(nodes[u].column[t]);
        for (auto& a : aresult.exterior)
            while (!a.empty() && a.back() == neutral) a.pop_back();
        // Independent finite-word audit of the extracted tuple path.
        for (unsigned t = 0; t < p; ++t) {
            const auto& a = aresult.exterior[t];
            const auto& b = aresult.exterior[(t + 1) % p];
            if (!a.empty() && a.front() == 0) throw std::runtime_error("zero exterior head");
            const auto f = normalize(a, 0);
            std::vector<unsigned> rev(a.rbegin(), a.rend());
            const auto r = normalize(rev, 1 - f.second);
            if (r.second != overflow[t]) throw std::runtime_error("wrong witness overflow");
            if (f.second != nodes[id].state.left[t]) throw std::runtime_error("wrong witness carry");
            aresult.e.push_back(static_cast<char>('0' + f.second));
            std::vector<unsigned> dd = f.first;
            std::vector<unsigned> rr(r.first.rbegin(), r.first.rend());
            if (overflow[t]) {
                dd.push_back(neutral * (1 - f.second));
                rr.insert(rr.begin(), 1);
            }
            std::vector<unsigned> raw;
            for (unsigned j = 0; j < dd.size(); ++j) raw.push_back(dd[j] + rr[j]);
            if (raw.size() < b.size() || !std::equal(b.begin(), b.end(), raw.begin()))
                throw std::runtime_error("wrong witness target");
            for (unsigned j = b.size(); j < raw.size(); ++j)
                if (raw[j] != neutral) throw std::runtime_error("wrong neutral witness trim");
            aresult.trims.push_back(static_cast<unsigned>(raw.size() - b.size()));
        }
        return aresult;
    }
    void record_accept(uint32_t id) {
        if (want_witness) answer.accepted.push_back(reconstruct(id));
        else {
            Acceptance a;
            a.depth = nodes[id].depth;
            for (unsigned t = 0; t < p; ++t) a.e.push_back(static_cast<char>('0'+nodes[id].state.left[t]));
            answer.accepted.push_back(std::move(a));
        }
    }

public:
    Search(const std::string& g, unsigned radix, uint64_t limit, double time_limit, bool witnesses, bool enumerate)
        : p(g.size()), base(radix), neutral(radix-1), cap(limit), seconds(time_limit),
          want_witness(witnesses), all_accepts(enumerate) {
        if (!p || p > MAX_PERIOD || g.find_first_not_of("01") != std::string::npos)
            throw std::runtime_error("binary period must have length 1..24");
        if (cap < 2 || cap >= NO_PARENT || !std::isfinite(seconds) || !(seconds > 0) || seconds > 1200)
            throw std::runtime_error("invalid state or time limit");
        if (base < 2 || base > 62) throw std::runtime_error("base must be 2..62");
        for (unsigned t = 0; t < p; ++t) overflow[t] = g[t] - '0';
    }
    Result run() {
        started = Clock::now();
        nodes.reserve(static_cast<size_t>(cap));
        visited.max_load_factor(0.85f);
        visited.reserve(static_cast<size_t>(std::min<uint64_t>(cap, 262144)));
        Node root;
        for (unsigned t = 0; t < p; ++t) {
            root.state.right[t] = overflow[t];
            root.state.previous[t] = overflow[t] ? 1 : 0;
        }
        nodes.push_back(root);
        // The root is not entered in visited: its positive-head rule is special.
        if (terminal(root.state)) {
            answer.status = "ACCEPT";
            record_accept(0);
        } else {
            expand(0, true);
            current.swap(next);
            while (!stopped && !current.empty()) {
                answer.frontier = std::max<uint64_t>(answer.frontier, current.size());
                for (uint32_t id : current) {
                    if (terminal(nodes[id].state)) {
                        record_accept(id);
                        if (!all_accepts) {
                            answer.status = "ACCEPT";
                            stopped = true;
                            break;
                        }
                    }
                    expand(id, false);
                    if (stopped || check_time()) break;
                }
                current.clear();
                current.swap(next);
            }
            if (answer.status.empty()) {
                answer.status = answer.accepted.empty() ? "EXHAUSTED" : "ACCEPT";
                answer.complete = true;
            }
        }
        answer.states = nodes.size();
        answer.elapsed = elapsed();
        struct rusage usage{};
        getrusage(RUSAGE_SELF, &usage);
        answer.rss_kb = usage.ru_maxrss;
        return answer;
    }
};

void print(unsigned base, const std::string& g, const Result& r) {
    std::cout << "{\"base\":" << base << ",\"g\":\"" << g << "\",\"status\":\"" << r.status
              << "\",\"states\":" << r.states << ",\"max_depth\":" << r.depth
              << ",\"max_frontier\":" << r.frontier << ",\"generated_transitions\":" << r.transitions
              << ",\"temporal_calls\":" << r.work << ",\"seconds\":" << std::fixed << std::setprecision(6)
              << r.elapsed << ",\"process_peak_rss_kb\":" << r.rss_kb
              << ",\"complete\":" << (r.complete ? "true" : "false") << ",\"accepted\":[";
    for (unsigned ai = 0; ai < r.accepted.size(); ++ai) {
        if (ai) std::cout << ',';
        const auto& a = r.accepted[ai];
        std::cout << "{\"e\":\"" << a.e << "\",\"depth\":" << a.depth;
        if (!a.exterior.empty()) {
        std::cout << ",\"B\":[";
        for (unsigned t = 0; t < a.exterior.size(); ++t) {
            if (t) std::cout << ',';
            std::cout << '[';
            for (unsigned j = 0; j < a.exterior[t].size(); ++j) {
                if (j) std::cout << ',';
                std::cout << a.exterior[t][j];
            }
            std::cout << ']';
        }
        std::cout << "],\"u\":[";
        for (unsigned t = 0; t < a.trims.size(); ++t) {
            if (t) std::cout << ',';
            std::cout << a.trims[t];
        }
        std::cout << ']';
        }
        std::cout << '}';
    }
    std::cout << "]}" << std::endl;
}

int main(int argc, char** argv) {
    try {
        auto integer_argument = [](const char* text) {
            const std::string s(text);
            if (s.empty() || s.find_first_not_of("0123456789") != std::string::npos)
                throw std::runtime_error("expected an unsigned decimal integer");
            size_t used = 0;
            const auto n = std::stoull(s, &used);
            if (used != s.size()) throw std::runtime_error("invalid integer suffix");
            return n;
        };
        auto time_argument = [](const char* text) {
            const std::string s(text);
            size_t used = 0;
            const double n = std::stod(s, &used);
            if (used != s.size() || !std::isfinite(n) || !(n > 0) || n > 1200)
                throw std::runtime_error("seconds must be finite, positive, and <= 1200");
            return n;
        };
        uint64_t cap = 12000000;
        double seconds = 1200;
        unsigned base = 10;
        bool witness = false, enumerate = false;
        std::string batch, word;
        for (int i = 1; i < argc; ++i) {
            std::string a = argv[i];
            if (a == "--witness") witness = true;
            else if (a == "--all-accepts") enumerate = true;
            else if (a == "--base" && i+1 < argc) {
                const auto n = integer_argument(argv[++i]);
                if (n < 2 || n > 62) throw std::runtime_error("base must be 2..62");
                base = static_cast<unsigned>(n);
            }
            else if (a == "--cap" && i+1 < argc) cap = integer_argument(argv[++i]);
            else if (a == "--seconds" && i+1 < argc) seconds = time_argument(argv[++i]);
            else if (a == "--batch" && i+1 < argc) batch = argv[++i];
            else if (word.empty() && a.find_first_not_of("01") == std::string::npos) word = a;
            else throw std::runtime_error("unrecognized or incomplete argument");
        }
        if (!batch.empty() && !word.empty()) throw std::runtime_error("choose one word or batch");
        // Bound the entire process address space, including hash/node storage.
        constexpr rlim_t MEMORY_LIMIT = static_cast<rlim_t>(4) * 1024 * 1024 * 1024;
        struct rlimit memory{};
        if (getrlimit(RLIMIT_AS, &memory) != 0) throw std::runtime_error("cannot inspect memory limit");
        memory.rlim_cur = std::min(memory.rlim_cur, MEMORY_LIMIT);
        if (setrlimit(RLIMIT_AS, &memory) != 0) throw std::runtime_error("cannot enforce memory limit");
        if (!batch.empty()) {
            std::ifstream input(batch);
            if (!input) throw std::runtime_error("cannot read batch file");
            while (input >> word) print(base, word, Search(word, base, cap, seconds, witness, enumerate).run());
        } else {
            if (word.empty()) throw std::runtime_error("supply a binary word or --batch file");
            print(base, word, Search(word, base, cap, seconds, witness, enumerate).run());
        }
    } catch (const std::bad_alloc&) {
        std::cerr << "RESOURCE_EXHAUSTED: allocation failed; outcome UNDECIDED\n";
        return 3;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 2;
    }
}
