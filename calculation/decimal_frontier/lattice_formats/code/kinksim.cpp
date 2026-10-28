// Free forward simulation of the window map (centre frame) for a periodic-band exterior; random seeds.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;
typedef uint64_t u64;
int p,nB,m; vector<int> gam; vector<vector<int>> Wt,cup; const int b=10;
static u64 rs=88172645463325252ULL; static inline u64 rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); long nseed=atol(argv[2]); int Wseed=atoi(argv[3]); int Wmax=atoi(argv[4]); int Tper=atoi(argv[5]); int maxper=atoi(argv[6]); rs^=strtoull(argv[7],0,10)*0x9E3779B97F4A7C15ULL;
  fscanf(f,"%d %d %d",&p,&nB,&m); gam.resize(p); for(int t=0;t<p;t++)fscanf(f,"%d",&gam[t]);
  Wt.assign(p,vector<int>(m)); cup.assign(p,vector<int>(m));
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)fscanf(f,"%d",&Wt[t][j]);
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)fscanf(f,"%d",&cup[t][j]);
  int K=Wmax+30;
  long found=0; long bounded=0; vector<long> hist(Wmax+2,0);
  for(long s=0;s<nseed;s++){
    int o=rnd()%(2*m); int w=1+rnd()%Wseed;
    vector<int> P(K),Pn(K);
    long n=o; // n mod 2m effectively; keep as long (offset) small
    // lattice at t=0
    auto hmod=[&](long nn){return (int)(((nn+1)/2)%m);};
    int t=0; int hm=hmod(n);
    for(int i=0;i<K;i++)P[i]=Wt[0][(((hm-K+i-nB)%m)+m)%m];
    for(int i=K-w;i<K;i++)P[i]=rnd()%19;
    // make palindromic centre ok: lower half only, nothing to do
    if(P[K-1]==0 && false) continue;
    unordered_set<u64> seen; bool dead=false; long step=0; int maxw=0;
    for(step=0;step<(long)Tper*maxper;step++){
      // width
      int lat_i=-1; // lowest mismatch
      for(int i=0;i<K;i++){ if(P[i]!=Wt[t%p][(((hm-K+i-nB)%m)+m)%m]){lat_i=i;break;} }
      int wd = lat_i<0?0:K-lat_i; if(wd>maxw)maxw=wd;
      if(wd>=Wmax){dead=true;break;}
      if(step%Tper==0){ u64 h=1469598103934665603ULL; for(int i=K-Wmax;i<K;i++){h^=P[i];h*=1099511628211ULL;} if(!seen.insert(h).second){ // cycle candidate
            found++; printf("CYCLE seed %ld o=%d w=%d at step %ld maxw=%d\n",s,o,w,step,maxw); fflush(stdout); break; } }
      // one step
      long nn=n; int g=gam[t%p]; bool odd=nn%2!=0;
      int c0=cup[t%p][(((hm-K-nB)%m)+m)%m];
      int cu[200],Oup[200],cd[200],Odn[200];
      cu[0]=c0; for(int i=0;i<K;i++){int sv=P[i]+cu[i];cu[i+1]=sv>=b;Oup[i]=sv-b*cu[i+1];}
      int top; if(odd){Odn[K-1]=Oup[K-1];cd[K-2]=cu[K];top=K-2;}else{cd[K-1]=cu[K];top=K-1;}
      for(int i=top;i>=0;i--){ if(i<top)cd[i]=(P[i+1]+cd[i+1])>=b; Odn[i]=(P[i]+cd[i])%b; }
      long n2=nn+g; int delta=(int)((n2+1)/2-(nn+1)/2);
      int nt=t+1; int hm2=hmod(n2);
      for(int i2=0;i2<K;i2++){
        if(i2<2){ Pn[i2]=Wt[nt%p][(((hm2-K+i2-nB)%m)+m)%m]; continue; }
        int i=i2+delta; int up,part;
        if(g==0){ up=Oup[i]; part=(odd&&i==K-1)?Oup[i]:Odn[i]; }
        else { up=(i<=K-1)?Oup[i]:Odn[K-1]; part=Odn[i-1]; }
        Pn[i2]=up+part;
      }
      P=Pn; n=n2; t=nt; hm=hm2;
    }
    if(!dead){ bounded++; }
    if(maxw<=Wmax)hist[maxw]++;
  }
  printf("seeds %ld bounded(no blowup in %d steps) %ld cycles %ld\n",nseed,Tper*maxper,bounded,found);
}
