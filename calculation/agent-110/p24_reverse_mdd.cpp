// Exact backward exterior-cut reachability, including complete correlations.
// Agent110: independent reverse construction for Agent101's P24 center target.
// Agent117 retains primary fixed-e completion; Agent108 retains forward MDD.
// Positional equations: neutral_band/structure/bauto.cpp. Neutral padding:
// Agent7/114. Correlated MDD motivation and exact interning/union: Agents118/108.
// The reverse tiles below are derived directly, without importing their code.
//
// A block begins at overflow and contains its following nonoverflow phases.
// Its symbol is L + (H << length) + (Y << (2*length)). Given a target
// (A,Q,Z), a coefficient x and old low carry l must satisfy
// floor((x+l)/b)=A. The old reverse carry is floor((x+Q)/b).
// At overflow (x+Q)%b=Z, and x_next=(x+l)%b+oldY; elsewhere
// x_next=(x+l)%b+(x+Q)%b. The coefficient ports close around all blocks.
// Every input MDD path is retained throughout preimage construction.
//
// R0 is the single fixed-e terminal; R(n+1)=Pre_INTERIOR(Rn).
// A neutral column gives the terminal a self-loop, so Rn is nested.
// Exact canonical root equality is a full reachability fixed point.
// FIRST is separate and requires every coefficient positive. A FIRST
// successor in Rn reconstructs n+1 columns and an actual padded B cycle.
// Caps, failed validation, incomplete images and malformed input are UNDECIDED.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <new>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#include <sys/resource.h>
#include "count256.hpp"

namespace {
using Id = std::uint32_t;
using Word = std::vector<std::uint32_t>;
using Arc = std::pair<std::uint32_t, Id>;
using Count = agent110::Count256;
using Clock = std::chrono::steady_clock;
struct Stop { std::string reason; };

std::uint64_t natural(const std::string& s) {
    if (s.empty()) throw std::invalid_argument("empty integer");
    std::uint64_t v = 0;
    for (char c : s) {
        if (c < '0' || c > '9') throw std::invalid_argument("invalid integer");
        const auto d = static_cast<unsigned>(c - '0');
        if (v > (std::numeric_limits<std::uint64_t>::max() - d) / 10)
            throw std::invalid_argument("integer overflow");
        v = 10 * v + d;
    }
    return v;
}

std::string decimal(Count v) {
    return v.decimal();
}

struct Options {
    unsigned base = 10;
    std::string e = "010100110100101011001011";
    std::string g = "110001001000110001001000";
    unsigned depth = 100;
    std::uint64_t nodes = 2000000;
    std::uint64_t operations = 500000000;
    unsigned seconds = 120;
    unsigned memory_mib = 2048;
    std::uint64_t export_cap = 1000000;
    int export_layer = -1;
    bool first = false;
    bool preimage = false;
    bool dump_root = false;
};

Options parse(int argc, char** argv) {
    Options o;
    int at = 1;
    if (at < argc && argv[at][0] != '-') {
        if (argc < 4) throw std::invalid_argument("expected BASE E G");
        auto b = natural(argv[at++]);
        if (b < 2 || b > 32) throw std::invalid_argument("base outside 2..32");
        o.base = static_cast<unsigned>(b);
        o.e = argv[at++]; o.g = argv[at++];
    }
    for (; at < argc; ++at) {
        const std::string flag = argv[at];
        if (flag == "--first") { o.first = true; continue; }
        if (flag == "--preimage") { o.preimage = true; continue; }
        if (flag == "--dump-root") { o.dump_root = true; continue; }
        if (++at >= argc) throw std::invalid_argument("missing option argument");
        const auto n = natural(argv[at]);
        if (flag == "--layers" || flag == "--depth") {
            if (n > 100000) throw std::invalid_argument("depth outside 0..100000");
            o.depth = static_cast<unsigned>(n);
        } else if (flag == "--nodes") o.nodes = n;
        else if (flag == "--operations") o.operations = n;
        else if (flag == "--seconds") {
            if (n == 0 || n > 1500) throw std::invalid_argument("seconds outside 1..1500");
            o.seconds = static_cast<unsigned>(n);
        } else if (flag == "--memory-mib") {
            if (n < 64 || n > 4096) throw std::invalid_argument("memory outside 64..4096 MiB");
            o.memory_mib = static_cast<unsigned>(n);
        } else if (flag == "--export-cap") o.export_cap = n;
        else if (flag == "--export-layer") {
            if (n > 100000) throw std::invalid_argument("export depth outside range");
            o.export_layer = static_cast<int>(n);
        } else throw std::invalid_argument("unknown option");
    }
    if (o.e.empty() || o.e.size() > 64 || o.e.size() != o.g.size() ||
        o.e.find_first_not_of("01") != std::string::npos ||
        o.g.find_first_not_of("01") != std::string::npos ||
        o.g.find('1') == std::string::npos)
        throw std::invalid_argument("E/G require equal positive periods <=64 and positive G");
    if (o.nodes < 2 || o.nodes >= std::numeric_limits<Id>::max() ||
        !o.operations || !o.export_cap || o.export_cap > 10000000)
        throw std::invalid_argument("invalid resource cap");
    if (static_cast<unsigned>(o.first) + static_cast<unsigned>(o.preimage) +
        static_cast<unsigned>(o.export_layer >= 0) > 1)
        throw std::invalid_argument("multiple export modes");
    if (o.export_layer >= 0) o.depth = std::max(o.depth, static_cast<unsigned>(o.export_layer));
    return o;
}

void memory_limit(unsigned mib) {
    rlimit limit{};
    if (getrlimit(RLIMIT_AS, &limit)) throw std::runtime_error("getrlimit failed");
    limit.rlim_cur = std::min(limit.rlim_max, static_cast<rlim_t>(mib) * 1024 * 1024);
    if (setrlimit(RLIMIT_AS, &limit)) throw std::runtime_error("setrlimit failed");
}

struct Budget {
    const Options& o;
    Clock::time_point began = Clock::now();
    std::uint64_t operations = 0;
    explicit Budget(const Options& options) : o(options) {}
    double elapsed() const { return std::chrono::duration<double>(Clock::now() - began).count(); }
    void tick() {
        if (operations >= o.operations) throw Stop{"operation_cap"};
        ++operations;
        if ((operations & 4095U) == 0 && elapsed() >= o.seconds) throw Stop{"wall_cap"};
    }
    void timecheck() const { if (elapsed() >= o.seconds) throw Stop{"wall_cap"}; }
};

struct State {
    std::uint64_t low = 0, high = 0;
    std::vector<unsigned> lag;
};
struct Block { unsigned start, length, mask, alphabet; };
struct Tile {
    std::uint32_t source;
    unsigned right;
    std::array<unsigned char, 6> coefficients{};
};
struct InverseTable { std::vector<std::vector<Tile>> by_left; };

class Geometry {
    std::map<std::pair<unsigned, std::uint32_t>, InverseTable> cache;
public:
    const Options& options;
    Budget& budget;
    const unsigned base, period, ports;
    std::vector<Block> blocks;
    std::uint64_t tile_count = 0;
    Geometry(const Options& o, Budget& b)
        : options(o), budget(b), base(o.base), period(static_cast<unsigned>(o.g.size())),
          ports(2 * base - 1) {
        std::vector<unsigned> positions;
        for (unsigned t = 0; t < period; ++t) if (o.g[t] == '1') positions.push_back(t);
        unsigned bits = 0;
        while ((1U << bits) < base) ++bits;
        if (2 * period + bits * positions.size() > 240)
            throw std::invalid_argument("cut-space bound exceeds 2^240");
        for (std::size_t j = 0; j < positions.size(); ++j) {
            const unsigned next = j + 1 < positions.size() ? positions[j + 1] : positions[0] + period;
            const unsigned length = next - positions[j];
            if (length == 0 || length > 6) throw std::invalid_argument("overflow gap outside 1..6");
            blocks.push_back({positions[j], length, (1U << length) - 1,
                              base * (1U << (2 * length))});
        }
    }
    Word encode(const State& s) const {
        // A uint64 mask already has exactly the permitted range at P=64.
        // Short-circuit before any shift by the full word width.
        if ((period < 64 && ((s.low >> period) || (s.high >> period))) ||
            s.lag.size() != blocks.size())
            throw std::invalid_argument("state dimensions");
        Word out;
        for (std::size_t j = 0; j < blocks.size(); ++j) {
            const auto& k = blocks[j];
            if (s.lag[j] >= base) throw std::invalid_argument("lag digit range");
            unsigned lo = 0, hi = 0;
            for (unsigned t = 0; t < k.length; ++t) {
                const auto phase = (k.start + t) % period;
                lo |= static_cast<unsigned>((s.low >> phase) & 1) << t;
                hi |= static_cast<unsigned>((s.high >> phase) & 1) << t;
            }
            out.push_back(lo | (hi << k.length) | (s.lag[j] << (2 * k.length)));
        }
        return out;
    }
    State decode(const Word& word) const {
        if (word.size() != blocks.size()) throw std::invalid_argument("word length");
        State out;
        for (std::size_t j = 0; j < blocks.size(); ++j) {
            const auto& k = blocks[j]; const auto s = word[j];
            if (s >= k.alphabet) throw std::invalid_argument("symbol range");
            for (unsigned t = 0; t < k.length; ++t) {
                const auto phase = (k.start + t) % period;
                out.low |= std::uint64_t((s >> t) & 1) << phase;
                out.high |= std::uint64_t((s >> (k.length + t)) & 1) << phase;
            }
            out.lag.push_back(s >> (2 * k.length));
        }
        return out;
    }
    Word terminal() const {
        State s;
        for (unsigned t = 0; t < period; ++t) {
            s.low |= std::uint64_t(options.e[t] == '1') << t;
            s.high |= std::uint64_t(options.e[t] == '0') << t;
        }
        for (const auto& k : blocks) s.lag.push_back((base - 1) * (options.e[k.start] - '0'));
        return encode(s);
    }
    const InverseTable& inverse(unsigned level, std::uint32_t target) {
        const auto& block = blocks.at(level);
        if (target >= block.alphabet) throw std::logic_error("target symbol range");
        const auto key = std::make_pair(block.length, target);
        auto found = cache.find(key);
        if (found != cache.end()) return found->second;
        InverseTable table; table.by_left.resize(ports);
        const unsigned length = block.length, mask = block.mask;
        const unsigned next_low = target & mask, inward = (target >> length) & mask;
        const unsigned reverse_digit = target >> (2 * length);
        for (unsigned initial = 0; initial < ports; ++initial) {
            if ((initial + (inward & 1U)) % base != reverse_digit) continue;
            std::array<unsigned char, 6> xs{};
            std::function<void(unsigned, unsigned, unsigned, unsigned, unsigned)> walk;
            walk = [&](unsigned t, unsigned x, unsigned lo, unsigned hi, unsigned lag) {
                budget.tick();
                if (t == length) {
                    table.by_left[initial].push_back({lo | (hi << length) | (lag << (2 * length)), x, xs});
                    ++tile_count; return;
                }
                const unsigned q = (inward >> t) & 1U;
                const unsigned h = (x + q) / base;
                if (h > 1 || x >= ports) throw std::logic_error("inverse coefficient range");
                xs[t] = static_cast<unsigned char>(x);
                for (unsigned l = 0; l <= 1; ++l) {
                    if ((x + l) / base != ((next_low >> t) & 1U)) continue;
                    const unsigned digit = (x + l) % base;
                    if (t == 0) {
                        for (unsigned y = 0; y < base; ++y)
                            walk(t + 1, digit + y, lo | (l << t), hi | (h << t), y);
                    } else walk(t + 1, digit + (x + q) % base,
                                lo | (l << t), hi | (h << t), lag);
                }
            };
            walk(0, initial, 0, 0, 0);
        }
        return cache.emplace(key, std::move(table)).first->second;
    }
    std::map<Word, std::vector<unsigned>> first_successors() {
        std::map<Word, std::vector<unsigned>> result;
        State target; target.lag.resize(blocks.size());
        std::vector<unsigned> column(period), lag_index(period, 0);
        for (unsigned j = 0; j < blocks.size(); ++j) lag_index[blocks[j].start] = j;
        std::function<void(unsigned, unsigned, unsigned)> visit;
        visit = [&](unsigned t, unsigned x, unsigned initial) {
            budget.tick();
            if (t == period) {
                if (x == initial) result.emplace(encode(target), column);
                return;
            }
            if (x == 0 || x >= ports) return;
            const unsigned g = static_cast<unsigned>(options.g[t] - '0');
            for (unsigned q = 0; q <= 1; ++q) {
                if ((x + q) / base != g) continue;
                const std::uint64_t bit = std::uint64_t(1) << t;
                target.low = (target.low & ~bit) | (std::uint64_t(x / base) << t);
                target.high = (target.high & ~bit) | (std::uint64_t(q) << t);
                if (g) target.lag[lag_index[t]] = (x + q) % base;
                column[t] = x;
                visit(t + 1, x % base + (g ? 1U : (x + q) % base), initial);
            }
        };
        for (unsigned x = 1; x < ports; ++x) visit(0, x, x);
        return result;
    }
};

struct Node { unsigned level; std::vector<Arc> arcs; Count count; };
class Arena {
    Geometry& geometry;
    Budget& budget;
    std::unordered_map<std::uint64_t, std::vector<Id>> unique;
    std::unordered_map<std::uint64_t, Id> unions;
    // Nodes are immutable and IDs are never reused. These exact memo entries
    // remain valid between layers; no frontier membership is inferred from them.
    std::unordered_map<std::uint64_t, Id> preimages;
public:
    std::deque<Node> nodes;
    explicit Arena(Geometry& g) : geometry(g), budget(g.budget) {
        nodes.push_back({0, {}, 0});
        nodes.push_back({static_cast<unsigned>(g.blocks.size()), {}, 1});
    }
    Id intern(unsigned level, std::vector<Arc> arcs) {
        budget.tick();
        arcs.erase(std::remove_if(arcs.begin(), arcs.end(), [](const Arc& x) { return x.second == 0; }), arcs.end());
        if (arcs.empty()) return 0;
        if (level >= geometry.blocks.size()) throw std::logic_error("node level");
        std::uint64_t hash = 14695981039346656037ULL;
        hash = (hash ^ level) * 1099511628211ULL;
        bool first = true; std::uint32_t previous = 0; Count count = 0;
        for (const auto& a : arcs) {
            if ((!first && a.first <= previous) || a.first >= geometry.blocks[level].alphabet ||
                a.second >= nodes.size() || nodes[a.second].level != level + 1)
                throw std::logic_error("malformed canonical arc");
            first = false; previous = a.first;
            hash = (hash ^ a.first) * 1099511628211ULL;
            hash = (hash ^ a.second) * 1099511628211ULL;
            count += nodes[a.second].count;
        }
        auto it = unique.find(hash);
        if (it != unique.end()) for (Id id : it->second)
            if (nodes[id].level == level && nodes[id].arcs == arcs) return id;
        if (nodes.size() >= geometry.options.nodes) throw Stop{"node_cap"};
        const auto id = static_cast<Id>(nodes.size());
        nodes.push_back({level, std::move(arcs), count});
        unique[hash].push_back(id); return id;
    }
    Id unite(Id a, Id b) {
        budget.tick();
        if (a == b || b == 0) return a;
        if (a == 0) return b;
        if (a > b) std::swap(a, b);
        if (nodes[a].level != nodes[b].level) throw std::logic_error("union levels");
        const auto key = (std::uint64_t(a) << 32) | b;
        auto hit = unions.find(key); if (hit != unions.end()) return hit->second;
        const auto& x = nodes[a].arcs; const auto& y = nodes[b].arcs;
        std::vector<Arc> out; out.reserve(x.size() + y.size());
        std::size_t i = 0, j = 0;
        while (i < x.size() || j < y.size()) {
            if (j == y.size() || (i < x.size() && x[i].first < y[j].first)) out.push_back(x[i++]);
            else if (i == x.size() || y[j].first < x[i].first) out.push_back(y[j++]);
            else { out.emplace_back(x[i].first, unite(x[i].second, y[j].second)); ++i; ++j; }
        }
        const auto answer = intern(nodes[a].level, std::move(out));
        unions.emplace(key, answer); return answer;
    }
    Id singleton(const Word& word) {
        if (word.size() != geometry.blocks.size()) throw std::invalid_argument("word width");
        Id id = 1;
        for (std::size_t j = word.size(); j-- > 0; ) id = intern(static_cast<unsigned>(j), {{word[j], id}});
        return id;
    }
    bool contains(Id root, const Word& word) const {
        if (word.size() != geometry.blocks.size()) return false;
        for (auto symbol : word) {
            if (root < 2) return false;
            const auto& arcs = nodes[root].arcs;
            auto it = std::lower_bound(arcs.begin(), arcs.end(), Arc{symbol, 0});
            if (it == arcs.end() || it->first != symbol) return false;
            root = it->second;
        }
        return root == 1;
    }
    Id preimage(Id root) {
        const auto ports = geometry.ports;
        std::function<Id(Id, unsigned, unsigned)> visit;
        visit = [&](Id node, unsigned required, unsigned initial) -> Id {
            budget.tick();
            if (node == 0) return 0;
            if (node == 1) return required == initial ? 1 : 0;
            const auto key = (std::uint64_t(node) * ports + required) * ports + initial;
            auto hit = preimages.find(key); if (hit != preimages.end()) return hit->second;
            std::map<std::uint32_t, Id> output;
            const auto level = nodes[node].level;
            for (const auto& a : nodes[node].arcs) {
                const auto& tiles = geometry.inverse(level, a.first).by_left[required];
                for (const auto& tile : tiles) {
                    budget.tick();
                    const auto child = visit(a.second, tile.right, initial);
                    if (child == 0) continue;
                    auto old = output.find(tile.source);
                    if (old == output.end()) output.emplace(tile.source, child);
                    else old->second = unite(old->second, child);
                }
            }
            const auto answer = intern(level, std::vector<Arc>(output.begin(), output.end()));
            preimages.emplace(key, answer); return answer;
        };
        Id answer = 0;
        for (unsigned initial = 0; initial < ports; ++initial) answer = unite(answer, visit(root, initial, initial));
        return answer;
    }
    std::size_t image_cache_size() const { return preimages.size(); }
    std::size_t union_cache_size() const { return unions.size(); }
    void dump(Id root, unsigned depth, const std::string& status, bool fixed_point) const {
        std::unordered_map<Id, Id> remap{{0,0},{1,1}};
        std::vector<Id> originals{0,1};
        std::function<Id(Id)> visit = [&](Id old) -> Id {
            auto hit = remap.find(old); if (hit != remap.end()) return hit->second;
            for (const auto& arc : nodes[old].arcs) visit(arc.second);
            const auto next = static_cast<Id>(originals.size());
            originals.push_back(old); remap.emplace(old, next); return next;
        };
        const Id exported_root = visit(root);
        std::cout << "{\"type\":\"CERTIFICATE\",\"base\":" << geometry.base
                  << ",\"e\":\"" << geometry.options.e << "\",\"g\":\"" << geometry.options.g
                  << "\",\"depth\":" << depth << ",\"status\":\"" << status
                  << "\",\"fixed_point\":" << (fixed_point ? "true" : "false")
                  << ",\"states\":\"" << decimal(nodes[root].count) << "\",\"blocks\":[";
        for (std::size_t j = 0; j < geometry.blocks.size(); ++j) {
            if (j) std::cout << ',';
            std::cout << "{\"start\":" << geometry.blocks[j].start
                      << ",\"length\":" << geometry.blocks[j].length << '}';
        }
        std::cout << "],\"root\":" << exported_root << ",\"nodes\":[";
        for (std::size_t j = 0; j < originals.size(); ++j) {
            if (j) std::cout << ',';
            const auto& node = nodes[originals[j]];
            std::cout << "{\"level\":" << node.level << ",\"arcs\":[";
            for (std::size_t k = 0; k < node.arcs.size(); ++k) {
                if (k) std::cout << ',';
                std::cout << '[' << node.arcs[k].first << ',' << remap.at(node.arcs[k].second) << ']';
            }
            std::cout << "]}";
        }
        std::cout << "]}\n";
    }
    std::pair<Word, std::vector<unsigned>> successor(Id target_root, const Word& source) {
        const auto ports = geometry.ports;
        Word target(source.size()); std::vector<unsigned> column(geometry.period);
        std::unordered_set<std::uint64_t> failed;
        std::function<bool(Id, unsigned, unsigned)> visit;
        visit = [&](Id node, unsigned required, unsigned initial) {
            budget.tick();
            if (!node) return false;
            if (node == 1) return required == initial;
            const auto key = (std::uint64_t(node) * ports + required) * ports + initial;
            if (failed.count(key)) return false;
            const auto level = nodes[node].level;
            for (const auto& a : nodes[node].arcs)
                for (const auto& tile : geometry.inverse(level, a.first).by_left[required]) {
                    if (tile.source != source[level]) continue;
                    if (!visit(a.second, tile.right, initial)) continue;
                    target[level] = a.first;
                    const auto& block = geometry.blocks[level];
                    for (unsigned t = 0; t < block.length; ++t)
                        column[(block.start + t) % geometry.period] = tile.coefficients[t];
                    return true;
                }
            failed.insert(key); return false;
        };
        for (unsigned initial = 0; initial < ports; ++initial)
            if (visit(target_root, initial, initial)) return {target, column};
        throw std::logic_error("preimage member lacks successor witness");
    }
    std::vector<State> export_states(Id root) {
        if (nodes[root].count > geometry.options.export_cap) throw Stop{"export_cap"};
        std::vector<State> states; Word word;
        std::function<void(Id)> visit = [&](Id node) {
            budget.tick();
            if (!node) return;
            if (node == 1) { states.push_back(geometry.decode(word)); return; }
            for (const auto& a : nodes[node].arcs) { word.push_back(a.first); visit(a.second); word.pop_back(); }
        };
        visit(root);
        std::sort(states.begin(), states.end(), [](const State& a, const State& b) {
            if (a.low != b.low) return a.low < b.low;
            if (a.high != b.high) return a.high < b.high;
            return a.lag < b.lag;
        });
        return states;
    }
};

void print_state(const State& s) {
    std::cout << '[' << s.low << ',' << s.high << ",[";
    for (std::size_t j = 0; j < s.lag.size(); ++j) { if (j) std::cout << ','; std::cout << s.lag[j]; }
    std::cout << "]]";
}
void print_states(const std::vector<State>& states) {
    std::cout << '[';
    for (std::size_t j = 0; j < states.size(); ++j) { if (j) std::cout << ','; print_state(states[j]); }
    std::cout << "]\n";
}

class Input {
    std::istream& in;
public:
    explicit Input(std::istream& stream) : in(stream) {}
    int peek() { in >> std::ws; return in.peek(); }
    void token(char expected) { if (peek() != expected) throw std::invalid_argument("malformed state JSON"); in.get(); }
    std::uint64_t number() {
        if (peek() < '0' || peek() > '9') throw std::invalid_argument("noninteger state entry");
        std::string value;
        while (in.peek() >= '0' && in.peek() <= '9') value += static_cast<char>(in.get());
        return natural(value);
    }
    std::vector<State> states(std::uint64_t cap) {
        std::vector<State> out; token('[');
        if (peek() != ']') for (;;) {
            if (out.size() >= cap) throw Stop{"input_set_cap"};
            State s; token('['); s.low = number(); token(','); s.high = number(); token(','); token('[');
            if (peek() != ']') for (;;) {
                auto n = number(); if (n > 32) throw std::invalid_argument("lag entry range");
                s.lag.push_back(static_cast<unsigned>(n));
                if (peek() != ',') break;
                token(',');
            }
            token(']'); token(']'); out.push_back(std::move(s));
            if (peek() != ',') break;
            token(',');
        }
        token(']'); if (peek() != std::char_traits<char>::eof()) throw std::invalid_argument("trailing JSON");
        return out;
    }
};

std::pair<std::vector<unsigned>, unsigned> normalize(unsigned base, const std::vector<unsigned>& word, unsigned carry) {
    std::vector<unsigned> digits;
    for (auto x : word) { const auto n = x + carry; digits.push_back(n % base); carry = n / base; }
    return {digits, carry};
}

void validate_witness(const Geometry& g, const std::vector<std::vector<unsigned>>& rows) {
    if (rows.size() != g.period || rows[0].empty()) throw std::logic_error("witness dimensions");
    const auto width = rows[0].size();
    for (unsigned t = 0; t < g.period; ++t) {
        const auto& word = rows[t];
        if (word.size() != width || word.front() == 0) throw std::logic_error("witness first boundary");
        for (auto x : word) if (x >= g.ports) throw std::logic_error("witness coefficient");
        auto low = normalize(g.base, word, 0);
        auto reversed = word; std::reverse(reversed.begin(), reversed.end());
        auto high = normalize(g.base, reversed, 1 - low.second);
        if (low.second != static_cast<unsigned>(g.options.e[t] - '0') ||
            high.second != static_cast<unsigned>(g.options.g[t] - '0'))
            throw std::logic_error("witness carry mismatch");
        std::reverse(high.first.begin(), high.first.end());
        if (high.second) {
            low.first.push_back((g.base - 1) * (1 - low.second));
            high.first.insert(high.first.begin(), 1);
        }
        auto expected = rows[(t + 1) % g.period];
        if (high.second) expected.push_back(g.base - 1);
        if (expected.size() != low.first.size() || expected.size() != high.first.size())
            throw std::logic_error("witness raw width");
        for (std::size_t j = 0; j < expected.size(); ++j)
            if (low.first[j] + high.first[j] != expected[j]) throw std::logic_error("witness raw equation");
    }
}

void print_witness(Geometry& g, Arena& a, const std::vector<Id>& roots,
                   Word current, const std::vector<unsigned>& first_column) {
    std::vector<std::vector<unsigned>> columns{first_column};
    for (std::size_t depth = roots.size() - 1; depth > 0; --depth) {
        auto step = a.successor(roots[depth - 1], current);
        current = std::move(step.first); columns.push_back(std::move(step.second));
    }
    if (current != g.terminal()) throw std::logic_error("witness terminal mismatch");
    std::vector<std::vector<unsigned>> rows(g.period);
    for (const auto& column : columns)
        for (unsigned t = 0; t < g.period; ++t) rows[t].push_back(column[t]);
    validate_witness(g, rows);
    std::cout << "{\"type\":\"WITNESS\",\"base\":" << g.base << ",\"e\":\"" << g.options.e
              << "\",\"g\":\"" << g.options.g << "\",\"width\":" << columns.size() << ",\"B_t\":[";
    for (unsigned t = 0; t < g.period; ++t) {
        if (t) std::cout << ',';
        std::cout << '[';
        for (std::size_t j = 0; j < rows[t].size(); ++j) { if (j) std::cout << ','; std::cout << rows[t][j]; }
        std::cout << ']';
    }
    std::cout << "],\"u\":[";
    for (unsigned t = 0; t < g.period; ++t) { if (t) std::cout << ','; std::cout << g.options.g[t]; }
    std::cout << "],\"literal_replay\":true}\n" << std::flush;
}

int run(const Options& o) {
    memory_limit(o.memory_mib); Budget budget(o); Geometry g(o, budget); Arena a(g);
    Id root = 0; unsigned depth = 0; std::string status = "UNDECIDED", reason;
    bool complete = false, fixed_point = false; std::size_t first_count = 0;
    try {
        if (o.preimage) {
            Input input(std::cin);
            for (const auto& s : input.states(o.export_cap)) root = a.unite(root, a.singleton(g.encode(s)));
            root = a.preimage(root); print_states(a.export_states(root)); return 0;
        }
        auto first = g.first_successors(); first_count = first.size();
        if (o.first) {
            std::vector<State> out;
            for (const auto& entry : first) out.push_back(g.decode(entry.first));
            std::sort(out.begin(), out.end(), [](const State& x, const State& y) {
                if (x.low != y.low) return x.low < y.low;
                if (x.high != y.high) return x.high < y.high;
                return x.lag < y.lag;
            });
            print_states(out); return 0;
        }
        root = a.singleton(g.terminal()); std::vector<Id> roots{root};
        Count previous_count = 0;
        for (;;) {
            budget.timecheck();
            complete = true;
            if (o.export_layer == static_cast<int>(depth)) { print_states(a.export_states(root)); return 0; }
            if (o.export_layer < 0) {
                std::cout << "{\"type\":\"LAYER\",\"depth\":" << depth << ",\"root\":" << root
                    << ",\"states\":\"" << decimal(a.nodes[root].count) << "\",\"novel_states\":\""
                    << decimal(a.nodes[root].count - previous_count) << "\",\"nodes\":" << a.nodes.size()
                    << ",\"tiles\":" << g.tile_count << ",\"operations\":" << budget.operations
                    << ",\"image_cache\":" << a.image_cache_size() << ",\"union_cache\":" << a.union_cache_size()
                    << ",\"seconds\":" << budget.elapsed() << "}\n" << std::flush;
                for (const auto& entry : first) if (a.contains(root, entry.first)) {
                    print_witness(g, a, roots, entry.first, entry.second);
                    status = "ACCEPT"; reason = "positive_first_boundary_reached"; goto finished;
                }
            }
            if (depth >= o.depth) { reason = "depth_cap"; break; }
            previous_count = a.nodes[root].count; complete = false;
            const auto next = a.preimage(root);
            if (!a.contains(next, g.terminal()) || a.unite(root, next) != next)
                throw std::logic_error("neutral self-loop or nested preimage failure");
            complete = true;
            if (next == root && o.export_layer < 0) {
                status = "EXHAUSTED"; reason = "exact_backward_fixed_point"; fixed_point = true; break;
            }
            root = next; roots.push_back(root); ++depth;
        }
    } catch (const Stop& stop) { reason = stop.reason; }
      catch (const std::bad_alloc&) { reason = "memory_cap"; }
finished:
    rusage usage{}; getrusage(RUSAGE_SELF, &usage);
    if (o.dump_root) a.dump(root, depth, status, fixed_point);
    std::cout << "{\"type\":\"RESULT\",\"status\":\"" << status << "\",\"reason\":\"" << reason
        << "\",\"base\":" << o.base << ",\"period\":" << o.e.size() << ",\"e\":\"" << o.e
        << "\",\"g\":\"" << o.g << "\",\"last_complete_depth\":" << depth
        << ",\"last_complete_states\":\"" << decimal(a.nodes[root].count)
        << "\",\"image_complete\":" << (complete ? "true" : "false")
        << ",\"first_states\":" << first_count << ",\"nodes\":" << a.nodes.size()
        << ",\"tiles\":" << g.tile_count << ",\"operations\":" << budget.operations
        << ",\"image_cache\":" << a.image_cache_size() << ",\"union_cache\":" << a.union_cache_size()
        << ",\"peak_rss_kib\":" << usage.ru_maxrss << ",\"seconds\":" << budget.elapsed() << "}\n";
    return status == "UNDECIDED" ? 2 : 0;
}
} // namespace

int main(int argc, char** argv) {
    std::cout << std::setprecision(10);
    try { return run(parse(argc, argv)); }
    catch (const std::bad_alloc&) {
        std::cout << "{\"type\":\"RESULT\",\"status\":\"UNDECIDED\",\"reason\":\"memory_cap\"}\n"; return 2;
    }
    catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        std::cout << "{\"type\":\"RESULT\",\"status\":\"UNDECIDED\",\"reason\":\"invalid_input_or_validation_failure\"}\n";
        return 2;
    }
}
