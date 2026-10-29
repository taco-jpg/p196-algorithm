// Independent ordinary decimal-string arithmetic checker, not a template engine.
// Unlike bubble_family.cpp this stores an integer as MSB-first text and
// independently performs schoolbook addition against the reversed string.
#include <bits/stdc++.h>
using namespace std;
static string make_seed(int L){int m=L+130;uint32_t state=196;string low,high;low.reserve(m);high.reserve(m);
for(int i=0;i<m;i++){int p;if(i==64||i==L+65)p=11;else if(i>=65&&i<65+L)p=9;else{state^=state<<13;state^=state>>17;state^=state<<5;p=state%19;}if(i==0)p=12;
low.push_back(char('0'+max(0,p-9)));high.push_back(char('0'+min(9,p)));}
return high+string(low.rbegin(),low.rend());}
static string add_reverse(const string&s){int n=s.size(),c=0;string little;little.reserve(n+1);
for(int k=0;k<n;k++){int v=(s[n-1-k]-'0')+(s[k]-'0')+c;little.push_back(char('0'+v%10));c=v/10;}if(c)little.push_back('1');return string(little.rbegin(),little.rend());}
static uint64_t hash_dec(const string&s){uint64_t h=1469598103934665603ull;for(auto i=s.rbegin();i!=s.rend();++i){h^=(*i-'0');h*=1099511628211ull;}return h;}
static bool palindrome(const string&s){return equal(s.begin(),s.begin()+s.size()/2,s.rbegin());}
int main(int argc,char**argv){if(argc<3){cerr<<"usage: bubble_independent L STEPS [CHECKPOINT_EVERY=1000]\n";return 2;}int L=atoi(argv[1]),steps=atoi(argv[2]),E=argc>3?atoi(argv[3]):1000;if(L<2*steps+3){cerr<<"not enough shield\n";return 2;}string s=make_seed(L);
for(int t=0;t<=steps;t++){
 if(palindrome(s)){cerr<<"PALINDROME t="<<t<<"\n";return 3;}
 if(t>0){int a=65+t,b=65+L-1-t;for(int i=a;i<=b;i++){int q=s[s.size()-1-i]+s[i]-2*'0';if(q){cerr<<"SHIELD VIOLATION t="<<t<<" i="<<i<<" q="<<q<<"\n";return 4;}}}
 if(t%E==0||t==steps)cout<<"t="<<t<<" length="<<s.size()<<" hash="<<hex<<hash_dec(s)<<dec<<"\n";
 if(t==steps)break;
 s=add_reverse(s);
}
cout<<"INDEPENDENT PASS L="<<L<<" steps="<<steps<<" no_pal="<<steps+1<<" all_shields=PASS final_digits="<<s.size()<<"\n";
}
