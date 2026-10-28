// Independent brute force for the centre system, own derivation from the Lean mirror definitions.
// usage: cfg b E G W [dump]    E,G strings of 0/1 (one per phase, aligned), W = max width.
// A centre state = palindromic coefficient vector C (len m), coeffs in [0,2b-2], odd m => middle coeff even,
// canonically (maximally) trimmed: m>=2 => C[0]!=b-1.
// One phase: need carry-out of norm(C, carry-in e)==1-e (that is e2 = 1-e, hyp), DC = digits, 
// C' = DC + rev(DC) (g=0) or (DC++[y]) + rev(DC++[y])... (g=1, y=(b-1)e), then maximal trim.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int b,P,W; vector<int> E,Gs;
struct St{int m; int c[24];};
static inline u64 key(const St&s){ u64 k=s.m; int h=(s.m+1)/2; for(int i=0;i<h;i++) k=(k<<5)|(u64)s.c[i]; return k; }
static inline St unkey(u64 k){ // m is in the top: recover by trying m from 1..W and checking consistency
  for(int m=1;m<=24;m++){ int h=(m+1)/2; u64 mm=k>>(5*h); if((int)mm==m){ St s; s.m=m; u64 kk=k; for(int i=h-1;i>=0;i--){s.c[i]=kk&31;kk>>=5;} for(int i=0;i<h;i++) s.c[m-1-i]=s.c[i]; return s; } }
  St s; s.m=0; return s; }
bool step(const St&s,int e,int g,St&out){
  int m=s.m; int dc[26]; int car=e;
  for(int i=0;i<m;i++){int v=s.c[i]+car; dc[i]=v%b; car=v/b;}
  if(car!=1-e) return false;
  int n2; int d2[28];
  if(g==0){ n2=m; for(int i=0;i<m;i++) d2[i]=dc[i]+dc[m-1-i]; }
  else { n2=m+1; int y=(b-1)*e; int dt[28]; for(int i=0;i<m;i++) dt[i]=dc[i]; dt[m]=y; for(int i=0;i<=m;i++) d2[i]=dt[i]+dt[m-i]; }
  int lo=0,hi=n2-1;
  while(hi-lo+1>=2 && d2[lo]==b-1 && d2[hi]==b-1){lo++;hi--;}
  int m2=hi-lo+1; if(m2<=0) return false;
  if(m2>24) return false;
  out.m=m2; for(int i=0;i<m2;i++) out.c[i]=d2[lo+i];
  return true;
}
int main(int argc,char**argv){
  b=atoi(argv[1]); string es=argv[2], gs=argv[3]; W=atoi(argv[4]); P=es.size();
  for(char ch:es) E.push_back(ch-'0'); for(char ch:gs) Gs.push_back(ch-'0');
  if(argc>5 && string(argv[5])=="img"){ // read states from stdin: m c0 c1 ... ; print lap image or DEAD
    int m; while(scanf("%d",&m)==1){ St s; s.m=m; for(int i=0;i<m;i++) scanf("%d",&s.c[i]); bool ok=true; St cur=s;
      for(int t=0;t<P&&ok;t++){ St nx; if(!step(cur,E[t],Gs[t],nx)) ok=false; else cur=nx; }
      if(!ok) printf("DEAD\n"); else { printf("%d",cur.m); for(int i=0;i<cur.m;i++) printf(" %d",cur.c[i]); printf("\n"); } }
    return 0; }
  unordered_map<u64,u64> img; u64 total=0, beyond=0;
  map<int,long long> lapHist; int maxLaps=0; vector<int> exampleMax; int exampleW=0; long long immortal=0; map<int,int> maxByW;
  for(int m=1;m<=W;m++){
    int h=(m+1)/2; bool odd=m&1; vector<int> idx(h,0);
    while(true){
      St s; s.m=m; bool ok=true;
      for(int i=0;i<h;i++) s.c[i]=idx[i];
      if(odd && (s.c[h-1]&1)) ok=false;
      if(m>=2 && s.c[0]==b-1) ok=false;
      if(ok){
        for(int i=0;i<h;i++) s.c[m-1-i]=s.c[i];
        total++;
        St cur=s; bool alive=true;
        for(int t=0;t<P&&alive;t++){ St nx; if(!step(cur,E[t],Gs[t],nx)) alive=false; else cur=nx; }
        if(alive){ if(cur.m<=W) img[key(s)] = key(cur); else beyond++;
          // follow the true orbit
          int laps=1; St z=cur; bool ok=true;
          while(laps<300){ St w2=z; bool al=true; for(int t=0;t<P&&al;t++){ St nx; if(!step(w2,E[t],Gs[t],nx)) al=false; else w2=nx; } if(!al) break; z=w2; laps++; }
          if(laps>=300) immortal++;
          lapHist[laps]++; if(laps>maxByW[m]) maxByW[m]=laps; if(laps>maxLaps){maxLaps=laps; exampleMax.assign(s.c,s.c+s.m); exampleW=m;} }
      }
      int i=0; while(i<h){ idx[i]++; if(idx[i]<2*b-1) break; idx[i]=0; i++; }
      if(i==h) break;
    }
  }
  fprintf(stderr,"states enumerated %llu, lap survivors within W %zu, survivors with image wider than W %llu\n",total,img.size(),beyond);
  unordered_set<u64> alive; for(auto&kv:img) alive.insert(kv.first);
  int it=0;
  while(true){
    vector<u64> rm; for(u64 k:alive){ u64 im=img[k]; if(!alive.count(im)) rm.push_back(k); }
    if(rm.empty()) break; for(u64 k:rm) alive.erase(k); it++;
    fprintf(stderr,"iter %d alive %zu\n",it,alive.size());
    if(alive.empty()) break;
  }
  printf("RESULT b=%d E=%s G=%s W=%d lap_survivors=%zu beyondW=%llu cyclic_core=%zu\n",b,es.c_str(),gs.c_str(),W,img.size(),beyond,alive.size());
  int cnt=0; for(u64 k:alive){ St s=unkey(k); printf("core:"); for(int i=0;i<s.m;i++) printf(" %d",s.c[i]); printf("\n"); if(++cnt>10) break; }
  // also print width histogram of survivors
  map<int,int> hist; for(auto&kv:img){ St s=unkey(kv.first); hist[s.m]++; }
  printf("lap-survival histogram (laps survived by states that survive >=1 lap):"); for(auto&kv:lapHist) printf(" %d:%lld",kv.first,kv.second); printf("\n");
  printf("max laps survived by start width:"); for(auto&kv:maxByW) printf(" %d:%d",kv.first,kv.second); printf("   immortal(>=300 laps)=%lld\n",immortal);
  printf("longest-surviving start state (width %d):",exampleW); for(int x:exampleMax) printf(" %d",x); printf("\n");
  printf("survivor widths:"); for(auto&kv:hist) printf(" %d:%d",kv.first,kv.second); printf("\n");
}
