// r13b subcheck: is E_acc(K) (eset3 file, WORDS=a) a subset of E(K) (eset2 file, WORDS=b) as sets, layer by layer? keys compared on the first min(a,b) words.
// usage: subcheck ACCFILE EFILE
#include <cstdio>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <tuple>
using namespace std;
typedef unsigned long long ull;
struct K3 { uint64_t a, b, c; bool operator<(const K3& o) const { return tie(c, b, a) < tie(o.c, o.b, o.a); } bool operator==(const K3& o) const { return a == o.a && b == o.b && c == o.c; } };
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "rb"), *g = fopen(argv[2], "rb"); int lo1, w1, lo2, w2; fread(&lo1, 4, 1, f); fread(&w1, 4, 1, f); fread(&lo2, 4, 1, g); fread(&w2, 4, 1, g); if (lo1 != lo2) { puts("layer mismatch"); return 1; }
    ull missing = 0, tot = 0;
    for (int l = 0; l < lo1; l++) {
        uint64_t n1, n2; fread(&n1, 8, 1, f); fread(&n2, 8, 1, g); vector<uint64_t> A(w1 * n1), B(w2 * n2); fread(A.data(), 8, w1 * n1, f); fread(B.data(), 8, w2 * n2, g);
        vector<K3> a(n1), b(n2); for (ull i = 0; i < n1; i++) { a[i].a = A[w1 * i]; a[i].b = w1 > 1 ? A[w1 * i + 1] : 0; a[i].c = w1 > 2 ? A[w1 * i + 2] : 0; } for (ull i = 0; i < n2; i++) { b[i].a = B[w2 * i]; b[i].b = w2 > 1 ? B[w2 * i + 1] : 0; b[i].c = w2 > 2 ? B[w2 * i + 2] : 0; }
        sort(a.begin(), a.end()); sort(b.begin(), b.end()); ull i = 0, j = 0;
        for (; i < a.size(); i++) { while (j < b.size() && b[j] < a[i]) j++; if (j == b.size() || !(b[j] == a[i])) missing++; } tot += n1;
    }
    printf("E_acc=%llu missing from E: %llu -> %s\n", tot, missing, missing ? "NOT SUBSET" : "E_acc subset E");
    return 0;
}
