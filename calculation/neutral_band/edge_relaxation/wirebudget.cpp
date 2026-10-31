// Caps on a 9-wire with a FIXED stream, frame with a shift budget: at most B shifts in any L consecutive steps
// (covers every Sturmian schedule of rate <= B/L, hence every cap/converter with average drift in [0, B/L], any period).
// Shifts may happen on any step: on an overflow step the new top cell = free e-digit + r(top); otherwise any 0..18.
// State: (t mod p, ages of the last B shifts capped at L) x window. Accepting: bottom cell != 9.
// usage: wirebudget clock stream B L K full OUT | ... K incr PREV OUT
#include <bits/stdc++.h>
using namespace std; typedef long long ll; typedef unsigned long long u64;
int P_, K_, BB, LL_; vector<int> G, S; ll NW; int NA;   // NA = number of age tuples encoded as base (LL_+1)
vector<array<int,2>> AGES; map<array<int,2>,int> AID;
static inline u64 enc(int t, int aid, const int* w) { u64 x = 0; for (int i = K_ - 1; i >= 0; i--) x = x * 19 + w[i]; return ((u64)(t * NA + aid)) * NW + x; }
static inline void dec(u64 s, int& t, int& aid, int* w) { u64 ph = s / NW, x = s % NW; aid = ph % NA; t = ph / NA; for (int i = 0; i < K_; i++) { w[i] = x % 19; x /= 19; } }
// one step with given shift dh, Din, top value tv; returns ok
bool step(int t, const int* w, int dh, int Din, int tv, int* out) {
    const int K = K_; int g = G[t], s = S[t];
    int e[32], D[32], r[32], a[33];
    a[0] = s;
    for (int i = 0; i < K; i++) { int x = w[i] + a[i]; e[i] = x % 10; a[i + 1] = x / 10; }
    D[K - 1] = Din;
    for (int i = K - 1; i > 0; i--) D[i - 1] = (w[i] + D[i]) / 10;
    for (int i = 0; i < K; i++) r[i] = (w[i] + D[i]) % 10;
    int dsent = (w[0] + D[0]) / 10;
    if (dsent != 1 - s) return false;                // wire condition
    int rwire = (9 + dsent) % 10;
    int nw[33];
    for (int i = 0; i < K + dh; i++) {
        if (i == K) { nw[i] = g ? tv + r[K - 1] : tv; continue; }
        int src = i - g; int rr = (src >= 0) ? r[src] : rwire;
        nw[i] = e[i] + rr;
    }
    if (dh) { if (nw[0] != 9) return false; for (int i = 0; i < K; i++) out[i] = nw[i + 1]; }
    else for (int i = 0; i < K; i++) out[i] = nw[i];
    return true;
}
int main(int argc, char** argv) {
    string clock = argv[1], stream = argv[2]; BB = atoi(argv[3]); LL_ = atoi(argv[4]); K_ = atoi(argv[5]); string how = argv[6];
    P_ = clock.size(); for (char ch : clock) G.push_back(ch - '0'); for (char ch : stream) S.push_back(ch - '0');
    if (BB < 1 || BB > 2) { fprintf(stderr, "B must be 1 or 2\n"); return 1; }
    // age tuples: (a1, a2) with 1<=a1<=LL_, a1<=a2<=LL_ (a2 unused when B=1 -> fixed LL_)
    for (int a1 = 1; a1 <= LL_; a1++) for (int a2 = (BB == 2 ? a1 : LL_); a2 <= LL_; a2++) { AID[{a1, a2}] = AGES.size(); AGES.push_back({a1, a2}); }
    NA = AGES.size();
    NW = 1; for (int i = 0; i < K_; i++) NW *= 19;
    vector<u64> C; const char* outfn;
    if (how == "full") {
        int w[32];
        for (int t = 0; t < P_; t++) for (int aid = 0; aid < NA; aid++) for (ll x = 0; x < NW; x++) { ll y = x; for (int i = 0; i < K_; i++) { w[i] = y % 19; y /= 19; } C.push_back(enc(t, aid, w)); }
        outfn = argv[7];
    } else {
        FILE* pf = fopen(argv[7], "rb"); u64 k; int Kp = K_ - 1; ll NWp = NW / 19; int w[32];
        while (fread(&k, 8, 1, pf) == 1) { u64 ph = k / NWp, x = k % NWp; int aid = ph % NA, t = ph / NA;
            for (int i = 0; i < Kp; i++) { w[i] = x % 19; x /= 19; }
            for (int v = 0; v < 19; v++) { w[Kp] = v; C.push_back(enc(t, aid, w)); } }
        fclose(pf); outfn = argv[8];
    }
    sort(C.begin(), C.end()); C.erase(unique(C.begin(), C.end()), C.end()); ll NC = C.size();
    auto pos = [&](u64 s) -> ll { auto it = lower_bound(C.begin(), C.end(), s); return (it != C.end() && *it == s) ? (ll)(it - C.begin()) : -1; };
    // successor k: dh = k%2, Din = (k/2)%2, tv = k/4 (0..18)
    auto succ = [&](u64 s, int k, u64& o) -> bool {
        int t, aid, w[32], nw[32]; dec(s, t, aid, w);
        int dh = k % 2, Din = (k / 2) % 2, tv = k / 4;
        int g = G[t];
        if (!dh && tv) return false;
        if (dh && g && tv > 9) return false;
        int a1 = AGES[aid][0], a2 = AGES[aid][1];
        if (dh) { bool allowed = (BB == 1) ? (a1 >= LL_) : (a2 >= LL_); if (!allowed) return false; }
        if (!step(t, w, dh, Din, tv, nw)) return false;
        int n1, n2;
        if (dh) { n1 = 1; n2 = (BB == 2) ? min(a1 + 1, LL_) : LL_; } else { n1 = min(a1 + 1, LL_); n2 = (BB == 2) ? min(a2 + 1, LL_) : LL_; }
        if (BB == 2 && n2 < n1) n2 = n1;
        o = enc((t + 1) % P_, AID[{n1, n2}], nw); return true;
    };
    const int NK = 2 * 2 * 19;
    vector<uint32_t> idx(NC, 0), low(NC, 0); vector<bool> onst(NC, false), cyc(NC, false);
    vector<uint32_t> st; struct Fr { uint32_t v; uint8_t k; }; vector<Fr> work; uint32_t cnt = 0;
    ll nscc = 0, ncyc = 0, nacc = 0, nmove = 0;
    for (ll root = 0; root < NC; root++) {
        if (idx[root]) continue;
        idx[root] = low[root] = ++cnt; st.push_back(root); onst[root] = true; work.push_back({(uint32_t)root, 0});
        while (!work.empty()) {
            Fr& fr = work.back(); uint32_t v = fr.v; bool pushed = false;
            while (fr.k < NK) { int k = fr.k++; u64 ws; if (!succ(C[v], k, ws)) continue; ll w = pos(ws); if (w < 0) continue;
                if (!idx[w]) { idx[w] = low[w] = ++cnt; st.push_back(w); onst[w] = true; work.push_back({(uint32_t)w, 0}); pushed = true; break; }
                else if (onst[w] && idx[w] < low[v]) low[v] = idx[w]; }
            if (pushed) continue;
            work.pop_back(); if (!work.empty()) { uint32_t u = work.back().v; if (low[v] < low[u]) low[u] = low[v]; }
            if (low[v] == idx[v]) {
                vector<uint32_t> comp; while (true) { uint32_t w = st.back(); st.pop_back(); onst[w] = false; comp.push_back(w); if (w == v) break; }
                bool c = comp.size() > 1; if (!c) for (int k = 0; k < NK; k++) { u64 ws; if (succ(C[v], k, ws) && ws == C[v]) c = true; }
                if (c) { nscc++; for (auto w : comp) { cyc[w] = true; ncyc++; int t, aid, ww[32]; dec(C[w], t, aid, ww); if (ww[0] != 9) nacc++; } }
            }
        }
    }
    vector<u64> Cy; for (ll i = 0; i < NC; i++) if (cyc[i]) Cy.push_back(C[i]);
    FILE* of = fopen(outfn, "wb"); fwrite(Cy.data(), 8, Cy.size(), of); fclose(of);
    printf("clock=%s stream=%s budget %d/%d K=%d candidates=%lld cyclicSCCs=%lld cyclicStates=%lld accepting=%lld\n",
           clock.c_str(), stream.c_str(), BB, LL_, K_, NC, nscc, ncyc, nacc);
}
