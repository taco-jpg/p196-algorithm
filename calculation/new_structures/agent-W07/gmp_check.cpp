// Independent GMP ordinary-bigint replay for W07; not digit-vector addition.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
string seed(int q,int centre=13){
 V p=B;for(int k=0;k<q;k++)p.insert(p.end(),W.begin(),W.end());
 if(centre!=13){assert(p.back()==13);p.back()=centre;}
 string low,high;
 for(int x:p){int a=min(x,9);low.push_back('0'+a);high.push_back('0'+x-a);}
 reverse(low.begin(),low.end());
 return high+low;
}
mpz_class next(mpz_class n){
 string r=n.get_str();reverse(r.begin(),r.end());
 return n+mpz_class(r,10);
}
V pairhalf(const string&s){
 int n=s.size();V p;
 for(int i=0;i<(n+1)/2;i++)p.push_back(s[n-1-i]+s[i]-2*'0');
 return p;
}
uint64_t fnv(const string&s){
 uint64_t h=1469598103934665603ULL;
 for(auto it=s.rbegin();it!=s.rend();++it){h^=(*it-'0')+1;h*=1099511628211ULL;}
 return h;
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):300,steps=argc>2?atoi(argv[2]):20000,centre=argc>3?atoi(argv[3]):13;
 mpz_class x(seed(q,centre),10);
 assert(x.get_str().size()==size_t(78+40*q));
 array<V,8> Bph,Wph;
 mpz_class cal(seed(max(q+200,500)),10);
 for(int t=0;t<8;t++){
  V p=pairhalf(cal.get_str());
  Bph[t]=V(p.begin(),p.begin()+39);
  Wph[t]=V(p.begin()+39,p.begin()+59);
  cal=next(cal);
 }
 assert(Bph[0]==B && Wph[0]==W);
 int minbands=1000000,overflows=0;
 for(int t=0;t<=steps;t++){
  string s=x.get_str(),sr=s;reverse(sr.begin(),sr.end());
  if(s==sr){cerr<<"PAL "<<t<<"\n";return 2;}
  V p=pairhalf(s);
  if(!equal(Bph[t%8].begin(),Bph[t%8].end(),p.begin())){
   cerr<<"CAP BAD "<<t<<"\n";return 3;
  }
  int j=0;
  while(39+(j+1)*20<=(int)p.size() &&
   equal(Wph[t%8].begin(),Wph[t%8].end(),p.begin()+39+20*j))++j;
  minbands=min(minbands,j);
  if(j<1){cerr<<"BAND BAD "<<t<<"\n";return 4;}
  if(t==steps){
   assert((int)s.size()==(int)(78+40*q+10000));
   cout<<"W07_GMP_"<<steps<<"_PASS centre="<<centre<<" len="<<s.size()
    <<" minbands="<<minbands<<" gammas1="<<overflows
    <<" final_fnv64="<<fnv(s)<<"\n";
   assert(q!=300 || fnv(s)==10989435956851471335ULL);
   break;
  }
  auto m=next(x);
  int g=(int)m.get_str().size()-(int)s.size();
  if(g!=(t%2==0)){cerr<<"OVERFLOW BAD "<<t<<"\n";return 5;}
  overflows+=g;x=move(m);
 }
}
