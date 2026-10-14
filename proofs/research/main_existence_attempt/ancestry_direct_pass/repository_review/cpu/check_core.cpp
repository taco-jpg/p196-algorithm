// Independent schoolbook oracle for the upstream bit-plane primitive.
// Build with -I pointing to the inspected, unmodified v8 source directory.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include "bits_core.h"

static std::string oracle(const std::string& x) {
  std::string y(x.size() + 1, '0');
  unsigned carry = 0;
  for (size_t j = 0; j < x.size(); ++j) {
    unsigned sum = unsigned(x[j] - '0') + unsigned(x[x.size()-1-j] - '0') + carry;
    y[x.size()-j] = char('0' + sum % 10);
    carry = sum / 10;
  }
  y[0] = char('0' + carry);
  return carry ? y : y.substr(1);
}

static void check(const std::string& x) {
  const int n = int(x.size()), W = (n + 64) / 64 + 4;
  std::vector<bits::u32> input(5 * W), output(5 * W);
  for (int j = 0; j < (n + 1)/2; ++j) {
    unsigned q = unsigned(x[j] - '0') + unsigned(x[n-1-j] - '0');
    for (int bit = 0; bit < 5; ++bit)
      input[bit*W + j/32] |= ((q >> bit) & 1u) << (j%32);
  }
  std::string next = oracle(x);
  bool mismatch = false;
  for (int w = 0; w < W; ++w) {
    int g = -1;
    mismatch |= bits::step_word(input.data(), output.data(), W, n, w, &g) != 0;
    if (g != int(next.size()) - n) throw std::runtime_error("growth mismatch");
  }
  for (int j = 0; j < (int(next.size()) + 1)/2; ++j) {
    unsigned got = 0;
    for (int bit = 0; bit < 5; ++bit)
      got |= ((output[bit*W + j/32] >> (j%32)) & 1u) << bit;
    unsigned expected = unsigned(next[j]-'0') + unsigned(next[next.size()-1-j]-'0');
    if (got != expected) throw std::runtime_error("pair-state mismatch");
  }
  bool pal = std::equal(next.begin(), next.end(), next.rbegin());
  if (mismatch == pal) throw std::runtime_error("palindrome-vote mismatch");
}

int main() {
  std::uint64_t count = 0;
  for (unsigned n = 1; n < 1000000; ++n) { check(std::to_string(n)); ++count; }
  std::mt19937 rng(1962026);
  std::vector<int> lengths = {31,32,33,63,64,65,127,128,129,255,256,257,
                             511,512,513,1023,1024,1025,2049,4097};
  for (int n : lengths) {
    for (int repeat = 0; repeat < 25; ++repeat) {
      std::string x(n, '0');
      for (char& d : x) d = char('0' + rng()%10);
      x[0] = char('1' + rng()%9);
      check(x); ++count;
    }
    // A carry-propagating 9-run across every internal word boundary.
    for (int center : {0, 8, 10, 18}) {
      std::string x(n, '0');
      for (int j = 0; j < (n+1)/2; ++j) {
        int q = j == (n+1)/2 - 1 ? center : 9;
        int left = std::max(0, q-9);
        if (j == 0) left = std::max(1, left);
        if (j == n-1-j) left = q/2;
        x[j] = char('0' + left);
        x[n-1-j] = char('0' + q-left);
      }
      check(x); ++count;
    }
  }
  std::cout << "{\"status\":\"PASS\",\"checked_inputs\":" << count
            << ",\"exhaustive_positive_inputs_below\":1000000,"
            << "\"long_input_lengths\":20,\"random_long_inputs\":500,"
            << "\"full_width_carry_run_inputs\":80,"
            << "\"checks\":[\"pair_state\",\"growth\",\"palindrome_vote\"]}\n";
}
