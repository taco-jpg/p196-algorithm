// X08: exact base-ten digit-vector arithmetic and short-seed paired-parity witnesses.
// g++ -O3 -std=c++17 replay.cpp -o replay
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Digits=vector<uint8_t>;
Digits digits(uint64_t n){Digits d;do{d.push_back(n%10);n/=10;}while(n);return d;}
uint64_t number(const Digits&d){uint64_t n=0;for(auto i=d.rbegin();i!=d.rend();++i)n=n*10+*i;return n;}
bool palindrome(const Digits&d){for(size_t i=0;i<d.size()/2;++i)if(d[i]!=d[d.size()-1-i])return false;return true;}
void step(Digits&d){int n=d.size(),c=0;Digits z(n+1);for(int i=0;i<n;++i){int x=d[i]+d[n-1-i]+c;z[i]=x%10;c=x/10;}if(!c)z.pop_back();else z[n]=c;d.swap(z);}
int first_odd(const Digits&d){int n=d.size();for(int i=0;i<n/2;++i)if((d[i]+d[n-1-i])&1)return i;return -1;}
void require(bool b,const string&msg){if(!b)throw runtime_error(msg);}
struct Audit {int maxodd=-1,miss=0,pal=-1,len=0;};
Audit audit(uint64_t seed,int steps,bool trace=false){
  Digits d=digits(seed);Audit a;
  for(int t=0;t<=steps;++t){
    if(trace){for(auto i=d.rbegin();i!=d.rend();++i)cout<<char('0'+*i);cout<<'\n';}
    if(palindrome(d)){a.pal=t;break;}
    int k=first_odd(d);if(k<0)++a.miss;else a.maxodd=max(a.maxodd,k);
    if(t<steps)step(d);
  }
  a.len=d.size();return a;
}
void family(){
  int A=0,B=0;
  for(int a=1;a<=8;++a)for(int b=4;b<=9;++b){
    int c=13-b,d=8-a;uint64_t n=1000*a+100*b+10*c+d;
    Digits x=digits(n);require(first_odd(x)==1,"A initial witness");step(x);
    require(number(x)==9438,"A successor");++A;
  }
  for(int a=1;a<=9;++a)for(int b=6;b<=9;++b){
    int d=15-b,e=10-a;uint64_t n=10000*a+1000*b+900+10*d+e;
    Digits x=digits(n);require(first_odd(x)==1,"B initial witness");step(x);
    require(number(x)==116960,"B successor");++B;
  }
  require(A==48&&B==36,"wrong family count");
  cout<<"FAMILY a="<<A<<" b="<<B<<" same_successors=9438,116960\n";
}
void survey(){
  map<uint64_t,uint64_t> cls;int survivors=0;
  for(uint64_t n=1;n<=99999;++n){
    auto d=digits(n);if(palindrome(d))continue;
    auto d1=d;step(d1);uint64_t s=number(d1);
    bool ok=true;
    for(int t=1;t<=128;++t){if(t==1)d=d1;else step(d);if(palindrome(d)){ok=false;break;}}
    if(ok){++survivors;if(!cls.count(s))cls[s]=n;}
  }
  int pass1024=0;vector<pair<uint64_t,int>> selected;
  for(auto [s,n]:cls){
    if(audit(n,1024).pal<0)++pass1024;
    auto r=audit(n,2048);
    if(r.pal<0 && r.miss==0)selected.push_back({n,0});
  }
  require(survivors==6020&&cls.size()==261&&pass1024==261&&selected.size()==40,"survey counts changed");
  int maxodd=-1;
  for(auto &[n,k]:selected){
    auto r=audit(n,20000);require(r.pal<0&&r.miss==0,"survey witness failed");
    k=r.maxodd;maxodd=max(maxodd,k);
  }
  require(maxodd==26,"survey bound changed");
  cout<<"SURVEY nonpal_128="<<survivors<<" distinct_successors="<<cls.size()
      <<" classes_1024="<<pass1024<<" odd_every_state_2048="<<selected.size()
      <<" max_first_odd_20000="<<maxodd<<'\n';
  for(auto [n,k]:selected)cout<<"CLASS "<<n<<" "<<k<<'\n';
}
int main(int argc,char**argv){
  try{
    require(argc>=2,"usage: replay --family | --survey | --audit seed steps | --fulltrace seed steps");
    string mode=argv[1];
    if(mode=="--family")family();
    else if(mode=="--survey")survey();
    else if(mode=="--audit"||mode=="--fulltrace"){
      require(argc==4,"seed/steps missing");
      uint64_t n=stoull(argv[2]);int steps=stoi(argv[3]);
      require(steps>=0&&steps<=1000000,"invalid steps");
      Audit a=audit(n,steps,mode=="--fulltrace");
      if(mode=="--audit")cout<<"AUDIT seed="<<n<<" steps="<<steps<<" len="<<a.len
        <<" first_odd_max="<<a.maxodd<<" no_odd_states="<<a.miss<<" first_pal="<<a.pal<<'\n';
    }else require(false,"invalid mode");
  }catch(const exception&e){cerr<<"ERROR "<<e.what()<<'\n';return 1;}
}
