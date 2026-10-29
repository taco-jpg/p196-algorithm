// W04 independent ordinary decimal-digit mask coalescence and long replay.
// No pairword normalization is used as the update oracle: actual digit addition.
#include <bits/stdc++.h>
using namespace std;
using D=vector<uint8_t>;
static D initial(int m,int n,int mode){
 vector<int> h{10};uint32_t state=47404;
 for(int i=0;i<m;i++){
   int bit=0;
   if(mode==1)bit=1;
   else if(mode==2)bit=i&1;
   else if(mode==3){state^=state<<13;state^=state>>17;state^=state<<5;bit=(state&1);}
   h.push_back(8+9*bit);
 }
 h.push_back(5);h.push_back(11);h.insert(h.end(),n,16);h.push_back(8);
 D d(2*h.size());for(int i=0;i<(int)h.size();i++){int upper=min(9,h[i]);d[i]=h[i]-upper;d[d.size()-1-i]=upper;}
 if(!d.back())throw runtime_error("noncanonical seed");
 return d;
}
static D direct_add(const D&d){
 int q=d.size();D a; a.reserve(q+1);int carry=0;
 for(int i=0;i<q;i++){
   int s=int(d[i])+int(d[q-1-i])+carry;a.push_back(uint8_t(s%10));carry=s/10;
 }
 if(carry)a.push_back(uint8_t(carry));
 return a;
}
static bool pal(const D&d){for(int i=0;i<(int)d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return false;return true;}
static vector<int> folded_pair(const D&d){vector<int> p((d.size()+1)/2);for(int i=0;i<(int)p.size();i++)p[i]=int(d[i])+int(d[d.size()-1-i]);return p;}
static uint64_t fnv(const D&d){uint64_t h=1469598103934665603ull;for(auto it=d.rbegin();it!=d.rend();++it){h^=uint64_t('0'+*it);h*=1099511628211ull;}return h;}
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage M N STEPS\n";return 1;}int m=atoi(argv[1]),n=atoi(argv[2]),steps=atoi(argv[3]);
 if(m<1||n<1||steps<2)return 2;
 array<D,4> v;for(int i=0;i<4;i++){v[i]=initial(m,n,i);if(pal(v[i]))return 3;}
 for(int i=0;i<4;i++)for(int j=0;j<i;j++)if(v[i]==v[j])return 4;
 for(auto&x:v)x=direct_add(x);
 for(int i=0;i<4;i++)for(int j=0;j<i;j++)if(v[i]==v[j])return 9;
 for(int i=1;i<4;i++)if(folded_pair(v[i])!=folded_pair(v[0]))return 5;
 for(auto&x:v){if(pal(x))return 6;x=direct_add(x);}
 for(int i=1;i<4;i++)if(v[i]!=v[0])return 7;
 cout<<"FOUR_MASKS_ALL_DISTINCT_AT_T0_AND_T1_COMMON_EXACT_INTEGER_AT_T2 digits="<<v[0].size()<<" fnv="<<hex<<fnv(v[0])<<dec<<"\n"<<flush;
 // From t=2 onward the orbit literally coincides with the no-mask integer.
 // Independently replay a random-mask descendant through all 20,000 steps.
 D d=move(v[3]);for(int t=2;t<=steps;t++){
   if(pal(d)){cerr<<"PAL "<<t<<"\n";return 8;}
   if(t%5000==0 ||t==steps) cout<<"MASKED_CHECKPOINT t="<<t<<" digits="<<d.size()<<" fnv="<<hex<<fnv(d)<<dec<<"\n"<<flush;
   if(t<steps)d=direct_add(d);
 }
 cout<<"MASKED_ORDINARY_DECIMAL_20000_PASS m="<<m<<" n="<<n<<" steps="<<steps<<"\n";
}
