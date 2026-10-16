/* Agent #102: randomized search for cycles of the complementary-band exterior map at larger |B|.
   Heuristic exploration only (UNKNOWN if nothing is found). Map identical to outer_graph.c.
   Each start: random c (even phase), random trimmed B with |B| in [Lmin,Lmax]; iterate up to STEPS,
   abort when |B| > ESC; Brent cycle detection on exact states. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXL 128
typedef struct { int c, L; unsigned char B[MAXL]; } S;
static int kk(int x){return x>=10;} static int tt(int x){return x-9*kk(x);}
static void step(const S*s,S*o){
  int L=s->L,c=s->c,DB[MAXL],DRB[MAXL],e=0;
  for(int i=0;i<L;i++){int v=s->B[i]+e;DB[i]=v%10;e=v/10;}
  int e0=e; e=kk(c);
  for(int i=0;i<L;i++){int v=s->B[L-1-i]+e;DRB[i]=v%10;e=v/10;}
  int g=e,tc=tt(c),u0=c+e0-10*kk(c);
  int n=L+1;
  for(int i=0;i<n;i++){int X=(i<L)?DB[i]:u0; int Y; if(g==0)Y=(i<L)?DRB[L-1-i]:tc; else Y=(i==0)?1:DRB[L-i]; o->B[i]=X+Y;}
  o->c=2*tc; while(n>0&&o->B[n-1]==o->c)n--; o->L=n;
}
static int eq(const S*a,const S*b){return a->c==b->c&&a->L==b->L&&!memcmp(a->B,b->B,a->L);}
static uint64_t rs=88172645463325252ULL; static uint64_t rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int argc,char**argv){
  long starts=atol(argv[1]); int Lmin=atoi(argv[2]),Lmax=atoi(argv[3]),STEPS=atoi(argv[4]),ESC=atoi(argv[5]);
  rs ^= (uint64_t)atol(argv[6])*0x9E3779B97F4A7C15ULL;
  long found=0, escaped=0, timeout=0; long dwellmax=0; S best={0};
  for(long r=0;r<starts;r++){
    S x; x.c=2*(1+rnd()%8); x.L=Lmin+rnd()%(Lmax-Lmin+1);
    for(int i=0;i<x.L;i++)x.B[i]=rnd()%19; if(x.L){ x.B[0]=1+rnd()%18; while(x.B[x.L-1]==x.c)x.B[x.L-1]=rnd()%19; if(x.L==1&&x.B[0]==0)x.B[0]=1;}
    S tort=x,hare=x,tmp; long power=1,lam=1; int done=0;
    for(long st=0;st<STEPS;st++){
      step(&hare,&tmp); hare=tmp;
      if(hare.L>ESC){escaped++;done=1; if(st>dwellmax){dwellmax=st;best=x;} break;}
      if(eq(&tort,&hare)){found++; done=1;
        printf("CYCLE length %ld from start c=%d L=%d; state c=%d B=(",lam,x.c,x.L,hare.c);
        for(int i=0;i<hare.L;i++)printf(i?",%d":"%d",hare.B[i]); printf(")\n"); fflush(stdout); break;}
      if(power==lam){tort=hare;power*=2;lam=0;} lam++;
    }
    if(!done)timeout++;
  }
  printf("starts=%ld cycles_found=%ld escaped=%ld timeouts=%ld max_steps_before_escape=%ld (start c=%d L=%d)\n",
    starts,found,escaped,timeout,dwellmax,best.c,best.L);
  return 0;
}
