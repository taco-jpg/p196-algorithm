// Full decimal digit-vector checker for W02 two-packet first nonlinear events.
// Deliberately uses no local carry maps or pairword transition tables.
#include <bits/stdc++.h>
using namespace std;
using Digits=vector<unsigned char>;
static const int B[34]={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11};
static const int W[9]={1,10,8,5,9,16,0,9,11};
static const int A[11]={6,1,0,1,11,14,10,6,11,16,1};
static const int K[11]={16,0,9,11,1,10,8,5,14,18,0};
Digits initial(int gap,int type,int n=20000){
    vector<int>pair(n);
    for(int i=0;i<n/2;i++)pair[i]=pair[n-1-i]=(i<34?B[i]:W[(i-34)%9]);
    auto put=[&](int x,const int*p){for(int j=0;j<11;j++)pair[x+j]=pair[n-1-x-j]=p[j];};
    if(type&1)put(1200,A);
    if(type&2)put(1200+gap,K);
    Digits d(n);
    for(int i=0;i<n/2;i++){int h=min(9,pair[i]);d[i]=pair[i]-h;d[n-1-i]=h;}
    if(!d.back())throw runtime_error("leading zero");return d;
}
void update(Digits&d){Digits orig=d;int c=0;int n=orig.size();for(int i=0;i<n;i++){int v=orig[i]+orig[n-1-i]+c;d[i]=v%10;c=v/10;}if(c)d.push_back(c);}
bool palindrome(const Digits&d){for(int i=0;i<(int)d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return false;return true;}
pair<int,int> firstCollision(int gap,int limit){vector<Digits>d;for(int i=0;i<4;i++)d.push_back(initial(gap,i));for(int t=0;t<=limit;t++){
    int n=d[0].size(),idx=-1,cnt=0;for(const auto&x:d){if(x.size()!=d[0].size()||palindrome(x))throw runtime_error("length divergence/palindrome");}
    for(int i=0;i<n/2;i++){
        int q[4];for(int j=0;j<4;j++)q[j]=d[j][i]+d[j][n-1-i];
        int diff=q[3]-q[1]-q[2]+q[0];
        if(diff){if(idx<0)idx=i;cnt++;}
    }
    if(idx>=0)return {t,idx};
    if(t<limit)for(auto&x:d)update(x);
}
return {-1,-1};}
int main(){
    struct Case{int gap,t,index;};
    const vector<Case> cases={{189,339,1341},{504,840,1561},{558,931,1600},{882,1448,1825},{936,1538,1863}};
    for(auto c:cases){auto actual=firstCollision(c.gap,c.t);if(actual.first!=c.t||actual.second!=c.index){cerr<<"collision mismatch gap="<<c.gap<<" actual="<<actual.first<<","<<actual.second<<" expected="<<c.t<<","<<c.index<<"\n";return 1;}
       cout<<"DECIMAL_COLLISION_PASS gap="<<c.gap<<" t="<<actual.first<<" x="<<actual.second<<"\n";}
}
