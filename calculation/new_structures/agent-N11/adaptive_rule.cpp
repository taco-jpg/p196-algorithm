// Exact finite-radius carry-shadow test on 196. For an interior pairword
// coefficient P_i, carry into i is determined by the closest predecessor
// coefficient !=9. Gamma 0 uses left + right scan; gamma 1 shifts right scan.
// The actual successor is computed independently from the original digits.
#include <bits/stdc++.h>
using namespace std;using ull=unsigned long long;
static int step(vector<uint8_t>&d,vector<uint8_t>&o){int n=d.size(),c=0;o.resize(n+1);for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+c;o[i]=v%10;c=v/10;}o[n]=c;d.swap(o);d.resize(n+(c!=0));return c;}
static int leftcarry(const vector<uint8_t>&p,int i,int K){for(int j=i-1;j>=0&&i-1-j<=K;j--)if(p[j]!=9)return int(p[j]>=10);return -1;}
static int rightcarry(const vector<uint8_t>&p,int i,int K){for(int j=i;j<(int)p.size()&&j-i<=K;j++)if(p[j]!=9)return int(p[j]>=10);return -1;}
int main(int argc,char**argv){int steps=argc>1?atoi(argv[1]):100000;int stride=argc>2?atoi(argv[2]):100;
 vector<uint8_t>d={6,9,1},o,p;ull eligible[9]={},total=0,errors[9]={},gammaN[2]={};int maxrun=0;int m,n;
 for(int t=0;t<steps;t++){
  n=d.size();m=n/2;bool take=t%stride==0;
  if(take){p.resize(m);for(int i=0;i<m;i++)p[i]=d[i]+d[n-1-i];int run=0;for(int z:p){run=z==9?run+1:0;maxrun=max(maxrun,run);}}
  int gamma=step(d,o);gammaN[gamma]++;
  if(take)for(int i=16;i<m-16;i++){total++;int actual=d[i]+d[d.size()-1-i];for(int K=0;K<=8;K++){
   int cL=leftcarry(p,i,K),cR=rightcarry(p,i+(gamma==0?1:0),K);
   if(cL<0||cR<0)continue;
   int v=(p[i]+cL)%10+(gamma==0?(p[i]+cR)%10:(p[i-1]+cR)%10);
   eligible[K]++;errors[K]+=(v!=actual);
  }}
 }
 cout<<"steps "<<steps<<" stride "<<stride<<" last_length "<<d.size()<<" gamma0 "<<gammaN[0]<<" gamma1 "<<gammaN[1]<<" max_run9_on_samples "<<maxrun<<" tested_cells "<<total<<"\n";
 for(int K=0;K<=8;K++)cout<<"K "<<K<<" eligible "<<eligible[K]<<" fraction "<<fixed<<setprecision(9)<<double(eligible[K])/total<<" errors "<<errors[K]<<"\n";
 for(int K=0;K<=8;K++)if(errors[K])return 2;
}
