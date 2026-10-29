// Agent N12: integer-in-base-10 digit-vector replay. No GMP or decimal text arithmetic.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using Dig=vector<uint8_t>;
static constexpr uint64_t FNV_OFFSET=14695981039346656037ULL;
static constexpr uint64_t FNV_PRIME=1099511628211ULL;
Dig make_seed(const string& L,int gap,const string& R){
    if(L.empty()||R.empty()||L[0]=='0'||R.back()=='0'||gap<0)abort();
    string s=L+string(gap,'0')+R; Dig d;d.reserve(s.size());
    for(auto it=s.rbegin();it!=s.rend();++it){if(*it<'0'||*it>'9')abort(); d.push_back(*it-'0');}
    return d;
}
struct Info {int w,z,mismatch;uint64_t hash;string first;};
Info info(const Dig& d){
    const int n=d.size(); Info v={0,0,-1,FNV_OFFSET,""};
    for(int i=0;i<n/2;i++){
        if(d[i]||d[n-1-i])v.w=i+1;
        if(v.mismatch==-1 && d[i]!=d[n-1-i])v.mismatch=i;
    }
    v.z=n-2*v.w;
    for(int i=0;i<n;i++)v.hash=(v.hash^d[i])*FNV_PRIME;
    for(int i=0;i<min(v.w,16);i++){
        int x=d[i]+d[n-1-i];v.first+=(x<10?"0":"")+to_string(x);
    }
    return v;
}
void step(Dig& d){
    const int n=d.size();int carry=0;Dig out(n+1);
    for(int i=0;i<n;i++){
        int z=d[i]+d[n-1-i]+carry;
        out[i]=z%10;carry=z/10;
    }
    if(carry)out[n]=carry;else out.pop_back();
    d.swap(out);
}
int main(int argc,char** argv){
    if(argc!=7){cerr<<"Usage: seed_cones LEFT GAP RIGHT STEPS MIN_ZERO TRACE.csv\n";return 2;}
    string L=argv[1],R=argv[3];int gap=atoi(argv[2]),steps=atoi(argv[4]),floor=atoi(argv[5]);
    ofstream f(argv[6]);if(!f){cerr<<"TRACE_OPEN_FAILED\n";return 2;}
    auto d=make_seed(L,gap,R);
    f<<"t,length,width,central_zeros,mismatch,fnv64,first16pairs\n";
    int minz=1e9,maxw=0,overflows=0;
    for(int t=0;t<=steps;t++){
        auto x=info(d);minz=min(minz,x.z);maxw=max(maxw,x.w);
        if(x.mismatch<0||x.z<floor){cerr<<"FAIL t="<<t<<" mismatch="<<x.mismatch<<" z="<<x.z<<"\n";return 1;}
        f<<t<<','<<d.size()<<','<<x.w<<','<<x.z<<','<<x.mismatch<<','<<hex<<x.hash<<dec<<','<<x.first<<'\n';
        if(t<steps){int old=d.size();step(d);overflows+=(int)d.size()-old;}
    }
    cout<<"PASS seed="<<L<<"+0^"<<gap<<"+"<<R<<" steps="<<steps<<" min_center_zero="<<minz<<" max_halfwidth="<<maxw<<" final_length="<<d.size()<<" total_overflow="<<overflows<<"\n";
}
