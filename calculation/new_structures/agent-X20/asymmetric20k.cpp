// Base-10^9 limb-engine independently replays exact arithmetic on independently chosen m,n.
// g++ -O3 -std=c++17 asymmetric20k.cpp -o /tmp/x20_big && /tmp/x20_big 427 509 20000
#define main X20_transducer_main
#include "two_counter.cpp"
#undef main
struct Big9 {
 static constexpr uint32_t base=1000000000;vector<uint32_t> a;
 explicit Big9(const string& s){for(int r=s.size();r>0;r-=9){int l=max(0,r-9);a.push_back((uint32_t)stoul(s.substr(l,r-l)));}while(a.size()>1&&a.back()==0)a.pop_back();}
 string str()const{string s=to_string(a.back());for(int j=(int)a.size()-2;j>=0;j--){string q=to_string(a[j]);s.append(9-q.size(),'0');s+=q;}return s;}
 void add(const Big9&b){uint64_t carry=0;size_t n=max(a.size(),b.a.size());a.resize(n,0);for(size_t i=0;i<n;i++){uint64_t v=(uint64_t)a[i]+(i<b.a.size()?b.a[i]:0)+carry;a[i]=v%base;carry=v/base;}if(carry)a.push_back(carry);}
};
static uint64_t fnv(const V&a){uint64_t h=1469598103934665603ull;for(auto v:a){h^=v;h*=1099511628211ull;}return h;}
static string msf(const V&d){string s;s.reserve(d.size());for(auto it=d.rbegin();it!=d.rend();++it)s.push_back('0'+*it);return s;}
int main(int argc,char**argv){int m=argc>1?stoi(argv[1]):427,n=argc>2?stoi(argv[2]):509,steps=argc>3?stoi(argv[3]):20000;if(m<400||n<400)return 2;
 V P=seed(m,n),D=norm(P).first,w=W,v=Q;Big9 big(msf(D));size_t wa=39+400,wb=39+1400,vc=39+20*m+1+15000,vd=39+20*m+1+15960;
 for(int t=0;t<=steps;t++){
  if(ispal(D)||P.size()/2<vd){cerr<<"palindrome or window bound t="<<t<<"\n";return 3;}
  for(size_t j=wa;j<wb;j++)if(P[j]!=w[(j-39)%20]){cerr<<"W lost t="<<t<<"\n";return 4;}
  size_t b=39+20*m+1;for(size_t j=vc;j<vd;j++)if(P[j]!=v[(j-b)%48]){cerr<<"V lost t="<<t<<"\n";return 5;}
  auto pp=norm(P);if(pp.first!=D||pp.second!=(t%2==0)){cerr<<"P/d mismatch t="<<t<<"\n";return 6;}
  if(big.str()!=msf(D)){cerr<<"independent bigint mismatch t="<<t<<"\n";return 7;}
  if(t==steps){cout<<"PASS m="<<m<<" n="<<n<<" steps="<<steps<<" final_digits="<<D.size()<<" fnv="<<hex<<fnv(D)<<dec<<"\n";return 0;}
  V nextD=add(D),nextP=pairs(D);D.swap(nextD);P.swap(nextP);
  // Independent arithmetic: reverse a base-10^9 integer's printed *canonical* digits,
  // parse the reversed decimal number back into 9-digit limbs, and add with limb carries.
  string s=big.str();reverse(s.begin(),s.end());Big9 backwards(s);big.add(backwards);
  w=bulk(w,t%2==0);v=bulk(v,t%2==0);
  if((t+1)%2000==0)cerr<<"X20 replay "<<t+1<<" digits="<<D.size()<<" FNV="<<hex<<fnv(D)<<dec<<"\n";
 }
}
