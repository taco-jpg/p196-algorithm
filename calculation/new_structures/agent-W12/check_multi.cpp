// W12: four six-digit decimal centre-pumped finite-horizon orbit families.
// C++17. Reproduce each: ./w12multi 2500 20000 428571 (etc.)
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
string step(const string&s){
 int n=s.size(),c=0;string r(n+1,'0');
 for(int i=0;i<n;i++){int v=s[i]-'0'+s[n-i-1]-'0'+c;r[n-i]='0'+v%10;c=v/10;}
 r[0]='0'+c;if(!c)r.erase(r.begin());return r;
}
vector<int> parse(const string&s){
 vector<int>r;
 for(int j=s.size();j>0;j-=4){
  int a=0;for(int k=max(0,j-4);k<j;k++)a=a*10+s[k]-'0';
  r.push_back(a);
 }
 return r;
}
string step_limbs(const string&s){
 string sr(s.rbegin(),s.rend());
 auto a=parse(s),b=parse(sr);
 vector<int>c(max(a.size(),b.size())+1);
 int carry=0;
 for(size_t i=0;i+1<c.size();i++){
  int z=(i<a.size()?a[i]:0)+(i<b.size()?b[i]:0)+carry;
  c[i]=z%10000;carry=z/10000;
 }
 c.back()=carry;
 while(c.size()>1&&!c.back())c.pop_back();
 string r=to_string(c.back());char x[6];
 for(int i=c.size()-2;i>=0;i--){
  snprintf(x,sizeof(x),"%04d",c[i]);r+=x;
 }
 return r;
}
uint64_t hash64(const string&s){
 uint64_t h=1469598103934665603ull;
 for(unsigned char c:s){h^=c;h*=1099511628211ull;}
 return h;
}
int period(const string&s,bool pair){
 int n=s.size(),l=n/2-64,r=n/2+64;
 auto f=[&](int j)->int{
  return pair?s[j]-'0'+s[n-1-j]-'0':s[j]-'0';
 };
 for(int p=1;p<=6;p++){
  bool good=true;
  for(int j=l+p;j<r;j++)if(f(j)!=f(j-p)){good=false;break;}
  if(good)return p;
 }
 return 0;
}
string seed(string w,int q){
 string s="12";for(int i=0;i<q;i++)s+=w;return s+"34";
}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):2500,steps=argc>2?atoi(argv[2]):20000;
 if(q<20||steps<0)return 1;
 for(const string w:{"428571","461538","561726","273438"}){
  if(argc>3 && w!=argv[3])continue;
  string a=seed(w,q),b=seed(w,q+1);
  int gamma[2]={},max_match=0;
  map<int,int> pp,dd;
  for(int t=0;t<=steps;t++){
   int n=a.size(),c=n/2;
   if(b.size()!=a.size()+6
      ||a.compare(0,c,b,0,c)
      ||a.compare(c,n-c,b,c+6,n-c)){
    cerr<<"PUMP_FAIL word="<<w<<" t="<<t<<"\n";return 2;
   }
   int d=period(a,false),p=period(a,true);
   if(!d||!p){
    cerr<<"PERIOD_FAIL word="<<w<<" t="<<t<<"\n";return 3;
   }
   dd[d]++;pp[p]++;
   int mm=0;
   while(mm<min(c,n-c)&&a[mm]==a[n-1-mm])mm++;
   if(mm>=min(c,n-c)){
    cerr<<"OUTER_NONPAL_FAIL word="<<w<<" t="<<t<<"\n";return 4;
   }
   max_match=max(max_match,mm);
   if(t==steps){
    cout<<"PASS word="<<w<<" q_ge="<<q<<" steps="<<steps
        <<" len="<<n<<" gamma0="<<gamma[0]<<" gamma1="<<gamma[1]
        <<" max_outer_match="<<max_match
        <<" inserted="<<b.substr(c,6)
        <<" final_fnv64="<<hex<<hash64(a)<<dec<<" periods=";
    for(auto [p,k]:dd)cout<<p<<":"<<k<<",";
    cout<<" pairperiods=";
    for(auto [p,k]:pp)cout<<p<<":"<<k<<",";
    cout<<"\n";break;
   }
   string na=step(a),nb=step(b);
   if(na!=step_limbs(a)||(t%1000==0&&nb!=step_limbs(b))){
    cerr<<"INDEPENDENT_ARITH_FAIL word="<<w<<" t="<<t<<"\n";return 5;
   }
   gamma[na.size()>a.size()]++;
   a.swap(na);b.swap(nb);
  }
 }
}
