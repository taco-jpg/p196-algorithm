// C-system matcher: given base b and a periodic driver stream (e1_t, gam_t), t=0..P-1, find every symmetric C0 (length 1..mmax,
// entries 0..2b-2) whose driven orbit survives forever (carry(C,e1)=1-e1 at each step) and is eventually periodic.
// usage: cmatch b mmax e1string gamstring [maxprint]    e.g.  cmatch 20 8 01 01
// The C-step is the exact C part of nextC/trim of calculation/neutral_band_search.py with e2 forced to 1-e1.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <set>
#include <map>
using namespace std;
int b;
// one C step; returns false if dead. in/out arrays of length m (symmetric)
bool cstep(int*C,int&m,int e1,int g,int&v){
  int DC[80];int c=e1;
  for(int i=0;i<m;i++){int x=C[i]+c;DC[i]=x%b;c=x/b;}
  int e2=c; if(e2!=1-e1) return false;
  int yd=(b-1)*(1-e2); int nc[82]; int nm;
  if(g==0){nm=m;for(int i=0;i<m;i++)nc[i]=DC[i]+DC[m-1-i];}
  else{nm=m+1;for(int k=0;k<=m;k++){int f=(k<m)?DC[k]:yd;int s=(k==0)?yd:DC[m-k];nc[k]=f+s;}}
  v=0;while(nm>=3&&nc[0]==b-1&&nc[nm-1]==b-1){ // mirror trim: while len>=2 and both ends b-1 (len>=2 -> keep>=0)
    // mirror: len(C2)>=2 ; after removing 2 we keep nm-2 (>=0).  we require result nonempty:
    for(int i=0;i+2<nm;i++)nc[i]=nc[i+1]; nm-=2; v++; }
  memcpy(C,nc,sizeof(int)*nm); m=nm; return true;
}
int main(int argc,char**argv){
  b=atoi(argv[1]);int mmax=atoi(argv[2]);string es=argv[3],gs=argv[4];int maxprint=argc>5?atoi(argv[5]):20;
  int P=es.size();int W=2*b-1;long found=0,tested=0;set<string> seen;
  for(int m0=1;m0<=mmax;m0++){
    int h=(m0+1)/2; long long cnt=1;for(int i=0;i<h;i++)cnt*=W;
    for(long long x=0;x<cnt;x++){
      int C[90],m=m0;long long y=x;
      for(int i=0;i<h;i++){C[i]=y%W;y/=W;} for(int i=0;i<h;i++)C[m0-1-i]=C[i];
      tested++;
      // simulate up to 40 periods, look for repetition at phase 0
      vector<vector<int>> hist;bool alive=true;
      int cur[90];memcpy(cur,C,sizeof(int)*m);int cm=m;
      bool cyc=false;
      for(int per=0;per<60&&alive;per++){
        vector<int> snap(cur,cur+cm);
        for(size_t j=0;j<hist.size();j++) if(hist[j]==snap){cyc=true;break;}
        if(cyc)break;
        hist.push_back(snap);
        for(int t=0;t<P;t++){int v;if(!cstep(cur,cm,es[t]-'0',gs[t]-'0',v)){alive=false;break;} if(cm>80){alive=false;break;}}
      }
      if(cyc){
        found++;
        string key;for(int i=0;i<m0;i++)key+=to_string(C[i])+",";
        if(found<=maxprint){printf("SURVIVOR m0=%d C=[",m0);for(int i=0;i<m0;i++)printf("%d%s",C[i],i+1<m0?",":"");printf("]\n");}
      }
    }
    fprintf(stderr,"m0=%d done, tested %ld found %ld\n",m0,tested,found);
  }
  printf("base %d stream e=%s g=%s mmax=%d: tested %ld, survivors %ld\n",b,es.c_str(),gs.c_str(),mmax,tested,found);
}
