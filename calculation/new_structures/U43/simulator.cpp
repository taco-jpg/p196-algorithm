// U43: independent, fast concrete decimal reverse-and-add trace engine.
// Input coefficients are least-significant first pair coefficients (digit[i]+digit[n-1-i]).
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using V = std::vector<int>;
struct Lattice { int p, nb, m, base; V gamma, B, W; };

V csv(const std::string& s, int maxv) {
  V out; std::istringstream in(s); std::string token;
  while (std::getline(in, token, ',')) {
    if (token.empty()) continue;
    std::size_t used = 0; int x = std::stoi(token, &used);
    if (used != token.size() || x < 0 || x > maxv) throw std::runtime_error("invalid CSV coefficient");
    out.push_back(x);
  }
  return out;
}
Lattice read_lattice(const std::string& path) {
  std::ifstream f(path); if (!f) throw std::runtime_error("cannot open lattice file");
  Lattice z{}; f >> z.p >> z.nb >> z.m >> z.base;
  if (!f || z.p <= 0 || z.nb <= 0 || z.m <= 0 || z.base != 10) throw std::runtime_error("invalid lattice header (this simulator is decimal-only)");
  z.gamma.resize(z.p); for (int& x : z.gamma) f >> x;
  std::vector<V> ws(z.p, V(z.m)), bs(z.p, V(z.nb));
  for (int t=0;t<z.p;t++) for (int i=0;i<z.m;i++) f >> ws[t][i];
  // The repository lattice format stores a second p-by-m phase table before B_t.
  // It is part of the file schema even though this concrete template uses only B_0 and W_0.
  for (int t=0;t<z.p;t++) for (int i=0;i<z.m;i++) { int ignored; f >> ignored; }
  for (int t=0;t<z.p;t++) for (int i=0;i<z.nb;i++) f >> bs[t][i];
  if (!f) throw std::runtime_error("truncated lattice data");
  z.W = ws[0]; z.B = bs[0];
  for (int x : z.gamma) if (x != 0 && x != 1) throw std::runtime_error("overflow clock is not binary");
  for (int x : z.B) if (x < 0 || x > 18) throw std::runtime_error("bad B coefficient");
  for (int x : z.W) if (x < 0 || x > 18) throw std::runtime_error("bad W coefficient");
  return z;
}
void append(V& dst, const V& src) { dst.insert(dst.end(), src.begin(), src.end()); }
void repeat(V& dst, const V& word, int n) {
  if (n < 0) throw std::runtime_error("negative exponent");
  if (word.empty() && n) throw std::runtime_error("empty repeated word");
  if (word.size() && static_cast<unsigned long long>(word.size()) * static_cast<unsigned long long>(n) > 10000000ULL)
    throw std::runtime_error("requested expansion exceeds 10 million coefficients");
  for (int i=0;i<n;i++) append(dst, word);
}
V reverse(V x) { std::reverse(x.begin(), x.end()); return x; }
V template_pairword(const Lattice& z, const V& J, const V& U, const V& C, int q, int k) {
  V h; append(h,z.B); repeat(h,z.W,q); append(h,J); repeat(h,U,k);
  V p=h; append(p,C); append(p,reverse(h)); return p;
}
V realize(const V& p) {
  if (p.empty() || p != reverse(p)) throw std::runtime_error("template pairword is not symmetric");
  for (int x : p) if (x < 0 || x > 18) throw std::runtime_error("pair coefficient outside 0..18");
  V d(p.size());
  for (std::size_t i=0;i<p.size()/2;i++) {
    int hi=std::min(9,p[i]), lo=p[i]-hi;
    if (lo < 0 || lo > 9) throw std::runtime_error("unrealizable pair coefficient");
    d[i]=lo; d[p.size()-1-i]=hi;
  }
  if (p.size()%2) {
    if (p[p.size()/2]%2) throw std::runtime_error("odd midpoint pair coefficient");
    d[p.size()/2]=p[p.size()/2]/2;
  }
  if (d.empty() || d.back()==0) throw std::runtime_error("source is not a canonical positive decimal integer");
  return d;
}
V pairword(const V& d) {
  V p(d.size());
  for (std::size_t i=0;i<d.size();i++) p[i]=d[i]+d[d.size()-1-i];
  return p;
}
V step(const V& d) {
  V out; out.reserve(d.size()+1); int carry=0;
  for (std::size_t i=0;i<d.size();i++) {
    int s=d[i]+d[d.size()-1-i]+carry;
    out.push_back(s%10); carry=s/10;
  }
  if (carry) out.push_back(carry);
  if (out.empty() || out.back()==0) throw std::runtime_error("step produced noncanonical digits");
  return out;
}
std::string digit_string(const V& d) {
  std::string s; s.reserve(d.size());
  for (auto it=d.rbegin();it!=d.rend();++it) s.push_back(char('0'+*it));
  return s;
}
std::string pair_string(const V& p) {
  static const std::string alphabet="0123456789ABCDEFGHI";
  std::string s; s.reserve(p.size());
  for (int x:p) { if (x<0 || x>=static_cast<int>(alphabet.size())) throw std::runtime_error("pair encoding overflow"); s.push_back(alphabet[x]); }
  return s;
}
int first_mismatch(const V& a, const V& b) {
  std::size_t i=0; while(i<a.size() && i<b.size() && a[i]==b[i]) ++i;
  return (i==a.size() && i==b.size()) ? -1 : static_cast<int>(i);
}
int main(int argc, char** argv) {
  try {
    if (argc != 10) {
      std::cerr << "usage: simulator lattice.txt q k J_csv U_csv C_csv steps epoch gain\n"; return 2;
    }
    Lattice z=read_lattice(argv[1]);
    int q=std::stoi(argv[2]), k=std::stoi(argv[3]), steps=std::stoi(argv[7]), epoch=std::stoi(argv[8]), gain=std::stoi(argv[9]);
    if (q<1 || k<1 || steps<0 || epoch<1 || gain<0 || steps%epoch!=0) throw std::runtime_error("q,k,epoch must be positive; steps must be a multiple of epoch; gain nonnegative");
    V J=csv(argv[4],18), U=csv(argv[5],18), C=csv(argv[6],18);
    if (U.size()!=3 || C!=reverse(C)) throw std::runtime_error("expected length-3 U and palindromic C");
    int nine_count=0, nine_pos=-1;
    for (int i=0;i<3;i++) if (U[i]==9) { ++nine_count; nine_pos=i; }
    if (nine_count!=1 || U[0]+U[1]+U[2]!=27 || U[(nine_pos+1)%3]%2!=0 || U[(nine_pos+2)%3] != 18-U[(nine_pos+1)%3])
      throw std::runtime_error("U is not one of the 30 cyclic charge-zero complement-nine words");
    V initial=template_pairword(z,J,U,C,q,k);
    if (static_cast<unsigned long long>(initial.size()) * static_cast<unsigned long long>(steps+1) > 50000000ULL)
      throw std::runtime_error("trace budget exceeded (50 million state-coefficients); reduce width or steps");
    V d=realize(initial);
    for (int t=0;t<=steps;t++) {
      V p=pairword(d); bool pal=(d==reverse(d));
      int gamma=-1, clock_match=-1;
      V next;
      if (t<steps) { next=step(d); gamma=static_cast<int>(next.size())-static_cast<int>(d.size()); clock_match=(gamma==z.gamma[t%z.p])?1:0; }
      int target_k=-1, checkpoint_match=-1;
      if (t%epoch==0) {
        target_k=k+gain*(t/epoch); V target=template_pairword(z,J,U,C,q,target_k);
        checkpoint_match=(p==target)?1:0;
      }
      std::cout << t << '\t' << d.size() << '\t' << (pal?1:0) << '\t' << gamma << '\t' << clock_match << '\t' << target_k << '\t' << checkpoint_match << '\t' << digit_string(d) << '\t' << pair_string(p) << '\n';
      if (t<steps) d.swap(next);
    }
  } catch (const std::exception& e) { std::cerr << "U43_SIMULATOR_ERROR: " << e.what() << '\n'; return 1; }
}