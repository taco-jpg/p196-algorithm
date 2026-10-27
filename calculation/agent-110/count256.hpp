#ifndef AGENT110_COUNT256_HPP
#define AGENT110_COUNT256_HPP

// Exact unsigned 256-bit cardinalities, without an external integer library.
// Four least-significant-first limbs; checked arithmetic never changes the
// operand on overflow/underflow. The 128-bit temporary is used only for
// one-limb arithmetic and division, never as the complete count.

#include <algorithm>
#include <array>
#include <cstdint>
#include <stdexcept>
#include <string>

namespace agent110 {

class Count256 {
    std::array<std::uint64_t, 4> words_{};
    __extension__ typedef unsigned __int128 Wide;

public:
    constexpr Count256(std::uint64_t value = 0) : words_{{value, 0, 0, 0}} {}

    static Count256 from_limbs(const std::array<std::uint64_t, 4>& words) {
        Count256 result;
        result.words_ = words;
        return result;
    }

    const std::array<std::uint64_t, 4>& limbs() const { return words_; }

    explicit operator bool() const {
        return words_[0] != 0 || words_[1] != 0 || words_[2] != 0 || words_[3] != 0;
    }

    friend bool operator==(const Count256& a, const Count256& b) {
        return a.words_ == b.words_;
    }
    friend bool operator!=(const Count256& a, const Count256& b) { return !(a == b); }
    friend bool operator<(const Count256& a, const Count256& b) {
        for (unsigned j = 4; j-- > 0; )
            if (a.words_[j] != b.words_[j]) return a.words_[j] < b.words_[j];
        return false;
    }
    friend bool operator>(const Count256& a, const Count256& b) { return b < a; }
    friend bool operator<=(const Count256& a, const Count256& b) { return !(b < a); }
    friend bool operator>=(const Count256& a, const Count256& b) { return !(a < b); }

    Count256& operator+=(const Count256& other) {
        std::array<std::uint64_t, 4> result{};
        Wide carry = 0;
        for (unsigned j = 0; j < 4; ++j) {
            const Wide total = Wide(words_[j]) + other.words_[j] + carry;
            result[j] = static_cast<std::uint64_t>(total);
            carry = total >> 64;
        }
        if (carry != 0) throw std::overflow_error("unsigned256 addition overflow");
        words_ = result;
        return *this;
    }

    Count256& operator-=(const Count256& other) {
        if (*this < other) throw std::underflow_error("unsigned256 subtraction underflow");
        std::array<std::uint64_t, 4> result{};
        Wide borrow = 0;
        for (unsigned j = 0; j < 4; ++j) {
            const Wide subtrahend = Wide(other.words_[j]) + borrow;
            const Wide value = words_[j];
            if (value < subtrahend) {
                result[j] = static_cast<std::uint64_t>((Wide(1) << 64) + value - subtrahend);
                borrow = 1;
            } else {
                result[j] = static_cast<std::uint64_t>(value - subtrahend);
                borrow = 0;
            }
        }
        if (borrow != 0) throw std::logic_error("unsigned256 subtraction invariant");
        words_ = result;
        return *this;
    }

    friend Count256 operator+(Count256 a, const Count256& b) { a += b; return a; }
    friend Count256 operator-(Count256 a, const Count256& b) { a -= b; return a; }

    std::uint32_t divmod(std::uint32_t divisor) {
        if (divisor == 0) throw std::invalid_argument("unsigned256 division by zero");
        std::array<std::uint64_t, 4> quotient{};
        Wide remainder = 0;
        for (unsigned j = 4; j-- > 0; ) {
            const Wide partial = (remainder << 64) | words_[j];
            quotient[j] = static_cast<std::uint64_t>(partial / divisor);
            remainder = partial % divisor;
        }
        words_ = quotient;
        return static_cast<std::uint32_t>(remainder);
    }

    std::string decimal() const {
        Count256 remaining = *this;
        if (!remaining) return "0";
        std::string result;
        result.reserve(78);
        while (remaining) result += static_cast<char>('0' + remaining.divmod(10));
        std::reverse(result.begin(), result.end());
        return result;
    }
};

} // namespace agent110

#endif
