// Independent GMP arbitrary-precision replay using decimal string reversal, not digit-vector addition.
#include <gmpxx.h>
#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using Row = vector<int>;
vector<Row> csv(const string&path){ifstream f(path);if(!f)throw runtime_error("no "+path);string line;vector<Row>a;while(getline(f,line)){stringstream ss(line);string z;Row r;while(getline(ss,z,','))r.push_back(stoi(z));a.push_back(r);}return a;}
string seed(const vector<Row>&B,const vector<Row>&W,const Row& tail,int q){
 vector<int>h=B[0];for(int k=0;k<q;k++)for(auto x:W[0])h.push_back(x);
 for(int v:tail)h.push_back(v);
 int n=2*h.size();string s(n,'0');
 for(int i=0;i<n/2;i++){
    int v=h[i],leading=min(v,9),trailing=v-leading;
    s[i]=char('0'+leading);s[n-1-i]=char('0'+trailing);
 }

 if(s.front()=='0')throw runtime_error("bad leading");
 return s;
}
int main(int argc,char**argv){
 if(argc<7){cerr<<"usage: outward_gmp rows.csv B.csv tail.csv steps q checkpoint_path\n";return 2;}
 auto W=csv(argv[1]),B=csv(argv[2]),Tail=csv(argv[3]);int steps=stoi(argv[4]),q=stoi(argv[5]);
 if(Tail.size()!=1 || Tail[0].size()!=80)throw runtime_error("expected 80-digit centre tail");
 map<int,string> checkpoints;{ifstream in(argv[6]);int t;string v;while(in>>t>>v)checkpoints[t]=v;}
 string init=seed(B,W,Tail[0],q);mpz_class N(init,10);
 if(N.get_str()!=init)throw runtime_error("bad seed");
 for(int t=0;t<=steps;t++){
  string s=N.get_str();int n=s.size();
  if(equal(s.begin(),s.end(),s.rbegin())){cerr<<"pal t="<<t<<"\n";return 1;}
  for(int i=0;i<11+128;i++){
    int expected=i<11?B[t%8][i]:W[t%8][(i-11)%48];
    if((s[i]-'0')+(s[n-1-i]-'0')!=expected){cerr<<"pair mismatch t="<<t<<" i="<<i<<"\n";return 1;}
  }
  auto cp=checkpoints.find(t);
  if(cp!=checkpoints.end()){
    if(cp->second!=s){cerr<<"FULL BIGINT/ARRAY MISMATCH t="<<t<<"\n";return 1;}
    cout<<t<<","<<n<<",FULL-DECIMAL-EQUAL\n";
  }
  if(t==steps)break;
  string rev=s;reverse(rev.begin(),rev.end());mpz_class R(rev,10);N+=R;
  int expected=(t%2==0);
  if(int(N.get_str().size())-n != expected){cerr<<"gamma mismatch at "<<t<<"\n";return 1;}
 }
 cout<<"PASS GMP: "<<steps<<" full arbitrary-precision decimal reverse-and-add steps; "<<checkpoints.size()<<" exact full-number checkpoints; all nonpal and p8 rec2 prefix checks\n";
}
