// W06: p8/m20 lattice / uniform buffer; independent decimal digit-array reverse-add.
// Compile: g++ -O3 -std=c++17 interface44.cpp -o /tmp/w06
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Dig=vector<uint8_t>;
const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
array<vector<int>,8> expectedB,expectedW;
[[noreturn]] void fail(const string&s){cerr<<"FAIL: "<<s<<"\n";exit(1);}
Dig seed(int k,int value,int L,int centre,int inside){
 vector<int> half=B;
 for(int j=0;j<k;j++)half.insert(half.end(),W.begin(),W.end());
 half.insert(half.end(),L,value);
 for(int j=0;j<inside;j++)half.insert(half.end(),W.begin(),W.end());
 vector<int> P=half;P.push_back(centre);P.insert(P.end(),half.rbegin(),half.rend());
 Dig d(P.size());int n=P.size();
 for(int i=0;i<n/2;i++){int a=min(9,P[i]);d[i]=a;d[n-i-1]=P[i]-a;}
 d[n/2]=centre/2;
 if(d.back()==0||d.front()==0)fail("non-canonical initial integer");
 return d;
}
void step(Dig&d){
 int n=d.size(),carry=0;Dig out(n+1);
 for(int i=0;i<n;i++){int v=d[i]+d[n-1-i]+carry;out[i]=v%10;carry=v/10;}
 if(carry)out[n]=carry;else out.pop_back();d.swap(out);
}
int P(const Dig&d,int i){return d[i]+d[d.size()-1-i];}
void init_phase(){
 auto d=seed(20,9,0,18,0);
 for(int t=0;t<8;t++){
  for(int i=0;i<39;i++)expectedB[t].push_back(P(d,i));
  for(int i=39+40;i<39+60;i++)expectedW[t].push_back(P(d,i));
  step(d);
 }
 if(expectedB[0]!=B||expectedW[0]!=W)fail("bad phase seed");
 for(int t=0;t<4;t++)for(int i=0;i<20;i++)
  if(expectedW[t+4][i]!=expectedW[t][(i+10)%20])fail("bulk half-phase rotation");
}
int frontier(const Dig&d,int t){
 int m=d.size()/2;
 for(int i=0;i<m;i++){
  int e=i<39?expectedB[t%8][i]:expectedW[t%8][(i-39)%20];
  if(P(d,i)!=e)return i;
 }
 return m;
}
string window(const Dig&d,int h){
 if(h<40||h+80>=(int)d.size()/2)return "";
 string s;for(int j=-40;j<80;j++)s+="0123456789ABCDEFGHI"[P(d,h+j)];return s;
}
bool palindrome(const Dig&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
uint64_t full_hash(const Dig&d){
 uint64_t h=1469598103934665603ull;
 for(auto it=d.rbegin();it!=d.rend();++it){h^=(uint8_t)('0'+*it);h*=1099511628211ull;}
 return h;
}
struct State{int h;string w;bool operator==(const State&b)const{return h==b.h&&w==b.w;}};
vector<State> orbit(int K,int value,int L,int centre,int inner,int T,int min_front,
 int& bad_clock,int& pals,uint64_t& final_hash,int& final_length){
 auto d=seed(K,value,L,centre,inner);vector<State> records(T+1);
 bad_clock=pals=0;
 for(int t=0;t<=T;t++){
  int h=frontier(d,t);if(h<min_front)fail("rooted bulk exhausted at t="+to_string(t));
  auto w=window(d,h);if(w.size()!=120)fail("interface window outside half-number");
  records[t]={h,w};pals+=palindrome(d);
  if(t<T){int n=d.size();step(d);bad_clock+=(int)d.size()-n != (t%2==0?1:0);}
 }
 final_hash=full_hash(d);final_length=d.size();return records;
}
void check_return(const vector<State>&s,int lag,int shift,int start){
 for(int t=start;t+lag<(int)s.size();t++)
  if(s[t+lag].h!=s[t].h+shift||s[t+lag].w!=s[t].w)
   fail("lag="+to_string(lag)+" mismatch at t="+to_string(t));
}
void long_run(){
 int clock,pals,nd;uint64_t hash;
 auto s=orbit(320,9,180,18,0,20000,512,clock,pals,hash,nd);
 if(clock||pals)fail("overflow/palindrome in 20k replay");
 check_return(s,44,-10,898);
 if(nd!=23239||s[0].h!=6439||s[898].h!=6234||s.back().h!=1894||
  hash!=0xa2032887cdcb0524ull)fail("20k fingerprints changed");
 cout<<"COMPUTED long steps=20000 states=20001 palindrome=0 clock_bad=0 "
  <<"h0="<<s[0].h<<" h898="<<s[898].h<<" h20000="<<s.back().h
  <<" return44_checks="<<20000-44-898+1<<" final_digits="<<nd
  <<" full_MSD_FNV64="<<hex<<hash<<dec<<"\n";
 Dig ctl={6,5};step(ctl);if(ctl!=Dig({1,2,1})||!palindrome(ctl))fail("palindrome control");
 if(s[898+44].h==s[898].h-9)fail("mutant shift control");
}
void sweep(){
 vector<int> values={0,4,8,9,12,16,18};
 vector<vector<State>>outer;
 for(int v:values){
  int c,p,n;uint64_t f;
  auto s=orbit(120,v,180,18,0,2500,1500,c,p,f,n);
  if(c||p)fail("overflow/palindrome value "+to_string(v));
  int start=(v==8?1046:v==12?1003:v==16?1074:v==18?1098:898);
  check_return(s,88,-20,start);
  if(v==0||v==4||v==9)check_return(s,44,-10,898);
  outer.push_back(s);
  auto q=orbit(120,v,180,18,3,2500,1500,c,p,f,n);
  if(c||p||s!=q)fail("inner lattice affected interface value="+to_string(v));
  cout<<"buffer="<<v<<" 88_shift=-20 starts="<<start
    <<" 44_recurrence="<<(v==0||v==4||v==9?"yes":"not observed")<<"\n";
 }
 for(int j:{0,1}){
  int first=(j==0?1:832);
  for(int t=first;t<=2500;t++)
   if(outer[j][t].h!=outer[3][t].h||outer[j][t].w!=outer[3][t].w)
    fail("reset attractor mismatch t="+to_string(t));
 }
 cout<<"COMPUTED sweep 14 orbits x2500; 0/9 interface coalesces t=1, "
    <<"4/9 interface coalesces by t=832\n";
}
int main(int argc,char**argv){
 init_phase();string mode=argc>1?argv[1]:"long";
 if(mode=="long")long_run();else if(mode=="sweep")sweep();else fail("mode long or sweep");
}