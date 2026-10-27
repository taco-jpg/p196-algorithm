// Local-tile enumeration interface for independent oracle comparison.
// With --dump, stdout contains ONLY lines: source_cfg start target_cfg end.
// The JSON summary is then printed on stderr. Without --dump it is on stdout.
#include "exterior_blocks.hpp"
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>

int main(int argc, char** argv) {
    try {
        if (argc < 3) throw std::invalid_argument(
            "usage: exterior_blocks BASE LENGTH [--first] [--dump] [--witness]");
        auto read_integer = [](const std::string& text) -> std::uint32_t {
            if (text.empty() || text.find_first_not_of("0123456789") != std::string::npos)
                throw std::invalid_argument("invalid integer argument");
            const auto value = std::stoull(text);
            if (value > std::numeric_limits<std::uint32_t>::max())
                throw std::invalid_argument("integer argument too large");
            return static_cast<std::uint32_t>(value);
        };
        const auto base = read_integer(argv[1]);
        const auto length = read_integer(argv[2]);
        if (length < 1 || length > agent116::blocks::max_block_length)
            throw std::invalid_argument("block length must be 1..5");
        bool first = false, dump = false, witness = false;
        for (int argument = 3; argument < argc; ++argument) {
            const std::string flag = argv[argument];
            if (flag == "--first") first = true;
            else if (flag == "--dump") dump = true;
            else if (flag == "--witness") witness = true;
            else throw std::invalid_argument("unknown flag: " + flag);
        }
        agent116::blocks::Generator generator(base, {0, static_cast<std::uint8_t>(length)});
        const auto before = std::chrono::steady_clock::now();
        std::uint64_t nonempty = 0, zero_ending = 0;
        for (std::uint32_t cfg = 0; cfg < generator.config_count(); ++cfg) {
            for (std::uint32_t starting = 0; starting <= generator.maximum_coefficient(); ++starting) {
                const auto tiles = generator.generate({0, cfg}, starting, first);
                nonempty += !tiles.empty();
                for (const auto& tile : tiles) {
                    zero_ending += tile.ending == 0;
                    if (!dump) continue;
                    std::cout << cfg << ' ' << starting << ' ' << tile.output.cfg << ' '
                              << unsigned(tile.ending);
                    if (witness) {
                        for (std::size_t t = 0; t < length; ++t)
                            std::cout << ' ' << unsigned(tile.coefficients[t]);
                    }
                    std::cout << '\n';
                }
            }
        }
        const auto& statistics = generator.statistics();
        std::ostream& summary = dump ? std::cerr : std::cout;
        summary << "{\"base\":" << base << ",\"length\":" << length
                << ",\"first\":" << (first ? "true" : "false")
                << ",\"configurations\":" << generator.config_count()
                << ",\"queries\":" << statistics.generated_queries
                << ",\"nonempty_queries\":" << nonempty
                << ",\"tiles\":" << statistics.generated_tiles
                << ",\"zero_ending_tiles\":" << zero_ending
                << ",\"recursive_nodes\":" << statistics.recursive_nodes
                << ",\"seconds\":" << std::chrono::duration<double>(
                    std::chrono::steady_clock::now() - before).count() << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "exterior_blocks: " << error.what() << '\n';
        return 2;
    }
}
