#ifndef P196_AGENT107_CHARGE_INDEX_HPP
#define P196_AGENT107_CHARGE_INDEX_HPP

// Dense indexing of the strong neutral-exterior residue, not a graph search.
// Units-first words have coefficients in [0,2(b-1)] and a nonzero first
// coefficient. Their alternating sum must equal (-1)^length modulo b+1.
// Padding with INITIAL zeros to fixed width is an encoding only; it is not
// a neutral-suffix operation. Decoding removes those initial zeros.

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <vector>

namespace p196 {
namespace agent107 {

class ChargeIndex {
public:
  using Word = std::vector<unsigned>;
  using Count = std::uint64_t;
  class Cursor;

  // These explicit representation bounds also keep the prefix tables small.
  // A construction fails if ANY necessary per-residue count exceeds uint64.
  // No count of the entire unconstrained word universe is ever formed.
  ChargeIndex(unsigned base, unsigned width)
      : base_(base), width_(width) {
    if (base < 2 || base > 62)
      throw std::invalid_argument("supported base range is 2..62");
    if (width > 64)
      throw std::invalid_argument("supported width range is 0..64");
    modulus_ = base + 1;
    alphabet_ = 2 * base - 1;
    target_ = width % 2 ? modulus_ - 1 : 1;
    ways_.assign(width + 1, std::vector<Count>(modulus_, 0));
    prefix_.assign(width,
        std::vector<std::vector<Count>>(modulus_,
                                      std::vector<Count>(alphabet_ + 1, 0)));
    ways_[width][0] = 1;
    for (unsigned position = width; position-- > 0;) {
      for (unsigned needed = 0; needed < modulus_; ++needed) {
        auto &row = prefix_[position][needed];
        for (unsigned digit = 0; digit < alphabet_; ++digit) {
          Count block = ways_[position + 1][after(position, needed, digit)];
          row[digit + 1] = add(row[digit], block);
        }
        ways_[position][needed] = row.back();
      }
    }
    count_ = ways_[0][target_];
  }

  unsigned base() const noexcept { return base_; }
  unsigned width() const noexcept { return width_; }
  unsigned modulus() const noexcept { return modulus_; }
  Count count() const noexcept { return count_; }

  bool contains(const Word &word) const noexcept {
    if (word.empty() || word.size() > width_ || word.front() == 0) return false;
    unsigned residue = 0;
    for (std::size_t i = 0; i < word.size(); ++i) {
      unsigned digit = word[i];
      if (digit >= alphabet_) return false;
      digit %= modulus_;
      if (i % 2) residue = (residue + modulus_ - digit) % modulus_;
      else residue = (residue + digit) % modulus_;
    }
    unsigned wanted = word.size() % 2 ? modulus_ - 1 : 1;
    return residue == wanted;
  }

  // Lexicographic order of the initial-zero-padded coefficient tuple.
  // An existing word keeps the same rank when the width cap is increased.
  Count rank(const Word &word) const {
    if (!contains(word))
      throw std::invalid_argument("word is outside the charge-index domain");
    Word padded(width_, 0);
    std::copy(word.begin(), word.end(), padded.begin() + (width_ - word.size()));
    Count result = 0;
    unsigned needed = target_;
    for (unsigned position = 0; position < width_; ++position) {
      unsigned digit = padded[position];
      result = add(result, prefix_[position][needed][digit]);
      needed = after(position, needed, digit);
    }
    if (needed != 0 || result >= count_)
      throw std::logic_error("internal rank inconsistency");
    return result;
  }

  Word unrank(Count id) const { return decode(unrank_padded(id)); }

  // A stream clips its requested length to the available suffix of IDs.
  // start==count is a valid empty stream, and start>count is an error.
  // The index must outlive its cursors and must not be moved or assigned
  // while those cursors are in use, as with ordinary container iterators.
  Cursor stream(Count start, Count requested) const &;
  Cursor stream(Count start, Count requested) const && = delete;

  template<class Visitor>
  void for_each(Count start, Count requested, Visitor visitor) const;

private:
  unsigned base_, width_, modulus_ = 0, alphabet_ = 0, target_ = 0;
  Count count_ = 0;
  std::vector<std::vector<Count>> ways_;
  std::vector<std::vector<std::vector<Count>>> prefix_;

  static Count add(Count left, Count right) {
    if (right > std::numeric_limits<Count>::max() - left)
      throw std::overflow_error("per-residue count exceeds uint64 capacity");
    return left + right;
  }

  unsigned after(unsigned position, unsigned needed, unsigned digit) const noexcept {
    digit %= modulus_;
    // Remove the digit's globally signed contribution. All arithmetic here
    // is bounded by 2*modulus; no negative unsigned intermediate occurs.
    return position % 2 ? (needed + digit) % modulus_
                        : (needed + modulus_ - digit) % modulus_;
  }

  static Word decode(const Word &padded) {
    auto first = std::find_if(padded.begin(), padded.end(),
                              [](unsigned digit) { return digit != 0; });
    if (first == padded.end())
      throw std::logic_error("zero padded word cannot satisfy the residue");
    return Word(first, padded.end());
  }

  Word unrank_padded(Count id) const {
    if (id >= count_) throw std::out_of_range("rank is outside the index");
    Word result(width_, 0);
    unsigned needed = target_;
    for (unsigned position = 0; position < width_; ++position) {
      const auto &row = prefix_[position][needed];
      auto stop = std::upper_bound(row.begin(), row.end(), id);
      if (stop == row.end() || stop == row.begin())
        throw std::logic_error("internal unrank interval inconsistency");
      unsigned digit = unsigned(stop - row.begin() - 1);
      id -= row[digit];
      result[position] = digit;
      needed = after(position, needed, digit);
    }
    if (id != 0 || needed != 0)
      throw std::logic_error("internal unrank leaf inconsistency");
    return result;
  }
};

class ChargeIndex::Cursor {
public:
  bool done() const noexcept { return remaining_ == 0; }
  Count id() const noexcept { return id_; }
  Count remaining() const noexcept { return remaining_; }
  const Word &padded_word() const {
    if (done()) throw std::out_of_range("cursor is exhausted");
    return padded_;
  }
  Word word() const { return ChargeIndex::decode(padded_word()); }

  // Advance directly between accepted tuples by skipping empty completion
  // subtrees; this never scans the unconstrained (2b-1)^M word universe.
  bool advance() {
    if (done()) return false;
    --remaining_;
    ++id_; // id<=count-1 before increment, so no uint64 overflow is possible.
    if (done()) return false;
    const auto &index = *index_;
    for (unsigned position = index.width_; position-- > 0;) {
      const auto &row = index.prefix_[position][needed_[position]];
      unsigned current = padded_[position];
      Count before = row[current + 1];
      auto next = std::upper_bound(row.begin() + current + 1, row.end(), before);
      if (next == row.end()) continue;
      unsigned digit = unsigned(next - row.begin() - 1);
      padded_[position] = digit;
      needed_[position + 1] = index.after(position, needed_[position], digit);
      for (unsigned tail = position + 1; tail < index.width_; ++tail) {
        const auto &tail_row = index.prefix_[tail][needed_[tail]];
        auto stop = std::upper_bound(tail_row.begin(), tail_row.end(), Count(0));
        if (stop == tail_row.end() || stop == tail_row.begin())
          throw std::logic_error("cursor entered an empty completion subtree");
        unsigned smallest = unsigned(stop - tail_row.begin() - 1);
        padded_[tail] = smallest;
        needed_[tail + 1] = index.after(tail, needed_[tail], smallest);
      }
      if (needed_.back() != 0)
        throw std::logic_error("cursor residue inconsistency");
      return true;
    }
    throw std::logic_error("cursor exhausted before its clipped range end");
  }

private:
  friend class ChargeIndex;
  const ChargeIndex *index_;
  Count id_, remaining_;
  Word padded_;
  std::vector<unsigned> needed_;

  Cursor(const ChargeIndex &index, Count start, Count requested)
      : index_(&index), id_(start), remaining_(0) {
    if (start > index.count_)
      throw std::out_of_range("stream start is outside the index");
    remaining_ = std::min(requested, index.count_ - start);
    if (!remaining_) return;
    padded_ = index.unrank_padded(start);
    needed_.resize(index.width_ + 1);
    needed_[0] = index.target_;
    for (unsigned position = 0; position < index.width_; ++position)
      needed_[position + 1] = index.after(position, needed_[position], padded_[position]);
  }
};

inline ChargeIndex::Cursor ChargeIndex::stream(Count start, Count requested) const & {
  return Cursor(*this, start, requested);
}

template<class Visitor>
inline void ChargeIndex::for_each(Count start, Count requested, Visitor visitor) const {
  auto cursor = stream(start, requested);
  while (!cursor.done()) {
    visitor(cursor.id(), cursor.word());
    cursor.advance();
  }
}

} // namespace agent107
} // namespace p196
#endif
