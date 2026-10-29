// X07: exhaustive, ordinary-decimal collision/re-entry scan.
// Compile: c++ -O3 -std=c++17 renewal_census.cpp -o renewal_census
// Run: ./renewal_census 4 200 ; ./renewal_census 6 200
// Pair front A is printed as a base-ten integer (leading zeroes allowed).
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using V = vector<uint8_t>;

V reverse_add(const V& in) {
    int carry = 0, n = (int)in.size();
    V out;
    out.reserve(n + 1);
    for (int i = 0; i < n; ++i) {
        int x = in[i] + in[n - i - 1] + carry;
        out.push_back(x % 10);
        carry = x / 10;
    }
    if (carry) out.push_back(carry);
    return out;
}

bool is_palindrome(const V& in) {
    for (int i = 0, n = (int)in.size(); i < n / 2; ++i)
        if (in[i] != in[n - 1 - i]) return false;
    return true;
}

int central_nines(const V& in) {
    int n = (int)in.size(), left = (n - 1) / 2, right = n / 2, len = 0;
    if (n % 2) {
        if (in[left] != 9) return 0;
        len = 1;
        --left;
        ++right;
    }
    while (left >= 0 && right < n && in[left] == 9 && in[right] == 9) {
        len += 2;
        --left;
        ++right;
    }
    return len;
}

// The protected family is A ++ nine^L ++ H, H[i] = 9 - A[i],
// sum(A) = 8 (mod 9), and the innermost digit A.back() <= 8.
// Return L>=0 for a protected state, -1 otherwise. The L=0 case matters.
int protected_gap(const V& in) {
    const int n = (int)in.size();
    for (int L = central_nines(in); L >= 0; L -= 2) {
        if ((n - L) % 2) continue;
        const int m = (n - L) / 2;
        if (m < 1 || in[m-1] > 8) continue;
        int digit_sum = 0;
        bool ok = true;
        for (int i = 0; i < m; ++i) {
            digit_sum += in[i];
            if (in[i] + in[m + L + i] != 9) { ok = false; break; }
        }
        if (ok && digit_sum % 9 == 8) return L;
    }
    return -1;
}

int main(int argc, char** argv) {
    if (argc != 3) { cerr << "usage: renewal_census WIDTH HORIZON\n"; return 2; }
    const int width = atoi(argv[1]), horizon = atoi(argv[2]);
    if (width < 1 || width > 7 || horizon < 1) return 2;
    int limit = 1;
    for (int i = 0; i < width; ++i) limit *= 10;
    long tested = 0, repaired = 0, multiple = 0;

    // All A, including leading-zero A, subject to charge/inner digit guards.
    for (int A = 0; A < limit; ++A) {
        int x = A, charge = 0;
        V a;
        for (int i = 0; i < width; ++i) {
            a.push_back(x % 10);
            charge += x % 10;
            x /= 10;
        }
        if (charge % 9 != 8 || a.back() > 8) continue;
        V d = a;
        for (uint8_t v : a) d.push_back(9 - v);
        ++tested;

        int mode = 0, first_lost = -1;
        vector<pair<int,int>> returns;
        for (int t = 0; t <= horizon; ++t) {
            if (is_palindrome(d)) break; // Critical: false regenerations via palindrome must be rejected.
            int L = protected_gap(d);
            if (mode == 0 && L < 0) { mode = 1; first_lost = t; }
            else if (mode == 1 && L >= 1) { returns.push_back({t,L}); mode = 2; }
            else if (mode == 2 && L < 0) mode = 1;
            if (t != horizon) d = reverse_add(d);
        }
        if (!returns.empty()) {
            ++repaired;
            if (returns.size() >= 2) ++multiple;
            cout << "A=" << A << " m=" << width << " firstbad=" << first_lost
                 << " entries=" << returns.size();
            for (auto [t,L] : returns) cout << " " << t << ":" << L;
            cout << "\n";
        }
    }
    cerr << "m=" << width << " H=" << horizon << " tested=" << tested
         << " repaired=" << repaired << " multiple=" << multiple << "\n";
}
