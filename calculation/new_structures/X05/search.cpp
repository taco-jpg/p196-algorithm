// X05 exact phase-0 T* fixed-U / odd-centre cell screen.
// Enumerates every J in {0,...,18}^3 union {0,...,18}^4 at q=14, k=100.
// Coefficients are LSD-first pair coefficients. Each step exactly normalizes
// sum_i p_i*10^i and then extracts the symmetric pair coefficients.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;
using V = vector<uint8_t>;

static const V B = {10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5};
static const V W = {5,18,4,8,1,15,4,0,5};
static const V U = {9,6,12};
// A legal 15-coefficient odd centre: midpoint 4, all other coefficients 0.
// The reset-cone argument makes the W9 endpoint independent of every C
// coefficient and every odd C length in the claimed range 15,17,19,21,23.
static const V C = {0,0,0,0,0,0,0,4,0,0,0,0,0,0,0};

static constexpr int MAXN = 1100;
static constexpr int PREFIX = 160;
static constexpr int HIST = 1100;

static void repeat(V& a, const V& b, int n) {
    for (int i=0; i<n; ++i) a.insert(a.end(), b.begin(), b.end());
}

static V decode_base19(long long x, int len) {
    V j(len);
    for (int i=0; i<len; ++i) {
        j[i] = static_cast<uint8_t>(x % 19);
        x /= 19;
    }
    return j;
}

struct Result { int mismatch; bool clock; };

static Result run_one(long long idx, long long n3, const V& target) {
    const int len = idx < n3 ? 3 : 4;
    const long long local = idx < n3 ? idx : idx - n3;
    const V J = decode_base19(local, len);

    V h = B;
    repeat(h, W, 14);
    h.insert(h.end(), J.begin(), J.end());
    repeat(h, U, 100);

    array<uint8_t, MAXN> p{}, d{}, out{};
    int n = 0;
    for (auto x : h) p[n++] = x;
    for (auto x : C) p[n++] = x;
    for (auto it=h.rbegin(); it!=h.rend(); ++it) p[n++] = *it;

    bool clock = true;
    for (int t=0; t<120; ++t) {
        int carry = 0;
        for (int i=0; i<n; ++i) {
            const int z = static_cast<int>(p[i]) + carry;
            d[i] = static_cast<uint8_t>(z % 10);
            carry = z / 10;
        }
        int nn = n;
        if (carry) d[nn++] = static_cast<uint8_t>(carry);
        for (int i=0; i<nn; ++i)
            out[i] = static_cast<uint8_t>(d[i] + d[nn-1-i]);
        if (carry != (t % 4 == 0)) clock = false;
        p.swap(out);
        n = nn;
    }

    int mismatch = -1;
    for (int i=0; i<PREFIX; ++i) {
        if (p[i] != target[i]) {
            mismatch = i;
            break;
        }
    }
    return {mismatch, clock};
}

int main(int argc, char** argv) {
    const long long n3 = 19LL*19*19;
    const long long n4 = n3*19;
    const long long total = n3+n4;
    const long long start = argc>1 ? atoll(argv[1]) : 0;
    const long long count = argc>2 ? atoll(argv[2]) : total;
    const long long end = min(total, start+count);
    if (start<0 || count<0 || start>total) return 2;

    V target = B;
    repeat(target, W, 14);
    array<long long, HIST> hist{};
    long long checked=0, clock_ok=0, prefix_returns=0;
    int earliest=9999, latest=-1;

    #pragma omp parallel for schedule(dynamic,64) reduction(+:checked,clock_ok,prefix_returns) reduction(min:earliest) reduction(max:latest) num_threads(5)
    for (long long idx=start; idx<end; ++idx) {
        const auto r = run_one(idx, n3, target);
        ++checked;
        clock_ok += r.clock;
        if (r.mismatch < 0) {
            ++prefix_returns;
        } else {
            #pragma omp atomic update
            hist[r.mismatch]++;
            earliest = min(earliest, r.mismatch);
            latest = max(latest, r.mismatch);
        }
    }

    cerr << "U=9,6,12 C=length15 midpoint4 q=14 k=100"
         << " domain=" << start << ":" << end
         << " checked=" << checked << " total=" << total
         << " clock=" << clock_ok << " Wprefix_returns=" << prefix_returns
         << " first_mismatch_range=" << earliest << ":" << latest << "\n";
    for (int i=0; i<HIST; ++i)
        if (hist[i]) cerr << "first_mismatch=" << i << " count=" << hist[i] << "\n";

    return checked==end-start && clock_ok==checked && prefix_returns==0 ? 0 : 1;
}
