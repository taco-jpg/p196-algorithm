// Agent N02: independent 20,000-step GMP big-integer replay, jointly checked
// by a separately implemented schoolbook digit-list arithmetic engine.
// Base-10 p8/m20 rooted lattice pulse, q=228 bulk pumps.
// Compile: g++ -O3 -std=c++17 -Wall -Wextra glider_replay.cpp -lgmpxx -lgmp -o /tmp/n02_replay
#include <gmpxx.h>
#include <array>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
using namespace std;
static const int path[39][8] = {
{17,8,17,8,17,8,17,8},{5,13,6,14,8,16,13,12},{0,5,11,8,17,16,14,9},
{1,1,2,4,8,16,14,10},{13,5,10,3,6,14,10,6},{4,8,16,8,17,14,10,2},
{14,9,18,16,13,12,6,7},{12,8,16,16,14,9,0,6},{9,2,5,12,6,11,4,4},
{8,18,17,13,8,14,9,14},{15,14,10,9,0,8,17,7},{16,13,8,9,0,0,0,8},
{17,15,12,11,4,4,8,8},{13,12,6,9,0,4,8,16},{17,12,5,11,4,4,9,18},
{9,7,16,12,5,9,9,9},{1,11,2,9,9,15,10,0},{4,5,11,4,10,0,1,2},
{4,8,16,9,9,0,1,2},{11,6,13,11,2,12,4,5},{8,10,1,5,11,4,9,14},
{16,15,11,3,6,8,17,7},{0,7,16,9,18,15,11,10},{9,10,0,7,15,15,11,4},
{14,4,9,10,0,6,14,7},{11,7,14,4,9,10,0,5},{9,2,4,9,18,8,18,9},
{11,2,4,8,17,17,15,15},{6,8,17,12,4,12,6,12},{13,10,1,9,9,14,9,16},
{18,13,7,8,18,8,18,8},{9,8,18,16,12,12,5,14},{4,14,9,8,18,12,6,11},
{7,11,4,14,8,17,16,13},{17,15,12,7,15,14,10,8},{15,14,9,3,6,12,6,7},
{9,5,12,3,7,13,8,14},{7,17,15,9,9,16,14,13},{13,11,4,10,1,10,1,6}};
static const int cyc[20][8]={
{17,12,6,10,2,3,7,8},{3,11,3,9,0,2,4,11},{1,4,9,13,7,7,15,10},
{13,5,11,1,3,10,0,6},{17,12,5,7,14,8,17,8},{11,10,1,6,12,8,16,15},
{14,7,15,7,15,9,18,16},{3,8,17,14,9,5,11,11},{18,12,5,13,7,17,15,8},
{1,10,1,6,13,11,4,10},{2,3,7,8,17,12,6,10},{0,2,4,11,3,11,3,9},
{7,7,15,10,1,4,9,13},{3,10,0,6,13,5,11,1},{14,8,17,8,17,12,5,7},
{12,8,16,15,11,10,1,6},{15,9,18,16,14,7,15,7},{9,5,11,11,3,8,17,14},
{7,17,15,8,18,12,5,13},{13,11,4,10,1,10,1,6}};

using Digit=unsigned char;
static vector<Digit> ordinary_step(const vector<Digit>& a){
    vector<Digit> result;result.reserve(a.size()+1);int carry=0;
    for(size_t i=0;i<a.size();++i){
        int z=int(a[i])+int(a[a.size()-1-i])+carry;
        result.push_back(Digit(z%10));carry=z/10;
    }
    if(carry)result.push_back(Digit(carry));
    return result;
}

static string to_str(const vector<Digit>& a){
    string s;s.reserve(a.size());
    for(auto it=a.rbegin();it!=a.rend();++it)s.push_back(char('0'+*it));
    return s;
}

static mpz_class reverse_gmp(const mpz_class& n){
    const string s=n.get_str(10);
    string r(s.rbegin(),s.rend());
    // mpz_set_str accepts leading zero; set via decimal constructor.
    return mpz_class(r,10);
}

int main(int argc,char**argv){
    int q=228,steps=20000;
    if(argc>=2)q=stoi(argv[1]);
    if(argc>=3)steps=stoi(argv[2]);
    if(q<1||q>10000||steps<1)throw runtime_error("bad arguments");
    vector<int> half;half.reserve(39+20*q);
    for(int j=0;j<39;j++)half.push_back(path[j][0]);
    for(int k=0;k<q;k++)for(int j=0;j<20;j++)half.push_back(cyc[j][0]);
    vector<Digit> d(2*half.size());
    for(size_t i=0;i<half.size();++i){
        int lo=min(half[i],9),hi=half[i]-lo;
        d[i]=Digit(lo);d[d.size()-1-i]=Digit(hi);
    }
    mpz_class n(to_str(d),10);
    assert(n>0&&d.back()>0);
    uint64_t checksum=1469598103934665603ULL;
    vector<int> fronts;
    int first_bad=-1;
    for(int t=0;t<steps;t++){
        if(n.get_str(10)!=to_str(d))throw runtime_error("GMP and independent digits DISAGREE at t="+to_string(t));
        if(equal(d.begin(),d.end(),d.rbegin()))throw runtime_error("palindrome at t="+to_string(t));
        int jbad=int((d.size()+1)/2),ph=t%8;
        for(int j=0;j<(int)((d.size()+1)/2);++j){
            int x=int(d[j])+int(d[d.size()-1-j]);
            int w=(j<39)?path[j][ph]:cyc[(j-39)%20][ph];
            if(x!=w){jbad=j;break;}
        }
        if(jbad<39){first_bad=t;cout<<"PREFIX_BREAK step="<<t<<" index="<<jbad<<"\n";break;}
        fronts.push_back(jbad);
        if(t>=98&&t>=10+88&&fronts[t]!=fronts[t-88]-20)
            throw runtime_error("88-step front translation failed at t="+to_string(t)+" j="+to_string(fronts[t]));
        checksum ^= (uint64_t(jbad)<<16)^uint64_t(t%8)^uint64_t(d.size());
        checksum*=1099511628211ULL;
        // Independently recompute the next arbitrary-precision integer in GMP.
        mpz_class sum=n+reverse_gmp(n);
        auto next=ordinary_step(d);
        if(sum.get_str(10)!=to_str(next))throw runtime_error("GMP addition differs from decimal digit schoolbook t="+to_string(t));
        int gamma=int(next.size())-int(d.size());
        if(gamma!=int(t%2==0))throw runtime_error("overflow pattern differs t="+to_string(t));
        d=move(next);n=move(sum);
        if((t+1)%5000==0)cout<<"CHECKPOINT step="<<t+1<<" digits="<<d.size()<<" front="<<jbad<<" checksum="<<checksum<<"\n"<<flush;
    }
    cout<<"N02_GMP_AND_DIGIT_REPLAY_PASS q="<<q<<" steps="<<steps<<" first_bad="<<first_bad
       <<" initial_digits="<<2*(39+20*q)<<" final_digits="<<d.size()<<" last_front="<<(fronts.empty()?-1:fronts.back())
       <<" checksum="<<checksum<<"\n";
}
