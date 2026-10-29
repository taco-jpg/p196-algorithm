// Seeded heuristic for the 60-step macro-gain; NOT a proof or a certificate.
#include <bits/stdc++.h>
using namespace std;using W=vector<uint8_t>;
mt19937_64 rng(20261028090037ULL);
static const int PH[6]={8,16,14,10,2,4};
struct R {int gain,minW,unsafe,gam;};
R eval(const W &L,int K,int T){
 W z=L;z.insert(z.end(),2*K,8);
 for(int j=(int)L.size()-1;j>=0;j--)z.push_back(L[j]);
 int len=z.size(),minW=9999,unsafe=0,gam=0;
 for(int t=0;t<=T;t++){
  int lo=(len-1)/2,hi=len/2;
  while(lo>=0&&hi<len&&z[lo]==PH[t%6]&&z[hi]==PH[t%6]){--lo;++hi;}
  int w=hi-lo-1;minW=min(minW,w);
  bool odd=false;for(int j=0;j<len/2;j++)if(z[j]&1){odd=true;break;}
  if(!odd)unsafe++;
  if(t==T)return {w-2*K,minW,unsafe,gam};
  int carry=0;W y;y.reserve(len+1);
  for(int x:z){int v=x+carry;y.push_back(v%10);carry=v/10;}
  if(carry)y.push_back(carry);
  if((int)y.size()!=len)gam++;
  W out;out.reserve(y.size());
  for(int j=0,n=y.size();j<n;j++)out.push_back(y[j]+y[n-1-j]);
  z.swap(out);len=z.size();
 }
 return {-999,0,0,0};
}
int main(int argc,char**argv){
 int iters=argc>1?atoi(argv[1]):160000,m=60,K=80,T=60;
 W cur={2,2,11,6,0,12,15,13,3,11,7,4,13,3,17,13,0,14,7,10,5,0,14,3,7,8,18,7,7,17,18,15,14,2,5,15,10,15,9,6,12,15,11,12,12,16,5,1,17,6,3,0,13,8,5,17,7,17,5,7};
 R a=eval(cur,K,T),best=a;W win=cur;int at=0;
 for(int t=1;t<=iters;t++){
  W cand=cur;int cnt=1+(rng()%((t%1000<700)?2:5));
  for(int j=0;j<cnt;j++){
   int pos=18+rng()%(m-18),x=rng()%19;
   if(pos==m-1&&x==8)x=7;
   cand[pos]=x;
  }
  auto b=eval(cand,K,T);
  int sc=a.gain-200*a.unsafe-100*(a.minW<8);
  int sn=b.gain-200*b.unsafe-100*(b.minW<8);
  double temp=0.1+2.5*(1.0-double(t%5000)/5000.0);
  bool accept=sn>=sc || uniform_real_distribution<double>(0,1)(rng)<exp(double(sn-sc)/temp);
  if(!b.unsafe&&b.minW>=8&&(b.gain>best.gain||best.unsafe)){best=b;win=cand;at=t;}
  if(accept){cur.swap(cand);a=b;}
 }
 cout<<"best gain="<<best.gain<<" iteration="<<at<<"\n";
 for(size_t i=0;i<win.size();i++){if(i)cout<<",";cout<<unsigned(win[i]);}
 cout<<"\n";
}
