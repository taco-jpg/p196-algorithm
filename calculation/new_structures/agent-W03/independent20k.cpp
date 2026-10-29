// Structurally independent LSD-first byte-digit oracle, full 20000-state palindrome check.
#include <bits/stdc++.h>
using namespace std;
using D=vector<unsigned char>;
D step(const D&a){int n=a.size(),c=0;D b;b.reserve(n+1);for(int i=0;i<n;i++){int v=a[i]+a[n-1-i]+c;b.push_back(v%10);c=v/10;}if(c)b.push_back(c);return b;}
bool pal(const D&a){for(int i=0,j=(int)a.size()-1;i<j;i++,j--)if(a[i]!=a[j])return false;return true;}
int main(int argc,char**argv){
 int q=argc>1?atoi(argv[1]):200,head=argc>2?atoi(argv[2]):88,tail=argc>3?atoi(argv[3]):26,steps=argc>4?atoi(argv[4]):20000;
 D a={(unsigned char)(tail%10),(unsigned char)(tail/10)};
 a.insert(a.end(),2*q,9);a.push_back(head%10);a.push_back(head/10);
 int gamma=0;
 for(int t=0;t<=steps;t++){
  if(pal(a)){cout<<"PAL at "<<t<<"\n";return 2;}
  if(t<steps){D b=step(a);gamma+=b.size()>a.size();a.swap(b);}
 }
 long long hash=0;for(int i=(int)a.size()-1;i>=0;i--)hash=(10*hash+a[i])%1000000007;
 cout<<"PASS "<<steps<<" steps, len="<<a.size()<<" gamma="<<gamma<<" hash="<<hash<<"\n";
}
