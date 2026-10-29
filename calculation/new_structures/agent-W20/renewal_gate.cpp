// Agent-W20: a programmable third-renewal gate in the decimal p8 / m20 centre.
// From repository root:
// g++ -std=c++17 -O3 calculation/new_structures/agent-W20/renewal_gate.cpp -o /tmp/w20_gate
// /tmp/w20_gate scan calculation/new_structures/agent-N18/lattice.txt
// /tmp/w20_gate long calculation/new_structures/agent-N18/lattice.txt 240 20000
// Ordinary digit operations and coefficient operations are separate implementations.
#include <array>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Bytes=vector<unsigned char>;
array<array<int,8>,39> ext;
array<int,39> B;
array<int,20> W;

void read_data(const string& filename){
  ifstream f(filename);
  if(!f)throw runtime_error("cannot open lattice fixture: "+filename);
  for(int i=0;i<39;i++)for(int t=0;t<8;t++){
    if(!(f>>ext[i][t]))throw runtime_error("incomplete 39-column exterior");
    if(t==0)B[i]=ext[i][0];
  }
  for(int t=0;t<8;t++)for(int i=0;i<20;i++){
    int x; if(!(f>>x))throw runtime_error("incomplete 8-phase band");
    if(t==0)W[i]=x;
  }
  int junk;if(f>>junk)throw runtime_error("unexpected extra rows");
}

Bytes core(int x,int y,int z){
  vector<int> U(43,1);
  U[13]=7;U[20]=7;U[30]=6;
  U[40]=x;U[41]=y;U[42]=z;
  Bytes C={8,0,0};for(int v:U)C.push_back(v);C.push_back(16);
  for(auto i=U.rbegin();i!=U.rend();++i)C.push_back(*i);
  C.insert(C.end(),{0,0,8});return C;
}
Bytes seed_pair(const Bytes& C, int q){
  if(q<1)throw runtime_error("q must be positive");
  Bytes A;for(int x:B)A.push_back(x);
  for(int k=0;k<q;k++)for(int x:W)A.push_back(x);
  Bytes P=A;P.insert(P.end(),C.begin(),C.end());
  P.insert(P.end(),A.rbegin(),A.rend());return P;
}
Bytes seed_digits(const Bytes& P){
  if(P!=Bytes(P.rbegin(),P.rend())||P.size()%2!=1)throw runtime_error("invalid pairword");
  Bytes d(P.size());size_t n=P.size();
  for(size_t i=0;i<n/2;i++){
    int p=P[i];
    // The high digit is nonzero because B[0]=17.
    d[i]=(unsigned char)min(p,9);d[n-1-i]=(unsigned char)(p-d[i]);
  }
  if(P[n/2]%2)throw runtime_error("odd midpoint coefficient");
  d[n/2]=P[n/2]/2;
  return d;
}
Bytes pair_of(const Bytes& d){
  Bytes P(d.size());for(size_t i=0;i<d.size();i++)P[i]=d[i]+d[d.size()-1-i];return P;
}
void coefficient_step(Bytes& P){
  Bytes digits;digits.reserve(P.size()+1);int carry=0;
  for(auto p:P){int s=p+carry;digits.push_back(s%10);carry=s/10;}
  if(carry)digits.push_back(carry);
  P=pair_of(digits);
}
void ordinary_digit_step(Bytes& d){
  // True N + reverse(N), with independent positional arithmetic.
  Bytes sum;sum.reserve(d.size()+1);
  int carry=0;size_t n=d.size();
  for(size_t j=0;j<n;j++){
    int v=d[j]+d[n-1-j]+carry;
    sum.push_back(v%10);carry=v/10;
  }
  if(carry)sum.push_back(carry);
  if(sum.back()==0)throw runtime_error("leading zero in ordinary addition");
  d.swap(sum);
}
int matched_band(const Bytes& P){
  if(P.size()<118)throw runtime_error("word too short for full band comparison");
  int k=0;while(k<20&&P[39+k]==W[k])k++;return k;
}
void root_check(const Bytes& P,int t){
  if(P.size()<78)throw runtime_error("word too short for root check");
  for(int i=0;i<39;i++)if(P[i]!=ext[i][t%8])throw runtime_error("root mismatch at t="+to_string(t)+" i="+to_string(i));
  // P[0]=17 or 8 at the two parity phases, and other outer columns are odd:
  bool odd=false;for(int i=0;i<39;i++)odd|=(P[i]&1)!=0;
  if(!odd)throw runtime_error("no odd outer coefficient");
}
struct Scan{int a,b,c,d;};
Scan run_gate(int x,int y,int z){
  Bytes P=seed_pair(core(x,y,z),1);
  int r[4]={};
  for(int t=0;t<=264;t++){
    root_check(P,t);
    if(t==88)r[0]=matched_band(P);
    if(t==176)r[1]=matched_band(P);
    if(t==264)r[2]=matched_band(P);
    if(t<264)coefficient_step(P);
  }
  if(r[0]!=20||r[1]!=20|| !(r[2]==8||r[2]==13||r[2]==20))throw runtime_error("unexpected collision class");
  if(r[2]==20){
    for(int t=264;t<352;t++){
      root_check(P,t);coefficient_step(P);
    }
    root_check(P,352);r[3]=matched_band(P);
    if(r[3]!=2)throw runtime_error("unexpected fourth-return prefix");
  }else r[3]=-1;
  return {r[0],r[1],r[2],r[3]};
}
void scan(){
  map<int,int> counts;map<int,array<int,3>> reps;
  for(int x=0;x<19;x++)for(int y=0;y<19;y++)for(int z=0;z<19;z++){
    Scan r=run_gate(x,y,z);
    counts[r.c]++;
    if(!reps.count(r.c))reps[r.c]={x,y,z};
  }
  if(counts[8]!=64||counts[13]!=603||counts[20]!=6192||counts.size()!=3)
    throw runtime_error("regression: counts do not match full scan");
  cout<<"EXHAUSTIVE_GATE total=6859 first_two_full=6859 "
      <<"third_prefix_8="<<counts[8]<<" third_prefix_13="<<counts[13]
      <<" third_prefix_20="<<counts[20]<<" fourth_prefix_after_three=2\n";
  for(auto [k,a]:reps)cout<<"REP prefix="<<k<<" U40="<<a[0]<<" U41="<<a[1]<<" U42="<<a[2]<<"\n";
  cout<<"PASS\n";
}
void long_replay(int q,int horizon){
  const int x=0,y=0,z=0; // success gate with third return 20/20
  Bytes P=seed_pair(core(x,y,z),q), d=seed_digits(P);
  cout<<"REPLAY q="<<q<<" seed_digits="<<d.size()<<" steps="<<horizon<<"\n";
  int firstbad=-1;int over=0;
  for(int t=0;t<=horizon;t++){
    if(d.size()!=P.size()||pair_of(d)!=P)throw runtime_error("two independent update algorithms disagree at t="+to_string(t));
    if(d.front()==d.back() && d==Bytes(d.rbegin(),d.rend()))throw runtime_error("palindrome at t="+to_string(t));
    if(firstbad<0){for(int j=0;j<39;j++)if(P[j]!=ext[j][t%8]){firstbad=t;break;}}
    if(t<=352){if(t%88==0 && t>0)cout<<"CHECK t="<<t<<" band_prefix="<<matched_band(P)<<"\n";}
    if(t==horizon)break;
    size_t before=d.size();ordinary_digit_step(d);coefficient_step(P);
    if(d.size()!=before)over++;
  }
  cout<<"LONG_RESULT q="<<q<<" step="<<horizon<<" final_digits="<<d.size()
      <<" total_overflows="<<over<<" first_root_mismatch="<<firstbad
      <<" palindrome_count=0 pairword_disagreements=0\n";
  if(firstbad>=0)throw runtime_error("expected full phase-8 root survival over the selected horizon");
  cout<<"PASS\n";
}
int main(int argc,char**argv){
 try{
  if(argc<3){cerr<<"usage: renewal_gate (scan|long) lattice.txt [q steps]\n";return 2;}
  read_data(argv[2]);
  string m=argv[1];if(m=="scan")scan();else if(m=="long")long_replay(argc>3?atoi(argv[3]):240,argc>4?atoi(argv[4]):20000);
  else{cerr<<"unknown mode\n";return 2;}
 }catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
