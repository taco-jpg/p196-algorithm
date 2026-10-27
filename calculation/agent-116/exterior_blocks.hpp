#ifndef AGENT116_EXTERIOR_BLOCKS_HPP
#define AGENT116_EXTERIOR_BLOCKS_HPP

// Exact local tiles for an exterior temporal block g = 1,0,...,0.
// This file generates tiles only; it does not implement a language or DFA.
//
// A block starts at the actual global overflow phase `phase` and has length
// 1..5. Its symbol stores two carry-bit vectors L,H and one lag digit Y:
//     cfg = Lmask | (Hmask << length) | (Y << (2*length)).
// Local time increases with the bit index. Valid cfg values form exactly
// [0, base*4^length). Input and output symbols retain the same phase type.
//
// At local time t, for coefficient x and reverse incoming carry q, require
//     floor((x+q)/base) = H_in[t].
// Write d=(x+L_in[t])%base and r=(x+q)%base. The output carries are
//     L_out[t]=floor((x+L_in[t])/base), H_out[t]=q.
// The first step has overflow: x_next=d+Y_in and Y_out=r.
// Every later step has no overflow: x_next=d+r.
// All used coefficients and the exiting coefficient lie in [0,2*(base-1)].
// FIRST additionally requires each coefficient USED inside this block >0.
// It does not impose positivity on the exiting coefficient: that coefficient
// belongs to the next block, whose FIRST check (or cyclic closure) enforces it.
// No temporal closure is imposed within one block; adjoining tiles match bonds.
//
// A terminal target associated to fixed carry bits E is
//     L=E, H=1-E, Y=(base-1)*E[0].
// The initial boundary has L=0,H=(1,0,...,0),Y=1. Neutral terminal
// padding is represented by the self-loop with every coefficient base-1.
// These formulas are the local decomposition of the independently authored
// explicit-tuple engine; there is no dependency on another author's solver.

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <unordered_map>
#include <utility>
#include <vector>

namespace agent116::blocks {

constexpr std::size_t max_block_length = 5;

struct BlockSpec {
    std::uint16_t phase; // actual global start phase, not the block's ordinal
    std::uint8_t length;
};

struct Symbol {
    std::uint16_t phase;
    std::uint32_t cfg;
    bool operator==(const Symbol& other) const {
        return phase == other.phase && cfg == other.cfg;
    }
    bool operator!=(const Symbol& other) const { return !(*this == other); }
};

struct Components {
    std::uint8_t low_mask;
    std::uint8_t high_mask;
    std::uint8_t lag;
};

struct Tile {
    Symbol output;
    std::uint8_t ending;
    // Only positions [0,length) are used; the remainder is deterministically 0.
    std::array<std::uint8_t, max_block_length> coefficients{};
};

struct Statistics {
    std::uint64_t cache_requests = 0;
    std::uint64_t cache_hits = 0;
    std::uint64_t generated_queries = 0;
    std::uint64_t generated_tiles = 0;
    std::uint64_t recursive_nodes = 0;
};

class Generator {
    const std::uint32_t radix_;
    const BlockSpec block_;
    const std::uint32_t mask_;
    Statistics statistics_;
    std::unordered_map<std::uint32_t, std::vector<Tile>> cache_;
    std::size_t cached_tiles_ = 0;

    static std::uint32_t checked_mask(std::uint32_t radix, BlockSpec block) {
        if (radix < 2 || radix > 32)
            throw std::invalid_argument("block base must be 2..32");
        if (block.length < 1 || block.length > max_block_length)
            throw std::invalid_argument("block length must be 1..5");
        return (1U << block.length) - 1U;
    }

    void check_symbol(Symbol symbol) const {
        if (symbol.phase != block_.phase)
            throw std::invalid_argument("block symbol has the wrong phase type");
        if (symbol.cfg >= config_count())
            throw std::invalid_argument("block configuration outside its alphabet");
    }

    void walk(const Components& input, std::uint32_t t, std::uint32_t coefficient,
              bool first, std::uint32_t low_out, std::uint32_t high_out,
              std::uint32_t lag_out, std::array<std::uint8_t, max_block_length>& columns,
              std::vector<Tile>& result) {
        if (t >= block_.length || t >= max_block_length)
            throw std::logic_error("local tile recursion escaped the block");
        ++statistics_.recursive_nodes;
        if (coefficient > maximum_coefficient()) return;
        if (first && coefficient == 0) return;
        columns[t] = static_cast<std::uint8_t>(coefficient);
        const std::uint32_t low_in = (input.low_mask >> t) & 1U;
        const std::uint32_t high_in = (input.high_mask >> t) & 1U;
        const std::uint32_t low_total = coefficient + low_in;
        const std::uint32_t digit = low_total % radix_;
        const std::uint32_t next_low = low_out | ((low_total / radix_) << t);
        for (std::uint32_t inward = 0; inward <= 1; ++inward) {
            const std::uint32_t high_total = coefficient + inward;
            if (high_total / radix_ != high_in) continue;
            const std::uint32_t reverse_digit = high_total % radix_;
            const std::uint32_t next_high = high_out | (inward << t);
            const std::uint32_t next_lag = t == 0 ? reverse_digit : lag_out;
            const std::uint32_t following = digit + (t == 0 ? input.lag : reverse_digit);
            if (following > maximum_coefficient()) continue;
            if (t + 1 == block_.length) {
                const Symbol output = encode(next_low, next_high, next_lag);
                result.push_back({output, static_cast<std::uint8_t>(following), columns});
            } else {
                walk(input, t + 1, following, first, next_low, next_high, next_lag,
                     columns, result);
            }
        }
    }

public:
    Generator(std::uint32_t radix, BlockSpec block)
        : radix_(radix), block_(block), mask_(checked_mask(radix, block)) {}

    std::uint32_t base() const { return radix_; }
    BlockSpec spec() const { return block_; }
    std::uint32_t config_count() const { return radix_ << (2U * block_.length); }
    std::uint32_t maximum_coefficient() const { return 2U * (radix_ - 1U); }

    Symbol encode(std::uint32_t low, std::uint32_t high, std::uint32_t lag) const {
        if (low > mask_ || high > mask_ || lag >= radix_)
            throw std::invalid_argument("invalid block carry masks or lag digit");
        return {block_.phase, low | (high << block_.length) | (lag << (2U * block_.length))};
    }

    Components decode(Symbol symbol) const {
        check_symbol(symbol);
        return {static_cast<std::uint8_t>(symbol.cfg & mask_),
                static_cast<std::uint8_t>((symbol.cfg >> block_.length) & mask_),
                static_cast<std::uint8_t>(symbol.cfg >> (2U * block_.length))};
    }

    Symbol initial_symbol() const { return encode(0, 1, 1); }

    Symbol terminal_symbol(std::uint32_t e_mask) const {
        if (e_mask > mask_) throw std::invalid_argument("terminal E mask outside block");
        return encode(e_mask, mask_ ^ e_mask, (radix_ - 1U) * (e_mask & 1U));
    }

    // Uncached path for exhaustive local oracles. Invalid inputs are rejected;
    // a valid FIRST query with starting=0 simply has no tiles.
    std::vector<Tile> generate(Symbol input, std::uint32_t starting, bool first) {
        const Components components = decode(input);
        if (starting > maximum_coefficient())
            throw std::invalid_argument("starting coefficient outside allowed range");
        ++statistics_.generated_queries;
        std::vector<Tile> result;
        std::array<std::uint8_t, max_block_length> columns{};
        walk(components, 0, starting, first, 0, 0, 0, columns, result);
        std::sort(result.begin(), result.end(), [](const Tile& a, const Tile& b) {
            if (a.output.cfg != b.output.cfg) return a.output.cfg < b.output.cfg;
            if (a.ending != b.ending) return a.ending < b.ending;
            return a.coefficients < b.coefficients;
        });
        statistics_.generated_tiles += result.size();
        return result;
    }

    // Cache indexed by the exact (source cfg, incoming coefficient, FIRST)
    // triple. The Generator itself fixes base, length and actual phase type.
    // References remain valid across unordered_map rehashes; clear_cache()
    // invalidates them. Memory/cancellation budgets are the caller's concern.
    const std::vector<Tile>& tiles(Symbol input, std::uint32_t starting, bool first) {
        check_symbol(input);
        if (starting > maximum_coefficient())
            throw std::invalid_argument("starting coefficient outside allowed range");
        ++statistics_.cache_requests;
        const std::uint32_t key = 2U * (input.cfg * (maximum_coefficient() + 1U) + starting)
                                  + std::uint32_t(first);
        const auto found = cache_.find(key);
        if (found != cache_.end()) {
            ++statistics_.cache_hits;
            return found->second;
        }
        auto produced = generate(input, starting, first);
        cached_tiles_ += produced.size();
        return cache_.emplace(key, std::move(produced)).first->second;
    }

    const Statistics& statistics() const { return statistics_; }
    std::size_t cached_queries() const { return cache_.size(); }
    std::size_t cached_tiles() const { return cached_tiles_; }
    void clear_cache() { cache_.clear(); cached_tiles_ = 0; }
};

} // namespace agent116::blocks

#endif // AGENT116_EXTERIOR_BLOCKS_HPP
