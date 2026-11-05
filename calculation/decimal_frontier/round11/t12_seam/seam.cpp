// r11c seam census: rooted W9|J|U3 junction return, sound for EVERY centre C.
// Prefix p = B0 ++ W0^14 ++ J ++ U^K (LSD-first folded pair coefficients from
// the integer root).  Low digits are exact (inlet 0 at the root).  High digits
// are normalized from the window end with BOTH unknown carry inlets e=0,1; the
// overflow must agree, and only the longest common prefix of the two candidate
// successors is kept (AC46 rooted-prefix argument, any interior).  After the
// forced clock (1000)^30 the protected prefix must equal the target
// B0 ++ W0^14 ++ J ++ U^(K+5) restricted to it.  Reports first mismatch
// position relative to the start of J (negative = W side).
#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
using V = std::vector<int>;
static const int B[34]={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const int W[9]={5,18,4,8,1,15,4,0,5};
static const int Q=14, J0=34+9*14;
// returns: 1e9 = survivor, -1e9 = gamma ambiguity/clock violation, else first mismatch pos rel J
static int run(const V &p0, const V &tgt, int *coreOut){
  V p=p0; int n; V d, a0, a1, l0, l1;
  for(int t=0;t<120;t++){
    n=p.size(); d.assign(n,0); a0.assign(n,0); a1.assign(n,0);
    int c=0; for(int i=0;i<n;i++){int z=p[i]+c; d[i]=z%10; c=z/10;}
    int e0=0,e1=1;
    for(int k=0;k<n;k++){int x=p[n-1-k]; int z=x+e0; a0[k]=z%10; e0=z/10; z=x+e1; a1[k]=z%10; e1=z/10;}
    if(e0!=e1) return -1000000000;
    int g=e0; if(g!=(t%4==0)) return -1000000001;
    l0.assign(n,0); l1.assign(n,0);
    if(g){ l0[0]=l1[0]=d[0]+1; for(int i=1;i<n;i++){l0[i]=d[i]+a0[n-i]; l1[i]=d[i]+a1[n-i];} }
    else { for(int i=0;i<n;i++){l0[i]=d[i]+a0[n-1-i]; l1[i]=d[i]+a1[n-1-i];} }
    int j=0; while(j<n && l0[j]==l1[j]) j++;
    p.assign(l0.begin(), l0.begin()+j);
    if(j==0) return -1000000002;
  }
  *coreOut=p.size();
  for(int i=0;i<(int)p.size();i++) if(p[i]!=tgt[i]) return i-J0;
  return 1000000000;
}
int main(int argc,char**argv){
  int Lj=atoi(argv[1]); int nth=argc>2?atoi(argv[2]):6; int K=argc>3?atoi(argv[3]):60;
  std::vector<std::array<int,3>> us;
  for(int a=0;a<=18;a+=2){int q[3]={9,a,18-a}; for(int r=0;r<3;r++) us.push_back({q[r],q[(r+1)%3],q[(r+2)%3]});}
  long long nj=1; for(int i=0;i<Lj;i++) nj*=19;
  long long total=nj*us.size(); std::atomic<long long> next(0); std::mutex mu;
  std::map<int,long long> hist; long long cases=0; int minCore=1<<30, maxCore=0; std::vector<std::string> surv;
  auto worker=[&](){
    std::map<int,long long> h; long long ct=0; int mc=1<<30, Mc=0; V p, tg;
    while(true){ long long st=next.fetch_add(1024); if(st>=total) break; long long en=std::min(total,st+1024);
      for(long long id=st;id<en;id++){
        int ui=id/nj; long long v=id%nj; p.clear();
        for(int i=0;i<34;i++) p.push_back(B[i]);
        for(int r=0;r<Q;r++) for(int i=0;i<9;i++) p.push_back(W[i]);
        std::vector<int> J(Lj); for(int i=0;i<Lj;i++){J[i]=v%19; v/=19;}
        for(int x:J) p.push_back(x);
        tg=p; for(int r=0;r<K;r++) for(int i=0;i<3;i++) p.push_back(us[ui][i]);
        for(int r=0;r<K+5;r++) for(int i=0;i<3;i++) tg.push_back(us[ui][i]);
        int core=0; int res=run(p,tg,&core);
        if(res<=-1000000000){ fprintf(stderr,"ANOMALY %d U=%d\n",res,ui); }
        if(res==1000000000){ std::lock_guard<std::mutex> lk(mu); char b[512]; int o=snprintf(b,512,"SURVIVOR U=%d,%d,%d J=",us[ui][0],us[ui][1],us[ui][2]); for(int x:J)o+=snprintf(b+o,512-o,"%d,",x); surv.push_back(b); }
        h[res]++; ct++; mc=std::min(mc,core-J0-Lj); Mc=std::max(Mc,core-J0-Lj);
      }}
    std::lock_guard<std::mutex> lk(mu); for(auto [k,n]:h) hist[k]+=n; cases+=ct; minCore=std::min(minCore,mc); maxCore=std::max(maxCore,Mc);
  };
  std::vector<std::thread> th; for(int i=0;i<nth;i++) th.emplace_back(worker); for(auto&t:th) t.join();
  printf("Jlen=%d cases=%lld K=%d protected_U_cols_after_J min=%d max=%d hist(firstMismatchRelJ)=",Lj,cases,K,minCore,maxCore);
  for(auto [k,n]:hist) printf("%d:%lld,",k,n);
  printf(" survivors=%zu\n",surv.size()); for(auto&s:surv) printf("%s\n",s.c_str());
}
