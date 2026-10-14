#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

// Exact functional graph for q=P B^M reverse(P), M>=3, with |P|=k.
// Coefficients and ordinary addition digits are written least-significant first.
// This file does not assert a Lychrel number exists unless a verified cycle is found.

static constexpr std::array<int,6> bulk{16,14,10,2,4,8};
static constexpr uint32_t dead=std::numeric_limits<uint32_t>::max();
struct Step {
  bool valid=false;
  int overflow=0;
  std::array<int,12> prefix{};
};

Step step(const std::array<int,12>& p,int k,int phase,int middle) {
  const int n=2*k+middle;
  std::array<int,40> q{},digits{},r{};
  for(int i=0;i<k;i++)q[i]=q[n-1-i]=p[i];
  for(int i=k;i<k+middle;i++)q[i]=bulk[phase];
  int carry=0;
  for(int i=0;i<n;i++){
    int s=q[i]+carry;
    digits[i]=s%10;carry=s/10;
  }
  const int out=n+carry;
  if(carry)digits[n]=carry;
  for(int i=0;i<out;i++)r[i]=digits[i]+digits[out-1-i];
  Step z;z.overflow=carry;
  for(int i=k;i<out-k;i++)if(r[i]!=bulk[(phase+1)%6])return z;
  for(int i=0;i<k;i++)z.prefix[i]=r[i];
  if(z.prefix[0]<=0||z.prefix[0]>18)throw std::runtime_error("noncanonical output");
  z.valid=true;return z;
}

std::array<int,12> decode(uint32_t code,int k){
  std::array<int,12> p{};
  p[0]=1+code%18;code/=18;
  for(int i=1;i<k;i++){p[i]=code%19;code/=19;}
  if(code)throw std::runtime_error("decode overflow");
  return p;
}
uint32_t encode(const std::array<int,12>&p,int k){
  uint32_t out=0;
  for(int i=k-1;i>=1;i--)out=out*19+p[i];
  return out*18+(p[0]-1);
}
void emit_array(std::ostream&o,const std::array<int,12>&p,int k){
  o<<'[';for(int i=0;i<k;i++){if(i)o<<',';o<<p[i];}o<<']';
}

int main(int argc,char**argv){
  const int min_k=argc>1?std::stoi(argv[1]):1;
  const int max_k=argc>2?std::stoi(argv[2]):5;
  const std::string output=argc>3?argv[3]:"exist_count_uniform_graph_results.json";
  if(min_k<1||max_k>7||min_k>max_k)throw std::runtime_error("unsupported k");
  std::ofstream report(output);
  report<<"{\"bulk_cycle\":[16,14,10,2,4,8],\"middle_controls\":[3,4],\"widths\":[\n";
  bool first_width=true;
  for(int k=min_k;k<=max_k;k++){
    auto start=std::chrono::steady_clock::now();
    uint32_t per=18;for(int i=1;i<k;i++)per*=19;
    const uint32_t total=6*per;
    std::vector<uint32_t> next(total,dead);
    uint64_t unsafe=0,core_fail=0,valid=0,overflow_edges=0;
    for(uint32_t id=0;id<total;id++){
      int phase=id/per;
      auto p=decode(id%per,k);
      bool safe=bulk[phase]>9;
      for(int i=0;i<k;i++)safe=safe||p[i]>9;
      // The other bad pattern (outer11, coefficients all0/11) is impossible
      // because the nonempty bulk is none of 0 or11.
      if(!safe){unsafe++;continue;}
      const auto a=step(p,k,phase,3),b=step(p,k,phase,4);
      if(a.valid!=b.valid||a.overflow!=b.overflow)
        throw std::runtime_error("middle parity mismatch");
      if(!b.valid){core_fail++;continue;}
      for(int i=0;i<k;i++)if(a.prefix[i]!=b.prefix[i])
        throw std::runtime_error("middle prefix mismatch");
      next[id]=((phase+1)%6)*per+encode(b.prefix,k);
      valid++;overflow_edges+=b.overflow;
    }
    std::vector<uint8_t> color(total,0);
    uint64_t cycles=0,cycle_states=0,max_depth=0;
    std::vector<std::vector<uint32_t>> witnesses;
    for(uint32_t id=0;id<total;id++){
      if(color[id])continue;
      uint32_t v=id;uint64_t depth=0;
      while(v!=dead&&color[v]==0){color[v]=1;v=next[v];depth++;}
      if(depth>max_depth)max_depth=depth;
      if(v!=dead&&color[v]==1){
        std::vector<uint32_t> c;uint32_t u=v;
        do{c.push_back(u);u=next[u];}while(u!=v);
        cycles++;cycle_states+=c.size();
        if(witnesses.size()<20)witnesses.push_back(std::move(c));
      }
      v=id;
      while(v!=dead&&color[v]==1){color[v]=2;v=next[v];}
    }
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    if(!first_width)report<<",\n";first_width=false;
    report<<"{\"boundary_width\":"<<k<<",\"states\":"<<total
      <<",\"unsafe_states\":"<<unsafe<<",\"core_mismatches\":"<<core_fail
      <<",\"valid_edges\":"<<valid<<",\"overflow_edges\":"<<overflow_edges
      <<",\"cycles\":"<<cycles<<",\"cycle_states\":"<<cycle_states
      <<",\"max_dfs_segment\":"<<max_depth<<",\"seconds\":"<<seconds
      <<",\"witnesses\":[";
    bool first_cycle=true;
    for(const auto&c:witnesses){
      if(!first_cycle)report<<',';first_cycle=false;report<<'[';
      bool first_state=true;
      for(uint32_t id:c){
        if(!first_state)report<<',';first_state=false;
        int phase=id/per;auto p=decode(id%per,k);auto z=step(p,k,phase,4);
        report<<"{\"phase\":"<<phase<<",\"bulk\":"<<bulk[phase]<<",\"prefix\":";
        emit_array(report,p,k);report<<",\"overflow\":"<<z.overflow<<'}';
      }
      report<<']';
    }
    report<<"]}";report.flush();
    std::cout<<"k="<<k<<" states="<<total<<" edges="<<valid<<" cycles="<<cycles
      <<" cycle_states="<<cycle_states<<" seconds="<<seconds<<std::endl;
  }
  report<<"\n]}\n";
}
