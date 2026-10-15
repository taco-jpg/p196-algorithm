/* Agent #102 independent enumerator of the complementary-band outer map (c,B)->(c',B',gamma).
   Written from METHOD_AND_PROOF.md (3),(4),(6),(7) + sec. 6 trim; independent of Agent #101's code.
   Usage: ./outer_graph CAP   (CAP <= 6). Domain: c in {2,4,...,16}; B empty or B[0] in 1..18,
   B[i] in 0..18, B[last] != c, |B| <= CAP. Exit: |B'| > CAP. Exit time counts the leaving step. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int CAP; static uint64_t P19[9], OFF[9], PER;
static int kk(int x){return x>=10;} static int tt(int x){return x-9*kk(x);}
static int phase_index(int c){return c/2-1;}
/* returns 0 on exit, 1 with *dst set */
static int step(int c,const int*B,int L,int*c2,int*Bp,int*Lp,int*gam){
  int DB[16],DRB[16],e=0;
  for(int i=0;i<L;i++){int s=B[i]+e;DB[i]=s%10;e=s/10;}
  int e0=e; e=kk(c);
  for(int i=0;i<L;i++){int s=B[L-1-i]+e;DRB[i]=s%10;e=s/10;}
  int g=e, tc=tt(c), u0=c+e0-10*kk(c);
  int X[17],Y[17]; for(int i=0;i<L;i++)X[i]=DB[i]; X[L]=u0;
  if(g==0){for(int i=0;i<L;i++)Y[i]=DRB[L-1-i]; Y[L]=tc;}
  else{Y[0]=1; for(int i=0;i<L;i++)Y[i+1]=DRB[L-1-i];}
  int n=L+1; for(int i=0;i<n;i++)Bp[i]=X[i]+Y[i];
  *c2=2*tc; while(n>0&&Bp[n-1]==*c2)n--;
  *Lp=n; *gam=g;
  if(n>0 && (Bp[0]<1||Bp[0]>18)){fprintf(stderr,"bad exterior\n");exit(2);}
  return n<=CAP;
}
static uint64_t idx(int c,const int*B,int L){uint64_t v=0;for(int i=L-1;i>=0;i--)v=v*19+B[i];return phase_index(c)*PER+OFF[L]+v;}
static int valid(int c,const int*B,int L){ if(L==0)return 1; if(B[0]<1)return 0; if(B[L-1]==c)return 0; return 1;}
static void decode(uint64_t s,int*c,int*B,int*L){int ci=s/PER; uint64_t r=s%PER; int l=0; while(l<CAP&&r>=OFF[l+1])l++;
  r-=OFF[l]; for(int i=0;i<l;i++){B[i]=r%19;r/=19;} *L=l; *c=2*(ci+1);}
int main(int argc,char**argv){
  CAP=atoi(argv[1]); P19[0]=1; for(int i=1;i<9;i++)P19[i]=P19[i-1]*19;
  OFF[0]=0; for(int l=1;l<=CAP+1;l++)OFF[l]=OFF[l-1]+P19[l-1]; PER=OFF[CAP+1];
  uint64_t TOT=8*PER; uint8_t*T=calloc(TOT,1); /* 0 unknown/invalid, 255 on stack, else exit time */
  uint64_t*stk=malloc(sizeof(uint64_t)*(8*(CAP+2)*64+1000000));
  uint64_t states=0,internal=0,exits=0,cycles=0; int maxt=0; uint64_t argmax=0,nmax=0;
  int B[16],Bp[17],L,Lp,c,c2,g;
  for(uint64_t s=0;s<TOT;s++){
    decode(s,&c,B,&L); if(!valid(c,B,L))continue; states++;
    if(step(c,B,L,&c2,Bp,&Lp,&g))internal++; else exits++;
    if(T[s])continue;
    /* follow functional path */
    int sp=0; uint64_t cur=s; int tval=0;
    for(;;){
      if(T[cur]==255){cycles++; fprintf(stderr,"CYCLE at %llu\n",(unsigned long long)cur); exit(3);}
      if(T[cur]){tval=T[cur];break;}
      int cc,BB[16],LL; decode(cur,&cc,BB,&LL);
      T[cur]=255; stk[sp++]=cur;
      if(!step(cc,BB,LL,&c2,Bp,&Lp,&g)){tval=0;break;}
      cur=idx(c2,Bp,Lp);
    }
    while(sp>0){uint64_t x=stk[--sp]; tval++; if(tval>254){fprintf(stderr,"overflow time\n");exit(4);} T[x]=tval;}
  }
  for(uint64_t s=0;s<TOT;s++){ if(!T[s])continue; if(T[s]>maxt){maxt=T[s];argmax=s;nmax=1;} else if(T[s]==maxt)nmax++; }
  decode(argmax,&c,B,&L);
  printf("cap=%d states=%llu internal_edges=%llu exit_edges=%llu cycles=%llu max_exit_time=%d argmax c=%d B=(",CAP,
    (unsigned long long)states,(unsigned long long)internal,(unsigned long long)exits,(unsigned long long)cycles,maxt,c);
  for(int i=0;i<L;i++)printf(i?",%d":"%d",B[i]); printf(") states_attaining_max=%llu\n",(unsigned long long)nmax);
  /* histogram of exit times */
  uint64_t H[256]={0}; for(uint64_t s=0;s<TOT;s++) if(T[s])H[T[s]]++;
  printf("hist"); for(int i=1;i<=maxt;i++)printf(" %d:%llu",i,(unsigned long long)H[i]); printf("\n");
  return 0;
}
