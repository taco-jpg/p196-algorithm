// Agent-X28 exact affine run-length reverse-and-add checker.
// Every run has affine length a*r+b; every branch is valid for ALL r >= R.
// g++ -O3 -std=c++17 affine_carry.cpp -o affine_carry
// ./affine_carry 14000 20000
#include <algorithm>
#include <cassert>
#include <climits>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
struct E {long long a=0,b=0; E operator+(E x) const{return {a+x.a,b+x.b};} E operator-(E x) const{return {a-x.a,b-x.b};} bool zero() const{return a==0&&b==0;} long long at(long long r)const{return a*r+b;}};
struct R {int d;E l;};
using Word=vector<R>;
long long Rmin=14000; long long testedPieces=0;
void require(bool ok,const char*s){if(!ok)throw runtime_error(s);}
void positive(E e){require(e.at(Rmin)>0&&e.a>=0,"length is not uniformly positive for all r>=R");}
E minimum(E a,E b){E d=a-b;if(d.at(Rmin)<=0&&d.a<=0)return a;if(d.at(Rmin)>=0&&d.a>=0)return b;throw runtime_error("length comparison crosses threshold R");}
void put(Word &w,int digit,E count){if(count.zero())return;positive(count);require(0<=digit&&digit<=9,"illegal digit");if(!w.empty()&&w.back().d==digit){w.back().l=w.back().l+count;}else w.push_back({digit,count});}
E total(const Word&w){E s{};for(auto z:w)s=s+z.l;return s;}
struct Scan {const Word &w;long long index,dir; E left;Scan(const Word&v,bool reversed):w(v),index(reversed?(long long)v.size()-1:0),dir(reversed?-1:1),left(v[index].l){}int digit(){return w[index].d;}bool done(){return index<0||index>=(long long)w.size();}void consume(E k){left=left-k;require(left.at(Rmin)>=0,"negative run residue");if(left.zero()){index+=dir;if(!done())left=w[index].l;}else positive(left);} };
struct Stats{long long totalColumns=0;long long max0=0,max9=0;int n0=0,n9=0;};
Word symbolic_step(const Word&w,Stats&stats){require(!w.empty(),"empty word");Scan lo(w,false),hi(w,true);Word result;int carry=0;E whole=total(w),read{};int target=-1;E seen{};
 auto flush=[&](){if(target==0||target==9){long long val=seen.at(Rmin);if(target==0){stats.max0=max(stats.max0,val);if(val>=1957){require(seen.a>=0,"zero band length cannot decrease for larger r");stats.n0++;}}else{stats.max9=max(stats.max9,val);if(val>=13991){require(seen.a>=0,"nine band length cannot decrease for larger r");stats.n9++;}}}};
 while(!lo.done()&&!hi.done()){
  E len=minimum(lo.left,hi.left);positive(len);read=read+len;int q=lo.digit()+hi.digit();
  if(q!=target){flush();target=q;seen=len;}else seen=seen+len;
  int next=(q+carry)/10,first=(q+carry)%10,bulk=(q+next)%10;
  put(result,first,{0,1});E rest=len-E{0,1};if(!rest.zero())put(result,bulk,rest);carry=next;
  lo.consume(len);hi.consume(len);++testedPieces;
 }
 flush();require(read.a==whole.a&&read.b==whole.b,"pairword length mismatch");
 if(carry)put(result,1,{0,1});return result;
}
bool nonpal(const Word&w){Scan a(w,false),b(w,true);while(!a.done()&&!b.done()) {if(a.digit()!=b.digit())return true;E len=minimum(a.left,b.left);positive(len);a.consume(len);b.consume(len);}return false;}
int main(int argc,char**argv){try{Rmin=argc>1?atoll(argv[1]):14000;int T=argc>2?atoi(argv[2]):20000;require(Rmin>=30,"R must >=30");
 Word w;put(w,0,{1,0});put(w,9,{0,1});put(w,0,{0,1});put(w,9,{1,0});put(w,0,{0,1});put(w,9,{0,1});
 long long min0=LLONG_MAX,min9=LLONG_MAX;long long min0cnt=LLONG_MAX,min9cnt=LLONG_MAX; for(int t=0;t<=T;t++){
  require(nonpal(w),"a palindrome exists in affine language");Stats s;Word next=symbolic_step(w,s);
  if(t<20){require(s.n9>=2,"no two invariant 9-bands");min9=min(min9,s.max9);min9cnt=min(min9cnt,(long long)s.n9);}else{require(s.n0>=2,"no two invariant 0-bands");min0=min(min0,s.max0);min0cnt=min(min0cnt,(long long)s.n0);}
  if(t==0||t==1||t==19||t==20||t==21||t==100||t==1000||t==5000||t==10000||t==15000||t==20000||t==T){E width=total(w);cout<<"AFFINE t="<<t<<" width="<<width.a<<"*r+"<<width.b<<" instantiated="<<width.at(Rmin)<<" runs="<<w.size()<<" q_run="<<(t<20?9:0)<<" longest="<<(t<20?s.max9:s.max0)<<" invariant_count="<<(t<20?s.n9:s.n0)<<"\n";}
  if(t==T)break;w=move(next);
 }
 cout<<"SUCCESS AFFINE for every integer r>="<<Rmin<<" t=0.."<<T<<" min9="<<min9<<" min0="<<min0<<" min9count="<<min9cnt<<" min0count="<<min0cnt<<" transitions="<<testedPieces<<"\n";return 0;
 }catch(const exception &e){cerr<<"UNDECIDED: "<<e.what()<<"\n";return 2;}}
