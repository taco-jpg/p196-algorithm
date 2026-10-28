#include "win.h"
int main(int argc,char**argv){
  Lat L; if(!L.load(argv[1])){fprintf(stderr,"load fail\n");return 1;}
  int t,K,w; long n;
  while(scanf("%d %ld %d %d",&t,&n,&w,&K)==4){
    int P[130],Pn[130]; for(int i=0;i<K;i++)scanf("%d",&P[i]);
    int dh; int r=win_step(L,P,t,n,K,w,Pn,&dh);
    printf("%d %d",r,dh); if(!r) for(int i=0;i<K;i++)printf(" %d",Pn[i]); printf("\n");
  }
}
