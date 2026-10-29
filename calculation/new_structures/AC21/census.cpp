// AC21 uses Z11's exhaustively self-tested AVX2 reset-cone implementation.
// Only endpoint W9 restoration can reject a candidate; NO intermediate-phase pruning.
#define main z11_original_main
#include "../Z11/bitparallel_census.cpp"
#undef main
int main(int argc, char** argv) {
  if (argc>1 && std::string(argv[1])=="--selftest") return selftest()?0:1;
  for (const V& U : std::array<V,3>{V{2,16,9},V{9,10,8},V{16,9,2}})
    run_u(U);
  std::cout<<"AC21_ENDPOINT_ONLY_EXHAUSTIVE_DONE\n";
}