#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// digits little-endian in arrays; T and outer-4 pair sums
static int Tstep(int *d,int n){int e[64];int c=0;for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;e[i]=s%10;c=s/10;} if(c){e[n]=1;n++;} memcpy(d,e,sizeof(int)*n); return n;}
static int pat(int *d,int n){ if(n<5) return 0; int q[4]; for(int i=0;i<4;i++) q[i]=d[i]+d[n-1-i];
  int ev(int x){return x==0||x==10||x==12||x==14||x==16;}
  return q[0]>=10 && ev(q[0]) && q[1]==0 && ev(q[2]) && q[3]==0; }
static int fullpat(int *d,int n){ if(n<5) return 0; for(int i=0;i<n;i++){int q=d[i]+d[n-1-i]; if(i%2){ if(q) return 0;} else { if(!(q==0||q==10||q==12||q==14||q==16)) return 0; } } return d[n-1]>0; }
int main(int argc,char**argv){ long N=atol(argv[1]); long viol=0, four=0, four_full=0; 
  for(long A=1;A<N;A++){ int d[64]; int n=0; long x=A; while(x){d[n++]=x%10;x/=10;}
    for(int t=1;t<=5;t++){ n=Tstep(d,n); if(t==5 && pat(d,n)) {viol++; if(viol<5) printf("violation A=%ld\n",A);} 
      if(t==4 && fullpat(d,n)) { four_full++; if(four_full<=3){printf("4-step full-pattern ancestor A=%ld -> ",A); for(int i=n-1;i>=0;i--)printf("%d",d[i]); printf("\n");} } } }
  printf("N=%ld violations(outer-4 pattern at t=5)=%ld  t=4 full-pattern hits=%ld\n",N,viol,four_full); }
