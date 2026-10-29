// X07: exact quotient recursion using only least-significant-first base-ten digits.
// q' = q + 1 + reverse_m(10^m-q), m=digitlen(q).
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
using V = vector<int>;

V next_q(const V &q) {
    int m=q.size(),borrow=0;
    V a(m),r(m),out;
    for(int i=0;i<m;i++) {
        int x=-q[i]-borrow;
        if(x<0){x+=10;borrow=1;} else borrow=0;
        a[i]=x;
    }
    assert(borrow==1);
    // rev_m(A) has low-first digits a[m-1],...,a[0].
    int carry=1;
    for(int i=0;i<m;i++) {
        int x=q[i]+a[m-1-i]+carry;
        out.push_back(x%10);carry=x/10;
    }
    if(carry)out.push_back(carry);
    return out;
}

uint64_t hashword(const V&d) {
    uint64_t h=14695981039346656037ULL;
    for(int x:d){h ^= (unsigned)x;h *=1099511628211ULL;}
    return h;
}

int main(int argc,char**argv){
    int m=argc>1?atoi(argv[1]):10,steps=argc>2?atoi(argv[2]):20000;
    if(m<1||steps<0)return 2;
    // q_1=10^m+1 after one coalescence; low-first: 1, (m-1)*0, 1.
    V q(m+1,0);q.front()=1;q.back()=1;
    int growth=0;
    for(int t=0;t<=steps;t++){
        if(t==0||t==1000||t==5000||t==10000||t==20000||t==steps){
            cerr<<"phase="<<t<<" digits="<<q.size()<<" hash="<<hex<<hashword(q)<<dec;
            cerr<<" low=";for(int i=0;i<min(12,(int)q.size());i++)cerr<<q[i];
            cerr<<" high=";for(int i=max(0,(int)q.size()-12);i<(int)q.size();i++)cerr<<q[i];
            cerr<<"\n";
        }
        if(t==steps)break;
        int was=q.size();q=next_q(q);
        assert((int)q.size()==was||(int)q.size()==was+1);
        if((int)q.size()>was)growth++;
        int checksum=0;for(int z:q)checksum+=z;
        assert(checksum%9==2);
    }
    cout<<"m="<<m<<" steps="<<steps<<" final_len="<<q.size()<<" digit_growth="<<growth<<" fnv64="<<hex<<hashword(q)<<dec<<"\n";
}
