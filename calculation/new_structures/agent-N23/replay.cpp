// Independent ordinary base-b digit-list reverse-and-add; no Python or polynomial code.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
struct State {vector<int> U,V,W;};
static vector<int> digits(const string& s,int b) {
 vector<int> d;for(char c:s){if(c<'0'||c>'9')throw 1;int x=c-'0';if(x>=b)throw 2;d.push_back(x);}return d;
}
static vector<int> build(const State& s,int q){
 vector<int> d=s.U;for(int i=0;i<2*q;i++)d.insert(d.end(),s.V.begin(),s.V.end());
 d.insert(d.end(),s.W.begin(),s.W.end());return d;
}
static vector<int> step(const vector<int>& d,int b){
 int carry=0;vector<int> out;out.reserve(d.size()+1);
 for(size_t i=0;i<d.size();i++){int x=d[i]+d[d.size()-i-1]+carry;out.push_back(x%b);carry=x/b;}
 if(carry)out.push_back(carry);return out;
}
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: replay data.txt steps\n";return 2;}
 ifstream in(argv[1]);int b,q,n;in>>b>>q>>n;if(!in||b>10||b<2||q<2||n<1)return 2;
 vector<State> states;
 for(int j=0;j<n;j++){string a,v,c;in>>a>>v>>c;if(!in)return 2;states.push_back({digits(a,b),digits(v,b),digits(c,b)});}
 int total=stoi(argv[2]);vector<int> x=build(states[0],q);
 for(int t=0;t<total;t++){
  if(x.empty()||x.back()==0||equal(x.begin(),x.end(),x.rbegin())){cerr<<"palindrome/leading-zero @"<<t<<"\n";return 3;}
  x=step(x,b);int phase=(t+1)%n;if(phase==0)q++;
  auto want=build(states[phase],q);
  if(x!=want){cerr<<"template mismatch @"<<t+1<<" expected="<<want.size()<<" actual="<<x.size()<<"\n";return 4;}
 }
 if(equal(x.begin(),x.end(),x.rbegin()))return 5;
 cout<<"PASS ordinary-digit reverse-add "<<total<<" steps, base="<<b<<", phases="<<n<<", final length="<<x.size()<<", band parameter="<<q<<"\n";
}
