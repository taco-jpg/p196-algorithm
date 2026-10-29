// Exact affine-sheet *overlap-capacity* verifier: permit central sheet collisions
// provided the total coefficient at every occupied exponent is <10.
// Compile: g++ -std=c++17 -O3 overlap_capacity.cpp -o overlap_capacity
#define main four_sheet_engine_entry
#include "four_sheet_fast.cpp"
#undef main
#include <stdexcept>
#include <string>

static constexpr int D=4;
// Every pair of distinct sheets is strictly separated except the central pair (1,2),
// whose supports may overlap when their aggregated digit sum is at most 9.
// Their affine bases are (0, q, q+D, 2*q+D).
static int max_outer_Q(const S&x){
 static constexpr int slope[4]={0,1,1,2};
 static constexpr int bias[4]={0,0,D,D};
 int Q=1;
 for(int i=0;i<4;i++)if(!x[i].empty()){
   if(slope[i]==0){
     if(bias[i]+x[i].start<0)throw runtime_error("fixed packet has negative exponent");
   }else Q=max(Q,ceil_div(-bias[i]-x[i].start,slope[i]));
   for(int j=i+1;j<4;j++)if(!x[j].empty() && !(i==1&&j==2)){
     // Enforce end_i(q) < start_j(q) for all q>=Q.
     int m=slope[j]-slope[i];
     if(m<=0)throw runtime_error("nonpositive exterior slope gap");
     Q=max(Q,ceil_div(bias[i]+x[i].end()-bias[j]-x[j].start+1,m));
   }
 }
 return Q;
}
struct Capacity{int maxdigit=0,overlaps=0,overload=0;};
static Capacity centre_capacity(const S&x){
 Capacity p;
 // Only sheets 1 and 2 can collide after Q>=max_outer_Q.
 int lo=INT32_MAX,hi=INT32_MIN;
 if(!x[1].empty()){lo=min(lo,x[1].start);hi=max(hi,x[1].end());}
 if(!x[2].empty()){lo=min(lo,D+x[2].start);hi=max(hi,D+x[2].end());}
 if(lo==INT32_MAX)return p;
 vector<int> sum(hi-lo+1,0),count(hi-lo+1,0);
 for(int i: {1,2})if(!x[i].empty())for(int j=0;j<x[i].length();j++)if(x[i].d[j]){
  int position=(i==1?0:D)+x[i].start+j-lo;
  sum[position]+=x[i].d[j];count[position]++;
 }
 for(size_t i=0;i<sum.size();i++){
  p.maxdigit=max(p.maxdigit,sum[i]);
  if(count[i]>1)p.overlaps++;
  if(sum[i]>=10)p.overload++;
 }
 return p;
}
static bool outer_witness(const S&x){
 if(x[3].empty())throw runtime_error("missing leading packet");
 int top=x[3].end();
 const auto&a=x[0],&b=x[3];
 for(int j=0;j<a.length();j++){
  int target=top-a.start-j-b.start;
  int rhs=(target>=0&&target<b.length())?b.d[target]:0;
  if(rhs!=a.d[j])return true;
 }
 for(int j=0;j<b.length();j++){
  int target=top-b.start-j-a.start;
  int lhs=(target>=0&&target<a.length())?a.d[target]:0;
  if(lhs!=b.d[j])return true;
 }
 return false;
}
static string complete_integer(const S&x,int q){
 int base[]={0,q,q+D,2*q+D};
 int high=base[3]+x[3].end();
 vector<int> num(high+1,0);
 for(int k=0;k<4;k++)for(int j=0;j<x[k].length();j++){
   int ex=base[k]+x[k].start+j;
   if(ex<0||ex>high)throw runtime_error("wrong absolute exponent");
   num[ex]+=x[k].d[j];
 }
 string out(high+1,'0');
 for(int i=0;i<=high;i++){
   if(num[i]>=10)throw runtime_error("inter-sheet aggregate needs carries");
   out[high-i]=(char)('0'+num[i]);
 }
 if(out[0]=='0')throw runtime_error("leading zero");
 return out;
}
static string arithmetic_step(const string&s){
 int n=s.length(),carry=0;string out(n,'0');
 for(int i=n-1;i>=0;i--){
  int v=(s[i]-'0')+(s[n-1-i]-'0')+carry;
  out[i]=(char)('0'+v%10);carry=v/10;
 }
 if(carry)out.insert(out.begin(),'0'+carry);
 return out;
}
int main(){
 S state;state[0]={0,{5,7}};state[1]={0,{8,7}};state[2]={};state[3]={0,{8,8}};
 const int safeT=13,badT=14;
 int Q=1;vector<S> states;vector<int> bounds;
 cout<<"t,Q,centre_overlap_sites,centre_max_aggregate,centre_overload_sites,outer_nonpal_witness\n";
 for(int t=0;t<=badT;t++){
  Q=max(Q,max_outer_Q(state));
  auto c=centre_capacity(state);bool witness=outer_witness(state);
  cout<<t<<","<<Q<<","<<c.overlaps<<","<<c.maxdigit<<","<<c.overload<<","<<witness<<"\n";
  if(t<=safeT){
    if(c.overload||!witness)throw runtime_error("safe-stage check failed");
    states.push_back(state);bounds.push_back(Q);
  }else if(c.overload==0)throw runtime_error("unsafe-stage mutation was not rejected");
  if(t<badT)state=evolve(state);
 }
 int safeQ=*max_element(bounds.begin(),bounds.end());
 cout<<"UNIVERSAL_Q_MIN="<<safeQ<<"\n";
 for(int q: {safeQ,safeQ+1,100,600}){
  if(q<safeQ)continue;
  string actual=complete_integer(states[0],q);
  for(int t=0;t<=safeT;t++){
     auto pred=complete_integer(states[t],q);
     if(actual!=pred)throw runtime_error("full integer mismatch at t="+to_string(t));
     if(t<safeT)actual=arithmetic_step(actual);
  }
  cout<<"INTEGER_CONTROL q="<<q<<" states="<<safeT+1<<" full_matches="<<safeT+1<<"\n";
 }
 // Deliberate bad-stage control: the next formal sheet state violates capacity,
 // so no cyclic proof may use the transparent-sheet checker across t=14.
 if(centre_capacity(state).overload==0)throw runtime_error("capacity mutation control incorrectly accepted");
 cout<<"ALL OVERLAP-CAPACITY CHECKS PASSED\n";
}
