// Exhaustive W26 phase-zero short-junction prefix screen.
// Exact coefficient semantics; no modular pruning or SAT/MDD assumptions.
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>
using namespace std;
using V = vector<int>;

const V B = {10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
const V W = {5,18,4,8,1,15,4,0,5};
const V U = {9,4,14};

void append(V& a, const V& b) { a.insert(a.end(), b.begin(), b.end()); }
void repeat(V& a, const V& b, int n) { for (int i=0; i<n; ++i) append(a,b); }
V reversed(V a) { reverse(a.begin(), a.end()); return a; }

V template_word(const V& J, int q=14, int k=100) {
    V h=B;
    repeat(h,W,q);
    append(h,J);
    repeat(h,U,k);
    V p=h;
    append(p,V{0,0,0}); // legal odd centre; endpoint prefix is centre-independent by T12
    append(p,reversed(h));
    return p;
}

// One genuine reverse-and-add pairword step. Carry-out is the true overflow bit.
pair<V,int> step(const V& p) {
    V d;
    d.reserve(p.size()+1);
    int carry=0;
    for (int x : p) {
        int z=x+carry;
        d.push_back(z%10);
        carry=z/10;
    }
    if (carry) d.push_back(carry);
    V out(d.size());
    for (size_t i=0; i<d.size(); ++i)
        out[i]=d[i]+d[d.size()-1-i];
    return {out,carry};
}

int first_prefix_mismatch(const V& p, int q=14) {
    V target=B;
    repeat(target,W,q);
    size_t n=min(p.size(),target.size());
    for (size_t i=0; i<n; ++i)
        if (p[i]!=target[i]) return static_cast<int>(i);
    return p.size()==target.size() ? -1 : static_cast<int>(n);
}

V decode_base19(long long x, int len) {
    V j(len);
    for (int i=0; i<len; ++i) {
        j[i]=static_cast<int>(x%19);
        x/=19;
    }
    return j;
}

int main(int argc, char** argv) {
    const long long n3=19LL*19*19;
    const long long n4=n3*19;
    const long long total_domain=n3+n4;
    const long long start=argc>1 ? stoll(argv[1]) : 0;
    const long long count=argc>2 ? stoll(argv[2]) : total_domain;
    const long long end=min(total_domain,start+count);
    long long checked=0, clock_ok=0, prefix_returns=0;
    map<int,long long> histogram;

    for (long long idx=start; idx<end; ++idx) {
        const int len=idx<n3 ? 3 : 4;
        const long long local=idx<n3 ? idx : idx-n3;
        const V J=decode_base19(local,len);
        V p=template_word(J);
        bool clock=true;
        for (int t=0; t<120; ++t) {
            auto next=step(p);
            if (next.second != (t%4==0)) clock=false;
            p.swap(next.first);
        }
        ++checked;
        clock_ok += clock;
        const int mismatch=first_prefix_mismatch(p);
        ++histogram[mismatch];
        if (mismatch==-1) ++prefix_returns;
    }

    cerr << "range=" << start << ":" << end
         << " checked=" << checked
         << " clock1000=" << clock_ok
         << " prefix_returns=" << prefix_returns
         << " total_domain=" << total_domain << "\n";
    for (const auto& [m,n] : histogram)
        cerr << "first_mismatch=" << m << " count=" << n << "\n";
    return (checked==end-start && clock_ok==checked && prefix_returns==0) ? 0 : 1;
}