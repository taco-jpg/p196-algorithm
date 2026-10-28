// ---------------- position-0 language DFA (counter) ----------------
struct Dfa {
  vector<vector<u64>> st; map<vector<u64>, int> id; vector<array<int, 2>> nx; vector<char> acc; int nn;
  Dfa(int b) {
    nn = 2 * b - 2;
    vector<u64> init(nn); for (int i = 0; i < nn; i++) init[i] = 1ULL << i;
    auto succ = [&](int x, int gg, vector<int>& out) { // x in 1..nn
      out.clear();
      for (int hn = 0; hn < 2; hn++) { int s = x + hn; if (s / b != gg) continue; int xn = x % b + (gg ? 1 : s % b); if (xn >= 1 && xn <= nn) out.push_back(xn); }
    };
    id[init] = 0; st.push_back(init); nx.push_back({-1, -1});
    for (size_t i = 0; i < st.size(); i++) {
      for (int gg = 0; gg < 2; gg++) {
        vector<u64> ns(nn, 0); bool any = false;
        for (int j = 0; j < nn; j++) {
          u64 m = st[i][j]; vector<int> o;
          for (int xi = 0; xi < nn; xi++) if ((m >> xi) & 1) { succ(xi + 1, gg, o); for (int xn : o) ns[j] |= 1ULL << (xn - 1); }
          if (ns[j]) any = true;
        }
        if (!any) { nx[i][gg] = -1; continue; }
        auto it = id.find(ns);
        if (it == id.end()) { int k = st.size(); id[ns] = k; st.push_back(ns); nx.push_back({-1, -1}); nx[i][gg] = k; }
        else nx[i][gg] = it->second;
      }
    }
    acc.assign(st.size(), 0);
    for (size_t i = 0; i < st.size(); i++) for (int j = 0; j < nn; j++) if ((st[i][j] >> j) & 1) acc[i] = 1;
  }
  vector<u64> gen(int P, bool dens4) {
    int S = st.size();
    vector<vector<char>> feas(P + 1, vector<char>(S, 0));
    for (int s = 0; s < S; s++) feas[0][s] = acc[s];
    for (int r = 1; r <= P; r++) for (int s = 0; s < S; s++) { char f = 0; for (int gg = 0; gg < 2; gg++) { int n2 = nx[s][gg]; if (n2 >= 0 && feas[r - 1][n2]) f = 1; } feas[r][s] = f; }
    vector<u64> out;
    // iterative DFS
    vector<int> stS(P + 1), stC(P + 1); u64 w = 0;
    if (!feas[P][0]) return out;
    int d = 0; stS[0] = 0; stC[0] = 0;
    while (d >= 0) {
      if (d == P) {
        // canonical (minimal rotation), optional density
        bool ok = true; for (int r = 1; r < P && ok; r++) { u64 rot = ((w >> r) | (w << (P - r))) & mask_p(); if (rot < w) ok = false; }
        if (ok && dens4 && 4 * __builtin_popcountll(w) < P) ok = false;
        if (ok) out.push_back(w);
        d--; continue;
      }
      if (stC[d] >= 2) { d--; continue; }
      int gg = stC[d]++; int n2 = nx[stS[d]][gg];
      if (n2 < 0 || !feas[P - d - 1][n2]) continue;
      if (gg) w |= 1ULL << d; else w &= ~(1ULL << d);
      stS[d + 1] = n2; stC[d + 1] = 0; d++;
    }
    return out;
  }
};

