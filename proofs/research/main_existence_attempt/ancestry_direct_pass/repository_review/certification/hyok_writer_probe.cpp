// Structural probe for simultaneously eligible hyok stores. CPU only: this
// establishes the valid-input branch geometry, not a CUDA race outcome.
#include <iostream>
#include <vector>
#include "bits_tb8.h"

int main() {
  tb::Conf c{};
  c.K = 1; c.TW = 64; c.HW = 4; c.Wcap = 200; c.hy = 1;
  c.PW = tb::prefix_words(c.HW);
  c.plenMax = tb::plen_max(c.PW, c.K);
  c.lenMax = tb::len_max(c.TW, c.HW, c.K);
  const int n = 10000, h = n / 2;
  std::vector<bits::u32> src(5 * c.Wcap, 0);
  // Every sum is 0..18. Even length: no center constraint. The outer sum is
  // 2, so high=min(sum,9), low=sum-high realizes a canonical n-digit integer.
  for (int j = 0; j < h; ++j) {
    const int value = j < 256 ? 2 : (j >= 60 * 32 && j < 138 * 32 ? 9 : 0);
    for (int q = 0; q < 5; ++q)
      src[q * c.Wcap + j / 32] |= bits::u32((value >> q) & 1) << (j % 32);
  }
  tb::State s{};
  tb::ph_setup(s, c, 1, n);
  std::vector<bits::u32> storage((tb::smem_bytes(c) + 3) / 4, 0);
  auto* base = storage.data();
  tb::ph_load(s, c, base, src.data(), 0, 1);
  tb::ph_init(s, c, base);
  auto prefix = s.ptr;
  const int prefixOK = tb::track_step(tb::pre_view(s, base, c, 0), prefix, n, s.gS[0]);
  if (!s.hy || !s.okP || !prefixOK || s.gS[0] != 0) return 1;
  tb::hy_init_spans(s, c, base, 0, 1);
  std::vector<int> eligible;
  for (int gi = 0; gi < s.len / 4; ++gi) {
    // Isolate each call's effect. hy_window never reads hyok; in the CUDA
    // launch all these identical stores instead target the one shared flag.
    s.hyok = 1;
    tb::hy_window(s, c, base, gi, 0, 1, 0);
    if (!s.hyok) eligible.push_back(gi);
  }
  if (eligible.size() != 16) return 2;
  std::cout << "{\"n_digits\":" << n << ",\"K\":1,\"tile_words\":64,"
    "\"halo_words\":4,\"hybrid_selected\":true,\"prefix_tape_certified\":true,"
    "\"groups\":" << s.len / 4 << ",\"eligible_same_address_zero_writers\":" << eligible.size()
    << ",\"cuda_runtime_executed\":false,\"worker_thread_ids\":[";
  for (size_t i = 0; i < eligible.size(); ++i) {
    if (i) std::cout << ',';
    std::cout << eligible[i];
  }
  std::cout << "]}\n";
}
