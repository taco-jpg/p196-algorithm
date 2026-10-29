// W21: independent pairword and actual decimal digit-list reverse-and-add.
// c++ -O3 -std=c++17 replay.cpp -o /tmp/w21; /tmp/w21 225 20000
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using V=vector<int>;
static const V B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const V W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static const V Q={17,10,13,11,18,15,1,2,10,4,1,8,17,4,10,2,15,16,8,0,5,4,14,9,8,0,3,11,18,1,0,9,0,17,9,8,5,1,3,1};
V start(int copies,const V& core){V half=B;for(int k=0;k<copies;k++)half.insert(half.end(),W.begin(),W.end());half.insert(half.end(),core.begin(),core.end());V p=half;reverse(half.begin(),half.end());p.insert(p.end(),half.begin(),half.end());return p;}
V realize(const V& p){V d(p.size());for(size_t i=0;i<p.size()/2;i++){d[i]=p[i]/2;d[p.size()-1-i]=p[i]-d[i];}if(p.size()%2)d[p.size()/2]=p[p.size()/2]/2;return d;}
V digits_step(const V& d){V out;out.reserve(d.size()+1);int carry=0;for(size_t i=0;i<d.size();i++){int x=d[i]+d[d.size()-1-i]+carry;out.push_back(x%10);carry=x/10;}if(carry)out.push_back(carry);return out;}
V pairs_step(const V& p){V d;d.reserve(p.size()+1);int carry=0;for(int v:p){int x=v+carry;d.push_back(x%10);carry=x/10;}if(carry)d.push_back(carry);V out(d.size());for(size_t i=0;i<d.size();i++)out[i]=d[i]+d[d.size()-1-i];return out;}
V pairs(const V& d){V out(d.size());for(size_t i=0;i<d.size();i++)out[i]=d[i]+d[d.size()-1-i];return out;}
uint64_t hash_digits(const V& d){uint64_t h=14695981039346656037ULL;for(int x:d){h^=(uint64_t)('0'+x);h*=1099511628211ULL;}return h;}
int first_diff(const V& a,const V& b,size_t cap){size_t lim=min({a.size()/2,b.size()/2,cap});for(size_t i=0;i<lim;i++)if(a[i]!=b[i])return (int)i;return (int)lim;}
int main(int argc,char**argv){
 const int copies=argc>1?atoi(argv[1]):225,steps=argc>2?atoi(argv[2]):20000;
 if(copies<0||steps<0||steps>25000)throw runtime_error("bad arguments");
 V p=start(copies,Q),d=realize(p);
 V ref=start(250,W);vector<V> phase(8);for(int t=0;t<8;t++){phase[t]=V(ref.begin(),ref.begin()+min(size_t(4000),ref.size()/2));ref=pairs_step(ref);}
 for(int f=0;f<8;f++)for(int j=39;j+20<2000;j++)if(phase[f][j]!=phase[f][j+20])throw runtime_error("reference phase not 20-periodic");
 int first_bad=-1,min_h=INT32_MAX,min_bulk=INT32_MAX,palindromes=0;
 for(int t=0;t<=steps;t++){
  V pv=pairs(d);if(pv!=p)throw runtime_error("full pairword mismatch at step "+to_string(t));
  if(d.back()==0)throw runtime_error("leading zero at step "+to_string(t));
  bool pal=true;for(size_t i=0;i<d.size()/2;i++)if(d[i]!=d[d.size()-1-i]){pal=false;break;}
  if(pal)palindromes++;
  int h=first_diff(p,phase[t%8],4000);
  min_h=min(h,min_h);min_bulk=min(min_bulk,max(0,(h-39)/20));
  if(h<39&&first_bad<0)first_bad=t;
  if(t==0||t==1000||t==5000||t==10000||t==20000||t==steps){
   cout<<"t="<<t<<" digits="<<d.size()<<" prefix="<<h<<" pal="<<pal
       <<" fnv64="<<hex<<hash_digits(d)<<dec<<"\n";
  }
  if(t<steps){p=pairs_step(p);d=digits_step(d);}
 }
 cout<<"copies="<<copies<<" core=Q40"<<" min_prefix="<<min_h
     <<" min_bulk="<<min_bulk<<" first_bad="<<first_bad
     <<" palindrome_states="<<palindromes<<"\n";
 if(palindromes)return 2;
 if(steps==20000&&(first_bad!=-1||min_bulk<0))return 3;
}
