// Independent actual decimal digit-list reverse-and-add; no pairword transition used.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include "phase.h"
using namespace std;
static vector<unsigned char> construct(int copies, int centre_kind) {
    vector<int> low;
    low.insert(low.end(),B0.begin(),B0.end());
    for(int j=0;j<copies;j++)low.insert(low.end(),W0.begin(),W0.end());
    // 0: empty; 1: [0,18,18,0]; 2: [2,4,4,2]; 3: [9,6,6,9].
    if(centre_kind==1){low.push_back(0);low.push_back(18);}
    else if(centre_kind==2){low.push_back(2);low.push_back(4);}
    else if(centre_kind==3){low.push_back(9);low.push_back(6);}
    else if(centre_kind!=0){cerr<<"bad centre_kind\n";exit(2);}
    vector<unsigned char> digits(2*low.size());
    for(size_t i=0;i<low.size();i++){
        int p=low[i],a=p/2;
        digits[i]=(unsigned char)a;
        digits[digits.size()-1-i]=(unsigned char)(p-a);
    }
    if(digits.back()==0){cerr<<"leading zero\n";exit(1);}
    return digits;
}
static int pal(const vector<unsigned char>& d) {
    for(size_t i=0;i<d.size()/2;i++)if(d[i]!=d[d.size()-1-i])return 0;
    return 1;
}
static void reverse_add(vector<unsigned char>& d) {
    vector<unsigned char> n(d.size()+1);
    int carry=0;
    for(size_t i=0,j=d.size()-1;i<d.size();i++,j--){
        int v=d[i]+d[j]+carry;
        n[i]=(unsigned char)(v%10);carry=v/10;
    }
    if(carry)n[d.size()]=(unsigned char)carry;
    else n.pop_back();
    d.swap(n);
}
static int matching(const vector<unsigned char>& d,int t) {
    size_t half=d.size()/2,matched=0;
    for(;matched<half;matched++){
        unsigned int p=d[matched]+d[d.size()-1-matched];
        int expected=(matched<39)?PHASE_B[t%8][matched]:PHASE_W[t%8][(matched-39)%20];
        if(p!=(unsigned)expected)break;
    }
    return (int)matched;
}
static uint64_t checksum(const vector<unsigned char>& d) {
    uint64_t h=1469598103934665603ull;
    for(auto c:d){h^=c;h*=1099511628211ull;}
    return h;
}
int main(int argc,char**argv) {
    const int copies=argc>1?atoi(argv[1]):300,
        steps=argc>2?atoi(argv[2]):20000,
        centre_kind=argc>3?atoi(argv[3]):0;
    if(copies<1||steps<1)return 2;
    auto d=construct(copies,centre_kind);
    int minmatch=2147483647,maxmatch=0,firstfailure=-1,minperiods=2147483647;
    array<int,8> gammas{};
    for(int t=0;t<=steps;t++){
        if(pal(d)){cout<<"PALINDROME at t="<<t<<" digits="<<d.size()<<"\n";return 3;}
        int m=matching(d,t),r=max(0,(m-39)/20);
        minmatch=min(minmatch,m);maxmatch=max(maxmatch,m);minperiods=min(minperiods,r);
        if(firstfailure<0&&m<59)firstfailure=t;
        if(t==0||t==1||t==100||t==1000||t==5000||t==10000||t==15000||t==19999||t==steps)
            cout<<"step="<<t<<" digits="<<d.size()<<" matched="<<m
                <<" full_band_blocks="<<r<<" fnv64="<<hex<<checksum(d)<<dec<<"\n";
        if(t<steps){auto oldlen=d.size();reverse_add(d);gammas[t%8]+=(int)(d.size()-oldlen);}
    }
    cout<<"PASS base10 copies="<<copies<<" steps="<<steps<<" centre_kind="<<centre_kind
        <<" no palindrome; min_match="<<minmatch<<" min_full_band_blocks="<<minperiods
        <<" first_band_failure_step="<<firstfailure<<" max_match="<<maxmatch<<"\n";
    cout<<"gamma_by_tmod8_total=";
    for(int g:gammas)cout<<g<<' ';
    cout<<"\n";
    return firstfailure==-1?0:4;
}
