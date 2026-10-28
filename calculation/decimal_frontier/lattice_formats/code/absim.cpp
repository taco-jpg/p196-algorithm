// Direct simulation of the padded exterior B-system for an ABSORBING outer band (independent of bauto2 and of gt.py).
// usage: absim b Lmax maxsteps k0   -- enumerates all B (len 1..Lmax, B[0]>=1) with band coefficient k0 and reports cycles
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <set>
using namespace std;
typedef vector<int> V;
int b;
// one step of the padded system with band coefficient k; returns new B (trimmed) and new k; gam output
bool stepB(V&B,int&k,int&gam){
  int cs=(k>=b)?1:0; int d=(k+cs)%b; int kn=2*d;
  if(k==b-1) return false;
  V P=B; for(int i=0;i<3;i++)P.push_back(k); // pad with band positions
  int n=P.size();
  // lower digits (carry in 0)
  V DB(n); int c=0; for(int i=0;i<n;i++){int t=P[i]+c; DB[i]=t%b; c=t/b;}
  // upper: reverse, carry-in cs
  V DR(n); c=cs; for(int i=0;i<n;i++){int t=P[n-1-i]+c; DR[i]=t%b; c=t/b;}
  gam=c;
  V R;
  if(!gam){ R.resize(n); for(int i=0;i<n;i++) R[i]=DB[i]+DR[n-1-i]; }
  else { R.resize(n+1); for(int i=0;i<=n;i++){ int x=(i<n)?DB[i]:d; int y=(i==0)?1:DR[n-i]; R[i]=x+y; } }
  while(!R.empty()&&R.back()==kn)R.pop_back();
  B=R;k=kn;return true;
}
int main(int argc,char**argv){
  b=atoi(argv[1]);int Lmax=atoi(argv[2]);int maxsteps=atoi(argv[3]);int k0=atoi(argv[4]);
  long cnt=0,cyc=0;
  for(int L=1;L<=Lmax;L++){
    V B(L,0);
    while(true){
      if(B[0]>=1){
        cnt++;
        V cur=B;int k=k0;map<pair<V,int>,int> seen;
        for(int t=0;t<maxsteps;t++){
          auto key=make_pair(cur,k);
          if(seen.count(key)){
            cyc++;
            printf("CYCLE b=%d k0=%d start=[",b,k0);for(int v:B)printf("%d,",v);printf("] period=%d at t=%d  B=[",t-seen[key],seen[key]);for(int v:cur)printf("%d,",v);printf("] k=%d\n",k);fflush(stdout);
            break;}
          seen[key]=t;
          int gam;if(!stepB(cur,k,gam))break;
          if((int)cur.size()>Lmax+14)break;
          if(cur.empty()&&k==0)break;
        }
      }
      int i=0;while(i<L){B[i]++;if(B[i]<=2*b-2)break;B[i]=0;i++;}
      if(i==L)break;
    }
  }
  fprintf(stderr,"b=%d k0=%d enumerated %ld B, cycles %ld\n",b,k0,cnt,cyc);
}
