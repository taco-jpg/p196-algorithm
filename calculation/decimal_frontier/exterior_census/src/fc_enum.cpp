// Enumerate rotation-canonical (necklace) binary words g of length p accepted by the first-coordinate NFA
// (cyclic: exists closed walk labelled g).  Base b general (states q=1..2b-2).
// usage: fc_enum b pmin pmax [-list dir] [-Gmin x -Gmax y]
// Output: counts per (p,G); with -list, writes words to dir/fc_b{b}_p{p}_G{G}.txt (one per line, necklace-minimal rotation).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <map>
using namespace std;
typedef uint64_t u32; typedef uint64_t u64;
int b, NS;               // NS = 2b-2 states 1..NS  -> index 0..NS-1
u32 succ[2][64];          // succ[g][q-1] mask over states
int p;
// FKM necklace generation with pruning by NFA viability.
struct Rows { u32 r[64]; };
static inline bool nonempty(const Rows&R){ for(int s=0;s<NS;s++) if(R.r[s]) return true; return false; }
static inline void extend(const Rows&R,int a,Rows&out){
  for(int s=0;s<NS;s++){ u32 m=R.r[s],o=0; while(m){int c=__builtin_ctzll(m); m&=m-1; o|=succ[a][c];} out.r[s]=o; }
}
static inline bool closed(const Rows&R){ for(int s=0;s<NS;s++) if(R.r[s]&(1ULL<<s)) return true; return false; }
vector<int> w;           // current word (1-indexed positions 1..p) as in FKM
map<int,long long> cntG; long long cntAll;
FILE* fout[64];
string dir;
bool listing=false; int Gmin=0,Gmax=1000;
void emit(int G){
  cntAll++; cntG[G]++;
  if(listing && G>=Gmin && G<=Gmax){
    if(!fout[G]){ char fn[512]; snprintf(fn,sizeof fn,"%s/fc_b%d_p%d_G%d.txt",dir.c_str(),b,p,G); fout[G]=fopen(fn,"w"); }
    for(int i=1;i<=p;i++) fputc('0'+w[i],fout[G]); fputc('\n',fout[G]);
  }
}
// gen(t, pp, G, R): w[1..t-1] fixed, pp = length of longest Lyndon prefix (period candidate)
void gen(int t,int pp,int G,const Rows&R){
  if(t>p){
    if(p%pp==0){ // necklace (possibly imprimitive: pp | p).  Count all necklaces incl. imprimitive.
      if(closed(R)) emit(G);
    }
    return;
  }
  // pruning: remaining steps can't be checked cheaply; use viability only
  for(int a=w[t-pp]; a<=1; a++){
    Rows R2; extend(R,a,R2); if(!nonempty(R2)) continue;
    w[t]=a;
    gen(t+1, (a==w[t-pp])?pp:t, G+a, R2);
  }
}
int main(int argc,char**argv){
  b=atoi(argv[1]); int pmin=atoi(argv[2]), pmax=atoi(argv[3]); NS=2*b-2;
  for(int i=4;i<argc;i++){ string a=argv[i]; if(a=="-list"){listing=true; dir=argv[++i];} else if(a=="-Gmin")Gmin=atoi(argv[++i]); else if(a=="-Gmax")Gmax=atoi(argv[++i]); }
  memset(succ,0,sizeof succ);
  for(int q=1;q<=NS;q++) for(int h=0;h<2;h++){
    if(q+h<b){ int q2=2*q+h; if(q2<=NS) succ[0][q-1]|=1ULL<<(q2-1); }
    else { int q2=(q%b)+1; if(q2<=NS) succ[1][q-1]|=1ULL<<(q2-1); }
  }
  for(p=pmin;p<=pmax;p++){
    cntG.clear(); cntAll=0; for(int i=0;i<64;i++) fout[i]=0;
    w.assign(p+2,0); w[0]=0;
    Rows R0; for(int s=0;s<NS;s++) R0.r[s]=1ULL<<s;
    gen(1,1,0,R0);
    // gen() with FKM: initial call explores w[1] from w[0]=0..1
    printf("p=%d total_necklaces=%lld  byG:",p,cntAll);
    for(auto&kv:cntG) printf(" %d:%lld",kv.first,kv.second);
    printf("\n"); fflush(stdout);
    for(int i=0;i<64;i++) if(fout[i]) fclose(fout[i]);
  }
}
