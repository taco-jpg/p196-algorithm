#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
using D=vector<unsigned char>;
D digits(string s){D d;for(auto i=s.rbegin();i!=s.rend();++i)d.push_back(*i-'0');return d;}
void next(D&d){D a(d.size()+1);int c=0;for(size_t i=0,n=d.size();i<n;i++){int x=d[i]+d[n-1-i]+c;a[i]=x%10;c=x/10;}if(c)a[d.size()]=1;else a.pop_back();d.swap(a);}
struct Count {long long states=0,hist=0,odd=0,edge=0,badall=0,pal=0;};
bool inspect(D const &d,Count &z){
  int mask=0;bitset<100> e;bool pal=true,odd=false;
  for(auto x:d)mask^=1<<x;
  for(size_t i=0;i+1<d.size();i++){int a=d[i],b=d[i+1];if(a!=b)e.flip(min(a,b)*10+max(a,b));}
  for(size_t i=0,n=d.size();i<n/2;i++){odd|=(d[i]+d[n-1-i])%2;if(d[i]!=d[n-1-i])pal=false;}
  if(pal){z.pal++;return false;}
  z.states++;z.hist+=(__builtin_popcount((unsigned)mask)>1);z.odd+=odd;z.edge+=e.any();z.badall+=(__builtin_popcount((unsigned)mask)<=1&&!odd&&!e.any());return true;
}
Count replay(string seed,int steps,bool gmp){
  if(seed.rfind("88Z",0)==0)seed="88"+string(stoi(seed.substr(3)),'0')+"75";
  D d=digits(seed);Count z;mpz_class n(seed,10);
  for(int t=0;t<=steps;t++){
    if(gmp){string s=n.get_str(10);if(s.size()!=d.size())throw runtime_error("length mismatch");for(size_t i=0;i<d.size();i++)if(d[i]!=s[s.size()-1-i]-'0')throw runtime_error("digit mismatch");}
    if(!inspect(d,z))break;
    if(t==steps)break;
    if(gmp){string s=n.get_str(10);reverse(s.begin(),s.end());n+=mpz_class(s,10);}
    next(d);
  }
  return z;
}
int main(int argc,char**argv){
  if(argc>1&&string(argv[1])=="--sweep"){
    mt19937_64 rng(290474);Count sum;int survive=0;
    for(int i=0;i<2400;i++){
      string s;if(i<900)s=to_string(100+i);else{int len=6+rng()%15;s+='1'+rng()%9;for(int j=1;j<len;j++)s+='0'+rng()%10;}
      Count x=replay(s,1000,false);survive+=(x.states==1001);
      sum.states+=x.states;sum.hist+=x.hist;sum.odd+=x.odd;sum.edge+=x.edge;sum.badall+=x.badall;sum.pal+=x.pal;
    }
    cout<<"sweep seeds=2400 survive="<<survive<<" inspected="<<sum.states<<" pal_seeds="<<sum.pal<<" hist="<<sum.hist<<" odd="<<sum.odd<<" edge="<<sum.edge<<" badall="<<sum.badall<<"\n";return 0;
  }
  string seed=argc>1?argv[1]:"196";int steps=argc>2?stoi(argv[2]):20000;
  Count x=replay(seed,steps,true);
  cout<<"seed="<<seed<<" steps="<<steps<<" inspected="<<x.states<<" hist="<<x.hist<<" odd="<<x.odd<<" edge="<<x.edge<<" badall="<<x.badall<<" pal="<<x.pal<<" independent_GMP_every_step=PASS\n";
}
