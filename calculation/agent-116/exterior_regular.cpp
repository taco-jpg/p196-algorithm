// Exact exterior cut languages for every positive repetition of a fixed driver.
//
// Letters are typed overflow-gap blocks, not individual temporal phases. A
// cyclic rational image remembers (input DFA state, current coefficient,
// initial coefficient). An accepting input boundary NEVER stops expansion:
// coefficient closure is required only at the end of the whole accepted word.
// FIRST is applied once and requires positive coefficients at every phase.
// Subsequent images allow zero. All language comparisons are exact; hashes
// only index structures whose full contents are compared for equality.
//
// A resource limit or a requested depth bound always returns UNDECIDED.
// This executable supplies computations and witnesses, not a Lean theorem.

#include "exterior_blocks.hpp"
#include "exterior_regular_witness.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <memory>
#include <new>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#include <sys/resource.h>

namespace {
using Id = std::uint32_t;
using Sym = std::uint64_t;
constexpr Id absent = std::numeric_limits<Id>::max();
using Clock = std::chrono::steady_clock;
struct Edge {
    Sym symbol;
    Id to;
    bool operator<(const Edge& b) const {
        return symbol < b.symbol || (symbol == b.symbol && to < b.to);
    }
    bool operator==(const Edge& b) const { return symbol == b.symbol && to == b.to; }
};
struct Node { bool final = false; std::vector<Edge> edges; };
struct DFA { Id start = 0; std::vector<Node> nodes; };
struct NFA { std::vector<Id> initial; std::vector<Node> nodes; };
struct Stop { std::string status; };

struct Options {
    unsigned base = 10;
    std::string e, g, mode;
    unsigned layers = 80, finite_k = 0;
    std::uint64_t nfa_cap = 500000, dfa_cap = 500000;
    std::uint64_t edge_cap = 20000000, ops_cap = 150000000;
    unsigned memory_mib = 2048;
    double seconds = 60;
    bool ignore_target = false, dump_dfa = false, stream_anchors = false, nfa_bisim = false;
};
std::uint64_t number(const std::string& s) {
    if (s.empty() || s.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument("expected a nonnegative decimal integer");
    std::size_t n = 0;
    const auto v = std::stoull(s, &n);
    if (n != s.size()) throw std::invalid_argument("invalid integer");
    return v;
}
Options parse(int argc, char** argv) {
    Options o;
    if (argc < 2) throw std::invalid_argument("usage: exterior_regular BASE E G [options], --automata or --model");
    int i;
    if (std::string(argv[1]) == "--automata" || std::string(argv[1]) == "--model") {
        o.mode = argv[1]; i = 2;
    } else {
        if (argc < 4) throw std::invalid_argument("BASE E G required");
        auto b = number(argv[1]);
        if (b < 2 || b > 32) throw std::invalid_argument("base must be 2..32");
        o.base = static_cast<unsigned>(b); o.e = argv[2]; o.g = argv[3]; i = 4;
        if (o.g.empty() || o.g.size() > 256 || o.g.front() != '1' ||
            o.g.find_first_not_of("01") != std::string::npos ||
            o.e.size() != o.g.size() || o.e.find_first_not_of("01") != std::string::npos)
            throw std::invalid_argument("equal binary E/G of length1..256 required; G must start with1");
    }
    for (; i < argc; ++i) {
        const std::string flag = argv[i];
        if (flag == "--ignore-target") { o.ignore_target = true; continue; }
        if (flag == "--dump-dfa") { o.dump_dfa = true; continue; }
        if (flag == "--stream-anchors") { o.stream_anchors = true; continue; }
        if (flag == "--nfa-bisim") { o.nfa_bisim = true; continue; }
        if (++i == argc) throw std::invalid_argument("missing option value");
        const std::string v = argv[i];
        if (flag == "--seconds") {
            std::size_t n = 0; o.seconds = std::stod(v, &n);
            if (n != v.size()) throw std::invalid_argument("invalid seconds");
        } else {
            const auto x = number(v);
            if (flag == "--layers") {
                if (x < 1 || x > 10000) throw std::invalid_argument("layers must be1..10000");
                o.layers = static_cast<unsigned>(x);
            } else if (flag == "--finite-k") {
                if (x < 1 || x > 1000) throw std::invalid_argument("finite-k must be1..1000");
                o.finite_k = static_cast<unsigned>(x);
            } else if (flag == "--memory-mib") {
                if (x < 64 || x > 8192) throw std::invalid_argument("memory must be64..8192MiB");
                o.memory_mib = static_cast<unsigned>(x);
            } else if (flag == "--nfa-cap") o.nfa_cap = x;
            else if (flag == "--dfa-cap") o.dfa_cap = x;
            else if (flag == "--edge-cap") o.edge_cap = x;
            else if (flag == "--ops-cap") o.ops_cap = x;
            else throw std::invalid_argument("unknown option: " + flag);
        }
    }
    if (!std::isfinite(o.seconds) || o.seconds <= 0 || o.seconds > 1190)
        throw std::invalid_argument("seconds must be positive and at most1190");
    if (o.nfa_cap == 0 || o.nfa_cap >= absent || o.dfa_cap == 0 || o.dfa_cap >= absent ||
        o.edge_cap == 0 || o.ops_cap == 0)
        throw std::invalid_argument("positive state/edge/operation limits required");
    return o;
}
struct Budget {
    const Options& o;
    Clock::time_point begin = Clock::now();
    std::uint64_t ops = 0;
    explicit Budget(const Options& options) : o(options) {}
    double elapsed() const { return std::chrono::duration<double>(Clock::now() - begin).count(); }
    void check() const { if (elapsed() >= o.seconds) throw Stop{"TIMEOUT_UNDECIDED"}; }
    void tick(std::uint64_t n = 1) {
        if (n > o.ops_cap - std::min(ops, o.ops_cap)) throw Stop{"OPERATION_CAP_UNDECIDED"};
        ops += n;
        if ((ops & 4095U) < n) check();
    }
    void states(std::size_t n, bool nfa) const {
        if (n > (nfa ? o.nfa_cap : o.dfa_cap))
            throw Stop{nfa ? "NFA_CAP_UNDECIDED" : "DFA_CAP_UNDECIDED"};
    }
    void edges(std::uint64_t n) const { if (n > o.edge_cap) throw Stop{"EDGE_CAP_UNDECIDED"}; }
};
void memory_limit(unsigned mib) {
    rlimit r{};
    if (getrlimit(RLIMIT_AS, &r) != 0) throw std::runtime_error("getrlimit failed");
    r.rlim_cur = std::min(r.rlim_max, static_cast<rlim_t>(mib) * 1024 * 1024);
    if (setrlimit(RLIMIT_AS, &r) != 0) throw std::runtime_error("setrlimit failed");
}
std::uint64_t edge_count(const DFA& a) {
    std::uint64_t n = 0; for (const auto& s : a.nodes) n += s.edges.size(); return n;
}
DFA empty_dfa() { return DFA{0, std::vector<Node>(1)}; }
bool empty(const DFA& a) {
    return std::none_of(a.nodes.begin(), a.nodes.end(), [](const Node& n) { return n.final; });
}
void sort_edges(std::vector<Edge>& es) {
    std::sort(es.begin(), es.end()); es.erase(std::unique(es.begin(), es.end()), es.end());
}
void validate_dfa(const DFA& a) {
    if (a.nodes.empty() || a.start >= a.nodes.size()) throw std::logic_error("invalid DFA root");
    for (const auto& s : a.nodes) {
        Sym last = 0; bool first = true;
        for (auto e : s.edges) {
            if (e.to >= a.nodes.size() || (!first && e.symbol <= last))
                throw std::logic_error("DFA not deterministic/sorted");
            first = false; last = e.symbol;
        }
    }
}
Id step(const DFA& a, Id s, Sym symbol) {
    if (s == absent) return absent;
    const auto& es = a.nodes[s].edges;
    auto it = std::lower_bound(es.begin(), es.end(), Edge{symbol, 0});
    return it != es.end() && it->symbol == symbol ? it->to : absent;
}
template<class T> struct VectorHash {
    std::size_t operator()(const std::vector<T>& v) const noexcept {
        std::size_t h = 0x9e3779b97f4a7c15ULL;
        for (const auto x : v) h ^= std::hash<T>{}(x) + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        return h;
    }
};

// Reachability has already been generated explicitly. Remove states without
// any path to a final state before determinization, using a reverse CSR graph.
NFA trim(NFA a, Budget& b) {
    b.states(a.nodes.size(), true);
    const auto n = a.nodes.size();
    std::vector<std::size_t> offsets(n + 1, 0);
    std::uint64_t m = 0;
    for (auto& s : a.nodes) {
        sort_edges(s.edges); m += s.edges.size(); b.edges(m);
        for (auto e : s.edges) { if (e.to >= n) throw std::logic_error("NFA target outside graph"); ++offsets[e.to + 1]; }
    }
    std::partial_sum(offsets.begin(), offsets.end(), offsets.begin());
    auto cursor = offsets;
    std::vector<Id> reverse(m);
    for (Id q = 0; q < n; ++q)
        for (auto e : a.nodes[q].edges) reverse[cursor[e.to]++] = q;
    std::vector<unsigned char> good(n, 0); std::vector<Id> queue;
    for (Id q = 0; q < n; ++q) if (a.nodes[q].final) { good[q] = 1; queue.push_back(q); }
    for (std::size_t i = 0; i < queue.size(); ++i) {
        const auto q = queue[i];
        for (auto j = offsets[q]; j < offsets[q + 1]; ++j) {
            b.tick(); const auto p = reverse[j];
            if (!good[p]) { good[p] = 1; queue.push_back(p); }
        }
    }
    std::vector<Id> remap(n, absent); NFA out;
    for (Id q = 0; q < n; ++q) if (good[q]) { remap[q] = static_cast<Id>(out.nodes.size()); out.nodes.push_back({a.nodes[q].final, {}}); }
    for (auto q : a.initial) {
        if (q >= n) throw std::logic_error("NFA initial outside graph");
        if (good[q]) out.initial.push_back(remap[q]);
    }
    std::sort(out.initial.begin(), out.initial.end());
    out.initial.erase(std::unique(out.initial.begin(), out.initial.end()), out.initial.end());
    if (out.initial.empty()) return NFA{};
    for (Id q = 0; q < n; ++q) if (good[q]) {
        auto& es = out.nodes[remap[q]].edges;
        for (auto e : a.nodes[q].edges) if (good[e.to]) { b.tick(); es.push_back({e.symbol, remap[e.to]}); }
    }
    return out;
}

struct Determinized { DFA dfa; std::vector<std::vector<Id>> subsets; };
NFA bisimulate(NFA a,Budget& b) {
    if(a.initial.empty())return a;
    const auto n=a.nodes.size();std::vector<Id> cls(n);
    bool has_final=false,has_nonfinal=false;
    for(Id q=0;q<n;++q){cls[q]=a.nodes[q].final?1:0;has_final|=a.nodes[q].final;has_nonfinal|=!a.nodes[q].final;}
    Id groups=unsigned(has_final)+unsigned(has_nonfinal);
    for(;;) {
        std::unordered_map<std::vector<Sym>,Id,VectorHash<Sym>> signatures;
        std::vector<Id> next(n);Id count=0;
        for(Id q=0;q<n;++q) {
            std::vector<Edge> pairs;
            for(auto e:a.nodes[q].edges){b.tick();pairs.push_back({e.symbol,cls[e.to]});}
            sort_edges(pairs);std::vector<Sym> key{cls[q]};key.reserve(1+2*pairs.size());
            for(auto e:pairs){key.push_back(e.symbol);key.push_back(e.to);}
            auto f=signatures.find(key);
            if(f==signatures.end()){next[q]=count;signatures.emplace(std::move(key),count++);}else next[q]=f->second;
        }
        cls.swap(next);if(count==groups){groups=count;break;}groups=count;
    }
    NFA out;out.nodes.resize(groups);std::vector<Id> representatives(groups,absent);
    for(Id q=0;q<n;++q)if(representatives[cls[q]]==absent) {
        representatives[cls[q]]=q;auto& r=out.nodes[cls[q]];r.final=a.nodes[q].final;
        for(auto e:a.nodes[q].edges)r.edges.push_back({e.symbol,cls[e.to]});
        sort_edges(r.edges);
    }
    // Strong bisimulation audit: every old state has the same final bit and
    // exact SET of labelled target classes as its quotient representative.
    // Sets, rather than edge multiplicities, determine an NFA's language.
    for(Id q=0;q<n;++q) {
        std::vector<Edge> expected;
        for(auto e:a.nodes[q].edges){b.tick();expected.push_back({e.symbol,cls[e.to]});}
        sort_edges(expected);const auto& r=out.nodes[cls[q]];
        if(r.final!=a.nodes[q].final||r.edges!=expected)throw std::logic_error("NFA bisimulation audit failed");
    }
    for(auto q:a.initial)out.initial.push_back(cls[q]);
    std::sort(out.initial.begin(),out.initial.end());out.initial.erase(std::unique(out.initial.begin(),out.initial.end()),out.initial.end());
    return out;
}
Determinized determinize(const NFA& a, Budget& b) {
    if (a.initial.empty()) return {empty_dfa(), {{}}};
    Determinized out;
    std::unordered_map<std::vector<Id>, Id, VectorHash<Id>> index;
    auto add = [&](std::vector<Id> set) {
        std::sort(set.begin(), set.end()); set.erase(std::unique(set.begin(), set.end()), set.end());
        auto f = index.find(set); if (f != index.end()) return f->second;
        b.states(out.subsets.size() + 1, false);
        const Id q = static_cast<Id>(out.subsets.size());
        bool final = false; for (auto p : set) final = final || a.nodes[p].final;
        index.emplace(set, q); out.subsets.push_back(std::move(set)); out.dfa.nodes.push_back({final, {}}); return q;
    };
    out.dfa.start = add(a.initial); std::uint64_t edges = 0;
    for (Id q = 0; q < out.subsets.size(); ++q) {
        std::map<Sym, std::vector<Id>> targets;
        for (auto p : out.subsets[q]) for (auto e : a.nodes[p].edges) { b.tick(); targets[e.symbol].push_back(e.to); }
        std::vector<Edge> es;
        for (auto& [symbol, set] : targets) {
            es.push_back({symbol, add(std::move(set))}); b.edges(++edges);
        }
        out.dfa.nodes[q].edges = std::move(es);
    }
    // Independent post-construction audit of every subset and every present or
    // absent transition. Flat sorted pairs avoid the builder's map-union path.
    for (Id q = 0; q < out.subsets.size(); ++q) {
        std::vector<Edge> pairs; bool final = false;
        for (auto p : out.subsets[q]) {
            final = final || a.nodes[p].final;
            for (auto e : a.nodes[p].edges) { b.tick(); pairs.push_back(e); }
        }
        sort_edges(pairs);
        if (final != out.dfa.nodes[q].final) throw std::logic_error("subset final audit failed");
        std::size_t cursor = 0, edge = 0;
        while (cursor < pairs.size()) {
            const auto symbol = pairs[cursor].symbol; std::vector<Id> expected;
            while (cursor < pairs.size() && pairs[cursor].symbol == symbol) expected.push_back(pairs[cursor++].to);
            if (edge >= out.dfa.nodes[q].edges.size()) throw std::logic_error("missing subset edge");
            const auto actual = out.dfa.nodes[q].edges[edge++];
            if (actual.symbol != symbol || out.subsets[actual.to] != expected)
                throw std::logic_error("subset transition audit failed");
        }
        if (edge != out.dfa.nodes[q].edges.size()) throw std::logic_error("extra subset edge");
    }
    validate_dfa(out.dfa); return out;
}

DFA minimize(const DFA& a, Budget& b) {
    validate_dfa(a); if (empty(a)) return empty_dfa();
    const auto n = a.nodes.size(); std::vector<Id> cls(n);
    for (Id q = 0; q < n; ++q) cls[q] = a.nodes[q].final ? 1 : 0;
    // An all-final input has only one populated initial class. Starting at2
    // would permit a premature count-based stop after its first split.
    Id groups = std::any_of(a.nodes.begin(),a.nodes.end(),[](const Node& q){return !q.final;}) ? 2 : 1;
    for (;;) {
        std::unordered_map<std::vector<Sym>, Id, VectorHash<Sym>> map;
        std::vector<Id> next(n); Id count = 0;
        for (Id q = 0; q < n; ++q) {
            std::vector<Sym> key; key.reserve(1 + 2 * a.nodes[q].edges.size());
            key.push_back(cls[q]);
            for (auto e : a.nodes[q].edges) { b.tick(); key.push_back(e.symbol); key.push_back(cls[e.to]); }
            const auto found = map.find(key);
            if (found == map.end()) { next[q] = count; map.emplace(std::move(key), count++); }
            else next[q] = found->second;
        }
        // Inclusion of the old class proves that each pass only refines it.
        cls.swap(next);
        if (count == groups) { groups = count; break; }
        groups = count;
    }
    std::vector<Id> representatives(groups, absent);
    for (Id q = 0; q < n; ++q) if (representatives[cls[q]] == absent) representatives[cls[q]] = q;
    // Exact quotient homomorphism, including absent labels and final bits.
    for (Id q = 0; q < n; ++q) {
        const auto r = representatives[cls[q]];
        if (a.nodes[q].final != a.nodes[r].final || a.nodes[q].edges.size() != a.nodes[r].edges.size())
            throw std::logic_error("quotient final/absent-edge audit failed");
        for (std::size_t j = 0; j < a.nodes[q].edges.size(); ++j) {
            b.tick(); auto x = a.nodes[q].edges[j], y = a.nodes[r].edges[j];
            if (x.symbol != y.symbol || cls[x.to] != cls[y.to]) throw std::logic_error("quotient transition audit failed");
        }
    }
    DFA out; std::vector<Id> ids(groups, absent), queue;
    const auto initial = cls[a.start]; ids[initial] = 0; queue.push_back(initial); out.nodes.push_back({});
    for (Id id = 0; id < queue.size(); ++id) {
        const auto q = representatives[queue[id]]; std::vector<Edge> es;
        for (auto e : a.nodes[q].edges) {
            const auto t = cls[e.to];
            if (ids[t] == absent) { ids[t] = static_cast<Id>(queue.size()); queue.push_back(t); out.nodes.push_back({}); }
            es.push_back({e.symbol, ids[t]});
        }
        out.nodes[id] = {a.nodes[q].final, std::move(es)};
    }
    validate_dfa(out); return out;
}

bool identical(const DFA& a, const DFA& z) {
    if (a.start != z.start || a.nodes.size() != z.nodes.size()) return false;
    for (std::size_t i = 0; i < a.nodes.size(); ++i)
        if (a.nodes[i].final != z.nodes[i].final || a.nodes[i].edges != z.nodes[i].edges) return false;
    return true;
}
bool equivalent(const DFA& a, const DFA& z, Budget& b) {
    std::unordered_set<std::uint64_t> seen; std::vector<std::pair<Id, Id>> todo;
    auto add = [&](Id x, Id y) {
        const auto key = (std::uint64_t(x) << 32) | y;
        if (seen.insert(key).second) { b.states(seen.size(), false); todo.push_back({x,y}); }
    };
    add(a.start,z.start);
    for (std::size_t i = 0; i < todo.size(); ++i) {
        auto [x,y] = todo[i];
        const bool ax = x != absent && a.nodes[x].final, zy = y != absent && z.nodes[y].final;
        if (ax != zy) return false;
        const std::vector<Edge> nil;
        const auto& es = x == absent ? nil : a.nodes[x].edges;
        const auto& fs = y == absent ? nil : z.nodes[y].edges;
        std::size_t j = 0, k = 0;
        while (j < es.size() || k < fs.size()) {
            b.tick();
            if (k == fs.size() || (j < es.size() && es[j].symbol < fs[k].symbol)) add(es[j++].to,absent);
            else if (j == es.size() || fs[k].symbol < es[j].symbol) add(absent,fs[k++].to);
            else { add(es[j].to,fs[k].to); ++j; ++k; }
        }
    }
    return true;
}

struct Out { Sym symbol; unsigned ending; };
struct TableRelation {
    unsigned controls = 0;
    std::map<std::pair<Sym,unsigned>,std::vector<Out>> rows;
    const std::vector<Out>& get(Sym symbol,unsigned coefficient,bool) {
        static const std::vector<Out> nil;
        auto i=rows.find({symbol,coefficient}); return i==rows.end()?nil:i->second;
    }
};
struct BlockRelation {
    unsigned controls;
    std::vector<std::unique_ptr<agent116::blocks::Generator>> generators;
    std::map<unsigned,std::size_t> phase_index;
    std::map<std::tuple<Sym,unsigned,bool>,std::vector<Out>> converted;
    explicit BlockRelation(const Options& o) : controls(2*o.base-1) {
        std::vector<unsigned> phases;
        for(unsigned t=0;t<o.g.size();++t) if(o.g[t]=='1') phases.push_back(t);
        for(std::size_t i=0;i<phases.size();++i) {
            unsigned end=i+1<phases.size()?phases[i+1]:o.g.size();
            unsigned length=end-phases[i];
            if(length<1||length>5) throw std::invalid_argument("overflow gaps outside1..5 are unsupported");
            phase_index[phases[i]]=generators.size();
            generators.push_back(std::make_unique<agent116::blocks::Generator>(o.base,
                agent116::blocks::BlockSpec{static_cast<std::uint16_t>(phases[i]),static_cast<std::uint8_t>(length)}));
        }
    }
    static Sym symbol(agent116::blocks::Symbol s) { return (Sym(s.phase)<<32)|s.cfg; }
    agent116::blocks::Generator& generator(Sym s) {
        auto i=phase_index.find(static_cast<unsigned>(s>>32));
        if(i==phase_index.end()) throw std::invalid_argument("unknown block phase type");
        return *generators[i->second];
    }
    const std::vector<Out>& get(Sym s,unsigned coefficient,bool first) {
        auto key=std::make_tuple(s,coefficient,first); auto i=converted.find(key);
        if(i!=converted.end()) return i->second;
        auto& gen=generator(s);
        std::vector<Out> out;
        for(const auto& tile:gen.tiles({static_cast<std::uint16_t>(s>>32),static_cast<std::uint32_t>(s)},coefficient,first))
            out.push_back({symbol(tile.output),tile.ending});
        return converted.emplace(key,std::move(out)).first->second;
    }
    std::vector<Sym> initial() {
        std::vector<Sym> v; for(auto& g:generators)v.push_back(symbol(g->initial_symbol()));return v;
    }
    std::vector<Sym> terminal(const std::string& e) {
        std::vector<Sym> v;
        for(auto& g:generators) {
            auto spec=g->spec();unsigned mask=0;
            for(unsigned j=0;j<spec.length;++j)mask|=unsigned(e[spec.phase+j]-'0')<<j;
            v.push_back(symbol(g->terminal_symbol(mask)));
        }
        return v;
    }
};
struct Triple { Id input; unsigned current,first; bool operator==(const Triple& x) const { return input==x.input&&current==x.current&&first==x.first; } };
struct TripleHash { std::size_t operator()(const Triple& x) const { return std::size_t(x.input)*65537U+x.current*257U+x.first; } };
struct ImageStats {
    std::uint64_t raw_states=0,raw_edges=0,trim_states=0,trim_edges=0,subset_states=0,subset_edges=0;
    std::uint64_t peak_raw_states=0,peak_raw_edges=0;
};
template<class Relation>
NFA image_nfa(const DFA& a,Relation& relation,bool first,unsigned lo,unsigned hi,Budget& b,ImageStats& stats) {
    NFA nfa;std::vector<Triple> triples;
    std::unordered_map<Triple,Id,TripleHash> index;
    auto add=[&](Triple t) {
        auto f=index.find(t);if(f!=index.end())return f->second;
        b.states(triples.size()+1,true);const auto id=static_cast<Id>(triples.size());
        index.emplace(t,id);triples.push_back(t);
        nfa.nodes.push_back({a.nodes[t.input].final&&t.current==t.first,{}});return id;
    };
    for(unsigned c=lo;c<hi;++c)nfa.initial.push_back(add({a.start,c,c}));
    std::uint64_t edges=0;
    for(Id q=0;q<triples.size();++q) {
        const auto t=triples[q];std::vector<Edge> outgoing;
        for(auto e:a.nodes[t.input].edges)for(auto tile:relation.get(e.symbol,t.current,first)) {
            b.tick();const auto target=add({e.to,tile.ending,t.first});
            outgoing.push_back({tile.symbol,target});b.edges(++edges);
        }
        sort_edges(outgoing);nfa.nodes[q].edges=std::move(outgoing);
    }
    stats.raw_states+=nfa.nodes.size();stats.raw_edges+=edges;
    stats.peak_raw_states=std::max<std::uint64_t>(stats.peak_raw_states,nfa.nodes.size());
    stats.peak_raw_edges=std::max(stats.peak_raw_edges,edges);
    return nfa;
}
template<class Relation>
DFA cyclic_image(const DFA& a,Relation& relation,bool first,Budget& b,ImageStats& stats) {
    if(empty(a))return empty_dfa();
    NFA nfa;
    if(!b.o.stream_anchors) {
        nfa=trim(image_nfa(a,relation,first,first?1:0,relation.controls,b,stats),b);
    } else {
        // R(A) is the exact union of images with a fixed cyclic coefficient.
        // Each anchor is retained across every intermediate accepted unit.
        // A complete next layer is emitted only after ALL anchors finish.
        std::uint64_t joined_edges=0;
        for(unsigned c=first?1:0;c<relation.controls;++c) {
            auto part=trim(image_nfa(a,relation,first,c,c+1,b,stats),b);
            if(b.o.nfa_bisim)part=bisimulate(std::move(part),b);
            b.states(nfa.nodes.size()+part.nodes.size(),true);
            const auto offset=static_cast<Id>(nfa.nodes.size());
            for(auto q:part.initial)nfa.initial.push_back(offset+q);
            for(auto& q:part.nodes) {
                for(auto& e:q.edges)e.to+=offset;
                joined_edges+=q.edges.size();b.edges(joined_edges);
                nfa.nodes.push_back(std::move(q));
            }
        }
    }
    if(b.o.nfa_bisim)nfa=bisimulate(std::move(nfa),b);
    stats.trim_states=nfa.nodes.size();for(const auto& n:nfa.nodes)stats.trim_edges+=n.edges.size();
    auto d=determinize(nfa,b);stats.subset_states=d.dfa.nodes.size();stats.subset_edges=edge_count(d.dfa);
    return minimize(d.dfa,b);
}
DFA repeated_word(const std::vector<Sym>& word,unsigned k) {
    if(word.empty())throw std::logic_error("empty driver word");
    const auto n=word.size()*(k?k:1);DFA a;a.nodes.resize(n+1);
    for(Id q=0;q<n;++q)a.nodes[q].edges.push_back({word[q%word.size()],q+1});
    a.nodes[n].final=true;
    if(!k)a.nodes[n].edges.push_back({word[0],1});
    return a;
}
unsigned terminal_hit(const DFA& a,const std::vector<Sym>& word,unsigned fixed_k) {
    Id q=a.start;std::set<Id> seen{q};unsigned k=0;
    for(;;) {
        for(auto symbol:word) {q=step(a,q,symbol);if(q==absent)return 0;}
        ++k;if((!fixed_k||k==fixed_k)&&a.nodes[q].final)return k;
        if(fixed_k&&k>=fixed_k)return 0;
        if(!fixed_k&&!seen.insert(q).second)return 0;
    }
}
// Tiny exact nonnegative integers: only addition and decimal printing are
// needed for finite-k frontier controls; no external arithmetic dependency.
struct Count {
    std::vector<std::uint32_t> digits;
    void one(){digits={1};}
    bool zero()const{return digits.empty();}
    void add(const Count& c) {
        if(c.zero())return;
        if(digits.size()<c.digits.size())digits.resize(c.digits.size());
        std::uint64_t carry=0;
        for(std::size_t i=0;i<digits.size();++i) {
            auto total=std::uint64_t(digits[i])+carry+(i<c.digits.size()?c.digits[i]:0);
            digits[i]=static_cast<std::uint32_t>(total%1000000000U);carry=total/1000000000U;
        }
        if(carry)digits.push_back(static_cast<std::uint32_t>(carry));
    }
    std::string str()const {
        if(zero())return "0";
        std::ostringstream out;out<<digits.back();
        for(std::size_t j=digits.size()-1;j>0;--j)out<<std::setw(9)<<std::setfill('0')<<digits[j-1];
        return out.str();
    }
};
std::vector<std::string> finite_counts(const DFA& a,std::size_t unit,Budget& b) {
    std::vector<std::string> out;std::vector<Count> counts(a.nodes.size());counts[a.start].one();
    for(std::size_t depth=1;depth<=3*unit;++depth) {
        std::vector<Count> next(a.nodes.size());
        for(Id q=0;q<a.nodes.size();++q)if(!counts[q].zero())for(auto e:a.nodes[q].edges){b.tick();next[e.to].add(counts[q]);}
        counts.swap(next);
        if(depth%unit==0){Count total;for(Id q=0;q<a.nodes.size();++q)if(a.nodes[q].final)total.add(counts[q]);out.push_back(total.str());}
    }
    return out;
}
void print_dfa(const DFA& a) {
    std::cout<<"{\"start\":"<<a.start<<",\"states\":[";
    for(std::size_t i=0;i<a.nodes.size();++i){if(i)std::cout<<',';std::cout<<"{\"final\":"<<(a.nodes[i].final?"true":"false")<<",\"edges\":[";
        for(std::size_t j=0;j<a.nodes[i].edges.size();++j){if(j)std::cout<<',';auto e=a.nodes[i].edges[j];std::cout<<'['<<e.symbol<<','<<e.to<<']';}std::cout<<"]}";}
    std::cout<<"]}";
}
void layer(const DFA& a,unsigned depth,const ImageStats& s,unsigned hit,std::size_t unit,Budget& b,const Options& o) {
    auto counts=finite_counts(a,unit,b);
    std::cout<<"{\"event\":\"layer\",\"depth\":"<<depth<<",\"dfa_states\":"<<a.nodes.size()<<",\"dfa_edges\":"<<edge_count(a)
        <<",\"raw_nfa_states\":"<<s.raw_states<<",\"raw_nfa_edges\":"<<s.raw_edges<<",\"trim_nfa_states\":"<<s.trim_states
        <<",\"peak_raw_nfa_states\":"<<s.peak_raw_states<<",\"peak_raw_nfa_edges\":"<<s.peak_raw_edges
        <<",\"trim_nfa_edges\":"<<s.trim_edges<<",\"subset_states\":"<<s.subset_states<<",\"subset_edges\":"<<s.subset_edges
        <<",\"target_hit_k\":";if(hit)std::cout<<hit;else std::cout<<"null";
    std::cout<<",\"k_counts\":[";for(std::size_t i=0;i<counts.size();++i){if(i)std::cout<<',';std::cout<<'"'<<counts[i]<<'"';}
    std::cout<<"],\"operations\":"<<b.ops<<",\"elapsed_seconds\":"<<b.elapsed();
    if(o.dump_dfa) {
        std::cout<<",\"dfa_schema\":\"p196-exterior-block-dfa-v1\",\"language_kind\":\"exact_spatial_frontier\""
            <<",\"base\":"<<o.base<<",\"e\":\""<<o.e<<"\",\"g\":\""<<o.g<<"\",\"finite_k\":"<<o.finite_k<<",\"dfa\":";
        print_dfa(a);
    }
    std::cout<<"}\n"<<std::flush;
}

NFA read_nfa(Budget& b) {
    std::string tag;std::uint64_t n,ni,nf,m;
    if(!(std::cin>>tag>>n>>ni>>nf>>m)||tag!="N"||n==0||n>=absent||ni>n||nf>n)
        throw std::invalid_argument("invalid NFA header");
    b.states(n,true);b.edges(m);NFA a;a.nodes.resize(n);
    for(std::uint64_t i=0;i<ni;++i){std::uint64_t q;if(!(std::cin>>q)||q>=n)throw std::invalid_argument("bad NFA initial");a.initial.push_back(q);}
    for(std::uint64_t i=0;i<nf;++i){std::uint64_t q;if(!(std::cin>>q)||q>=n)throw std::invalid_argument("bad NFA final");a.nodes[q].final=true;}
    for(std::uint64_t i=0;i<m;++i){std::uint64_t q,r;Sym s;if(!(std::cin>>q>>s>>r)||q>=n||r>=n)throw std::invalid_argument("bad NFA edge");a.nodes[q].edges.push_back({s,static_cast<Id>(r)});}
    return a;
}
std::pair<DFA,TableRelation> read_model(Budget& b) {
    std::string tag;std::uint64_t n,start,nf,m;
    if(!(std::cin>>tag>>n>>start>>nf>>m)||tag!="A"||n==0||n>=absent||start>=n||nf>n)
        throw std::invalid_argument("invalid DFA model header");
    b.states(n,false);b.edges(m);DFA a;a.start=start;a.nodes.resize(n);
    for(std::uint64_t i=0;i<nf;++i){std::uint64_t q;if(!(std::cin>>q)||q>=n)throw std::invalid_argument("bad model final");a.nodes[q].final=true;}
    for(std::uint64_t i=0;i<m;++i){std::uint64_t q,r;Sym s;if(!(std::cin>>q>>s>>r)||q>=n||r>=n)throw std::invalid_argument("bad model edge");a.nodes[q].edges.push_back({s,static_cast<Id>(r)});}
    for(auto& q:a.nodes)sort_edges(q.edges);
    validate_dfa(a);
    std::uint64_t controls,tiles;
    if(!(std::cin>>tag>>controls>>tiles)||tag!="T"||controls<1||controls>63)throw std::invalid_argument("bad relation header");
    b.edges(tiles);TableRelation r;r.controls=controls;
    for(std::uint64_t i=0;i<tiles;++i){Sym x,y;std::uint64_t c,d;if(!(std::cin>>x>>y>>c>>d)||c>=controls||d>=controls)throw std::invalid_argument("bad relation tile");r.rows[{x,c}].push_back({y,static_cast<unsigned>(d)});}
    return {std::move(a),std::move(r)};
}
void end_of_input() {std::string extra;if(std::cin>>extra)throw std::invalid_argument("unexpected trailing input");}
void print_witness(const agent116::witness::Witness& w,unsigned base) {
    std::cout<<"{\"event\":\"witness\",\"base\":"<<base<<",\"width\":"<<w.width
        <<",\"repetitions\":"<<w.repetitions<<",\"e\":\""<<w.e<<"\",\"g\":\""<<w.g<<"\",\"B\":[";
    for(std::size_t t=0;t<w.B.size();++t) {
        if(t)std::cout<<',';
        std::cout<<'[';
        for(std::size_t j=0;j<w.B[t].size();++j){if(j)std::cout<<',';std::cout<<w.B[t][j];}
        std::cout<<']';
    }
    std::cout<<"],\"u\":[";for(std::size_t i=0;i<w.u.size();++i){if(i)std::cout<<',';std::cout<<w.u[i];}
    std::cout<<"],\"initial_word_replay\":"<<(w.initial_word_replay?"true":"false")
        <<",\"direct_word_replay\":"<<(w.direct_word_replay?"true":"false")
        <<",\"inverse_dp_states\":"<<w.inverse_dp_states<<",\"inverse_initial_trials\":"<<w.inverse_initial_trials
        <<",\"maximum_inverse_dp_states\":"<<w.maximum_inverse_dp_states<<"}\n"<<std::flush;
}
void metrics(const Budget& b,const Options& o,int completed) {
    rusage usage{};
    if(getrusage(RUSAGE_SELF,&usage)!=0)throw std::runtime_error("getrusage failed");
    std::cout<<",\"last_completed_depth\":"<<completed<<",\"operations\":"<<b.ops
        <<",\"elapsed_seconds\":"<<b.elapsed()<<",\"peak_rss_mib\":"<<double(usage.ru_maxrss)/1024.0
        <<",\"finite_k\":"<<o.finite_k<<",\"stream_anchors\":"<<(o.stream_anchors?"true":"false")
        <<",\"nfa_bisim\":"<<(o.nfa_bisim?"true":"false");
}

int run(const Options& o) {
    memory_limit(o.memory_mib);Budget b(o);
    int completed=-1;
    try {
    if(o.mode=="--automata") {
        auto n=read_nfa(b);end_of_input();n=trim(std::move(n),b);const auto before=n.nodes.size();
        if(o.nfa_bisim)n=bisimulate(std::move(n),b);
        const auto after=n.nodes.size();auto d=determinize(n,b);auto a=minimize(d.dfa,b);
        std::cout<<"{\"status\":\"OK\",\"dfa\":";print_dfa(a);std::cout<<",\"operations\":"<<b.ops<<",\"bisim_before\":"<<before<<",\"bisim_after\":"<<after<<"}\n";return 0;
    }
    if(o.mode=="--model") {
        auto [a,r]=read_model(b);end_of_input();ImageStats s;auto d=cyclic_image(a,r,false,b,s);
        std::cout<<"{\"status\":\"OK\",\"dfa\":";print_dfa(d);std::cout<<",\"operations\":"<<b.ops<<"}\n";return 0;
    }
    BlockRelation r(o);auto initial=r.initial(),terminal=r.terminal(o.e);
    std::vector<DFA> history;history.push_back(repeated_word(initial,o.finite_k));
    layer(history.back(),0,{},0,initial.size(),b,o);
    completed=0;
    for(unsigned depth=1;depth<=o.layers;++depth) {
        b.check();ImageStats stats;auto a=cyclic_image(history.back(),r,depth==1,b,stats);
        const auto hit=terminal_hit(a,terminal,o.finite_k);layer(a,depth,stats,hit,initial.size(),b,o);
        completed=static_cast<int>(depth);
        if(hit&&!o.ignore_target) {
            const auto witness=agent116::witness::reconstruct(history,terminal,hit,depth,r,o.base,o.e,o.g,b);
            print_witness(witness,o.base);
            std::cout<<"{\"event\":\"result\",\"status\":\"TARGET_HIT\",\"depth\":"<<depth<<",\"repetitions\":"<<hit<<",\"witness_pending\":false";
            metrics(b,o,completed);std::cout<<"}\n";return 0;
        }
        if(empty(a)) {
            std::cout<<"{\"event\":\"result\",\"status\":\""<<(o.ignore_target?"DIAGNOSTIC_ONLY":"EXHAUSTED")<<"\",\"depth\":"<<depth;
            metrics(b,o,completed);std::cout<<"}\n";return 0;
        }
        for(unsigned earlier=1;earlier<history.size();++earlier)if(identical(a,history[earlier])) {
            if(!equivalent(a,history[earlier],b))throw std::logic_error("structural and product equivalence disagree");
            std::cout<<"{\"event\":\"result\",\"status\":\""<<(o.ignore_target?"DIAGNOSTIC_ONLY":"REPEATED_LANGUAGE")<<"\",\"depth\":"<<depth<<",\"repeat_depth\":"<<earlier;
            metrics(b,o,completed);std::cout<<"}\n";return 0;
        }
        history.push_back(std::move(a));
    }
    throw Stop{"DEPTH_CAP_UNDECIDED"};
    } catch(const Stop& e) {
        std::cout<<"{\"event\":\"result\",\"status\":\""<<e.status<<"\"";metrics(b,o,completed);std::cout<<"}\n";return 2;
    } catch(const std::bad_alloc&) {
        std::cout<<"{\"event\":\"result\",\"status\":\"MEMORY_CAP_UNDECIDED\"";metrics(b,o,completed);std::cout<<"}\n";return 2;
    }
}
} // namespace

int main(int argc,char**argv) {
    std::cout<<std::setprecision(9);
    try{return run(parse(argc,argv));}
    catch(const Stop& e){std::cout<<"{\"event\":\"result\",\"status\":\""<<e.status<<"\"}\n";return 2;}
    catch(const std::bad_alloc&){std::cout<<"{\"event\":\"result\",\"status\":\"MEMORY_CAP_UNDECIDED\"}\n";return 2;}
    catch(const std::exception& e){std::cerr<<e.what()<<'\n';std::cout<<"{\"event\":\"result\",\"status\":\"ERROR_UNDECIDED\"}\n";return 3;}
}
