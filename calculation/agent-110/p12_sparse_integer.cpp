// Independent positional-integer reference for the documented p12 center driver.
// No carry-by-column normalization and no dependency on the primary implementation.
// Odd-width source pruning uses Agent 3's necessary A(C)=9 (mod 11), even-middle
// invariant.  Complete return graphs are checked by sparse Kahn indegree peeling.
// --map W is deliberately UNFILTERED; W --edges emits the complete sorted graph.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
using I = std::uint32_t;
constexpr U BAD = std::numeric_limits<U>::max();
constexpr I NO_NEXT = std::numeric_limits<I>::max();
constexpr std::array<int,12> E = {1,0,1,0,1,0,0,1,0,1,0,1};
constexpr std::array<int,12> G = {1,0,0,0,1,0,0,0,1,0,0,0};
constexpr std::array<int,11> EVEN = {0,12,2,14,4,16,6,18,8,-1,10};

struct Edge {
  U source, target;
  bool operator<(const Edge& other) const {
    return source != other.source ? source < other.source : target < other.target;
  }
};
struct Options {
  int width = 0;
  bool map = false, edges = false;
  double seconds = 1500;
  U max_candidates = 1000000000ULL;
  U max_edges = 2000000ULL;
  U memory_bytes = 512ULL*1024*1024;
};
struct Clock {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  double elapsed() const {
    return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  }
};
int mod11(int x) { x %= 11; return x < 0 ? x+11 : x; }
U power(U base,int exponent) {
  U result = 1;
  for (int i=0;i<exponent;++i) {
    if (result > std::numeric_limits<U>::max()/base) throw std::runtime_error("power overflow");
    result *= base;
  }
  return result;
}

struct Driver {
  int width, half;
  U full_states;
  std::array<U,19> ten{};
  std::array<int,24> entry{}, overflow{}, trim{}, offset{};
  explicit Driver(int w):width(w),half((w-1)/2),full_states(power(19,half)) {
    ten[0] = 1;
    for (int i=1;i<19;++i) ten[i]=10*ten[i-1];
    int sum = 0;
    std::array<int,24> original_v{}, original_r{};
    for (int i=0;i<24;++i) {
      original_r[i]=sum%2;
      original_v[i]=(sum+G[i%12])/2-sum/2;
      sum+=G[i%12];
    }
    if (sum!=6) throw std::runtime_error("bad overflow period");
    for (int i=0;i<24;++i) {
      int t=(i+4)%24;
      entry[i]=E[t%12]; overflow[i]=G[t%12]; trim[i]=original_v[t];
      offset[i]=original_r[t]-1;
    }
    if (entry[0]!=1 || overflow[0]!=1 || trim[0]!=1 || offset[0]!=0)
      throw std::runtime_error("bad anchor");
  }

  std::array<int,18> word(U code) const {
    if (code>=full_states) throw std::runtime_error("source ID outside domain");
    std::array<int,18> c{};
    c[0]=c[width-1]=9;
    for (int j=0;j<half;++j) {
      int d=static_cast<int>(code%19); code/=19;
      c[j+1]=c[width-2-j]=d;
    }
    return c;
  }
  U value(U code) const {
    auto c=word(code);
    U v=0;
    for (int j=width-1;j>=0;--j) v=10*v+static_cast<U>(c[j]);
    return v;
  }
  bool allowed(U code) const {
    if (code>=full_states) return false;
    if (width%2==0) return true;
    int twice_sum=0, middle=0;
    for (int j=0;j<half;++j) {
      int d=static_cast<int>(code%19); code/=19;
      if (j+1==half) middle=d;
      else twice_sum += (j%2 ? -2 : 2)*d;
    }
    int sign=((half-1)%2 ? -1 : 1);
    return middle%2==0 && mod11(twice_sum+sign*middle)==9;
  }
  U candidate_count() const {
    if (width%2==0) return full_states;
    std::array<U,11> counts{}; counts[0]=1;
    for (int j=0;j<half-1;++j) {
      std::array<U,11> next{};
      for (int r=0;r<11;++r) for (int digit=0;digit<19;++digit)
        next[mod11(r+(j%2 ? -2 : 2)*digit)] += counts[r];
      counts=next;
    }
    int sign=((half-1)%2 ? -1 : 1);
    U total=0;
    for (int r=0;r<11;++r) if (EVEN[mod11(sign*(9-r))]>=0) total+=counts[r];
    return total;
  }

  // The entire coefficient word is represented by its positional integer.
  // Its normalization is obtained by integer quotient and repeated divmod.
  // No coefficient-to-coefficient carry recurrence appears in this routine.
  U successor(U positional, bool& completed) const {
    completed=false;
    int length=width;
    for (int t=0;t<24;++t) {
      if (length!=width+offset[t]) throw std::runtime_error("width profile mismatch");
      U n=positional+static_cast<U>(entry[t]);
      if (n>=2*ten[length]) throw std::runtime_error("coefficient value out of bounds");
      if (static_cast<int>(n>=ten[length])!=1-entry[t]) return BAD;
      std::array<int,18> digits{};
      U rest=n;
      for (int j=0;j<length;++j) {
        digits[j]=static_cast<int>(rest%10); rest/=10;
      }
      if (rest!=static_cast<U>(1-entry[t])) throw std::runtime_error("normalization mismatch");
      int raw_length=length;
      if (overflow[t]) digits[raw_length++]=9*entry[t];
      const int cut=trim[t];
      if (raw_length-2*cut<1) return BAD;
      if (cut && digits[0]+digits[raw_length-1]!=9) return BAD;
      int next_length=raw_length-2*cut;
      if (t==23) {
        completed=true;
        if (next_length!=width) throw std::runtime_error("return width mismatch");
        if (digits[cut]+digits[raw_length-1-cut]!=9) return BAD;
        U code=0;
        for (int j=half;j>=1;--j) {
          int index=cut+j;
          int coefficient=digits[index]+digits[raw_length-1-index];
          code=19*code+static_cast<U>(coefficient);
        }
        return code;
      }
      positional=0;
      for (int j=raw_length-cut-1;j>=cut;--j)
        positional=10*positional+static_cast<U>(digits[j]+digits[raw_length-1-j]);
      length=next_length;
    }
    throw std::runtime_error("unreachable return path");
  }
};

std::string digest(const std::vector<Edge>& edges) {
  U hash=14695981039346656037ULL;
  for (const auto& edge:edges) for (U n:{edge.source,edge.target})
    for (int byte=0;byte<8;++byte) {
      hash^=(n>>(8*byte))&255U; hash*=1099511628211ULL;
    }
  std::ostringstream out;
  out<<std::hex<<std::setw(16)<<std::setfill('0')<<hash;
  return out.str();
}
void print_word(const Driver& d,U id) {
  auto c=d.word(id);
  std::cout<<'[';
  for (int j=0;j<d.width;++j) std::cout<<(j ? "," : "")<<c[j];
  std::cout<<']';
}

int census(const Options& opt) {
  Clock clock;
  Driver d(opt.width);
  U candidates=d.candidate_count(), evaluated=0, initial=0, complete=0;
  auto undecided=[&](const char* reason) {
    std::cout<<"{\"width\":"<<d.width<<",\"full_source_states\":"<<d.full_states
      <<",\"candidate_states\":"<<candidates<<",\"evaluated_candidates\":"<<evaluated
      <<",\"cycle_scan_complete\":false,\"status\":\"UNDECIDED\",\"reason\":\""
      <<reason<<"\",\"seconds\":"<<clock.elapsed()<<"}\n";
    return 2;
  };
  if (candidates>opt.max_candidates) return undecided("candidate cap");
  const bool odd=(d.width%2)==1;
  int free_digits=d.half-(odd ? 1 : 0);
  U outer_count=power(19,free_digits);
  std::array<int,8> digits{};
  std::array<U,8> weight{};
  for (int j=0;j<free_digits;++j) weight[j]=d.ten[j+1]+d.ten[d.width-2-j];
  U outer_value=9+9*d.ten[d.width-1];
  int twice_alternating=0;
  std::vector<Edge> edges;
  for (U outer=0;outer<outer_count;++outer) {
    if ((outer&4095U)==0 && clock.elapsed()>opt.seconds) return undecided("time cap");
    int middle=0;
    if (odd) {
      int sign=((d.half-1)%2 ? -1 : 1);
      middle=EVEN[mod11(sign*(9-twice_alternating))];
    }
    if (middle>=0) {
      ++evaluated;
      U source=outer+(odd ? static_cast<U>(middle)*outer_count : 0);
      U positional=outer_value+(odd ? static_cast<U>(middle)*d.ten[d.half] : 0);
      if (positional+1<d.ten[d.width]) {
        ++initial;
        bool finished=false;
        U target=d.successor(positional,finished);
        if (finished) ++complete;
        if (target!=BAD && d.allowed(target)) {
          if (edges.size()>=opt.max_edges) return undecided("edge cap");
          // This bound includes vector growth plus the eventual sparse graph.
          if ((static_cast<U>(edges.size())+1)*160>opt.memory_bytes)
            return undecided("memory guard");
          edges.push_back({source,target});
        }
      }
    }
    for (int j=0;j<free_digits;++j) {
      int sign=(j%2 ? -2 : 2);
      if (digits[j]<18) {
        ++digits[j]; outer_value+=weight[j]; twice_alternating+=sign; break;
      }
      digits[j]=0; outer_value-=18*weight[j]; twice_alternating-=18*sign;
    }
  }
  if (evaluated!=candidates) throw std::runtime_error("candidate DP mismatch");
  U expected_initial=odd ? candidates/2 : (candidates-1)/2;
  if (initial!=expected_initial) throw std::runtime_error("carry complement count mismatch");
  if (clock.elapsed()>opt.seconds) return undecided("time cap before graph check");
  std::sort(edges.begin(),edges.end());
  std::vector<U> vertices;
  vertices.reserve(2*edges.size());
  for (const auto& edge:edges) { vertices.push_back(edge.source); vertices.push_back(edge.target); }
  std::sort(vertices.begin(),vertices.end());
  vertices.erase(std::unique(vertices.begin(),vertices.end()),vertices.end());
  if (vertices.size()>=NO_NEXT) return undecided("sparse index guard");
  std::vector<I> indegree(vertices.size(),0), next(vertices.size(),NO_NEXT), ready;
  ready.reserve(vertices.size());
  auto index=[&](U id) { return static_cast<I>(std::lower_bound(vertices.begin(),vertices.end(),id)-vertices.begin()); };
  for (const auto& edge:edges) {
    I a=index(edge.source), b=index(edge.target);
    if (next[a]!=NO_NEXT) throw std::runtime_error("return map is not a function");
    next[a]=b; ++indegree[b];
  }
  for (I i=0;i<vertices.size();++i) if (!indegree[i]) ready.push_back(i);
  std::size_t peeled=0;
  while (peeled<ready.size()) {
    if ((peeled&16383U)==0 && clock.elapsed()>opt.seconds) return undecided("graph time cap");
    I node=ready[peeled++], target=next[node];
    if (target!=NO_NEXT && --indegree[target]==0) ready.push_back(target);
  }
  U cycle_nodes=vertices.size()-peeled;
  U removed=candidates-cycle_nodes;
  if (opt.edges) for (const auto& edge:edges)
    std::cout<<"EDGE "<<edge.source<<' '<<edge.target<<'\n';
  std::cout<<std::setprecision(9)<<"{\"width\":"<<d.width
    <<",\"full_source_states\":"<<d.full_states<<",\"candidate_states\":"<<candidates
    <<",\"evaluated_candidates\":"<<evaluated<<",\"initial_flip_valid\":"<<initial
    <<",\"completed_returns\":"<<complete<<",\"edges\":"<<edges.size()
    <<",\"removed\":"<<removed<<",\"cycle_nodes\":"<<cycle_nodes
    <<",\"cycle_scan_complete\":true,\"edge_digest\":\""<<digest(edges)
    <<"\",\"seconds\":"<<clock.elapsed()<<",\"status\":\""
    <<(cycle_nodes ? "CENTER_CYCLE" : "NONE")<<"\"}\n";
  if (cycle_nodes) {
    I seed=0; while (!indegree[seed]) ++seed;
    I node=seed;
    do {
      I target=next[node];
      std::cout<<"CYCLE_EDGE "<<vertices[node]<<' '<<vertices[target]<<" source=";
      print_word(d,vertices[node]); std::cout<<" target="; print_word(d,vertices[target]); std::cout<<'\n';
      node=target;
    } while (node!=seed);
    return 3;
  }
  return 0;
}

U parse_u(const std::string& s) {
  if (s.empty() || s.find_first_not_of("0123456789")!=std::string::npos)
    throw std::runtime_error("expected unsigned integer");
  std::size_t used=0;
  U v=std::stoull(s,&used);
  if (used!=s.size()) throw std::runtime_error("bad integer");
  return v;
}
int main(int argc,char** argv) {
  try {
    if (argc<2) throw std::runtime_error("usage: program W [--edges] [--seconds S] [--max-candidates N] [--max-edges N] [--memory-mib N], or --map W");
    Options opt;
    int at=1;
    if (std::string(argv[at])=="--map") { opt.map=true; ++at; }
    if (at>=argc) throw std::runtime_error("missing width");
    U parsed_width=parse_u(argv[at++]);
    if (parsed_width<2 || parsed_width>17) throw std::runtime_error("supported widths: 2..17");
    opt.width=static_cast<int>(parsed_width);
    while (at<argc) {
      std::string arg=argv[at++];
      if (arg=="--edges") { opt.edges=true; continue; }
      if (at>=argc) throw std::runtime_error("missing option value");
      std::string val=argv[at++];
      if (arg=="--seconds") { std::size_t end=0; opt.seconds=std::stod(val,&end); if (end!=val.size()) throw std::runtime_error("bad seconds"); }
      else if (arg=="--max-candidates") opt.max_candidates=parse_u(val);
      else if (arg=="--max-edges") opt.max_edges=parse_u(val);
      else if (arg=="--memory-mib") { U mb=parse_u(val); if (mb>4096) throw std::runtime_error("memory cap exceeds 4096 MiB"); opt.memory_bytes=mb*1024*1024; }
      else throw std::runtime_error("unknown option");
    }
    if (!(opt.seconds>0 && opt.seconds<=1500) || !opt.max_candidates || !opt.max_edges || opt.memory_bytes<16*1024*1024)
      throw std::runtime_error("invalid resource budget");
    if (opt.map) {
      Driver d(opt.width); Clock clock; std::string token;
      while (std::cin>>token) {
        if (clock.elapsed()>opt.seconds) { std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"map time cap\"}\n"; return 2; }
        U id=parse_u(token); bool complete=false;
        U target=d.successor(d.value(id),complete);
        std::cout<<id<<' '; if (target==BAD) std::cout<<-1; else std::cout<<target; std::cout<<'\n';
      }
      if (!std::cin.eof()) throw std::runtime_error("stdin read error");
      return 0;
    }
    return census(opt);
  } catch (const std::bad_alloc&) {
    std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"allocation failure\"}\n"; return 2;
  } catch (const std::exception& ex) {
    std::cerr<<"ERROR: "<<ex.what()<<'\n'; return 1;
  }
}
