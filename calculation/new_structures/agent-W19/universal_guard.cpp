// Universal two-step decimal packet erasure with length-two guards.
// Checks exact boundary-carry tables and arbitrary contexts.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <random>
#include <set>
#include <stdexcept>
#include <vector>
using namespace std;
using Word=vector<int>;
static constexpr array<int,4> C0={14,9,9,0},C1={0,14,9,0};
static Word digits(const Word&word,int carry){
 Word out;
 for(int x:word){int s=x+carry;out.push_back(s%10);carry=s/10;}
 if(carry)out.push_back(carry);
 return out;
}
static Word step(const Word&p){
 Word d=digits(p,0),out;out.reserve(d.size());
 for(size_t i=0;i<d.size();i++)out.push_back(d[i]+d[d.size()-1-i]);
 return out;
}
static Word form(const Word&exterior,const Word&inner,int center,const Word&guards,int mask){
 if(exterior.empty()||exterior[0]<10||exterior[0]>17)throw runtime_error("outer guard invalid");
 Word h=exterior;
 for(size_t i=0;i<guards.size();i++){
  int a=guards[i];if(a<6||a>8)throw runtime_error("invalid guard");
  h.insert(h.end(),{a,13});
  const auto&c=(mask&(1u<<i))?C1:C0;
  h.insert(h.end(),c.begin(),c.end());
 }
 h.insert(h.end(),inner.begin(),inner.end());
 Word p=h;if(center>=0)p.push_back(center);
 p.insert(p.end(),h.rbegin(),h.rend());
 return p;
}
static void local_table(){
 size_t tests=0;
 for(int a=6;a<=8;a++)for(int outer=0;outer<=1;outer++)for(int inner=0;inner<=1;inner++){
  for(int bit=0;bit<=1;bit++){
   // Low guard a,13 and packet; high side reversed packet,13,a.
   const auto&c=(bit?C1:C0);
   Word low={a,13};low.insert(low.end(),c.begin(),c.end());
   Word high(c.rbegin(),c.rend());high.insert(high.end(),{13,a});
   Word dl=digits(low,outer),dh=digits(high,inner);
   if(dl.size()!=6||dh.size()!=6)throw runtime_error("guard carry did not reset");
   int before=dl[1]+dh[5];
   Word w={dl[2]+dh[4],dl[3]+dh[3],dl[4]+dh[2]};
   int after=dl[5]+dh[1];
   if(before!=a+4||after!=10||
      w!=Word(bit?Word{4,5,4}:Word{9,4,9}))
      throw runtime_error("bad exact first-image carry table");
   Word d=digits(w,1);
   if(d!=Word(bit?Word{5,5,4}:Word{0,5,9}))
      throw runtime_error("bad exact second-image carry table");
   if(d[0]+d[2]!=9||2*d[1]!=10)
      throw runtime_error("not erased at second image");
   tests++;
  }
 }
 cout<<"EXACT_LOCAL_TABLE_PASS configurations="<<tests
     <<" guard_choices=6,7,8 outer_incoming=0,1 inner_incoming=0,1\n";
}
static void exhaustive_random_contexts(){
 mt19937 rng(20261029);uint64_t masks=0;
 for(int t=0;t<240;t++){
  Word e={10+int(rng()%8)},q,guards;
  for(int i=0,k=int(rng()%30);i<k;i++)e.push_back(int(rng()%19));
  for(int i=0,k=int(rng()%40);i<k;i++)q.push_back(int(rng()%19));
  int m=1+int(rng()%9),center=(rng()%3==0)?int(rng()%19):-1;
  for(int i=0;i<m;i++)guards.push_back(6+int(rng()%3));
  Word ref;set<Word> p1s,p0s;int n=1<<m;
  for(int mask=0;mask<n;mask++){
   Word p=form(e,q,center,guards,mask),p1=step(p),p2=step(p1);
   p0s.insert(p);p1s.insert(p1);
   if(mask==0)ref=p2;
   else if(p2!=ref)throw runtime_error("context erasure failed");
   masks++;
  }
  if(p0s.size()!=size_t(n)||p1s.size()!=size_t(n))
   throw runtime_error("preimage distinction failed");
 }
 cout<<"UNIVERSAL_CONTEXT_PASS contexts=240 tested_masks="<<masks
     <<" odd_even_centres=true arbitrary_exteriors=true arbitrary_inner_words=true\n";
}
int main(){try{
 local_table();exhaustive_random_contexts();return 0;
}catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
