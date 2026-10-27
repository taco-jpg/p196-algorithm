// Agent 110: sparse all-repetition p12 center graph, widths2..17.
// The balanced cap-lift/phase4 anchor is explained in the preceding report.
// Odd-width source pruning credits Agent3's PAPER invariant (issue303):
// alt(C)=9 mod11 和 an even middle on every positive-overflow center cycle.
// This removes transient states as well; path counts concern the filtered graph.
//
// State IDs always use the UNFILTERED base19 half(D) encoding of C=9++D++9.
// For odd W, D has length2d+1. Its middle is uniquely determined, if permitted,
// by x=(-1)^d*(9-2*alt(outer_half)) mod11 和 x even in0..18.
// Raw --map comparisons deliberately ignore source/target invariant pruning.
//
// Build: g++ -O3 -std=c++17 -Wall -Wextra -pedantic p12_sparse_graph.cpp -o p12_sparse
// Run: p12_sparse W [--edges] [--seconds 1500] [--edge-cap 10000000]
// Probe: p12_sparse --map W  (stdin IDs; stdout exactly "ID NEXT")
// Regression only: --unfiltered, permitted for W<=14.
// --edges emits the complete sorted retained relation, then a JSON summary.
// A center cycle is an intermediate witness, never independently a certificate.

#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <exception>
#include <iomanip>
#include <iostream>
#include <limits>
#include <new>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
#include <sys/resource.h>

namespace {
using Clock = std::chrono::steady_clock;
constexpr uint64_t NONE = std::numeric_limits<uint64_t>::max();
constexpr uint32_t NO_INDEX = std::numeric_limits<uint32_t>::max();
constexpr int MAX_WIDTH = 17;
constexpr int PERIOD = 24;
constexpr uint64_t MEMORY_LIMIT = 1000000000ULL;
constexpr uint64_t MAX_EDGES = 10000000ULL;
constexpr char ES[] = "101010010101";
constexpr char GS[] = "100010001000";
constexpr int MIDDLE[11] = {0,12,2,14,4,16,6,18,8,-1,10};

int mod11(int value) {
    value %= 11;
    return value < 0 ? value + 11 : value;
}

uint64_t peak_rss_kib() {
    rusage usage{};
    if (getrusage(RUSAGE_SELF, &usage) != 0) return 0;
#if defined(__APPLE__)
    return static_cast<uint64_t>(usage.ru_maxrss) / 1024;
#else
    return static_cast<uint64_t>(usage.ru_maxrss);
#endif
}

struct Word {
    std::array<uint8_t, MAX_WIDTH + 2> digit{};
    int size = 0;
};
struct Edge { uint64_t source, target; };
struct Counts {
    uint64_t prefixes = 0, evaluated = 0, initial_flip = 0;
    uint64_t step_attempts = 0, valid_steps = 0, completed = 0;
    uint64_t endpoint_returns = 0, endpoint_failures = 0;
    uint64_t retained = 0, target_rejections = 0;
    uint64_t carry_failures = 0, trim_failures = 0, shape_failures = 0;
    uint64_t finished_active = 0, max_path = 0;
    std::string digest;
    bool enumeration_complete = false;
};

struct Context {
    int width, half;
    uint64_t states = 1, prefixes = 1, expected_candidates = 0, edge_cap;
    bool filtered, emit_edges;
    std::array<int, PERIOD> e{}, g{}, v{};
    std::array<int, PERIOD + 1> length{};
    Clock::time_point started = Clock::now();
    double seconds;

    Context(int W, bool unfiltered, bool emit, uint64_t cap, double limit)
        : width(W), half((W-1)/2), edge_cap(cap),
          filtered(!unfiltered && W%2==1), emit_edges(emit), seconds(limit) {
        if (W < 2 || W > MAX_WIDTH || (unfiltered && W > 14))
            throw std::invalid_argument("width must be2..17; unfiltered mode stops at14");
        if (cap == 0 || cap > MAX_EDGES || 32*cap+32000000ULL > MEMORY_LIMIT)
            throw std::invalid_argument("edge-cap exceeds the explicit memory budget");
        for (int i=0; i<half; ++i) states *= 19;
        prefixes = filtered ? states/19 : states;
        if (!filtered) expected_candidates = states;
        else {
            std::array<uint64_t,11> distribution{};
            distribution[0] = 1;
            int d = half-1;
            for (int j=0; j<d; ++j) {
                std::array<uint64_t,11> next{};
                for (int r=0; r<11; ++r)
                    for (int x=0; x<19; ++x)
                        next[mod11(r+(j%2 ? -x : x))] += distribution[r];
                distribution = next;
            }
            for (int r=0; r<11; ++r)
                if (MIDDLE[mod11((d%2 ? -1 : 1)*(9-2*r))] >= 0)
                    expected_candidates += distribution[r];
        }
        length[0] = W;
        for (int t=0; t<PERIOD; ++t) {
            int original = (t+4)%PERIOD;
            e[t] = ES[original%12]-'0';
            g[t] = GS[original%12]-'0';
            v[t] = original==4 || original==12 || original==20;
            length[t+1] = length[t]+g[t]-2*v[t];
            if (length[t+1] < W-1 || length[t+1] > W)
                throw std::logic_error("invalid balanced width profile");
        }
        if (length[PERIOD] != W || !g[0] || !v[0])
            throw std::logic_error("invalid anchor");
    }
    double elapsed() const {
        return std::chrono::duration<double>(Clock::now()-started).count();
    }
    const char* exceeded() const {
        if (elapsed() >= seconds) return "wall_time";
        if (peak_rss_kib()*1024 > MEMORY_LIMIT) return "resident_memory";
        return nullptr;
    }
};

Word decode(const Context& c, uint64_t id) {
    Word word;
    word.size = c.width;
    word.digit[0] = word.digit[c.width-1] = 9;
    for (int j=0; j<c.half; ++j) {
        uint8_t digit = static_cast<uint8_t>(id%19);
        id /= 19;
        word.digit[j+1] = word.digit[c.width-2-j] = digit;
    }
    return word;
}

bool candidate(const Context& c, uint64_t prefix, uint64_t& id, Word& word) {
    if (!c.filtered) { id=prefix; word=decode(c,id); return true; }
    word.size = c.width;
    word.digit[0] = word.digit[c.width-1] = 9;
    uint64_t encoded = prefix;
    int d=c.half-1, alternating=0;
    for (int j=0; j<d; ++j) {
        int digit = static_cast<int>(encoded%19);
        encoded /= 19;
        alternating += j%2 ? -digit : digit;
        word.digit[j+1] = word.digit[c.width-2-j] = static_cast<uint8_t>(digit);
    }
    int middle = MIDDLE[mod11((d%2 ? -1 : 1)*(9-2*alternating))];
    if (middle < 0) return false;
    word.digit[d+1] = static_cast<uint8_t>(middle);
    id = prefix + static_cast<uint64_t>(middle)*c.prefixes;
    return true;
}

uint64_t encode(const Context& c, const Word& word) {
    if (word.size != c.width || word.digit[0] != 9 || word.digit[c.width-1] != 9)
        return NONE;
    for (int j=0; j<word.size; ++j)
        if (word.digit[j]>18 || word.digit[j]!=word.digit[word.size-1-j]) return NONE;
    uint64_t id=0, power=1;
    for (int j=0; j<c.half; ++j) {
        id += word.digit[j+1]*power;
        power *= 19;
    }
    return id<c.states ? id : NONE;
}

bool in_domain(const Context& c, uint64_t id) {
    if (!c.filtered) return true;
    Word word=decode(c,id);
    if (word.digit[c.width/2]%2) return false;
    int alternating=0;
    for (int j=0; j<word.size; ++j)
        alternating += j%2 ? -word.digit[j] : word.digit[j];
    return mod11(alternating)==9;
}

enum class Failure { none, carry, trim, shape };
Failure step(const Context& c, int phase, Word& word) {
    if (word.size!=c.length[phase] || word.size<1 || word.size>MAX_WIDTH)
        return Failure::shape;
    std::array<uint8_t,MAX_WIDTH+2> digits{}, raw{};
    int carry=c.e[phase];
    for (int j=0; j<word.size; ++j) {
        if (word.digit[j]>18) return Failure::shape;
        int sum=word.digit[j]+carry;
        digits[j]=static_cast<uint8_t>(sum%10);
        carry=sum/10;
    }
    if (carry!=1-c.e[phase]) return Failure::carry;
    int size=word.size;
    if (c.g[phase]) digits[size++]=static_cast<uint8_t>(9*c.e[phase]);
    for (int j=0; j<size; ++j)
        raw[j]=static_cast<uint8_t>(digits[j]+digits[size-1-j]);
    int trim=c.v[phase];
    if (trim && (size<3 || raw[0]!=9 || raw[size-1]!=9)) return Failure::trim;
    int result_size=size-2*trim;
    if (result_size!=c.length[phase+1] || result_size<1 || result_size>MAX_WIDTH)
        return Failure::shape;
    word.size=result_size;
    for (int j=0; j<result_size; ++j) word.digit[j]=raw[j+trim];
    return Failure::none;
}

uint64_t return_word(const Context& c, Word word, Counts* n=nullptr) {
    for (int t=0; t<PERIOD; ++t) {
        if (n) ++n->step_attempts;
        Failure failure=step(c,t,word);
        if (failure!=Failure::none) {
            if (n) {
                if (failure==Failure::carry) ++n->carry_failures;
                else if (failure==Failure::trim) ++n->trim_failures;
                else ++n->shape_failures;
            }
            return NONE;
        }
        if (n) {
            ++n->valid_steps;
            // At the phase4 anchor, endpoints9 make trim automatic after flip.
            if (t==0) ++n->initial_flip;
        }
    }
    if (n) ++n->completed;
    uint64_t id=encode(c,word);
    if (id==NONE && n) ++n->endpoint_failures;
    return id;
}

std::string digest(const std::vector<Edge>& edges) {
    uint64_t hash=14695981039346656037ULL;
    for (const Edge& edge: edges)
        for (uint64_t value: {edge.source,edge.target})
            for (int shift=0; shift<64; shift+=8) {
                hash ^= (value>>shift)&255ULL;
                hash *= 1099511628211ULL;
            }
    std::ostringstream text;
    text << "fnv1a64:" << std::hex << std::setfill('0') << std::setw(16) << hash;
    return text.str();
}

void summary(const Context& c, const Counts& n, const char* status, const char* reason,
             int cycles, bool complete) {
    std::cout << "{\"status\":\"" << status << "\",\"reason\":\"" << reason
      << "\",\"width\":" << c.width << ",\"odd_invariant_filter\":" << (c.filtered?"true":"false")
      << ",\"unfiltered_states\":" << c.states << ",\"outer_prefixes_total\":" << c.prefixes
      << ",\"enumerated_prefixes\":" << n.prefixes << ",\"expected_candidates\":" << c.expected_candidates
      << ",\"evaluated_candidates\":" << n.evaluated << ",\"initial_flip_valid\":" << n.initial_flip
      << ",\"step_attempts\":" << n.step_attempts << ",\"valid_steps\":" << n.valid_steps
      << ",\"completed_24_steps\":" << n.completed << ",\"endpoint_returns\":" << n.endpoint_returns
      << ",\"retained_edges\":" << n.retained << ",\"target_invariant_rejections\":" << n.target_rejections
      << ",\"carry_failures\":" << n.carry_failures << ",\"trim_failures\":" << n.trim_failures
      << ",\"shape_failures\":" << n.shape_failures << ",\"endpoint_failures\":" << n.endpoint_failures
      << ",\"finished_active_sources\":" << n.finished_active << ",\"max_path_edges\":" << n.max_path
      << ",\"cycles_found\":" << cycles << ",\"cycle_scan_complete\":" << (complete?"true":"false")
      << ",\"enumeration_complete\":" << (n.enumeration_complete?"true":"false")
      << ",\"edge_digest\":";
    if (n.digest.empty()) std::cout << "null";
    else std::cout << '"' << n.digest << '"';
    std::cout << ",\"peak_rss_kib\":" << peak_rss_kib() << ",\"seconds\":" << c.elapsed() << "}\n";
    std::cout.flush();
}

void emit_edges(const Context& c, const std::vector<Edge>& edges) {
    if (c.emit_edges)
        for (const Edge& edge: edges) std::cout << "EDGE " << edge.source << ' ' << edge.target << '\n';
}

void print_word(const Word& word) {
    std::cout << '[';
    for (int j=0; j<word.size; ++j) {
        if (j) std::cout << ',';
        std::cout << static_cast<int>(word.digit[j]);
    }
    std::cout << ']';
}

void print_cycle(const Context& c, const std::vector<Edge>& edges,
                 const std::vector<uint32_t>& path, size_t first) {
    for (size_t j=first; j<path.size(); ++j) {
        uint64_t expected=edges[path[j+1==path.size()?first:j+1]].source;
        if (return_word(c,decode(c,edges[path[j]].source))!=expected)
            throw std::logic_error("cycle replay failed");
    }
    std::cout << "{\"type\":\"center_cycle\",\"graph_nodes\":" << path.size()-first
              << ",\"center_period\":" << (path.size()-first)*PERIOD << "}\n";
    uint64_t index=0;
    for (size_t j=first; j<path.size(); ++j) {
        Word word=decode(c,edges[path[j]].source);
        for (int t=0; t<PERIOD; ++t) {
            Word source=word;
            if (step(c,t,word)!=Failure::none) throw std::logic_error("edge replay failed");
            std::cout << "{\"type\":\"center_edge\",\"edge\":" << index++
                      << ",\"phase12\":" << (t+4)%12 << ",\"e\":" << c.e[t]
                      << ",\"g\":" << c.g[t] << ",\"v\":" << c.v[t] << ",\"C\":";
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
        std::vector<Edge> edges;
        for (uint64_t prefix=0; prefix<c.prefixes; ++prefix) {
            if ((prefix&16383ULL)==0)
                if (const char* reason=c.exceeded()) {
                    summary(c,n,"UNDECIDED",reason,0,false); return 2;
                }
            ++n.prefixes;
            Word word;
            uint64_t source=0;
            if (!candidate(c,prefix,source,word)) continue;
            ++n.evaluated;
            uint64_t target=return_word(c,word,&n);
            if (target==NONE) continue;
            ++n.endpoint_returns;
            if (!in_domain(c,target)) { ++n.target_rejections; continue; }
            ++n.retained;
            if (edges.size()>=c.edge_cap) {
                summary(c,n,"UNDECIDED","edge_cap",0,false); return 2;
            }
            if (edges.size()==edges.capacity()) {
                uint64_t capacity=std::max<uint64_t>(1024,2*edges.capacity());
                edges.reserve(static_cast<size_t>(std::min(capacity,c.edge_cap)));
            }
            edges.push_back({source,target});
        }
        if (n.evaluated!=c.expected_candidates || n.prefixes!=c.prefixes)
            throw std::logic_error("candidate census disagrees with residue DP");
        n.enumeration_complete=true;
        std::sort(edges.begin(),edges.end(),[](const Edge& a,const Edge& b){return a.source<b.source;});
        for (size_t i=1; i<edges.size(); ++i)
            if (edges[i-1].source==edges[i].source) throw std::logic_error("duplicate source ID");
        n.digest=digest(edges);
        if (const char* reason=c.exceeded()) {
            summary(c,n,"UNDECIDED",reason,0,false); return 2;
        }
        std::vector<uint32_t> next(edges.size(),NO_INDEX), distance(edges.size(),0), path;
        std::vector<uint8_t> color(edges.size(),0);
        path.reserve(edges.size());
        for (size_t i=0; i<edges.size(); ++i) {
            auto found=std::lower_bound(edges.begin(),edges.end(),edges[i].target,
                [](const Edge& edge,uint64_t id){return edge.source<id;});
            if (found!=edges.end() && found->source==edges[i].target)
                next[i]=static_cast<uint32_t>(found-edges.begin());
        }
        uint64_t traversed=0;
        for (uint32_t start=0; start<edges.size(); ++start) {
            if (color[start]) continue;
            path.clear();
            uint32_t current=start;
            while (current!=NO_INDEX && color[current]==0) {
                if ((traversed++&16383ULL)==0)
                    if (const char* reason=c.exceeded()) {
                        summary(c,n,"UNDECIDED",reason,0,false); return 2;
                    }
                color[current]=1; path.push_back(current); current=next[current];
            }
            if (current!=NO_INDEX && color[current]==1) {
                auto position=std::find(path.begin(),path.end(),current);
                if (position==path.end()) throw std::logic_error("active path mismatch");
                emit_edges(c,edges);
                print_cycle(c,edges,path,static_cast<size_t>(position-path.begin()));
                summary(c,n,"CENTER_CYCLE","first_cycle_only",1,false); return 0;
            }
            for (auto it=path.rbegin(); it!=path.rend(); ++it) {
                uint32_t node=*it;
                // Each stored source already has one edge. An absent target
                // source is a terminal vertex with implicit distance0.
                distance[node]=next[node]==NO_INDEX ? 1 : distance[next[node]]+1;
                n.max_path=std::max<uint64_t>(n.max_path,distance[node]);
                color[node]=2; ++n.finished_active;
            }
        }
        if (n.finished_active!=edges.size()) throw std::logic_error("incomplete graph classification");
        if (const char* reason=c.exceeded()) {
            summary(c,n,"UNDECIDED",reason,0,false); return 2;
        }
        emit_edges(c,edges);
        summary(c,n,"NO_CENTER_CYCLE","exhausted",0,true); return 0;
    } catch (const std::bad_alloc&) {
        summary(c,n,"UNDECIDED","allocation_failed",0,false); return 2;
    }
}

uint64_t unsigned_number(const std::string& token) {
    uint64_t value=0;
    auto parsed=std::from_chars(token.data(),token.data()+token.size(),value);
    if (parsed.ec!=std::errc() || parsed.ptr!=token.data()+token.size())
        throw std::invalid_argument("invalid nonnegative integer");
    return value;
}

int map_states(const Context& c) {
    std::string token;
    uint64_t count=0;
    while (std::cin>>token) {
        uint64_t id=unsigned_number(token);
        if (id>=c.states) throw std::invalid_argument("state ID outside unfiltered domain");
        if ((count++&1023ULL)==0)
            if (const char* reason=c.exceeded()) { std::cerr<<"UNDECIDED: "<<reason<<'\n'; return 2; }
        uint64_t target=return_word(c,decode(c,id));
        std::cout<<id<<' ';
        if (target==NONE) std::cout<<-1;
        else std::cout<<target;
        std::cout<<'\n';
    }
    return 0;
}
} // namespace

int main(int argc,char** argv) {
    bool map=false, emit=false, unfiltered=false, have_width=false;
    uint64_t width=0, seconds=1500, edge_cap=MAX_EDGES;
    try {
        for (int i=1; i<argc; ++i) {
            std::string option=argv[i];
            if (option=="--map") map=true;
            else if (option=="--edges") emit=true;
            else if (option=="--unfiltered") unfiltered=true;
            else if (option=="--seconds" || option=="--edge-cap") {
                if (++i==argc) throw std::invalid_argument("missing option value");
                uint64_t value=unsigned_number(argv[i]);
                if (option=="--seconds") seconds=value;
                else edge_cap=value;
            } else {
                if (have_width) throw std::invalid_argument("multiple widths or unknown option");
                width=unsigned_number(option); have_width=true;
            }
        }
        if (!have_width || width<2 || width>MAX_WIDTH || seconds==0 || seconds>1500 || (map&&emit))
            throw std::invalid_argument("usage: p12_sparse [--map] W [--edges] [--seconds1..1500] [--edge-capN]");
        Context context(static_cast<int>(width),unfiltered,emit,edge_cap,static_cast<double>(seconds));
        return map ? map_states(context) : graph(context);
    } catch (const std::exception& error) {
        std::cerr<<"UNDECIDED: "<<error.what()<<'\n';
        if (!map) std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"invalid_input_or_internal_error\"}\n";
        return 2;
    }
}
