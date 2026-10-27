// Independent fixed-width exterior functional graph; no center is tested.
// Depends only on charge_index.hpp. No queue or on-disk graph is created.
// Build: c++ -O3 -std=c++17 charge_graph.cpp -o /tmp/charge-graph-107
// CLI: BASE WIDTH count
//      BASE WIDTH edge [comma,separated,coefficients]
//      BASE WIDTH census [--seconds S] [--memory-mib M] [--state-cap N]
//                        [--path-cap K]
// path-cap limits the acceleration buffer only; longer paths are recomputed.
// Exit 0: completed result; 3: UNDECIDED; 2: input/representation/internal error.

#include "charge_index.hpp"
#include <array>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>

using p196::agent107::ChargeIndex;
using U64 = std::uint64_t;
using Word = ChargeIndex::Word;
using Clock107 = std::chrono::steady_clock;

static U64 integer107(const std::string &s) {
  if(s.empty())throw std::invalid_argument("missing unsigned integer");
  U64 n=0, maximum=std::numeric_limits<U64>::max();
  for(char c:s) {
    if(c<'0'||c>'9')throw std::invalid_argument("invalid unsigned integer");
    unsigned d=unsigned(c-'0');
    if(n>maximum/10||(n==maximum/10&&d>maximum%10))
      throw std::overflow_error("integer exceeds uint64 capacity");
    n=10*n+d;
  }
  return n;
}

static std::string trim107(const std::string &s) {
  auto a=s.find_first_not_of(" \t\r\n");
  return a==std::string::npos?"":s.substr(a,s.find_last_not_of(" \t\r\n")-a+1);
}

static Word word107(const std::string &input) {
  auto s=trim107(input);
  if(s.size()<2||s.front()!='['||s.back()!=']')
    throw std::invalid_argument("word must be a bracketed integer list");
  auto body=trim107(s.substr(1,s.size()-2));
  Word word;
  if(body.empty())return word;
  std::size_t from=0;
  for(;;) {
    auto comma=body.find(',',from);
    U64 value=integer107(trim107(body.substr(from,comma==std::string::npos?comma:comma-from)));
    if(value>std::numeric_limits<unsigned>::max())
      throw std::invalid_argument("coefficient exceeds unsigned capacity");
    word.push_back(unsigned(value));
    if(comma==std::string::npos)break;
    from=comma+1;
  }
  return word;
}

static void print_word107(std::ostream &out,const Word &w) {
  out<<'[';
  for(std::size_t i=0;i<w.size();++i){if(i)out<<',';out<<w[i];}
  out<<']';
}

struct Trace107 {
  Word B,raw,B2;
  unsigned e=0,g=0;
  bool exit=false;
  U64 target=0;
};

struct Next107 { bool exit; U64 target; };

class Domain107 {
public:
  ChargeIndex index;
  U64 offset,total,color_bytes;
  explicit Domain107(unsigned base,unsigned width):index(base,width) {
    offset=width?ChargeIndex(base,width-1).count():0;
    if(offset>index.count())throw std::logic_error("width-count monotonicity failed");
    total=index.count()-offset;
    color_bytes=total/4+(total%4!=0);
    target_.resize(width);
  }
  U64 workspace_overhead() const {
    U64 w=index.width(),m=index.modulus(),a=2*index.base()-1;
    return w*m*(a+1)*sizeof(U64)+(w+1)*m*sizeof(U64)
         +(w*m+w+2)*sizeof(std::vector<U64>)+65536;
  }
  Next107 next(U64 relative,Trace107 *trace=nullptr) {
    if(relative>=total)throw std::out_of_range("relative state ID is outside domain");
    // The index already establishes coefficients and R=0. Keep shape/head
    // sanity here, without repeating the same residue calculation.
    return transform_word(index.unrank(offset+relative),trace);
  }
  Next107 next_word(const Word &B,Trace107 *trace=nullptr) {
    if(B.size()!=index.width()||!index.contains(B))
      throw std::invalid_argument("edge source must be an actual exact-width positive-head R-zero word");
    return transform_word(B,trace);
  }
private:
  Word target_;
  Next107 transform_word(const Word &B,Trace107 *trace) {
    unsigned n=index.width(),b=index.base();
    if(B.size()!=n||B.empty()||B[0]==0)
      throw std::logic_error("indexed source has an invalid width or head");
    // Every subsequently read element is explicitly assigned below. In
    // particular raw[n] is read only when g=1, after the n+1-entry loop.
    std::array<unsigned,65> D,H,raw;
    unsigned carry=0;
    for(unsigned i=0;i<n;++i){unsigned x=B[i]+carry;D[i]=x%b;carry=x/b;}
    unsigned e=carry;
    if(e>1)throw std::logic_error("forward carry is not a bit");
    carry=1-e;
    for(unsigned i=0;i<n;++i){unsigned x=B[n-1-i]+carry;H[i]=x%b;carry=x/b;}
    unsigned g=carry;
    if(g>1)throw std::logic_error("overflow is not a bit");
    for(unsigned i=0;i<n+g;++i) {
      unsigned left=i<n?D[i]:(b-1)*(1-e);
      unsigned right=g?(i?H[n-i]:1):H[n-1-i];
      raw[i]=left+right;
    }
    bool exits=g&&raw[n]!=b-1;
    if(trace) {
      trace->B=B;trace->raw.assign(raw.begin(),raw.begin()+n+g);
      trace->e=e;trace->g=g;trace->exit=exits;trace->B2.clear();
    }
    if(exits)return {true,0};
    for(unsigned i=0;i<n;++i)target_[i]=raw[i];
    if(target_.empty()||target_[0]==0)
      throw std::logic_error("internal successor violates head/coefficient/residue invariant");
    // rank itself validates the full coefficient and strong-residue domain.
    U64 absolute=index.rank(target_);
    if(absolute<offset||absolute>=index.count())
      throw std::logic_error("exact-width successor rank lies outside its interval");
    U64 relative=absolute-offset;
    if(trace){trace->B2=target_;trace->target=relative;}
    return {false,relative};
  }
};

struct Limits107 {
  double seconds=1200;
  U64 memory_mib=4096,state_cap=std::numeric_limits<U64>::max(),path_cap=65536;
};
struct Stop107 { std::string reason; };

class Census107 {
public:
  Domain107 &domain;
  Limits107 limits;
  U64 visited=0,finished=0,edges=0,exited=0,successor_calls=0,fallback_paths=0;
  std::string status="UNDECIDED",reason="not_started";
  std::vector<Trace107> witness;
  bool found_cycle=false;
  U64 planned_bytes=0;

  Census107(Domain107 &d,Limits107 l):domain(d),limits(l),began_(Clock107::now()){}
  double seconds() const {return std::chrono::duration<double>(Clock107::now()-began_).count();}

  void run() {
    try {
      if(!domain.total){status="ACYCLIC";reason="empty_domain";return;}
      check_time();
      if(!limits.state_cap)throw Stop107{"state_cap"};
      U64 capacity=std::min(limits.path_cap,domain.total);
      // Representation bounds make the small terms <= a few MiB. Color
      // bytes can be huge; subtract before adding to avoid unsigned wrap.
      U64 small=capacity*sizeof(U64)+domain.workspace_overhead();
      U64 budget=limits.memory_mib*1024*1024;
      if(small>budget||domain.color_bytes>budget-small)
        throw Stop107{"memory_budget"};
      planned_bytes=small+domain.color_bytes;
      if(domain.color_bytes>std::numeric_limits<std::size_t>::max())
        throw Stop107{"address_space"};
      try {
        colors_.assign(static_cast<std::size_t>(domain.color_bytes),0);
        path_.reserve(static_cast<std::size_t>(capacity));
      } catch(const std::bad_alloc &){throw Stop107{"memory_allocation"};}
      for(U64 start=0;start<domain.total;++start) {
        if((start&65535)==0)check_time(); // Also checked when skipping black IDs.
        if(color(start)==2)continue;
        if(color(start)!=0)throw std::logic_error("unresolved gray state between paths");
        path_.clear();
        U64 current=start,length=0;
        bool fallback=false,terminal=false;
        while(color(current)==0) {
          if(visited>=limits.state_cap)throw Stop107{"state_cap"};
          set_color(current,1);++visited;++length;
          if(path_.size()<capacity)path_.push_back(current);
          else if(!fallback){fallback=true;++fallback_paths;}
          Next107 successor=step(current);
          if(successor.exit){++exited;terminal=true;break;}
          ++edges;current=successor.target;
        }
        if(!terminal&&color(current)==1) {
          found_cycle=true;
          replay_cycle(current);
          check_time();
          status="CYCLIC";reason="replayed_exterior_cycle";return;
        }
        U64 resolved=0;
        if(fallback) {
          current=start;
          while(color(current)==1) {
            set_color(current,2);++finished;++resolved;
            Next107 successor=step(current); // Recompute, but do not recount arcs/exits.
            if(successor.exit)break;
            current=successor.target;
          }
        } else {
          for(U64 id:path_) {
            if(color(id)!=1)throw std::logic_error("path buffer contains a resolved vertex");
            set_color(id,2);++finished;++resolved;
          }
        }
        if(resolved!=length)throw std::logic_error("path blackening count mismatch");
      }
      if(visited!=domain.total||finished!=domain.total||edges+exited!=domain.total)
        throw std::logic_error("incomplete graph cannot receive ACYCLIC status");
      check_time();
      status="ACYCLIC";reason="all_states_finished";
    } catch(const Stop107 &stop){status="UNDECIDED";reason=stop.reason;}
      catch(const std::bad_alloc &){status="UNDECIDED";reason="memory_allocation";}
  }

private:
  Clock107::time_point began_;
  std::vector<std::uint8_t> colors_;
  std::vector<U64> path_;
  unsigned color(U64 id) const {
    return (colors_[static_cast<std::size_t>(id>>2)]>>((id&3)*2))&3;
  }
  void set_color(U64 id,unsigned value) {
    auto &cell=colors_[static_cast<std::size_t>(id>>2)];
    unsigned shift=unsigned((id&3)*2),mask=3u<<shift;
    cell=std::uint8_t((unsigned(cell)&~mask)|(value<<shift));
  }
  void check_time() const {if(seconds()>=limits.seconds)throw Stop107{"deadline"};}
  Next107 step(U64 id,Trace107 *trace=nullptr) {
    if((successor_calls&4095)==0)check_time();
    ++successor_calls;
    return domain.next(id,trace);
  }
  void replay_cycle(U64 anchor) {
    constexpr U64 maximum=4096;
    U64 per=sizeof(Trace107)+(3*domain.index.width()+1)*sizeof(unsigned);
    U64 budget=limits.memory_mib*1024*1024;
    if(planned_bytes>budget||maximum*per>budget-planned_bytes)
      throw Stop107{"witness_memory_budget"};
    witness.reserve(maximum);
    U64 current=anchor,overflows=0;
    do {
      if(witness.size()>=maximum)throw Stop107{"witness_limit"};
      Trace107 trace;
      Next107 next=step(current,&trace);
      if(next.exit)throw std::logic_error("cycle replay exited its domain");
      if(color(next.target)!=1)throw std::logic_error("cycle replay left its gray path");
      overflows+=trace.g;
      witness.push_back(std::move(trace));
      current=next.target;
    } while(current!=anchor);
    if(!overflows)throw std::logic_error("positive-head exterior cycle has no overflow");
  }
};

static void print_trace107(std::ostream &out,const Trace107 &t,bool include_raw) {
  out<<"{\"B\":";print_word107(out,t.B);
  if(include_raw){out<<",\"raw\":";print_word107(out,t.raw);}
  out<<",\"e\":"<<t.e<<",\"g\":"<<t.g<<",\"u\":";
  if(t.exit)out<<"null";else out<<t.g;
  out<<",\"exit\":"<<(t.exit?"true":"false")<<",\"B2\":";
  if(t.exit)out<<"null";else print_word107(out,t.B2);
  out<<",\"target\":";
  if(t.exit)out<<"null";else out<<t.target;
  out<<'}';
}

int main(int argc,char **argv) {
  try {
    if(argc<4)throw std::invalid_argument("usage: BASE WIDTH count|edge|census [arguments]");
    U64 base=integer107(argv[1]),width=integer107(argv[2]);
    if(base>62||width>64)throw std::invalid_argument("supported base2..62 and width0..64 only");
    Domain107 domain{unsigned(base),unsigned(width)};
    std::string command=argv[3];
    std::cout<<std::setprecision(9);
    if(command=="count") {
      if(argc!=4)throw std::invalid_argument("count takes no arguments");
      std::cout<<"{\"status\":\"COUNT\",\"base\":"<<base<<",\"width\":"<<width
        <<",\"total\":"<<domain.total<<",\"offset\":"<<domain.offset
        <<",\"upper_count\":"<<domain.index.count()<<",\"color_bytes\":"<<domain.color_bytes<<"}\n";
      return 0;
    }
    if(command=="edge") {
      if(argc<5)throw std::invalid_argument("edge requires one bracketed word");
      std::string input;
      for(int i=4;i<argc;++i){if(i>4)input+=' ';input+=argv[i];}
      Trace107 trace;
      domain.next_word(word107(input),&trace);
      std::ostringstream edge;
      print_trace107(edge,trace,true);
      std::cout<<"{\"status\":\"EDGE\","<<edge.str().substr(1)<<'\n';
      return 0;
    }
    if(command!="census")throw std::invalid_argument("unknown command");
    Limits107 limits;
    for(int i=4;i<argc;++i) {
      std::string flag=argv[i];
      if(++i>=argc)throw std::invalid_argument("missing census option value");
      std::string value=argv[i];
      if(flag=="--seconds") {
        std::size_t used=0;
        limits.seconds=std::stod(value,&used);
        if(used!=value.size()||!std::isfinite(limits.seconds)||limits.seconds<0||limits.seconds>1700)
          throw std::invalid_argument("seconds must be finite in [0,1700]");
      } else if(flag=="--memory-mib") {
        limits.memory_mib=integer107(value);
        if(limits.memory_mib>4096)throw std::invalid_argument("memory budget maximum is 4096MiB");
      } else if(flag=="--state-cap")limits.state_cap=integer107(value);
      else if(flag=="--path-cap") {
        limits.path_cap=integer107(value);
        if(limits.path_cap>65536)throw std::invalid_argument("path buffer maximum is 65536 IDs");
      } else throw std::invalid_argument("unknown census option");
    }
    Census107 run(domain,limits);run.run();
    std::cout<<"{\"status\":\""<<run.status<<"\",\"reason\":\""<<run.reason
      <<"\",\"scope\":\"fixed_width_exterior_only\",\"base\":"<<base<<",\"width\":"<<width
      <<",\"total\":"<<domain.total<<",\"offset\":"<<domain.offset<<",\"color_bytes\":"<<domain.color_bytes
      <<",\"planned_bytes\":"<<run.planned_bytes<<",\"visited\":"<<run.visited<<",\"finished\":"<<run.finished
      <<",\"edges\":"<<run.edges<<",\"exited\":"<<run.exited<<",\"successor_calls\":"<<run.successor_calls
      <<",\"fallback_paths\":"<<run.fallback_paths<<",\"seconds\":"<<run.seconds()
      <<",\"found_cycle\":"<<(run.found_cycle?"true":"false")<<",\"witness\":[";
    if(run.status=="CYCLIC")for(std::size_t i=0;i<run.witness.size();++i) {
      if(i)std::cout<<',';
      print_trace107(std::cout,run.witness[i],false);
    }
    std::cout<<"]}\n";
    return run.status=="UNDECIDED"?3:0;
  } catch(const std::exception &error) {
    std::cout<<"{\"status\":\"ERROR\",\"error\":\""<<error.what()<<"\"}\n";
    return 2;
  }
}
