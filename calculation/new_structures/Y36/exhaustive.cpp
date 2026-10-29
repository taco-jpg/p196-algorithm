#include <bits/stdc++.h>
using namespace std;

const vector<int> B={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
const vector<int> W={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
const vector<int> V={9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4,6,3};
const vector<int> J0={18,0,1,1};

struct Mod { int typ, i, oldv, newv; };
struct Stats {
    long long total=0, first_equal=0, hit=0, non_equal_hit=0;
};

vector<int> step(const vector<int>& d) {
    int n=d.size(), carry=0;
    vector<int> out;
    out.reserve(n+1);
    for (int i=0; i<n; ++i) {
        int z=d[i]+d[n-1-i]+carry;
        out.push_back(z%10);
        carry=z/10;
    }
    if (carry) out.push_back(carry);
    return out;
}

vector<int> pairword(const vector<int>& d) {
    vector<int> p(d.size());
    for (int i=0; i<(int)d.size(); ++i) p[i]=d[i]+d[d.size()-1-i];
    return p;
}

vector<int> source_digits(const vector<int>& p) {
    int n=p.size();
    vector<int> d(n);
    for (int i=0; i<n/2; ++i) {
        int low=min(p[i],9);
        d[i]=low;
        d[n-1-i]=p[i]-low;
    }
    return d;
}

vector<int> source_pairword(const vector<int>& E, const vector<int>& J, int q, int k) {
    vector<int> H=B;
    for (int z=0; z<q; ++z) H.insert(H.end(),W.begin(),W.end());
    H.insert(H.end(),E.begin(),E.end());
    H.insert(H.end(),J.begin(),J.end());
    for (int z=0; z<k; ++z) H.insert(H.end(),V.begin(),V.end());
    vector<int> p=H;
    p.push_back(5);
    p.push_back(5);
    for (auto it=H.rbegin(); it!=H.rend(); ++it) p.push_back(*it);
    return p;
}

bool prefix_is(const vector<int>& d, const vector<int>& target) {
    int n=d.size();
    if (n<(int)target.size()) return false;
    for (int i=0; i<(int)target.size(); ++i)
        if (d[i]+d[n-1-i]!=target[i]) return false;
    return true;
}

int main() {
    const int q=20, k=20, max_edits=4;
    vector<Mod> mods;
    for (int i=0; i<20; ++i) {
        int p=W[i];
        if (p<=9) mods.push_back({0,i,p,p+9});
        if (p>=9) mods.push_back({0,i,p,p-9});
    }
    for (int i=0; i<4; ++i) {
        int p=J0[i];
        if (p<=9) mods.push_back({1,i,p,p+9});
        if (p>=9) mods.push_back({1,i,p,p-9});
    }

    vector<int> target=B;
    for (int z=0; z<q+1; ++z) target.insert(target.end(),W.begin(),W.end());
    vector<int> baseE=W;
    baseE[9]=10;
    vector<int> baseDigits=source_digits(source_pairword(baseE,J0,q,k));
    baseDigits=step(baseDigits);
    const vector<int> baseline_first=pairword(baseDigits);

    vector<Stats> stats(max_edits+1);
    vector<Mod> chosen;
    set<pair<int,int>> sites;

    function<void(int,int)> dfs = [&](int start, int wanted) {
        if ((int)chosen.size()==wanted) {
            Stats& st=stats[wanted];
            ++st.total;
            vector<int> E=W, J=J0;
            for (const auto& m:chosen) (m.typ ? J : E)[m.i]=m.newv;
            vector<int> d=source_digits(source_pairword(E,J,q,k));
            d=step(d);
            const bool same_first=pairword(d)==baseline_first;
            if (same_first) {
                // Determinism plus the independently checked T14 baseline
                // makes this packet a t=160 W20-prefix restorer.
                ++st.first_equal;
                ++st.hit;
                return;
            }
            for (int t=1; t<160; ++t) d=step(d);
            if (prefix_is(d,target)) {
                ++st.hit;
                ++st.non_equal_hit;
            }
            return;
        }
        for (int i=start; i<(int)mods.size(); ++i) {
            const auto& m=mods[i];
            pair<int,int> site={m.typ,m.i};
            if (sites.count(site)) continue;
            sites.insert(site);
            chosen.push_back(m);
            dfs(i+1,wanted);
            chosen.pop_back();
            sites.erase(site);
        }
    };

    for (int r=1; r<=max_edits; ++r) {
        dfs(0,r);
        const auto& s=stats[r];
        cout << "r=" << r
             << " total=" << s.total
             << " first-successor-equal=" << s.first_equal
             << " t160-W-prefix-hit=" << s.hit
             << " hit-not-equivalent=" << s.non_equal_hit << "\n";
    }
}
