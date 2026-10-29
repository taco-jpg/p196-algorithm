// AC29: exact full 120-step decimal pairword calculation; no strict W9 pruning.
#include <array>
#include <algorithm>
#include <iostream>
#include <string>
#include <map>
#include <cstdint>
#include <cstdlib>
using namespace std;
const int B[34]={10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15};
const int W[9]={4,0,5,5,18,4,8,1,15};
int mod(int x,int m){return (x%m+m)%m;}
int main(int argc,char**argv){
 if(argc<3){cerr<<"usage: scan ODD|EVEN end_code [u_index=-1] [start_code=0]\n";return 1;}
 bool odd=string(argv[1])=="ODD";int end=min(2476099,atoi(argv[2])),ui=argc>3?atoi(argv[3]):-1,start=argc>4?atoi(argv[4]):0,q=argc>5?atoi(argv[5]):14,k=argc>6?atoi(argv[6]):100;
 uint64_t tested=0,skipped=0,clockbad=0,returned=0;map<int,uint64_t> hist;
 for(int aa=0;aa<=18;aa+=2)for(int rot=0;rot<3;rot++){
  int u[3]={9,aa,18-aa};rotate(u,u+rot,u+3);int idx=3*(aa/2)+rot;
  if(ui>=0 && idx!=ui)continue;
  if(odd&&mod(u[0]-u[1]+u[2],11)!=5){skipped+=end-start;continue;}
  for(int z=start;z<end;z++){
   int J[5],v=z,A=0;
   for(int i=0;i<5;i++){J[i]=v%19;v/=19;A+=(i&1)?-J[i]:J[i];}
   if(odd&&mod(A,11)!=6){skipped++;continue;}
   int C[3]={4,14,4},nc=odd?3:2;if(!odd)C[1]=4;
   // H=B8 ++ W8^14 ++ J ++ U^100; P=H ++ C ++ reverse(H).
   int H[10000],N=0;
   for(int x:B)H[N++]=x;
   for(int t=0;t<q;t++)for(int x:W)H[N++]=x;
   for(int x:J)H[N++]=x;
   for(int t=0;t<k;t++)for(int x:u)H[N++]=x;
   int p[20000],d[20000],temp[20000],T[20000],L=0;
   for(int i=0;i<N;i++)p[L++]=H[i];
   for(int i=0;i<nc;i++)p[L++]=C[i];
   for(int i=N-1;i>=0;i--)p[L++]=H[i];
   int M=0;
   for(int i=0;i<34+9*q+5;i++)T[M++]=H[i];
   for(int t=0;t<k+5;t++)for(int x:u)T[M++]=x;
   int half=M;
   for(int i=0;i<nc;i++)T[M++]=C[i];
   for(int i=half-1;i>=0;i--)T[M++]=T[i];
   bool okclock=true;
   for(int t=0;t<120;t++){
    int old=L,carry=0;
    for(int i=0;i<L;i++){int x=p[i]+carry;d[i]=x%10;carry=x/10;}
    if(carry)d[L++]=carry;
    while(L>1&&!d[L-1])L--;
    if(L-old != (t%4==0))okclock=false;
    int h=(L+1)/2;
    for(int i=0;i<h;i++)temp[i]=d[i]+d[L-1-i];
    for(int i=h;i<L;i++)p[i]=temp[L-1-i];
    for(int i=0;i<h;i++)p[i]=temp[i];
   }
   int mismatch=L==M?-1:min(L,M);
   for(int i=0;i<min(L,M);i++)if(p[i]!=T[i]){mismatch=i;break;}
   tested++;hist[mismatch]++;returned+=(mismatch==-1);clockbad+=!okclock;
  }
 }
 cout<<"tested "<<tested<<" skipped_allwidth_mod11 "<<skipped<<" returns "<<returned<<" clockbad "<<clockbad<<"\n";
 for(auto [i,n]:hist)cout<<i<<" "<<n<<"\n";
}