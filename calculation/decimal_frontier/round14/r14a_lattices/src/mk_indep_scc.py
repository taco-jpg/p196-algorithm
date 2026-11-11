#!/usr/bin/env python3
"""mk_indep_scc.py: derive indep_scc.cpp (second pipeline for the ALL-PERIOD closure) from r13b indep_acc.cpp:
same independent rule (rstep2, genuine carries) and genuine-addition fold (fstep); closure replaced by Kosaraju SCCs over the dense graph; exact orbits by functional graph."""
import re, os
src = open(os.path.expanduser('~/p196_run/r13b/src/indep_acc.cpp')).read()
# usage line
src = src.replace('usage: indep_acc ROWS orbit L Kmax OUTDIR threads [q] [-cmp ESET3DIR] [-noexact]', 'usage: indep_scc ROWS orbit 1 Kmax OUTDIR threads [q] [-noexact]   (all-period closure Cyc_acc)')
# closure block
start = src.index('        // closure: from every accepting node')
end = src.index('        // E_acc(K): per layer windows (bytes), sorted')
new_closure = r'''        // closure (all periods): Kosaraju SCCs on the dense graph; keep SCCs of size >= 2 containing an accepting node
        vector<vector<uint8_t>> on(Lo); for (int l = 0; l < Lo; l++) on[l].assign(G_[l].n, 0);
        ull closed = 0, nodeops = 0; (void)nodeops;
        {
            vector<uint64_t> gb(Lo + 1, 0); for (int l = 0; l < Lo; l++) gb[l + 1] = gb[l] + G_[l].n;
            uint64_t NN = gb[Lo];
            if (NN >= 0xFFFFFFF0ULL) { fprintf(stderr, "too many nodes\n"); exit(9); }
            vector<uint32_t> ro(NN + 2, 0), re;
            vector<uint8_t> layerOf_acc(NN, 0);
            for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) { layerOf_acc[gb[l] + v] = Acc[l][v]; for (uint32_t q = OFF[l][v]; q < OFF[l][v + 1]; q++) { uint64_t tg = gb[(l + 1) % Lo] + EDGE[l][q]; ro[tg + 1]++; } }
            for (uint64_t i = 0; i < NN; i++) ro[i + 1] += ro[i];
            re.resize(ro[NN]);
            { vector<uint32_t> pos(ro.begin(), ro.end()); for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) for (uint32_t q = OFF[l][v]; q < OFF[l][v + 1]; q++) { uint64_t tg = gb[(l + 1) % Lo] + EDGE[l][q]; re[pos[tg]++] = (uint32_t)(gb[l] + v); } }
            // pass 1: iterative DFS, finishing order
            vector<uint32_t> fin; fin.reserve(NN);
            vector<uint8_t> seen(NN, 0);
            struct F { uint32_t id; uint32_t e, eend; int l; };
            vector<F> st;
            for (int l0 = 0; l0 < Lo; l0++) for (uint32_t v0 = 0; v0 < G_[l0].n; v0++) {
                uint32_t g0 = (uint32_t)(gb[l0] + v0);
                if (seen[g0]) continue;
                seen[g0] = 1;
                st.push_back({g0, OFF[l0][v0], OFF[l0][v0 + 1], l0});
                while (!st.empty()) {
                    F& f = st.back();
                    if (f.e < f.eend) {
                        int l2 = (f.l + 1) % Lo; uint32_t w = EDGE[f.l][f.e++];
                        uint32_t g2 = (uint32_t)(gb[l2] + w);
                        if (!seen[g2]) { seen[g2] = 1; st.push_back({g2, OFF[l2][w], OFF[l2][w + 1], l2}); }
                    } else { fin.push_back(f.id); st.pop_back(); }
                }
            }
            // pass 2: reverse graph in decreasing finishing order
            vector<uint32_t> compid(NN, 0xFFFFFFFFu); uint32_t ncomp = 0;
            vector<uint32_t> stack2, members;
            vector<uint32_t> csize; vector<uint8_t> cacc;
            for (int64_t i = (int64_t)NN - 1; i >= 0; i--) {
                uint32_t s = fin[i]; if (compid[s] != 0xFFFFFFFFu) continue;
                compid[s] = ncomp; stack2.clear(); stack2.push_back(s); uint32_t sz = 0; uint8_t a = 0;
                while (!stack2.empty()) { uint32_t x = stack2.back(); stack2.pop_back(); sz++; a |= layerOf_acc[x]; for (uint32_t q = ro[x]; q < ro[x + 1]; q++) { uint32_t y = re[q]; if (compid[y] == 0xFFFFFFFFu) { compid[y] = ncomp; stack2.push_back(y); } } }
                csize.push_back(sz); cacc.push_back(a); ncomp++;
            }
            for (int l = 0; l < Lo; l++) for (uint32_t v = 0; v < G_[l].n; v++) { uint32_t c = compid[gb[l] + v]; if (csize[c] >= 2 && cacc[c]) { on[l][v] = 1; closed++; } }
        }
'''
src = src[:start] + new_closure + src[end:]
# exact orbits: replace by functional graph of the anchor-layer return map (all periods)
start = src.index('        // exact fold orbits inside E_acc (genuine addition, q = Q): from the first layer with E_acc states')
end = src.index('        // compare with eset3 file')
new_exact = r'''        // exact fold orbits of any period inside Cyc_acc (genuine addition): functional graph of the one-lap return map on the anchor layer
        ull exactO = 0;
        if (Etot && !noexact) {
            int anc = -1; for (int l = 0; l < Lo; l++) if (!NP[l].empty() && (anc < 0 || NP[l].size() < NP[anc].size())) anc = l;
            auto inE = [&](int l, const int* w) -> bool { uint8_t tmp[64]; for (int i = 0; i < Km1; i++) tmp[i] = (uint8_t)w[i]; ll pi = find_parent(Ls[l], tmp, Km1); if (pi < 0) return false; uint64_t c = pi * DV + w[K - 1]; LayerG& A = G_[l]; if (!A.alive[c]) return false; return on[l][A.did[c]]; };
            uint64_t na = NP[anc].size() / K;
            std::unordered_map<std::string, int64_t> idx; idx.reserve(na * 2);
            for (uint64_t i = 0; i < na; i++) idx[std::string((const char*)NP[anc].data() + i * K, K)] = (int64_t)i;
            vector<int64_t> ret(na, -1);
            for (uint64_t i = 0; i < na; i++) {
                int w0[64], w[64], nw[64]; for (int q = 0; q < K; q++) w0[q] = NP[anc][i * K + q]; memcpy(w, w0, sizeof(int) * K); int l = anc; bool ok = true;
                for (int k = 0; k < TT && ok; k++) { LayerI& I = Ls[l]; if (!fstep(I.t, I.j, I.par, w, K, Q + 1, nw)) { ok = false; break; } l = (l + 1) % Lo; if (!inE(l, nw)) { ok = false; break; } memcpy(w, nw, sizeof(int) * K); }
                if (ok) { std::string key(K, 0); for (int q = 0; q < K; q++) key[q] = (char)w[q]; auto it = idx.find(key); ret[i] = it == idx.end() ? -1 : it->second; }
            }
            vector<uint8_t> col(na, 0);
            for (uint64_t i = 0; i < na; i++) { if (col[i]) continue; vector<int64_t> path; int64_t x = (int64_t)i; while (x >= 0 && col[x] == 0) { col[x] = 1; path.push_back(x); x = ret[x]; }
                if (x >= 0 && col[x] == 1) { size_t z = 0; while (path[z] != x) z++; exactO += path.size() - z; printf("EXACT PERIODIC K=%d laps=%zu anchor layer %d win", K, path.size() - z, anc); for (int q = 0; q < K; q++) printf(" %d", (int)NP[anc][(uint64_t)x * K + q]); puts(""); }
                for (int64_t y : path) col[y] = 2; }
        }
'''
src = src[:start] + new_exact + src[end:]
# remove compare block
start = src.index('        // compare with eset3 file')
end = src.index('        printf("K=%d T=%d orbit=%d candidates=')
src = src[:start] + '        string cmpmsg;\n' + src[end:]
src = src.replace('#include <thread>\n', '#include <thread>\n#include <unordered_map>\n#include <string>\n', 1)
# TT must be Lo for the exact part: LL=1
src = src.replace('Lo = Ls.size(); int TT = LL * Lo;', 'Lo = Ls.size(); int TT = Lo; (void)LL;')
src = src.replace('printf("indep_acc orbit %d/%d', 'printf("indep_scc(all periods) orbit %d/%d')
open(os.path.expanduser('~/p196_run/r14a/src/indep_scc.cpp'), 'w').write(src)
print('ok')
