// W27 independent least-significant-first decimal-digit arithmetic control.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Row=pair<pair<string,int>,string>;
const vector<Row> rows={
 {{"2905",0},"8723"},{{"6184",0},"3815"},{{"11368",-1},"88631"},
 {{"25057",-1},"74942"},{{"50005",-1},"49994"},{{"100000",-2},"899999"},
 {{"10",2},"8900000"},{{"1100098",-3},"8899901"},{{"2200087",-3},"7799912"},
 {{"4400065",-3},"5599934"},{{"8800021",-3},"1199978"},
 {{"17599933",-4},"82400066"},{{"83600362",-4},"16399637"}
};
vector<uint8_t> from(const string&s){
 vector<uint8_t>d;for(auto i=s.rbegin();i!=s.rend();i++)d.push_back(*i-'0');return d;
}
string literal(int q,const Row&r){
 return r.first.first+string(2*q+r.first.second,'9')+r.second;
}
void step(vector<uint8_t>&d,vector<uint8_t>&tmp){
 int n=d.size(),c=0;tmp.resize(n+1);
 for(int i=0;i<n;i++){int x=d[i]+d[n-i-1]+c;tmp[i]=x%10;c=x/10;}
 if(c)tmp[n]=c;else tmp.pop_back();d.swap(tmp);
}
int main(){
 for(int q:{2,3,4,5,40,100,600}){
  auto d=from(literal(q,rows[0]));vector<uint8_t>tmp;
  for(size_t t=0;t<rows.size();t++){
   auto want=from(literal(q,rows[t]));
   if(d!=want){cerr<<"MISMATCH q="<<q<<" step="<<t<<"\n";return 1;}
   int n=d.size();bool neq=false;
   for(int i=0;i<n/2;i++)if(d[i]!=d[n-i-1]){neq=true;break;}
   if(!neq){cerr<<"PAL q="<<q<<" step="<<t<<"\n";return 2;}
   if(t+1<rows.size())step(d,tmp);
  }
  cout<<"PASS q="<<q<<" phases=13\n";
 }
}