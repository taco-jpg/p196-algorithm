// Follow the actual 0-domain walls far beyond conservative L-2t lower bound.
// Zero band is followed by its moving midpoint, not a fixed coordinate.
#include <bits/stdc++.h>
using namespace std;
static int add(vector<uint8_t>&d,vector<uint8_t>&o){int c=0,n=d.size();o.resize(n+1);for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;o[i]=s%10;c=s/10;}o[n]=c;d.swap(o);d.resize(n+(c!=0));return c;}
int main(int argc,char**argv){int L=argc>1?atoi(argv[1]):45000,T=argc>2?atoi(argv[2]):50000,E=argc>3?atoi(argv[3]):1000;
 int m=L+130,n=2*m,mid=65+L/2;vector<uint8_t>d(n),o;uint32_t state=196u;
 for(int i=0;i<m;i++){int p;if(i==64||i==L+65)p=11;else if(i>=65&&i<65+L)p=9;else{state^=state<<13;state^=state>>17;state^=state<<5;p=state%19;}if(i==0)p=12;d[i]=max(0,p-9);d[n-1-i]=min(9,p);}
 int prvL=-1,prvR=-1,g=0;long long stepdiffL[8]={},stepdiffR[8]={},grow=0,shrink=0,stable=0,maxGrow=0;long long tab[2][3][3]={};
 for(int t=0;t<=T;t++){
  int len=d.size();bool pal=true;for(int j=0;j<len/2;j++)if(d[j]!=d[len-1-j]){pal=false;break;}if(pal){cerr<<"PAL step "<<t<<"\n";return 3;}
  if(t>0){auto pv=[&](int i){return int(d[i])+int(d[len-1-i]);};int probe=prvL>=0?(prvL+prvR)/2:mid;if(pv(probe)!=0){int closest=-1;for(int k=max(0,prvL-2);k<=min(len/2-1,prvR+2);k++)if(pv(k)==0){closest=k;break;}if(closest<0){cout<<"ZERO DOMAIN ENDED t="<<t<<" previous_range="<<prvL<<","<<prvR<<" final_digits="<<len<<"\n";break;}probe=closest;}
   int a=probe,b=probe;while(a>0&&pv(a-1)==0)a--;while(b+1<len/2&&pv(b+1)==0)b++;
   if(prvL>=0){int dl=a-prvL,dr=b-prvR;stepdiffL[min(7,abs(dl))]++;stepdiffR[min(7,abs(dr))]++;if(dl>=0&&dl<=2&&dr<=0&&dr>=-2)tab[g][dl][-dr]++;int widthdiff=(b-a+1)-(prvR-prvL+1);if(widthdiff>0){grow++;maxGrow=max(maxGrow,(long long)widthdiff);}else if(widthdiff==0)stable++;else shrink++;}
   if(t%E==0||t==1)cout<<"t="<<t<<" gamma="<<g<<" len="<<len<<" a="<<a<<" b="<<b<<" width="<<b-a+1<<" guaranteed="<<max(0,L-2*t)<<"\n";
   prvL=a;prvR=b;
  }
  if(t==T)break;
  g=add(d,o);
 }
 cout<<"wall_dynamics: grow="<<grow<<" stable="<<stable<<" shrink="<<shrink<<" max_positive_gain="<<maxGrow<<"\n";
 cout<<"abs_delta_left";for(int i=0;i<8;i++)cout<<' '<<i<<':'<<stepdiffL[i];cout<<"\nabs_delta_right";for(int i=0;i<8;i++)cout<<' '<<i<<':'<<stepdiffR[i];cout<<'\n';for(int phase=0;phase<2;phase++)for(int dl=0;dl<3;dl++)for(int dr=0;dr<3;dr++)if(tab[phase][dl][dr])cout<<"wall_transition gam="<<phase<<" left+="<<dl<<" right-="<<dr<<" count="<<tab[phase][dl][dr]<<"\n";
}
