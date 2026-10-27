#define main a113_wrapped_entry_not_used
#ifndef A113_CAUTO_SOURCE
#error "Define A113_CAUTO_SOURCE as the quoted path of the generated cauto source."
#endif
#include A113_CAUTO_SOURCE
#undef main
#include <iostream>
#include <random>

static void need(bool value, const char* message) {
  if (!value) throw std::runtime_error(message);
}

static LKey oracle(const St& s) {
  LKey k;
  int j = 0;
  auto append = [&](unsigned x, int width) {
    for (int z = 0; z < width; ++z, ++j)
      if ((x >> z) & 1u) k.w[j / 64] |= uint64_t(1) << (j % 64);
  };
  for (int t=0; t<P; ++t) append(unsigned(s.l[t]),1);
  for (int t=0; t<P; ++t) append(unsigned(s.r[t]),1);
  for (int t=0; t<P; ++t) if(g[t]) append(unsigned(int(s.Rd[t])+1),6);
  for (int t=0; t<P; ++t) if(v[t]) append(unsigned(int(s.Z[t])+1),7);
  return k;
}

int main() {
  std::mt19937_64 rng(113484862ULL);
  unsigned long long random_cases = 0;
  for (int trial=0; trial<100000; ++trial) {
    P=1+int(rng()%48); b=2+int(rng()%61);
    int G=2*int(rng()%(P/2+1)), K=G/2;
    g.assign(P,0); v.assign(P,0);
    std::fill(g.begin(),g.begin()+G,1); std::shuffle(g.begin(),g.end(),rng);
    std::fill(v.begin(),v.begin()+K,1); std::shuffle(v.begin(),v.end(),rng);
    St s{};
    for(int t=0;t<P;++t) {
      s.l[t]=rng()%2; s.r[t]=rng()%2;
      s.Rd[t]=int(rng()%(b+1))-1;
      s.Z[t]=int(rng()%(2*b))-1;
    }
    need(pack(s)==oracle(s),"random pack differs from independent bit oracle");
    ++random_cases;
  }

  P=48; b=62; g.assign(P,1); v.assign(P,0);
  std::fill(v.begin(),v.begin()+24,1);
  St z{};
  for(int t=0;t<P;++t){z.Rd[t]=-1;z.Z[t]=-1;}
  std::set<LKey> keys;
  keys.insert(pack(z));
  int position=0;
  auto basis = [&](int8_t& value,int width,int offset) {
    for(int h=0;h<width;++h,++position) {
      value=(1<<h)+offset;
      const LKey k=pack(z);
      LKey want; want.w[position/64]=uint64_t(1)<<(position%64);
      need(k==want,"basis bit missing or misplaced");
      need(keys.insert(k).second,"basis keys collide");
      value=offset;
    }
  };
  for(int t=0;t<P;++t) basis(z.l[t],1,0);
  for(int t=0;t<P;++t) basis(z.r[t],1,0);
  for(int t=0;t<P;++t) basis(z.Rd[t],6,-1);
  for(int t=0;t<P;++t) if(v[t]) basis(z.Z[t],7,-1);
  need(position==552 && keys.size()==553,"wrong maximal key dimension");

  int insertions=0;
  for(int width=1;width<=7;++width) for(int shift=0;shift+width<=576;++shift) {
    const uint64_t val=(uint64_t(1)<<width)-1;
    LKey got, want;
    int sh=shift;
    putbits(got,sh,val,width);
    for(int h=0;h<width;++h) want.w[(shift+h)/64] |= uint64_t(1)<<((shift+h)%64);
    need(got==want && sh==shift+width,"field insertion differs from bit oracle");
    ++insertions;
  }

  int rejected=0;
  auto rejects=[&](int shift,uint64_t val,int width) {
    LKey k; int sh=shift;
    try { putbits(k,sh,val,width); } catch(const std::runtime_error&) {++rejected;return;}
    throw std::runtime_error("invalid putbits accepted");
  };
  rejects(-1,0,1); rejects(0,0,0); rejects(0,0,8);
  rejects(576,0,1); rejects(570,0,7); rejects(0,128,7); rejects(0,2,1);
  need(rejected==7,"invalid field rejection count");
  std::cout << "KEY_PROBE PASS random=" << random_cases << " basis_bits=" << position
            << " unique_basis_keys=" << keys.size() << " field_placements=" << insertions
            << " rejected_invalid=" << rejected << "\n";
}
