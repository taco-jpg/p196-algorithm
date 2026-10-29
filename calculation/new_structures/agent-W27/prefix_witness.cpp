// W27: exact near-root odd-pair witness depths, ordinary decimal carry engine.
// Reproduce: c++ -O3 -std=c++17 prefix_witness.cpp -o prefix_witness && ./prefix_witness
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
static void advance(vector<uint8_t>&d,vector<uint8_t>&tmp){
 int n=int(d.size()),carry=0;tmp.resize(n+1);
 for(int i=0;i<n;i++){int s=int(d[i])+int(d[n-i-1])+carry;tmp[i]=s%10;carry=s/10;}
 if(carry)tmp[n]=carry;else tmp.pop_back();d.swap(tmp);
}
static void run(string name,string s,int steps,int bound,int expected_max,int expected_at){
 vector<uint8_t>d,tmp;for(auto it=s.rbegin();it!=s.rend();++it)d.push_back(uint8_t(*it-'0'));
 int maxodd=-1,tmax=-1,maxmis=-1,noodd=0;map<int,int>hist;
 for(int t=0;t<=steps;t++){
  int n=int(d.size()),m=n/2,odd=m,mis=m;
  for(int i=0;i<m;i++)if((int(d[i])+d[n-i-1])%2){odd=i;break;}
  for(int i=0;i<m;i++)if(d[i]!=d[n-i-1]){mis=i;break;}
  // Three early even-pairword 196 exceptions are checked independently.
  if((odd==m && (name!="196" || t>=20))||
     (odd!=m && odd>=bound)||mis==m){
   cerr<<"SAFETY_FAIL "<<name<<" t="<<t<<" odd="<<odd<<" mismatch="<<mis<<"\n";exit(2);
  }
  if(odd==m)noodd++;
  else if(odd>maxodd){maxodd=odd;tmax=t;}
  maxmis=max(maxmis,mis);
  if(odd!=m)hist[odd]++;
  if(t<steps)advance(d,tmp);
 }
 if(maxodd!=expected_max||tmax!=expected_at){
  cerr<<"EXPECTED_FAIL "<<name<<" got="<<maxodd<<" at="<<tmax<<"\n";exit(3);
 }
 cout<<"PASS "<<name<<" states="<<steps+1<<" max_first_odd="<<maxodd
     <<" at="<<tmax<<" max_first_mismatch="<<maxmis
     <<" final_digits="<<d.size()<<" all_even_pairword_count="<<noodd
     <<" odd_depth0_count="<<hist[0]<<"\n";
}
int main(){
 run("196","196",100000,29,28,9777);
 run("196-nine-shell","196"+string(12010,'9')+"196",20000,19,18,4852);
}