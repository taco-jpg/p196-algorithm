// Exact digit-array controls for the R18 phase-4 fixed-seam centre-independence audit.
// The all-q,k>=512 seed mismatch is inherited from S08/verify.py; this file checks actual decimal orbits.
// Build: g++ -O3 -std=c++17 r18_center_independence.cpp -o r18_center_independence
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <vector>
using namespace std;
using Dig=vector<int>;
const Dig B={10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4};
const Dig W={8,1,15,4,0,5,5,18,4};
const Dig J={17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2};
const Dig U={18,0,9};
Dig rep(const Dig& x,int n){Dig y;for(int i=0;i<n;i++)y.insert(y.end(),x.begin(),x.end());return y;}
Dig rev(Dig x){reverse(x.begin(),x.end());return x;}
Dig pairword(int q,int k,const Dig&C){Dig H=B;auto w=rep(W,q),u=rep(U,k);H.insert(H.end(),w.begin(),w.end());H.insert(H.end(),J.begin(),J.end());H.insert(H.end(),u.begin(),u.end());Dig P=H;P.insert(P.end(),C.begin(),C.end());auto rh=rev(H);P.insert(P.end(),rh.begin(),rh.end());return P;}
Dig source(const Dig&P){if(P.size()%2||!equal(P.begin(),P.end(),P.rbegin()))throw runtime_error("P not symmetric/even");int h=int(P.size()/2);Dig lo,hi;for(int i=0;i<h;i++){int x=max(P[i]-9,0);lo.push_back(x);hi.push_back(P[i]-x);}Dig d=lo;for(auto it=hi.rbegin();it!=hi.rend();++it)d.push_back(*it);for(size_t i=0;i<d.size();i++)if(d[i]+d[d.size()-1-i]!=P[i])throw runtime_error("source mismatch");return d;}
Dig pairdigits(const Dig&d){Dig p(d.size());for(size_t i=0;i<d.size();i++)p[i]=d[i]+d[d.size()-1-i];return p;}
tuple<Dig,int> step(const Dig&d){Dig out(d.size());int c=0;for(size_t i=0;i<d.size();i++){int z=d[i]+d[d.size()-1-i]+c;out[i]=z%10;c=z/10;}int g=c;if(c)out.push_back(c);return {out,g};}
bool pal(const Dig&d){return equal(d.begin(),d.end(),d.rbegin());}
int mismatch(const Dig&a,const Dig&b){for(size_t i=0;i<min(a.size(),b.size());i++)if(a[i]!=b[i])return int(i);return a.size()==b.size()?-1:int(min(a.size(),b.size()));}
int main(){vector<Dig> Cs={{1,1},{12,4,4,12},{2,8,12,12,8,2},{4,0,8,12,12,8,0,4}};long long count=0;for(const Dig&C:Cs)for(int q:{20,40,80,160})for(int k:{20,40,80,160}){Dig P=pairword(q,k,C),d=source(P);int palcount=0;for(int t=0;t<240;t++){if(pal(d))palcount++;auto [nd,g]=step(d);if(g!=(t%4==0?1:0))throw runtime_error("overflow clock mismatch");d=move(nd);if(t+1==120){int m=mismatch(pairdigits(d),pairword(q,k+5,C));if(m!=9*q+35||pairdigits(d)[m]!=9||pairword(q,k+5,C)[m]!=5)throw runtime_error("120-step mismatch differs");}if(t+1==240){auto actual=pairdigits(d),target=pairword(q,k+10,C);int m=mismatch(actual,target);if(m!=9*q+12||actual[m]!=6||target[m]!=5)throw runtime_error("240-step mismatch differs");}}if(palcount)throw runtime_error("palindrome encountered");count++;}cout<<"PASS R18 centre-independence digit-array controls: "<<count<<" cases; 16 independent (q,k) pairs x 4 even centres; 240 exact steps each.\n";}