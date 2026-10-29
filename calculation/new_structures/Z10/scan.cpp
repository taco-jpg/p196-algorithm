#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;
using U64 = uint64_t;
static constexpr U64 ALL = ~U64(0);
static constexpr size_t FULL_J_SPACE = 2476099; // 19^5

struct Planes {
    array<vector<U64>,5> b;
    explicit Planes(size_t n) { for (auto &x:b) x.assign(n,0); }
};
struct Cell {
    int v=0;
    shared_ptr<Planes> p;
    Cell()=default;
    explicit Cell(int x):v(x),p(nullptr) { if(x<0||x>18) throw runtime_error("coefficient outside 0..18"); }
    explicit Cell(shared_ptr<Planes> q):v(0),p(move(q)) {}
    bool constant() const { return !p; }
};
struct Mask {
    bool c=true, v=false;
    shared_ptr<vector<U64>> p;
    static Mask constant(bool x) { Mask m; m.c=true; m.v=x; return m; }
    static Mask variable(shared_ptr<vector<U64>> x) { Mask m; m.c=false; m.p=move(x); return m; }
};
struct Lattice { vector<int> gamma; vector<vector<int>> W,B; };
static inline U64 cb(const Cell& x,int b,size_t w) { return x.p ? x.p->b[b][w] : ((x.v>>b)&1 ? ALL : U64(0)); }
static inline U64 mb(const Mask& x,size_t w) { return x.c ? (x.v?ALL:U64(0)) : (*x.p)[w]; }
static inline bool any_alive(const vector<U64>& a) { for(U64 x:a) if(x) return true; return false; }
static size_t count_bits(const vector<U64>& a) { size_t n=0; for(U64 x:a) n+=__builtin_popcountll(x); return n; }
static void apply_mask(vector<U64>& alive,const Mask& m,bool expected) {
    if(m.c) { if(m.v!=expected) fill(alive.begin(),alive.end(),0); return; }
    for(size_t w=0;w<alive.size();++w) alive[w] &= expected ? (*m.p)[w] : ~(*m.p)[w];
}
static pair<Cell,Mask> normalize_cell(const Cell& x,const Mask& carry,size_t words) {
    if(x.constant() && carry.c) {
        int z=x.v+(carry.v?1:0);
        return {Cell(z%10),Mask::constant(z>=10)};
    }
    auto y=make_shared<Planes>(words);
    shared_ptr<vector<U64>> g;
    if(x.p) g=make_shared<vector<U64>>(words,0);
    for(size_t w=0;w<words;++w) {
        U64 x0=cb(x,0,w),x1=cb(x,1,w),x2=cb(x,2,w),x3=cb(x,3,w),x4=cb(x,4,w),c=mb(carry,w);
        U64 s0=x0^c, c1=x0&c;
        U64 s1=x1^c1, c2=x1&c1;
        U64 s2=x2^c2, c3=x2&c2;
        U64 s3=x3^c3, c4=x3&c3;
        U64 s4=x4^c4;
        U64 ge10=x4 | (x3 & (x2|x1));
        U64 eq9=x3 & ~x2 & ~x1 & x0;
        U64 gg=ge10 | (c & eq9);
        U64 b2=gg & ~s1;
        U64 b3=b2 & ~s2;
        U64 y0=s0;
        U64 y1=s1^gg;
        U64 y2=s2^b2;
        U64 y3=s3^gg^b3;
        U64 b4=(gg & ~s3) | (b3 & ~s3) | (gg & b3);
        U64 y4=s4^b4;
        y->b[0][w]=y0; y->b[1][w]=y1; y->b[2][w]=y2; y->b[3][w]=y3; y->b[4][w]=y4;
        if(g) (*g)[w]=gg;
    }
    Mask gout;
    if(x.constant()) {
        if(x.v==9) gout=carry;
        else gout=Mask::constant(x.v>=10);
    } else gout=Mask::variable(move(g));
    return {Cell(move(y)),move(gout)};
}
static Cell add_digits(const Cell& a,const Cell& b,size_t words) {
    if(a.constant()&&b.constant()) return Cell(a.v+b.v);
    auto s=make_shared<Planes>(words);
    for(size_t w=0;w<words;++w) {
        U64 carry=0;
        for(int bit=0;bit<5;++bit) {
            U64 x=cb(a,bit,w),y=cb(b,bit,w);
            U64 z=x^y^carry;
            carry=(x&y)|(x&carry)|(y&carry);
            s->b[bit][w]=z;
        }
    }
    return Cell(move(s));
}
static Lattice load_lattice(const string& path) {
    ifstream f(path); if(!f) throw runtime_error("cannot open lattice: "+path);
    int p,nb,m,base; f>>p>>nb>>m>>base;
    if(p!=12||nb!=34||m!=9||base!=10) throw runtime_error("unexpected p12/m9 lattice header");
    Lattice x; x.gamma.resize(12); for(int &v:x.gamma) f>>v;
    x.W.assign(12,vector<int>(9));
    for(int t=0;t<12;++t) for(int i=0;i<9;++i) f>>x.W[t][i];
    for(int t=0;t<12;++t) for(int i=0;i<9;++i) { int dummy; f>>dummy; }
    x.B.assign(12,vector<int>(34));
    for(int t=0;t<12;++t) for(int i=0;i<34;++i) f>>x.B[t][i];
    if(!f) throw runtime_error("truncated lattice file");
    return x;
}
static array<int,5> decode_j(size_t idx) {
    array<int,5> d{};
    for(int i=4;i>=0;--i) { d[i]=int(idx%19); idx/=19; }
    return d;
}
static array<shared_ptr<Planes>,5> make_j_planes(size_t n,size_t words) {
    array<shared_ptr<Planes>,5> jp;
    for(auto &p:jp) p=make_shared<Planes>(words);
    for(size_t idx=0;idx<n;++idx) {
        auto d=decode_j(idx); size_t w=idx/64; U64 bit=U64(1)<<(idx%64);
        for(int j=0;j<5;++j) for(int b=0;b<5;++b) if((d[j]>>b)&1) jp[j]->b[b][w]|=bit;
    }
    return jp;
}
static vector<Cell> build_template(const vector<int>& B,const vector<int>& W,const vector<int>& U,
                                  const array<shared_ptr<Planes>,5>& jp,int q,int k) {
    vector<Cell> h; h.reserve(B.size()+W.size()*q+5+U.size()*k);
    for(int x:B) h.emplace_back(x);
    for(int r=0;r<q;++r) for(int x:W) h.emplace_back(x);
    for(int j=0;j<5;++j) h.emplace_back(Cell(jp[j]));
    for(int r=0;r<k;++r) for(int x:U) h.emplace_back(x);
    vector<Cell> p; p.reserve(h.size()*2+1);
    for(const auto& x:h) p.push_back(x);
    p.emplace_back(2); // canonical one-coefficient palindromic centre; midpoint digit is 1
    for(auto it=h.rbegin();it!=h.rend();++it) p.push_back(*it);
    return p;
}
static void step_pairword(vector<Cell>& P,vector<U64>& alive,size_t words,bool expected_overflow) {
    vector<Cell> D; D.reserve(P.size()+1);
    Mask carry=Mask::constant(false);
    for(const Cell& x:P) {
        auto z=normalize_cell(x,carry,words);
        D.push_back(move(z.first)); carry=move(z.second);
    }
    apply_mask(alive,carry,expected_overflow);
    size_t newlen=P.size()+(expected_overflow?1:0);
    if(expected_overflow) D.emplace_back(1); // correct on every still-live lane
    vector<Cell>().swap(P); // input pairword is no longer needed
    vector<Cell> next(newlen);
    for(size_t i=0;i<(newlen+1)/2;++i) {
        Cell z=add_digits(D[i],D[newlen-1-i],words);
        next[i]=z; next[newlen-1-i]=z;
    }
    vector<Cell>().swap(D);
    P=move(next);
}
static void compare_templates(vector<U64>& alive,const vector<Cell>& got,const vector<Cell>& want,size_t words) {
    if(got.size()!=want.size()) { fill(alive.begin(),alive.end(),0); return; }
    for(size_t i=0;i<got.size() && any_alive(alive);++i) {
        const Cell&a=got[i]; const Cell&b=want[i];
        if(a.constant()&&b.constant()) { if(a.v!=b.v) fill(alive.begin(),alive.end(),0); continue; }
        for(size_t w=0;w<words;++w) {
            U64 eq=ALL;
            for(int bit=0;bit<5;++bit) eq &= ~(cb(a,bit,w)^cb(b,bit,w));
            alive[w]&=eq;
        }
    }
}
static vector<size_t> survivor_indices(const vector<U64>& alive,size_t n) {
    vector<size_t> v; v.reserve(count_bits(alive));
    for(size_t w=0;w<alive.size();++w) { U64 x=alive[w]; while(x) { unsigned b=__builtin_ctzll(x); size_t idx=w*64+b; if(idx<n) v.push_back(idx); x&=x-1; } }
    return v;
}
static string jstr(array<int,5> d) { ostringstream o; for(int i=0;i<5;++i){if(i)o<<',';o<<d[i];}return o.str(); }
int main(int argc,char**argv) try {
    string lattice="calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt";
    int q=14,k=100; size_t limit=FULL_J_SPACE; string us="both";
    for(int i=1;i<argc;++i) {
        string a=argv[i];
        if(a=="--lattice"&&i+1<argc) lattice=argv[++i];
        else if(a=="--q"&&i+1<argc) q=stoi(argv[++i]);
        else if(a=="--k"&&i+1<argc) k=stoi(argv[++i]);
        else if(a=="--limit"&&i+1<argc) limit=stoull(argv[++i]);
        else if(a=="--u"&&i+1<argc) us=argv[++i];
        else throw runtime_error("unknown or incomplete argument: "+a);
    }
    Lattice lat=load_lattice(lattice);
    if(q<14||k<100) throw runtime_error("reference run requires q>=14,k>=100");
    if(limit==0||limit>FULL_J_SPACE) limit=FULL_J_SPACE;
    vector<array<int,3>> Uall={{0,9,18},{0,18,9},{2,9,16},{2,16,9},{4,9,14},{4,14,9},{6,9,12},{6,12,9},{8,9,10},{8,10,9},{9,0,18},{9,2,16},{9,4,14},{9,6,12},{9,8,10},{9,10,8},{9,12,6},{9,14,4},{9,16,2},{9,18,0},{10,8,9},{10,9,8},{12,6,9},{12,9,6},{14,4,9},{14,9,4},{16,2,9},{16,9,2},{18,0,9},{18,9,0}};
    vector<int> chosen;
    if(us=="both") {chosen={9,21};} else { array<int,3> want{}; stringstream ss(us); string tok; int z=0; while(getline(ss,tok,',')){if(z>=3)throw runtime_error("U must have three values");want[z++]=stoi(tok);} if(z!=3)throw runtime_error("U must have three values"); auto it=find(Uall.begin(),Uall.end(),want); if(it==Uall.end())throw runtime_error("U is not a charge-zero rotation"); chosen={int(it-Uall.begin())}; }
    const size_t words=(limit+63)/64;
    vector<U64> initial_alive(words,ALL);
    if(limit%64) initial_alive.back()=(U64(1)<<(limit%64))-1;
    cout<<"SPACE "<<FULL_J_SPACE<<" explored_per_U "<<limit<<" fraction "<<double(limit)/double(FULL_J_SPACE)<<" q="<<q<<" k="<<k<<" C=[2]\n";
    for(int urank:chosen) {
        const auto U=Uall[urank];
        auto jp=make_j_planes(limit,words);
        vector<Cell> P=build_template(lat.B[0],lat.W[0],vector<int>(U.begin(),U.end()),jp,q,k);
        vector<U64> alive=initial_alive;
        size_t start_len=P.size();
        for(int t=0;t<120;++t) {
            bool expected=lat.gamma[t%12]!=0;
            step_pairword(P,alive,words,expected);
            if(!any_alive(alive)) break;
        }
        size_t clock_survivors=count_bits(alive);
        size_t prefix_len=lat.B[0].size()+q*lat.W[0].size();
        map<long long,size_t> mismatch_hist;
        map<long long,size_t> mismatch_example;
        if(any_alive(alive)) {
            if(P.size()<prefix_len) throw runtime_error("pairword shorter than rooted prefix");
            for(size_t i=0;i<prefix_len && any_alive(alive);++i) {
                int want = i<lat.B[0].size() ? lat.B[0][i] : lat.W[0][(i-lat.B[0].size())%9];
                if(P[i].constant()) {
                    if(P[i].v!=want) {
                        long long off=static_cast<long long>(i)-static_cast<long long>(prefix_len);
                        mismatch_hist[off]+=count_bits(alive);
                        for(size_t w=0;w<words;++w) if(alive[w]) { mismatch_example.emplace(off,w*64+size_t(__builtin_ctzll(alive[w]))); break; }
                        fill(alive.begin(),alive.end(),0);
                    }
                } else {
                    size_t failed=0;
                    size_t first_bad=limit;
                    for(size_t w=0;w<words;++w) {
                        U64 eq=ALL;
                        for(int b=0;b<5;++b) eq &= ((want>>b)&1) ? P[i].p->b[b][w] : ~P[i].p->b[b][w];
                        U64 bad=alive[w]&~eq;
                        failed+=__builtin_popcountll(bad);
                        if(bad && first_bad==limit) first_bad=w*64+size_t(__builtin_ctzll(bad));
                        alive[w]&=eq;
                    }
                    if(failed) {
                        long long off=static_cast<long long>(i)-static_cast<long long>(prefix_len);
                        mismatch_hist[off]+=failed;
                        mismatch_example.emplace(off,first_bad);
                    }
                }
            }
        }
        size_t w9_survivors=count_bits(alive);
        size_t mismatch_total=0; for(const auto& kv:mismatch_hist) mismatch_total+=kv.second;
        if(mismatch_total != clock_survivors-w9_survivors) throw runtime_error("first-mismatch histogram does not partition clock survivors");
        vector<U64> full1=alive;
        if(any_alive(full1)) {
            auto target1=build_template(lat.B[0],lat.W[0],vector<int>(U.begin(),U.end()),jp,q,k+5);
            compare_templates(full1,P,target1,words);
        }
        size_t full120=count_bits(full1);
        vector<size_t> survivor_ids;
        if(w9_survivors) survivor_ids=survivor_indices(alive,limit);
        cout<<"U_RANK "<<(urank+1)<<" U="<<U[0]<<","<<U[1]<<","<<U[2]
            <<" source_len="<<start_len<<" clock_survivors="<<clock_survivors
            <<" W9_prefix_survivors="<<w9_survivors<<" mismatch_hist_total="<<mismatch_total<<" full_120_returns="<<full120;
        if(!mismatch_hist.empty()) {
            cout<<" first_mismatch_from_cut="; bool first=true;
            for(const auto &kv:mismatch_hist){if(!first)cout<<',';first=false;cout<<kv.first<<':'<<kv.second;}
            cout<<" examples="; first=true;
            for(const auto &kv:mismatch_example){if(!first)cout<<',';first=false;cout<<kv.first<<'@'<<kv.second<<"["<<jstr(decode_j(kv.second))<<"]";}
        }
        cout<<"\n";
        if(w9_survivors==0) { cout<<"SECOND_EPOCH skipped: no first-epoch W9-prefix survivors\n"; continue; }
        for(int t=120;t<240 && any_alive(alive);++t) {
            bool expected=lat.gamma[t%12]!=0;
            step_pairword(P,alive,words,expected);
        }
        size_t second_clock=count_bits(alive);
        auto target2=build_template(lat.B[0],lat.W[0],vector<int>(U.begin(),U.end()),jp,q,k+10);
        compare_templates(alive,P,target2,words);
        size_t full240=count_bits(alive);
        cout<<"U_RANK "<<(urank+1)<<" second_epoch_clock_survivors="<<second_clock<<" full_240_returns="<<full240<<"\n";
        if(full240) {
            auto ids=survivor_indices(alive,limit);
            cout<<"ALERT_CANDIDATES "; for(size_t i=0;i<min<size_t>(ids.size(),100);++i){if(i)cout<<';';cout<<ids[i]<<":"<<jstr(decode_j(ids[i]));} cout<<"\n";
        }
    }
    return 0;
} catch(const exception& e) { cerr<<"ERROR: "<<e.what()<<"\n"; return 2; }
