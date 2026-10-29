#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using std::vector;
using V=vector<int>;
static const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W={5,18,4,8,1,15,4,0,5};
static const V U={8,9,10};
static V repeat(const V&w,int n){V r; r.reserve(w.size()*n);for(int i=0;i<n;i++)r.insert(r.end(),w.begin(),w.end());return r;}
static int next_non9_carry(const V& p, const V& next, int i){
  int j=next[i]; if(j<0) return -1; return p[j]>=10 ? 1 : 0;
}
struct StepResult { V p; int gamma; bool ok; int trim; };
// Exact centre-free update. For a symmetric full pairword P of length L,
// the partner of low coefficient i is at L-1-i when gamma=0, and at
// L-i when gamma=1 (the i=0 partner is the overflow digit 1). Carry into
// that partner is fixed by the first non-9 coefficient after i+1 (gamma=0)
// or i (gamma=1). Trimming the terminal 9-run plus one guarantees every
// requested partner carry is reset inside the known prefix, not in C.
static StepResult cone_step(const V& p){
  const int M=(int)p.size();
  if(M<3) return {{},0,false,0};
  int trail=0; while(trail<M && p[M-1-trail]==9) ++trail;
  int outlen=M-trail-1;
  if(outlen<=0) return {{},0,false,trail+1};
  V next(M+1,-1); int last=-1;
  for(int i=M-1;i>=0;--i){if(p[i]!=9)last=i;next[i]=last;}
  if(next[0]<0) return {{},0,false,trail+1};
  int gamma=p[next[0]]>=10 ? 1:0;
  V out(outlen); int carry=0;
  for(int i=0;i<outlen;i++){
    int z=p[i]+carry; int low=z%10; carry=z/10;
    int high;
    if(gamma==0){
      int hc=next_non9_carry(p,next,i+1); if(hc<0)return {{},gamma,false,trail+1};
      high=(p[i]+hc)%10;
    }else if(i==0){high=1;}
    else{
      int hc=next_non9_carry(p,next,i); if(hc<0)return {{},gamma,false,trail+1};
      high=(p[i-1]+hc)%10;
    }
    out[i]=low+high;
  }
  return {std::move(out),gamma,true,trail+1};
}
static V initial_prefix(const V& J,int q,int k){
  V p=B; V w=repeat(W,q); p.insert(p.end(),w.begin(),w.end()); p.insert(p.end(),J.begin(),J.end()); V u=repeat(U,k); p.insert(p.end(),u.begin(),u.end()); return p;
}
static V target_prefix(const V& J,int q,int k,int n){
  V p=B; V w=repeat(W,q); p.insert(p.end(),w.begin(),w.end()); p.insert(p.end(),J.begin(),J.end()); V u=repeat(U,k+5); p.insert(p.end(),u.begin(),u.end()); if((int)p.size()>n)p.resize(n); return p;
}
static V full_step(const V& p){V y; y.reserve(p.size()+1); int c=0;for(int x:p){int z=x+c;y.push_back(z%10);c=z/10;}if(c)y.push_back(c);V r(y.size());for(size_t i=0;i<y.size();++i)r[i]=y[i]+y[y.size()-1-i];return r;}
static V full_source(const V& J,const V& C,int q,int k){
  V h=B;V w=repeat(W,q);h.insert(h.end(),w.begin(),w.end());h.insert(h.end(),J.begin(),J.end());V u=repeat(U,k);h.insert(h.end(),u.begin(),u.end());V p=h;p.insert(p.end(),C.begin(),C.end());for(auto it=h.rbegin();it!=h.rend();++it)p.push_back(*it);return p;
}
static bool selftest(){
  const int q=14,k=100; const std::array<V,4> Js={V{0,0,0,0},V{8,9,10,0},V{12,14,9,16},V{9,9,9,9}};
  const std::array<V,5> Cs={V{0,0},V{18,18,18,18},V{6,12,12,6,8,10,10,8,6,12,12,6},V{4,12,4},V{6,12,8,12,6}};
  for(const auto& J:Js)for(const auto& C:Cs){
    V full=full_source(J,C,q,k); V pre(full.begin(),full.begin()+464);
    for(int t=0;t<120;t++){
      auto s=cone_step(pre); if(!s.ok){std::cerr<<"SELFTEST cone unavailable J="<<J.size()<<" t="<<t<<"\n";return false;}
      full=full_step(full);
      if(s.p.size()>full.size() || !std::equal(s.p.begin(),s.p.end(),full.begin())){
        std::cerr<<"SELFTEST mismatch J=";for(int x:J)std::cerr<<x<<',';std::cerr<<" C_len="<<C.size()<<" t="<<t<<"\n";return false;
      }
      pre=std::move(s.p);
    }
  }
  std::cout<<"SELFTEST_PASS: 4 J x 5 even/odd centres, all 120 phases, full symmetric pairword vs centre-free cone\n";
  return true;
}
struct Counts { uint64_t tested=0, wrong_clock=0, prefix_mismatch=0, prefix_survivor=0, outer_mismatch=0, inner_mismatch=0; uint64_t mismatch_at[500]={}; uint64_t final_len_sum=0; int min_final=9999,max_final=0,mismatch_min=9999,mismatch_max=-1; V minJ,maxJ; };
static void run_len(int jlen,Counts& c,bool print_survivors){
  const int q=14,k=100,K=34+9*q+jlen;
  const V targetBase=B; V wb=repeat(W,q);V fixed=targetBase;fixed.insert(fixed.end(),wb.begin(),wb.end());
  for(int code=0;code< (jlen==3?19*19*19:19*19*19*19);++code){
    int x=code; V J(jlen);for(int i=0;i<jlen;i++){J[i]=x%19;x/=19;}
    V pre=initial_prefix(J,q,k); // 34+9q+jlen+300 coefficients, independent of C
    int sumg=0; bool clock=true;
    for(int t=0;t<120;t++){
      auto s=cone_step(pre); if(!s.ok){std::cerr<<"CONE_ERROR jlen="<<jlen<<" code="<<code<<" t="<<t<<" len="<<pre.size()<<"\n";std::exit(3);}
      int expected=(t%4==0)?1:0;
      if(s.gamma!=expected)clock=false;
      sumg+=s.gamma; pre=std::move(s.p);
    }
    ++c.tested; c.final_len_sum+=pre.size();c.min_final=std::min(c.min_final,(int)pre.size());c.max_final=std::max(c.max_final,(int)pre.size());
    if(!clock){++c.wrong_clock;continue;}
    V tgt=fixed; tgt.insert(tgt.end(),J.begin(),J.end());V ub=repeat(U,k+5);tgt.insert(tgt.end(),ub.begin(),ub.end());
    int n=std::min((int)pre.size(),(int)tgt.size());int mm=-1;
    for(int i=0;i<n;i++)if(pre[i]!=tgt[i]){mm=i;break;}
    if(mm>=0){
      ++c.prefix_mismatch; if(mm<K)++c.outer_mismatch;else ++c.inner_mismatch;
      if(mm<500)c.mismatch_at[mm]++;
      if(mm<c.mismatch_min){c.mismatch_min=mm;c.minJ=J;}
      if(mm>c.mismatch_max){c.mismatch_max=mm;c.maxJ=J;}
    }
    else{++c.prefix_survivor;if(print_survivors){std::cout<<"SURVIVOR jlen="<<jlen<<" J=";for(int z:J)std::cout<<z<<',';std::cout<<" finalprefix="<<pre.size()<<" compared="<<n<<" gamma_sum="<<sumg<<"\n";}}
  }
}
int main(int argc,char**argv){
  if(argc>1 && std::string(argv[1])=="--selftest") return selftest()?0:1;
  Counts c3,c4;run_len(3,c3,false);run_len(4,c4,true);
  auto report=[](const char*name,const Counts&c){
    std::cout<<name<<" tested="<<c.tested<<" wrong_clock="<<c.wrong_clock<<" prefix_mismatch="<<c.prefix_mismatch<<" survivors="<<c.prefix_survivor<<" outer_mismatch="<<c.outer_mismatch<<" inner_mismatch="<<c.inner_mismatch<<" first_mismatch_min="<<c.mismatch_min<<" first_mismatch_max="<<c.mismatch_max<<" final_len_min="<<c.min_final<<" final_len_max="<<c.max_final<<" final_len_avg="<<(double)c.final_len_sum/c.tested<<"\n";
    std::cout<<name<<" minJ=";for(int x:c.minJ)std::cout<<x<<',';std::cout<<" maxJ=";for(int x:c.maxJ)std::cout<<x<<',';std::cout<<"\n";
    for(int i=0;i<500;i++)if(c.mismatch_at[i])std::cout<<name<<" mismatch["<<i<<"]="<<c.mismatch_at[i]<<"\n";
  };
  report("J3",c3);report("J4",c4);
  if(c3.tested!=6859 || c4.tested!=130321 || c3.wrong_clock || c4.wrong_clock ||
     c3.prefix_survivor || c4.prefix_survivor || c3.outer_mismatch!=c3.tested ||
     c4.outer_mismatch!=c4.tested || c3.mismatch_min!=135 || c3.mismatch_max!=144 ||
     c4.mismatch_min!=135 || c4.mismatch_max!=147 || c3.min_final!=298 || c3.max_final!=298 ||
     c4.min_final!=299 || c4.max_final!=299){
    std::cerr<<"W17_EXPECTED_OBSTRUCTION_CHECK_FAILED\n";return 4;
  }
  std::cout<<"CELL_PREFIX_CONE_DONE\n";
}
