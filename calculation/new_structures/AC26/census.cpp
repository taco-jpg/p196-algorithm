// Phase-5 120-step endpoint-only genuine decimal digit-array census.
// Build: c++ -std=c++17 -O3 -o census census.cpp
// Run: ./census 100 0   (6000 distinct J/U/C; the first 100 base-19 J codes)
// This is a finite diagnostic, NOT an all-time Lychrel certificate.
#include <vector>
#include <iostream>
#include <map>
#include <algorithm>
#include <cstdlib>
using V=std::vector<int>;
const int B[]={1,5,11,12,9,10,8,3,11,6,14,16,10,0,14,12,9,8,7,2,8,12,5,17,14,8,9,13,14,17,14,12,15,13};
const int W[]={12,9,7,10,4,5,10,14,13};
V templ(const V&J,const V&U,const V&C,int k){
    V h(std::begin(B),std::end(B));
    for(int a=0;a<14;a++)h.insert(h.end(),std::begin(W),std::end(W));
    h.insert(h.end(),J.begin(),J.end());
    for(int a=0;a<k;a++)h.insert(h.end(),U.begin(),U.end());
    V p=h;p.insert(p.end(),C.begin(),C.end());
    p.insert(p.end(),h.rbegin(),h.rend());return p;
}
V init(const V&p){
    V d(p.size());
    for(size_t i=0;i<p.size()/2;i++){
        int hi=std::min(9,p[i]);d[i]=p[i]-hi;d[p.size()-1-i]=hi;
    }
    if(p.size()%2)d[p.size()/2]=p[p.size()/2]/2;
    if(d.back()==0)throw "noncanonical";
    return d;
}
int step(V&d,V&scratch){
    scratch.clear();int carry=0,n=int(d.size());
    for(int i=0;i<n;i++){
        int sum=d[i]+d[n-1-i]+carry;
        scratch.push_back(sum%10);carry=sum/10;
    }
    if(carry)scratch.push_back(carry);
    d.swap(scratch);
    return carry;
}
V decode(int code){
    V j(5);
    for(int i=0;i<5;i++){j[i]=code%19;code/=19;}
    return j;
}
int main(int argc,char**argv){
    int limit=argc>1?std::atoi(argv[1]):100;
    int start=argc>2?std::atoi(argv[2]):0;
    if(limit<1||start<0||start+limit>2476099)return 2;
    long long total=0,gamma_bad=0,returns=0,early=0;
    std::map<int,long long> hist;
    V scratch;
    for(int a=0;a<=18;a+=2)for(int r=0;r<3;r++){
        V b={9,a,18-a},U={b[r],b[(r+1)%3],b[(r+2)%3]};
        for(V C:{V{4,4},V{4,14,4}})
        for(int code=start;code<start+limit;code++){
            V J=decode(code),want=templ(J,U,C,105),d=init(templ(J,U,C,100));
            int growth=0;
            for(int t=0;t<120;t++)growth+=step(d,scratch);
            if(growth!=30)gamma_bad++;
            int i=0;
            while(i<int(d.size())&&i<int(want.size())&&
                  d[i]+d[d.size()-1-i]==want[i])i++;
            if(i==int(want.size())&&d.size()==want.size())returns++;
            if(i<70)early++;
            hist[i]++;total++;
        }
    }
    std::cout<<"tested="<<total<<" gamma_bad="<<gamma_bad
             <<" returns="<<returns<<" first_less_70="<<early<<"\n";
    for(auto [i,n]:hist)std::cout<<i<<":"<<n<<" ";
    std::cout<<"\n";
}
