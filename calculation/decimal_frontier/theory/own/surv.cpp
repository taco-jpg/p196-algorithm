// maximum number of phases a trimmed palindromic centre of width m survives (true dynamics, any width up to 24), per width, for a periodic driver.
// usage: surv b E G W [startphase]
#include <bits/stdc++.h>
using namespace std;
int b,P,W; vector<int> E,Gs;
struct St{int m; int c[28];};
bool step(const St&s,int e,int g,St&out){
  int m=s.m; int dc[30]; int car=e;
  for(int i=0;i<m;i++){int v=s.c[i]+car; dc[i]=v%b; car=v/b;}
  if(car!=1-e) return false;
  int n2; int d2[32];
  if(g==0){ n2=m; for(int i=0;i<m;i++) d2[i]=dc[i]+dc[m-1-i]; }
  else { n2=m+1; int y=(b-1)*e; int dt[32]; for(int i=0;i<m;i++) dt[i]=dc[i]; dt[m]=y; for(int i=0;i<=m;i++) d2[i]=dt[i]+dt[m-i]; }
  int lo=0,hi=n2-1;
  while(hi-lo+1>=2 && d2[lo]==b-1 && d2[hi]==b-1){lo++;hi--;}
  int m2=hi-lo+1; if(m2<=0) return false;
  if(m2>26) return false;
  out.m=m2; for(int i=0;i<m2;i++) out.c[i]=d2[lo+i];
  return true;
}
int main(int argc,char**argv){
  b=atoi(argv[1]); string es=argv[2], gs=argv[3]; W=atoi(argv[4]); int st0=argc>5?atoi(argv[5]):0; P=es.size();
  for(char ch:es) E.push_back(ch-'0'); for(char ch:gs) Gs.push_back(ch-'0');
  map<int,int> best; map<int,vector<int>> ex; map<int,map<int,long long>> hist;
  for(int m=1;m<=W;m++){
    int h=(m+1)/2; bool odd=m&1; vector<int> idx(h,0);
    while(true){
      St s; s.m=m; bool ok=true;
      for(int i=0;i<h;i++) s.c[i]=idx[i];
      if(odd && (s.c[h-1]&1)) ok=false;
      if(m>=2 && s.c[0]==b-1) ok=false;
      if(ok){
        for(int i=0;i<h;i++) s.c[m-1-i]=s.c[i];
        St cur=s; int n=0; int t=st0;
        while(n<600){ St nx; if(!step(cur,E[t%P],Gs[t%P],nx)) break; cur=nx; n++; t++; }
        if(n>=3) hist[m][n]++;
        if(!best.count(m)||n>best[m]){best[m]=n; ex[m].assign(s.c,s.c+m);}
      }
      int i=0; while(i<h){ idx[i]++; if(idx[i]<2*b-1) break; idx[i]=0; i++; }
      if(i==h) break;
    }
    printf("width %2d max phases survived %3d  example:",m,best[m]); for(int x:ex[m]) printf(" %d",x);
    // top of histogram
    printf("   top:"); int c=0; for(auto it=hist[m].rbegin(); it!=hist[m].rend()&&c<3; ++it,++c) printf(" %d:%lld",it->first,it->second); printf("\n"); fflush(stdout);
  }
}
