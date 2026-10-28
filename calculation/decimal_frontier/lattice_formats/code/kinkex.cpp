// Exhaustive search of bounded time-periodic centre kinks (width <= Wlim) for a given exterior lattice.
// state = top Wlim digits of the lower half in the centre frame; lattice below.  Deterministic forward map.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <unordered_set>
using namespace std;
typedef uint64_t u64;
int p,nB,m; vector<int> gam; vector<vector<int>> Wt,cup; const int b=10;
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int Wlim=atoi(argv[2]); int Tper=atoi(argv[3]); int maxper=atoi(argv[4]); int olo=atoi(argv[5]),ohi=atoi(argv[6]);
  if(fscanf(f,"%d %d %d",&p,&nB,&m)!=3)return 1; gam.resize(p); for(int t=0;t<p;t++)if(fscanf(f,"%d",&gam[t])!=1)return 1;
  Wt.assign(p,vector<int>(m)); cup.assign(p,vector<int>(m));
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)if(fscanf(f,"%d",&Wt[t][j])!=1)return 1;
  for(int t=0;t<p;t++)for(int j=0;j<m;j++)if(fscanf(f,"%d",&cup[t][j])!=1)return 1;
  int K=Wlim+10; if(K>120)return 2;
  long long total=0, survivedT=0, cycles=0; long long maxsteps=0;
  if(ohi>2*m)ohi=2*m;
  for(int o=olo;o<ohi;o++){
    vector<int> dig(Wlim,0);
    long long cnt=1; for(int i=0;i<Wlim;i++)cnt*=19;
    for(long long idx=0;idx<cnt;idx++){
      long long q=idx; for(int i=0;i<Wlim;i++){dig[i]=q%19;q/=19;}
      int P[128],Pn[128];
      long n=o; int t=0;
      auto hmod=[&](long nn){return (int)(((nn+1)/2)%m);};
      int hm=hmod(n);
      for(int i=0;i<K-Wlim;i++)P[i]=Wt[0][(((hm-K+i-nB)%m)+m)%m];
      for(int i=0;i<Wlim;i++)P[K-Wlim+i]=dig[i];
      unordered_set<u64> seen; long step; bool dead=false;
      for(step=0;step<(long)Tper*maxper;step++){
        // width check: every position below K-Wlim must equal the lattice
        bool bad=false;
        for(int i=0;i<K-Wlim;i++){ if(P[i]!=Wt[t%p][(((hm-K+i-nB)%m)+m)%m]){bad=true;break;} }
        if(bad){dead=true;break;}
        if(step%Tper==0){ u64 h=1469598103934665603ULL; for(int i=K-Wlim;i<K;i++){h^=P[i];h*=1099511628211ULL;}
          if(!seen.insert(h).second){ cycles++; printf("CYCLE o=%d idx=%lld step=%ld digits:",o,idx,step); for(int i=0;i<Wlim;i++)printf(" %d",dig[i]); printf("\n"); fflush(stdout); break; } }
        long nn=n; int g=gam[t%p]; bool odd=nn%2!=0;
        int c0=cup[t%p][(((hm-K-nB)%m)+m)%m];
        int cu[130],Oup[130],cd[130],Odn[130];
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
        memcpy(P,Pn,sizeof(int)*K); n=n2; t=nt; hm=hm2;
      }
      total++; if(step>=Tper)survivedT++; if(step>maxsteps)maxsteps=step;
    }
    fprintf(stderr,"o=%d done total=%lld survived>=T=%lld cycles=%lld maxsteps=%lld\n",o,total,survivedT,cycles,maxsteps);
  }
  printf("Wlim=%d total=%lld survived>=T=%lld cycles=%lld maxsteps=%lld\n",Wlim,total,survivedT,cycles,maxsteps);
}
