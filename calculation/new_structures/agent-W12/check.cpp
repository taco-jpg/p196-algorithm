// Agent W12: decimal central four-digit pumping, all-q finite-horizon proof.
// Reproduce with: g++ -O3 -std=c++17 check.cpp -o w12 && ./w12 6000 20000
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

string step(const string& s) {
  int n=(int)s.size(), carry=0;
  string out(n+1,'0');
  for(int i=0;i<n;i++) {
    int x=s[i]-'0'+s[n-1-i]-'0'+carry;
    out[n-i]=char('0'+x%10); carry=x/10;
  }
  out[0]=char('0'+carry);
  if(!carry)out.erase(out.begin());
  return out;
}
// Independent whole-number implementation: base-10000 limbs and
// explicit decimal reversal, not the digit-by-digit carry code above.
vector<int> parse(const string& s) {
  vector<int> v;
  for(int r=(int)s.size();r>0;r-=4) {
    int x=0;
    for(int i=max(0,r-4);i<r;i++)x=x*10+s[i]-'0';
    v.push_back(x);
  }
  return v;
}
string step_limbs(const string& s) {
  string rev(s.rbegin(),s.rend());
  vector<int> a=parse(s),b=parse(rev),v(max(a.size(),b.size())+1,0);
  int carry=0;
  for(size_t i=0;i+1<v.size();i++) {
    int z=(i<a.size()?a[i]:0)+(i<b.size()?b[i]:0)+carry;
    v[i]=z%10000;carry=z/10000;
  }
  v.back()=carry;
  while(v.size()>1&&v.back()==0)v.pop_back();
  string out=to_string(v.back());char buffer[6];
  for(int i=(int)v.size()-2;i>=0;i--) {
    snprintf(buffer,sizeof(buffer),"%04d",v[i]);out+=buffer;
  }
  return out;
}
string initial(int q) {
  string s="12";
  for(int i=0;i<q;i++)s+="0297";
  return s+"34";
}
uint64_t fnv(const string& s) {
  uint64_t h=1469598103934665603ull;
  for(unsigned char c:s){h^=c;h*=1099511628211ull;}
  return h;
}
int period(const string& s,bool pairs=false) {
  int n=(int)s.size(),l=n/2-64,r=n/2+64;
  if(l<0||r>n)return 0;
  auto val=[&](int j) {
    return pairs ? s[j]-'0'+s[n-1-j]-'0' : s[j]-'0';
  };
  for(int p=1;p<=6;p++) {
    bool good=true;
    for(int i=l+p;i<r;i++)if(val(i)!=val(i-p)){good=false;break;}
    if(good)return p;
  }
  return 0;
}
void verify_three() {
  for(int q:{2,3,9,45,1000}) {
    string s=initial(q);
    vector<string> expected(4);
    expected[0]=s;
    expected[1]="55";for(int j=0;j<q;j++)expected[1]+="8217";expected[1]+="55";
    expected[2]="111";for(int j=0;j<q;j++)expected[2]+="5346";expected[2]+="10";
    expected[3]="127";for(int j=1;j<q;j++)expected[3]+="9702";expected[3]+="969721";
    for(int t=0;t<=3;t++) {
      if(s!=expected[t]){cerr<<"THREE_FAIL q="<<q<<" t="<<t<<"\n";exit(10);}
      if(t<3) {
        string u=step(s);
        if(u!=step_limbs(s)){cerr<<"THREE_ARITH_FAIL\n";exit(11);}
        s=u;
      }
    }
  }
  cout<<"THREE_PASS q=2,3,9,45,1000\n";
}
int main(int argc,char**argv) {
  int q=argc>1?atoi(argv[1]):6000,tmax=argc>2?atoi(argv[2]):20000;
  if(q<2||tmax<0)return 1;
  verify_three();
  string a=initial(q),b=initial(q+1);
  int gamma[2]={0,0},max_match=0;
  map<int,int> periods,pairperiods;
  for(int t=0;t<=tmax;t++) {
    int n=(int)a.size(),cut=n/2;
    if(b.size()!=a.size()+4
       ||a.compare(0,cut,b,0,cut)!=0
       ||a.compare(cut,n-cut,b,cut+4,n-cut)!=0) {
      cerr<<"PUMP_FAIL t="<<t<<"\n";return 2;
    }
    int p=period(a),pp=period(a,true);
    if(!p||!pp){cerr<<"PERIOD_FAIL t="<<t<<"\n";return 3;}
    periods[p]++;pairperiods[pp]++;
    int mismatch=0;
    while(mismatch<min(cut,n-cut)
          &&a[mismatch]==a[n-1-mismatch])mismatch++;
    if(mismatch>=min(cut,n-cut)){
      cerr<<"PALINDROME_WITNESS_FAIL t="<<t<<"\n";return 4;
    }
    max_match=max(max_match,mismatch);
    if(t%1000==0||t==tmax) {
      cout<<"t="<<t<<" digits="<<n<<" period="<<p
          <<" pairperiod="<<pp<<" mismatch="<<mismatch
          <<" inserted="<<b.substr(cut,4)
          <<" fnv64="<<hex<<fnv(a)<<dec<<"\n";
    }
    if(t==tmax)break;
    string na=step(a),nb=step(b);
    if(na!=step_limbs(a)||(t%1000==0&&nb!=step_limbs(b))) {
      cerr<<"INDEPENDENT_ARITH_FAIL t="<<t<<"\n";return 5;
    }
    gamma[na.size()>a.size()]++;
    a.swap(na);b.swap(nb);
  }
  cout<<"PASS ALL_Q_GE_"<<q<<" steps="<<tmax
      <<" gamma0="<<gamma[0]<<" gamma1="<<gamma[1]
      <<" max_outer_equal_prefix="<<max_match
      <<" periods=";
  for(auto [p,n]:periods)cout<<p<<":"<<n<<",";
  cout<<" pairperiods=";
  for(auto [p,n]:pairperiods)cout<<p<<":"<<n<<",";
  cout<<"\n";
  return 0;
}
