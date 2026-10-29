// W13 independent decimal STRING arithmetic vs low-first byte carry arithmetic.
#include <bits/stdc++.h>
using namespace std;using V=vector<unsigned char>;
V start(int h){V p;p.push_back(17);for(int i=1;i<h;i++)p.push_back(i%3==1?4:1);V w=p;for(int i=h-1;i>=0;i--)w.push_back(p[i]);V d(w.size());for(int i=0;i<h;i++){d[i]=min(9,int(w[i]));d[2*h-1-i]=w[i]-d[i];}assert(d.back());return d;}
V stepv(const V&d){V z;int c=0;for(size_t i=0;i<d.size();i++){int x=d[i]+d[d.size()-1-i]+c;z.push_back(x%10);c=x/10;}if(c)z.push_back(c);return z;}
string step_string(const string&s){string r(s.rbegin(),s.rend()),z;int c=0;for(int i=int(s.size())-1;i>=0;i--){int x=(s[i]-'0')+(r[i]-'0')+c;z+=char('0'+x%10);c=x/10;}if(c)z+=char('0'+c);reverse(z.begin(),z.end());return z;}
string stamp(const V&d){string s;for(auto it=d.rbegin();it!=d.rend();it++)s+=char('0'+*it);return s;}
string checksum(const V&d){uint64_t h=1469598103934665603ULL;for(int x:d){h^=x;h*=1099511628211ULL;}char buf[32];snprintf(buf,sizeof(buf),"%016llx",(unsigned long long)h);return buf;}
int main(int argc,char**argv){int h=argc>1?atoi(argv[1]):80,steps=argc>2?atoi(argv[2]):100000,L=argc>3?atoi(argv[3]):32;
 V a=start(h);string s=stamp(a);size_t overflow=0;long oddCount=0;long long duplicated=0,ambiguous=0;unordered_map<string,string> nextByState;vector<string> states;states.reserve(steps+1);int first_ambiguous=-1;
 for(int t=0;t<=steps;t++){
  if(s!=stamp(a))throw runtime_error("INDEPENDENT_FULL_DECIMAL_MISMATCH t="+to_string(t));
  if(equal(s.begin(),s.begin()+s.size()/2,s.rbegin()))throw runtime_error("PALINDROME t="+to_string(t));
  string sig;sig.reserve(L);int odd=0;
  for(int i=0;i<L;i++){unsigned v=a[i]+a[a.size()-1-i];sig+=char('A'+v);odd|=v&1;}
  if(!odd)throw runtime_error("ODD_PREFIX_FAIL t="+to_string(t));
  oddCount++;states.push_back(sig);
  if(t==steps)break;
  V b=stepv(a);string r=step_string(s);
  if(r.size()>s.size())overflow++;
  string sigNext;sigNext.reserve(L);
  for(int i=0;i<L;i++)sigNext+=char('A'+b[i]+b[b.size()-1-i]);
  auto it=nextByState.find(sig);
  if(it!=nextByState.end()){
    duplicated++;
    if(it->second!=sigNext){ambiguous++;if(first_ambiguous<0)first_ambiguous=t;}
  }else nextByState.emplace(sig,sigNext);
  a.swap(b);s.swap(r);
  if(t%20000==19999)cerr<<"independent progress "<<t+1<<" length="<<s.size()<<" distinct32="<<nextByState.size()<<"\n";
 }
 int shift=0;for(int p=1;p<=4096;p++){
  bool ok=true;for(int t=steps-10000;t<=steps;t++)if(states[t]!=states[t-p]){ok=false;break;}if(ok){shift=p;break;}
 }
 cout<<"W13_STRING100K_PASS h="<<h<<" steps="<<steps<<" source_digits="<<2*h<<" final_digits="<<a.size()<<" overflows="<<overflow
     <<" all_outer_odd="<<oddCount<<" distinct_prefix_states="<<nextByState.size()<<" repeated_states="<<duplicated
     <<" ambiguous_successors="<<ambiguous<<" first_ambiguous="<<first_ambiguous<<" observed_tail_period="<<shift
     <<" fnv64="<<checksum(a)<<"\n";
}
