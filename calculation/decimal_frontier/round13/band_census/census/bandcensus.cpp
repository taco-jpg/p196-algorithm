// bandcensus.cpp -- r13a.  Enumerate all time-periodic rows ("bands") of the folded reverse-and-add row map
// for a given base b and overflow clock g (period p), spatial period s.
// Row map (periodic carries): alpha_(c+1)=[x_c+alpha_c>=b], beta_c=[x_c+beta_(c+1)>=b],
//   lo_c=(x_c+alpha_c)%b, hi_c=(x_c+beta_(c+1))%b; y_c=lo_c+hi_c (g=0), y_c=lo_c+hi_(c-1) (g=1).
// All-(b-1) rows are excluded (carries undetermined).
// Method: bitset of all words of length s over {0..2b-2}, iterate A <- F(A), F = composition of the p row maps,
// until stable (then F is a bijection on A, A = periodic points of F).  Then cycle decomposition up to rotation.
// usage: bandcensus base clock s nthreads > out
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <thread>
#include <atomic>
#include <algorithm>
#include <unordered_set>
#include <map>
using namespace std;
typedef uint64_t u64; typedef uint8_t u8;
static int B, NL, S, P; static vector<int> CLK; static u64 PW[32]; static u64 N;
static inline bool rowstep(const u8*x,int n,int g,u8*y){
  int st=-1; for(int i=0;i<n;i++) if(x[i]!=B-1){st=i;break;}
  if(st<0) return false;
  u8 al[64],be[64],lo[64],hi[64];
  // low carries entering each column
  int a = x[st]>=B; // carry out of column st
  for(int k=1;k<n;k++){int i=(st+k)%n; al[i]=a; a=(x[i]+a>=B);} al[st]=a;
  // high carries be[c]=beta_c
  int h = x[st]>=B; be[st]=h;
  for(int k=1;k<n;k++){int i=(st-k+n)%n; h=(x[i]+h>=B); be[i]=h;}
  for(int c=0;c<n;c++){ lo[c]=(x[c]+al[c])%B; hi[c]=(x[c]+be[(c+1)%n])%B; }
  for(int c=0;c<n;c++){ y[c]=lo[c]+(g?hi[(c-1+n)%n]:hi[c]); }
  return true;
}
static inline void decode(u64 v,u8*x){ for(int i=0;i<S;i++){x[i]=v%NL; v/=NL;} }
static inline u64 encode(const u8*x){ u64 v=0; for(int i=S-1;i>=0;i--) v=v*NL+x[i]; return v; }
static inline bool Fstep(u8*x){ u8 y[64]; for(int t=0;t<P;t++){ if(!rowstep(x,S,CLK[t],y)) return false; memcpy(x,y,S);} return true; }
int main(int argc,char**argv){
  B=atoi(argv[1]); NL=2*B-1; string cs=argv[2]; P=cs.size(); for(char c:cs) CLK.push_back(c-'0'); S=atoi(argv[3]); int NT=atoi(argv[4]);
  PW[0]=1; for(int i=1;i<32;i++) PW[i]=PW[i-1]*NL; N=PW[S];
  u64 words=(N+63)/64; vector<u64> A(words,~0ULL); 
  if(N%64) A[words-1]=(1ULL<<(N%64))-1;
  // remove the all-(b-1) word
  { u64 v=0; for(int i=S-1;i>=0;i--) v=v*NL+(B-1); A[v/64]&=~(1ULL<<(v%64)); }
  vector<atomic<u64>> Bv(words);
  u64 cnt=0; for(u64 w:A) cnt+=__builtin_popcountll(w);
  fprintf(stderr,"b=%d clock=%s p=%d s=%d N=%llu\n",B,cs.c_str(),P,S,(unsigned long long)N);
  int iter=0;
  for(;;){
    for(auto&w:Bv) w.store(0,memory_order_relaxed);
    atomic<u64> next{0}; const u64 CH=1<<16; // chunk of words
    vector<thread> th;
    for(int ti=0;ti<NT;ti++) th.emplace_back([&](){
      u8 x[64],y[64];
      for(;;){ u64 b=next.fetch_add(CH); if(b>=words) break; u64 e=min(b+CH,words);
        for(u64 w=b;w<e;w++){ u64 bits=A[w]; while(bits){ int k=__builtin_ctzll(bits); bits&=bits-1; u64 v=w*64+k;
            decode(v,x); if(!Fstep(x)) continue; u64 r=encode(x); Bv[r/64].fetch_or(1ULL<<(r%64),memory_order_relaxed);} }
      }});
    for(auto&t:th)t.join();
    u64 c2=0; for(u64 w=0;w<words;w++){ A[w]=Bv[w].load(memory_order_relaxed); c2+=__builtin_popcountll(A[w]); }
    iter++;
    fprintf(stderr,"iter %d set size %llu\n",iter,(unsigned long long)c2);
    if(c2==cnt) break; cnt=c2;
  }
  // cycle decomposition up to rotation.  visited bitset.
  vector<u64> V(words,0);
  u64 nb=0; 
  for(u64 w=0;w<words;w++){ u64 bits=A[w]; while(bits){ int k=__builtin_ctzll(bits); bits&=bits-1; u64 v=w*64+k;
      if(V[v/64]>>(v%64)&1) continue;
      u8 x[64]; decode(v,x);
      // minimal spatial period of x
      int ms=S; for(int d=1;d<S;d++){ if(S%d) continue; bool ok=true; for(int i=0;i<S;i++) if(x[i]!=x[(i+d)%S]){ok=false;break;} if(ok){ms=d;break;} }
      // walk the F-cycle from v, collect rows (phase 0 rows)
      vector<u64> cyc; u64 cur=v; u8 y[64]; memcpy(y,x,S);
      for(;;){ cyc.push_back(cur); if(!Fstep(y)){fprintf(stderr,"BUG\n");return 1;} u64 r=encode(y); if(r==v) break; cur=r; }
      u64 c=cyc.size();
      // canonical word = min over cycle and rotations; mark visited all rotations of all rows; twist detection
      u64 canon=~0ULL; 
      // first find whether some rotation of v appears in cycle: rotation orbit of v = {rot^j v}
      // Trot/twist: smallest index i>0 such that cyc[i] is a rotation of cyc[0]
      long imin=-1; int twist=0;
      vector<u64> rotv(S); { u8 z[64]; for(int r=0;r<S;r++){ for(int i=0;i<S;i++) z[i]=x[(i+r)%S]; rotv[r]=encode(z);} }
      for(u64 i=1;i<c;i++){ for(int r=0;r<S;r++) if(cyc[i]==rotv[r]){ imin=i; twist=r; goto found; } }
      found:;
      for(u64 i=0;i<c;i++){ u8 z[64],z2[64]; decode(cyc[i],z); for(int r=0;r<S;r++){ for(int j=0;j<S;j++) z2[j]=z[(j+r)%S]; u64 rv=encode(z2); V[rv/64]|=1ULL<<(rv%64); if(rv<canon) canon=rv; } }
      if(ms==S){ // primitive only
        u8 z[64]; decode(canon,z); nb++;
        printf("BAND s=%d T=%llu Trot=%llu twist=%d cyclelen=%llu V=", S,(unsigned long long)(c*P),(unsigned long long)((imin>0?imin:c)*P),twist,(unsigned long long)c);
        for(int i=0;i<S;i++) printf("%d%s",z[i],i+1<S?",":"\n");
      }
  } }
  fprintf(stderr,"primitive bands up to rotation (classes of F-cycles): %llu\n",(unsigned long long)nb);
  return 0;
}
