#ifndef P196_AGENT108_WIDE_COUNT_HPP
#define P196_AGENT108_WIDE_COUNT_HPP

#include <algorithm>
#include <array>
#include <cstdint>
#include <stdexcept>
#include <string>

namespace agent108 {

// Exact unsigned 256-bit language counts, stored least-significant limb first.
// For nonuniform exterior blocks, the full cut domain has size
//   D = product_j(10 * 4^ell_j) = 10^G * 2^(2P) < 2^(2P + 4G).
// Thus 2P + 4G <= 240 bounds every suffix language and accepting subset
// strictly below 2^240. Disjoint labeled arcs make node sums obey that bound.
// This bound does not apply to cumulative totals over arbitrarily many layers.
class WideCount {
 public:
  // Implicit construction supports count = 0 and count += uint64_t_value.
  constexpr WideCount(std::uint64_t value = 0) noexcept
      : limbs_{value, 0, 0, 0} {}

  WideCount& operator+=(const WideCount& other) {
    std::array<std::uint64_t, 4> next{};
    unsigned __int128 carry = 0;
    for (std::size_t i = 0; i < limbs_.size(); ++i) {
      const unsigned __int128 sum =
          static_cast<unsigned __int128>(limbs_[i]) + other.limbs_[i] + carry;
      next[i] = static_cast<std::uint64_t>(sum);
      carry = sum >> 64;
    }
    // Commit only after checking the final carry; aliasing/self-add is safe,
    // and an overflow leaves the original count unchanged rather than wrapped.
    if (carry) throw std::overflow_error("WideCount addition exceeds 256 bits");
    limbs_ = next;
    return *this;
  }

  explicit constexpr operator bool() const noexcept {
    return limbs_[0] || limbs_[1] || limbs_[2] || limbs_[3];
  }

  constexpr bool operator>(std::uint64_t other) const noexcept {
    return limbs_[1] || limbs_[2] || limbs_[3] || limbs_[0] > other;
  }

  std::string decimal() const {
    if (!static_cast<bool>(*this)) return "0";
    auto quotient = limbs_;
    std::string digits;
    for (;;) {
      unsigned __int128 remainder = 0;
      bool nonzero = false;
      for (std::size_t i = quotient.size(); i-- > 0;) {
        const unsigned __int128 dividend = (remainder << 64) | quotient[i];
        quotient[i] = static_cast<std::uint64_t>(dividend / 10);
        remainder = dividend % 10;
        nonzero = nonzero || quotient[i] != 0;
      }
      digits.push_back(static_cast<char>('0' + static_cast<unsigned>(remainder)));
      if (!nonzero) break;
    }
    std::reverse(digits.begin(), digits.end());
    return digits;
  }

 private:
  std::array<std::uint64_t, 4> limbs_;
};

}  // namespace agent108

#endif
