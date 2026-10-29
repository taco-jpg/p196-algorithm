// Independent MSB-first decimal-string replay of two N_L seeds.
// Full literal reverse-and-add, every-iterate palindrome testing and exterior clocks.
#include <bits/stdc++.h>
using namespace std;
static string seed(int L){uint32_t x=196;int m=L+130;string hi,lo;hi.reserve(m);lo.reserve(m);for(int i=0;i<m;i++){int p;if(i==64||i==L+65)p=11;else if(i>=65&&i<65+L)p=9;else{x^=x<<13;x^=x>>17;x^=x<<5;p=x%19;}if(i==0)p=12;hi+=char('0'+min(9,p));lo+=char('0'+max(0,p-9));}return hi+string(lo.rbegin(),lo.rend());}
static string addrev(const string&s){int n=s.size(),c=0;string r; r.reserve(n+1);for(int i=n-1;i>=0;i--){int v=(s[i]-'0')+(s[n-1-i]-'0')+c;r+=char('0'+v%10);c=v/10;}if(c)r+='1';reverse(r.begin(),r.end());return r;}
static bool same_outer(const string&a,const string&b,int K){for(int i=0;i<K;i++){int x=a[i]+a[a.size()-1-i],y=b[i]+b[b.size()-1-i];if(x!=y)return false;}return true;}
int main(int argc,char**argv){int L1=argc>1?atoi(argv[1]):2000,L2=argc>2?atoi(argv[2]):45000,T=argc>3?atoi(argv[3]):70000,K=argc>4?atoi(argv[4]):64;string a=seed(L1),b=seed(L2);int prevA=0,prevB=0;int diffP=-1,diffG=-1,diffP1=-1,diffP1024=-1;for(int t=0;t<=T;t++){
  if(!same_outer(a,b,K)&&diffP==-1)diffP=t;
  if(!same_outer(a,b,1)&&diffP1==-1)diffP1=t;
  if(!same_outer(a,b,1024)&&diffP1024==-1)diffP1024=t;
  if(prevA!=prevB&&diffG==-1)diffG=t;
  if(equal(a.begin(),a.begin()+a.size()/2,a.rbegin())||equal(b.begin(),b.begin()+b.size()/2,b.rbegin())){cerr<<"PAL step "<<t<<"\n";return 3;}
  if(diffP!=-1&&diffG!=-1&&diffP1!=-1&&diffP1024!=-1){cout<<"INDEPENDENT L="<<L1<<" comparator="<<L2<<" outerK="<<K<<" diffP="<<diffP<<" diffP1="<<diffP1<<" diffP1024="<<diffP1024<<" diffGamma="<<diffG<<" all_nonpal_checked_through="<<t<<"\n";return 0;}
  if(t==T)break;
  string an=addrev(a),bn=addrev(b);prevA=an.size()>a.size();prevB=bn.size()>b.size();a.swap(an);b.swap(bn);
}
cout<<"INDEPENDENT L="<<L1<<" comparator="<<L2<<" diffP="<<diffP<<" diffP1="<<diffP1<<" diffP1024="<<diffP1024<<" diffGamma="<<diffG<<" checked_through="<<T<<"\n";return (diffP<0||diffG<0)?1:0;
}
