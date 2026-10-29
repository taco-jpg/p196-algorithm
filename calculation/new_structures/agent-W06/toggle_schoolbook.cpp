// Independent digit-array ordinary decimal reverse-and-add 20k replay.
// g++ -O3 -std=c++17 toggle_schoolbook.cpp -o /tmp/w06tbook
// /tmp/w06tbook [M=320] [T=20000]
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
using Dig=vector<uint8_t>;
Dig build(int M){
 vector<int> half=B;
 for(int r=0;r<M;r++)half.insert(half.end(),W.begin(),W.end());
 vector<int> p=half;p.push_back(18);p.insert(p.end(),half.rbegin(),half.rend());
 Dig d(p.size());for(int i=0;i<(int)half.size();i++){
  int x=min(9,p[i]);d[i]=x;d[p.size()-1-i]=p[i]-x;
 }
 d[half.size()]=9;return d;
}
void revadd(Dig&d){Dig v(d.size()+1);int carry=0,n=d.size();for(int i=0;i<n;i++){
 int t=d[i]+d[n-1-i]+carry;v[i]=t%10;carry=t/10;
 }if(carry)v[n]=carry;else v.pop_back();d.swap(v);}
uint64_t fnv(const Dig&d){uint64_t h=1469598103934665603ull;for(auto it=d.rbegin();it!=d.rend();++it){h^=uint8_t('0'+*it);h*=1099511628211ull;}return h;}
int main(int argc,char**argv){int M=argc>1?atoi(argv[1]):320,T=argc>2?atoi(argv[2]):20000;
 if(M<1||T<2)return 2;
 Dig d=build(M);int pal=0,clockbad=0,rootbad=0;
 std::array<std::array<int,39>,8> Bphase{};
 std::array<std::array<int,20>,8> Wphase{};
 Dig ref=build(20);
 for(int phase=0;phase<8;phase++){
  for(int j=0;j<39;j++)Bphase[phase][j]=int(ref[j])+int(ref[ref.size()-1-j]);
  for(int j=0;j<20;j++){int ix=39+40+j;Wphase[phase][j]=int(ref[ix])+int(ref[ref.size()-1-ix]);}
  revadd(ref);
 }
 int shape_bad=0;
 for(int t=0;t<=T;t++){
  if(equal(d.begin(),d.begin()+d.size()/2,d.rbegin()))pal++;
  // Independent external root phase: its first two coefficients suffice for nonpal guard.
  const int root0[8]={17,8,17,8,17,8,17,8};
  const int root1[8]={5,13,6,14,8,16,13,12};
  rootbad+=int(d[0])+int(d.back())!=root0[t%8];
  rootbad+=int(d[1])+int(d[d.size()-2])!=root1[t%8];
  for(int i=0;i<39+256;i++){
   int expected=i<39?Bphase[t%8][i]:Wphase[t%8][(i-39)%20];
   if(int(d[i])+int(d[d.size()-1-i])!=expected)shape_bad++;
  }
  if(t==0||t==1||t==2||t==T)cout<<"t="<<t<<" digits="<<d.size()<<" fnv="<<hex<<fnv(d)<<dec<<"\n";
  if(t<T){int old=d.size();revadd(d);clockbad+=int(d.size())-old!=(t%2==0?1:0);}
 }
 cout<<"COMPUTED digit-array M="<<M<<" T="<<T<<" initial_digits="<<2*(39+20*M)+1
  <<" final_digits="<<d.size()<<" palindrome_count="<<pal<<" clockbad="<<clockbad
  <<" root_guard_bad="<<rootbad<<" exact_295cell_shape_bad="<<shape_bad<<" final_full_msd_FNV64="<<hex<<fnv(d)<<dec<<"\n";
 return pal||clockbad||rootbad||shape_bad?1:0;
}
