// Independent base-1e9 integer arithmetic, from literal original seed to target state.
#include <bits/stdc++.h>
using namespace std;
struct Big {
 static constexpr uint64_t B=1000000000ULL;
 vector<uint32_t>a;
 Big(string s){for(int e=s.size();e>0;e-=9){int b=max(0,e-9);uint32_t v=0;for(int i=b;i<e;i++)v=v*10+s[i]-'0';a.push_back(v);}trim();}
 void trim(){while(a.size()>1&&!a.back())a.pop_back();}
 string str()const{string s=to_string(a.back());for(int j=(int)a.size()-2;j>=0;j--){string v=to_string(a[j]);s+=string(9-v.size(),'0')+v;}return s;}
 void add(const Big&rhs){size_t n=max(a.size(),rhs.a.size());a.resize(n+1,0);uint64_t c=0;for(size_t i=0;i<n;i++){uint64_t v=c+a[i]+(i<rhs.a.size()?rhs.a[i]:0);a[i]=v%B;c=v/B;}a[n]=c;trim();}
};
int main(int argc,char**argv){
 if(argc!=3)return 2;
 int gap=atoi(argv[1]),tmax=atoi(argv[2]);
 Big n("39"+string(gap,'0')+"43");
 for(int t=0;t<=tmax;t++){
  string s=n.str();
  if(s==string(s.rbegin(),s.rend())){cerr<<"PAL t="<<t<<"\n";return 1;}
  if(t==tmax){cout<<s<<'\n';return 0;}
  string r(s.rbegin(),s.rend());n.add(Big(r));
 }
}
