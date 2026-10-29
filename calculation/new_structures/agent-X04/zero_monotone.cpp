// X04: exhaustive tests of the exact central-zero budget law.
#include <bits/stdc++.h>
using namespace std;using V=vector<uint8_t>;
int zv(const V&d){int n=d.size(),w=0;for(int i=(n-1)/2;i>=0;i--){if(d[i]+d[n-1-i])break;w+=(2*i==n-1?1:2);}return w;}
pair<V,int> next(const V&d){int n=d.size(),c=0;V v;v.reserve(n+1);for(int i=0;i<n;i++){int s=d[i]+d[n-1-i]+c;v.push_back(s%10);c=s/10;}if(c)v.push_back(c);return {v,c};}
int main(int argc,char**argv){uint64_t tested=0,eq0=0,eq1=0,g0=0,g1=0;string witness0,witness1;auto check=[&](const V&d){int z=zv(d);if(!z)return;auto [e,g]=next(d);int zz=zv(e);tested++;if(g)g1++;else g0++;int a=(int(d.size())-z)/2,c=0;for(int i=0;i<a;i++)c=(d[i]+d[d.size()-1-i]+c)/10;int expected=g?z-1:max(0,z-2*c);if(zz!=expected){cerr<<"EXACT_FAIL z="<<z<<" expected="<<expected<<" actual="<<zz<<" g="<<g<<" c="<<c<<"\n";exit(2);}if(zz+g>z){cerr<<"COUNTEREXAMPLE z="<<z<<" z'="<<zz<<" g="<<g<<" n="<<d.size()<<"\n";exit(1);}if(zz+g==z){string s;for(auto i=d.rbegin();i!=d.rend();i++)s+=char('0'+*i);if(g){eq1++;if(witness1.empty())witness1=s;}else{eq0++;if(witness0.empty())witness0=s;}}};
 for(int n=2,lim=100;n<=7;n++,lim*=10){for(int k=lim/10;k<lim;k++){V d(n);int x=k;for(int j=0;j<n;j++){d[j]=x%10;x/=10;}check(d);}}
 mt19937 rng(471104);for(int trial=0;trial<1000000;trial++){int n=8+rng()%192;V d(n);for(int i=0;i<n;i++)d[i]=rng()%10;d.back()=1+rng()%9;int width=1+rng()%min(100,n-2);int a=(n-width)/2;for(int i=a;i<n-a;i++)d[i]=0;check(d);}
 cout<<"PASS checked="<<tested<<" gamma0="<<g0<<" gamma1="<<g1<<" equality_gamma0="<<eq0<<" equality_gamma1="<<eq1<<" eg0="<<witness0<<" eg1="<<witness1<<"\n";
}
