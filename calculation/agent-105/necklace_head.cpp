// Independent binary-necklace census and exterior lowest-coefficient filter.
// Derived from neutral_band_search.py nextB; no primary agent filter is used.
// Compile: g++ -O3 -std=c++17 -Wall -Wextra -pedantic necklace_head.cpp -o necklace_head
// Run: ./necklace_head 23 p23-head-survivors.txt
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

class HeadRelation {
    static constexpr int states = 18;
    std::array<std::array<uint32_t, states>, 2> edge{};
    std::array<std::vector<uint32_t>, 2> advance;
public:
    HeadRelation() {
        for (int x = 1; x <= states; ++x) for (int c = 0; c <= 1; ++c) {
            const int g = (x+c)/10;
            const int y = g == 0 ? 2*x+c : x%10+1;
            if (g < 0 || g > 1 || y < 1 || y > states)
                throw std::logic_error("invalid exact head transition");
            edge[g][x-1] |= uint32_t{1} << (y-1);
        }
        for (int g = 0; g <= 1; ++g) {
            advance[g].assign(uint32_t{1} << states, 0);
            for (uint32_t mask = 1; mask < advance[g].size(); ++mask) {
                const unsigned bit = __builtin_ctz(mask);
                advance[g][mask] = advance[g][mask & (mask-1)] | edge[g][bit];
            }
        }
    }

    bool accepts(const std::string& word) const {
        for (int x = 1; x <= states; ++x) {
            const uint32_t start = uint32_t{1} << (x-1);
            uint32_t current = start;
            for (char ch : word) {
                current = advance[ch-'0'][current];
                if (!current) break;
            }
            if (current & start) return true;
        }
        return false;
    }

    std::vector<int> closed_heads(const std::string& word) const {
        std::vector<int> out;
        for (int x = 1; x <= states; ++x) {
            const uint32_t start = uint32_t{1} << (x-1);
            uint32_t current = start;
            for (char ch : word) current = advance[ch-'0'][current];
            if (current & start) out.push_back(x);
        }
        return out;
    }

    std::vector<int> witness(const std::string& word, int x) const {
        std::vector<uint32_t> forward(word.size()+1);
        forward[0] = uint32_t{1} << (x-1);
        for (size_t t = 0; t < word.size(); ++t)
            forward[t+1] = advance[word[t]-'0'][forward[t]];
        if (!(forward.back() & forward[0])) return {};
        std::vector<int> path(word.size()+1);
        path.back() = x;
        for (size_t t = word.size(); t-- > 0;) {
            bool found = false;
            for (int previous = 1; previous <= states; ++previous) {
                if ((forward[t] & (uint32_t{1} << (previous-1))) &&
                    (edge[word[t]-'0'][previous-1] & (uint32_t{1} << (path[t+1]-1)))) {
                    path[t] = previous;
                    found = true;
                    break;
                }
            }
            if (!found) throw std::logic_error("witness backtracking failed");
        }
        if (path.front() != x) throw std::logic_error("witness did not close");
        return path;
    }

    static std::vector<int> witness_carries(const std::string& word, const std::vector<int>& path) {
        std::vector<int> carries;
        for (size_t t = 0; t < word.size(); ++t) {
            bool found = false;
            for (int c = 0; c <= 1; ++c) {
                const int x = path.at(t), g = (x+c)/10;
                const int y = g == 0 ? 2*x+c : x%10+1;
                if (g == word[t]-'0' && y == path.at(t+1)) {
                    carries.push_back(c);
                    found = true;
                    break;
                }
            }
            if (!found) throw std::logic_error("witness replay failed");
        }
        return carries;
    }
};

std::string least_rotation(const std::string& word) {
    std::string best = word;
    for (size_t i = 1; i < word.size(); ++i)
        best = std::min(best, word.substr(i)+word.substr(0,i));
    return best;
}

template<class T> void print_array(const std::vector<T>& a) {
    std::cout << '[';
    for (size_t i = 0; i < a.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << a[i];
    }
    std::cout << ']';
}

class NecklaceCensus {
    int n;
    std::vector<int> digits;
    const HeadRelation& relation;
    void visit(int t, int period) {
        if (t > n) {
            if (n%period) return;
            std::string word;
            int weight = 0;
            for (int i = 1; i <= n; ++i) {
                word.push_back(static_cast<char>('0'+digits[i]));
                weight += digits[i];
            }
            ++necklaces[weight];
            if (relation.accepts(word)) {
                ++survivors[weight];
                words[weight].push_back(word);
            }
            return;
        }
        digits[t] = digits[t-period];
        visit(t+1, period);
        for (int next = digits[t-period]+1; next <= 1; ++next) {
            digits[t] = next;
            visit(t+1, t);
        }
    }
public:
    std::vector<uint64_t> necklaces, survivors;
    std::vector<std::vector<std::string>> words;
    NecklaceCensus(int period, const HeadRelation& rel)
      : n(period), digits(period+1), relation(rel), necklaces(period+1),
        survivors(period+1), words(period+1) {}
    void run() { visit(1,1); }
    void write(const std::string& path) {
        std::ofstream out(path);
        if (!out) throw std::runtime_error("cannot create manifest");
        for (auto& group : words) {
            std::sort(group.begin(), group.end());
            for (const auto& word : group) {
                if (word != least_rotation(word))
                    throw std::logic_error("noncanonical generated necklace");
                out << word << '\n';
            }
        }
        if (!out) throw std::runtime_error("manifest write failed");
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::invalid_argument("usage: necklace_head PERIOD MANIFEST");
        size_t end = 0;
        const int n = std::stoi(argv[1], &end);
        if (end != std::string(argv[1]).size() || n < 1 || n > 25)
            throw std::invalid_argument("PERIOD must be an integer in 1..25");
        HeadRelation relation;
        if (relation.accepts(std::string(n,'0')))
            throw std::logic_error("positive head cannot close under only g=0");
        if (!relation.accepts("11100010000") || !relation.accepts("100010001000"))
            throw std::logic_error("known p11/p12 control rejected");
        NecklaceCensus census(n, relation);
        census.run();
        census.write(argv[2]);
        uint64_t total = 0, kept = 0;
        for (auto x : census.necklaces) total += x;
        for (auto x : census.survivors) kept += x;
        std::cout << "{\"status\":\"COMPLETE\",\"period\":" << n
                  << ",\"all_necklaces\":" << total << ",\"survivors\":" << kept
                  << ",\"necklaces_by_weight\":";
        print_array(census.necklaces);
        std::cout << ",\"survivors_by_weight\":";
        print_array(census.survivors);
        std::cout << ",\"controls\":{\"p11\":true,\"p12\":true,\"all_zero\":false}"
                  << ",\"hard_word\":{\"g\":\"10101010101001001110000\",\"canonical\":\""
                  << least_rotation("10101010101001001110000") << "\",\"closed_heads\":";
        const std::string hard = "10101010101001001110000";
        auto starts = relation.closed_heads(hard);
        print_array(starts);
        std::cout << ",\"head_path\":";
        const auto path = starts.empty() ? std::vector<int>{} : relation.witness(hard, starts.front());
        print_array(path);
        std::cout << ",\"inward_carries\":";
        print_array(starts.empty() ? std::vector<int>{} : HeadRelation::witness_carries(hard,path));
        std::cout << "}}\n";
    } catch (const std::exception& ex) {
        std::cerr << "ERROR: " << ex.what() << '\n';
        return 2;
    }
}
