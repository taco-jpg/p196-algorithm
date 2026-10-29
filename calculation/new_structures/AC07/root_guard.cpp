// AC07: exact upper-carry-set prefix transfer; conditional on supplied 120-bit clock.
// For any palindrome C, P = H ++ C ++ reverse(H); the prefix is independent
// of C if the high incoming carry is quantified over {0,1,2}.
#include <array>
#include <vector>
#include <iostream>
#include <algorithm>
#include <cstdint>
#include <string>
using namespace std;
using V=vector<uint8_t>;
const V B={10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W={5,18,4,8,1,15,4,0,5};
const V US[3]={{9,12,6},{12,6,9},{6,9,12}};
constexpr int G[]={1,0,0,0,1,0,0,0,1,0,0,0};
void cat(V&a,const V&b){a.insert(a.end(),b.begin(),b.end());}
void rep(V&a,const V&b,int n){for(int i=0;i<n;i++)cat(a,b);}
V prefix(const V&J,const V&U,int q=14,int k=100){V p=B;rep(p,W,q);cat(p,J);rep(p,U,k);return p;}
V next_pref(const V &p,int g){
 size_t n=p.size();V left(n);vector<uint16_t> highmask(n,0);int carry=0;
 for(size_t i=0;i<n;i++){int z=p[i]+carry;left[i]=z%10;carry=z/10;}
 for(int c0=0;c0<=2;c0++){int c=c0;
   for(size_t j=0;j<n;j++){int z=p[n-j-1]+c;highmask[j]|=(1u<<(z%10));c=z/10;}
 }
 V out;out.reserve(n);
 for(size_t i=0;i<n;i++){
   if(i==0 && g==1){out.push_back(left[i]+1);continue;}
   size_t j=n-1-i+g;if(j>=n)break;
   unsigned int m=highmask[j];if(__builtin_popcount(m)!=1)break;
   out.push_back(left[i]+__builtin_ctz(m));
 }
 return out;
}
struct Result{bool contradicted;int first,observed,expected,prefix_len;};
Result run(const V&J,int ui,int q=14,int k=100){
 V p=prefix(J,US[ui],q,k),wanted=prefix(J,US[ui],q,k+5);
 for(int t=0;t<120;t++)p=next_pref(p,G[t%12]);
 for(int i=0;i<(int)p.size();i++)if(p[i]!=wanted[i])return {true,i,p[i],wanted[i],(int)p.size()};
 return {false,-1,-1,-1,(int)p.size()};
}
uint64_t ipow(int n){uint64_t p=1;while(n--)p*=19;return p;}
int main(int argc,char**argv){
 int maxj=argc>1?stoi(argv[1]):3;
 for(int l=0;l<=maxj;l++)for(int ui=0;ui<3;ui++){
  uint64_t total=ipow(l),excluded=0;int minpref=1000000;array<int,300> hist{};
  V survivors;int exfirst=-1,exgot=-1,exwant=-1;
  for(uint64_t id=0;id<total;id++){
   V j(l);uint64_t v=id;for(int t=0;t<l;t++){j[t]=v%19;v/=19;}
   auto r=run(j,ui);minpref=min(minpref,r.prefix_len);
   if(r.contradicted){excluded++;if(r.first<(int)hist.size())hist[r.first]++;
     if(exfirst<0)exfirst=r.first,exgot=r.observed,exwant=r.expected;}
   else if(survivors.empty())survivors=j;
  }
  cout<<"JLEN="<<l<<" U="<<ui<<" total="<<total<<" excluded="<<excluded
      <<" surviving="<<total-excluded<<" min_known="<<minpref
      <<" first_example="<<exfirst<<":"<<exgot<<"/"<<exwant<<" hist=";
  for(size_t i=0;i<hist.size();i++)if(hist[i])cout<<i<<":"<<hist[i]<<",";
  cout<<" first_survivor=";for(int i:survivors)cout<<i<<",";cout<<'\n';
 }
}
