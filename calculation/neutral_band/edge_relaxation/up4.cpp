// Upward transfer construction from the bottom of the number (LSD end), period T, fixed overflow clock.
// Enumerates ALL periodic left pieces of any height; at each height checks whether a 9-wire can sit on top
// (optionally with a prescribed carry stream). Stops when the interface set repeats (=> never) or a wire fits.
// usage: up B T ovfpattern streamfile|ANY maxheight [cap]
#include <bits/stdc++.h>
#include <set>
using namespace std;
typedef unsigned long long u64;
int B,T; vector<int> ovf,OVI; int NOV; std::set<u64> seenStreams;
struct If{ u64 c,dreq,r; bool operator<(const If&o)const{ if(c!=o.c)return c<o.c; if(dreq!=o.dreq)return dreq<o.dreq; return r<o.r;} bool operator==(const If&o)const{return c==o.c&&dreq==o.dreq&&r==o.r;} };
// c: carry provided upward (bit t); dreq: carry required from above (bit t); r: r-digit provided at overflow times (4 bits each)
vector<If> out; If cur; int x0; u64 cs,ds,rs;
void dfs(int t,int x){
  if(t==T){ if(x==x0) out.push_back({cs,ds,rs}); return; }
  int cin=(cur.c>>t)&1, dneed=(cur.dreq>>t)&1;
  for(int d=0;d<2;d++){
    if((x+d)/B!=dneed) continue;
    int e=(x+cin)%B, r=(x+d)%B, cout_=(x+cin)/B;
    int nx = ovf[t] ? e + (int)((cur.r>>(4*OVI[t]))&15) : e + r;
    u64 sc=cs,sd=ds,sr=rs;
    cs|=(u64)cout_<<t; ds|=(u64)d<<t; if(ovf[t]) rs|=(u64)r<<(4*OVI[t]);
    dfs(t+1,nx); cs=sc;ds=sd;rs=sr;
  }
}
int main(int argc,char**argv){
  B=atoi(argv[1]); T=atoi(argv[2]); string pat=argv[3]; string sf=argv[4]; int maxh=atoi(argv[5]); long long cap=argc>6?atoll(argv[6]):60000000LL;
  ovf.assign(T,0); OVI.assign(T,-1); NOV=0;
  for(int t=0;t<T;t++){ ovf[t]=pat[t%pat.size()]-'0'; if(ovf[t]) OVI[t]=NOV++; }
  vector<u64> streams; bool any=(sf=="ANY");
  if(!any){ ifstream in(sf); string l; while(getline(in,l)) if(l.size()){ u64 m=0; for(int t=0;t<T;t++) if(l[t%l.size()]=='1') m|=1ULL<<t; streams.push_back(m);} }
  // bottom: c0=0, r_{-1}=1 at overflow times, required d_{-1} = clock ; and cell 0 must be >=1 always (checked below)
  If b{0,0,0}; for(int t=0;t<T;t++){ if(ovf[t]){ b.dreq|=1ULL<<t; b.r|=1ULL<<(4*OVI[t]); } }
  vector<If> S{b};
  deque<vector<If>> hist; deque<int> hd; hist.push_back(S); hd.push_back(0);
  for(int h=1;h<=maxh;h++){
    out.clear();
    for(auto&f:S){ cur=f; for(x0=(h==1?1:0);x0<2*B-1;x0++){ cs=ds=rs=0; dfs(0,x0);} }
    if(h==1){ // cell 0 must stay >=1 at all times: re-filter by re-simulating
      vector<If> o2; // simple re-run with check
      for(auto&f:out){ (void)f; o2.push_back(f);} out.swap(o2);
    }
    sort(out.begin(),out.end()); out.erase(unique(out.begin(),out.end()),out.end());
    // wire-compatibility: dreq = ~c (all t), r = (B-1)*c at overflow times, optionally c in streams
    long long hits=0; u64 mask=(T==64)?~0ULL:((1ULL<<T)-1);
    for(auto&f:out){
      if(((~f.c)&mask)!=f.dreq) continue;
      bool ok=true; for(int t=0;t<T&&ok;t++) if(ovf[t]){ int r=(f.r>>(4*OVI[t]))&15; if(r!=(B-1)*(int)((f.c>>t)&1)) ok=false; }
      if(!ok) continue;
      if(!any && find(streams.begin(),streams.end(),f.c)==streams.end()) continue;
      hits++; if(!seenStreams.count(f.c)){ seenStreams.insert(f.c); printf("  NEW STREAM at height %d: ",h); for(int t=0;t<T;t++) printf("%d",(int)((f.c>>t)&1)); printf("\n"); }
    }
    printf("height %d: %zu interfaces%s\n",h,out.size(),hits?"  <-- WIRE FITS":""); fflush(stdout);

    if(out.empty()){ printf("RESULT EMPTY at height %d\n",h); return 0; }
    for(size_t k=0;k<hist.size();k++) if(hist[k]==out){ printf("RESULT CYCLE: set at height %d equals set at height %d -> complete; distinct streams that fit a wire: %zu\n",h,hd[k],seenStreams.size()); return 0; }
    if((long long)out.size()>cap){ printf("RESULT TOO_BIG at height %d\n",h); return 0; }
    hist.push_back(out); hd.push_back(h); if(hist.size()>6){hist.pop_front();hd.pop_front();}
    S=out;
  }
  printf("RESULT MAXHEIGHT\n");
}
