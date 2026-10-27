// Batch/one-shot interface for the header-only exact charge index.
// Build: c++ -O2 -std=c++17 charge_index.cpp -o /tmp/charge-index-107
// One shot: /tmp/charge-index-107 10 8 count
// Batch: /tmp/charge-index-107 10 8, then one command per stdin line.
// Commands: count; contains [B]; rank [B]; unrank N;
// enumerate START LIMIT; benchmark START LIMIT; roundtrip SAMPLES SEED.
// Every command emits one JSON record. Invalid commands emit ok:false,
// processing continues, and the final exit code is 2 if any command failed.

#include "charge_index.hpp"
#include <chrono>
#include <cctype>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>

using p196::agent107::ChargeIndex;
using Count107 = ChargeIndex::Count;

static std::string trim107(const std::string &s) {
  auto first = s.find_first_not_of(" \t\r\n");
  if (first == std::string::npos) return "";
  return s.substr(first, s.find_last_not_of(" \t\r\n") - first + 1);
}

static Count107 integer107(const std::string &token) {
  if (token.empty()) throw std::invalid_argument("missing unsigned integer");
  Count107 value = 0, maximum = std::numeric_limits<Count107>::max();
  for (char c : token) {
    if (c < '0' || c > '9') throw std::invalid_argument("invalid unsigned integer");
    unsigned digit = unsigned(c - '0');
    if (value > maximum/10 || (value == maximum/10 && digit > maximum%10))
      throw std::overflow_error("integer exceeds uint64 capacity");
    value = 10*value + digit;
  }
  return value;
}

static std::vector<Count107> numbers107(const std::string &rest, std::size_t count) {
  std::istringstream input(rest);
  std::string token;
  std::vector<Count107> values;
  while (input >> token) values.push_back(integer107(token));
  if (values.size() != count) throw std::invalid_argument("wrong number of command arguments");
  return values;
}

static ChargeIndex::Word word107(const std::string &input) {
  std::string s = trim107(input);
  if (s.size() < 2 || s.front() != '[' || s.back() != ']')
    throw std::invalid_argument("word must be a bracketed integer list");
  std::string body = trim107(s.substr(1, s.size()-2));
  ChargeIndex::Word result;
  if (body.empty()) return result;
  std::size_t from = 0;
  for (;;) {
    std::size_t comma = body.find(',', from);
    std::string token = trim107(body.substr(from, comma == std::string::npos ? comma : comma-from));
    Count107 digit = integer107(token);
    if (digit > std::numeric_limits<unsigned>::max())
      throw std::overflow_error("coefficient exceeds unsigned capacity");
    result.push_back(unsigned(digit));
    if (comma == std::string::npos) break;
    from = comma + 1;
  }
  return result;
}

static void print_word107(std::ostream &out, const ChargeIndex::Word &word) {
  out << '[';
  for (std::size_t i=0;i<word.size();++i) { if(i)out<<',';out<<word[i]; }
  out << ']';
}

static Count107 checksum107(Count107 previous, Count107 id, const ChargeIndex::Word &word) {
  previous ^= id;
  for (unsigned digit : word) {
    previous = (previous << 7) | (previous >> 57);
    previous ^= Count107(digit) + 1;
  }
  return previous;
}

static std::string command107(const ChargeIndex &index, const std::string &line) {
  std::string input = trim107(line);
  auto split = input.find_first_of(" \t");
  std::string command = input.substr(0, split);
  std::string rest = split == std::string::npos ? "" : trim107(input.substr(split));
  std::ostringstream out;
  out << std::setprecision(9) << "{\"ok\":true,\"command\":\"";
  if (command == "count") {
    numbers107(rest,0);
    out << "count\",\"base\":" << index.base() << ",\"width\":" << index.width()
        << ",\"modulus\":" << index.modulus() << ",\"count\":" << index.count();
  } else if (command == "contains" || command == "rank") {
    auto word = word107(rest);
    out << command << "\",";
    if (command == "contains") out << "\"contains\":" << (index.contains(word)?"true":"false");
    else out << "\"rank\":" << index.rank(word);
  } else if (command == "unrank") {
    Count107 id = numbers107(rest,1)[0];
    auto word = index.unrank(id);
    out << "unrank\",\"rank\":" << id << ",\"B\":";
    print_word107(out,word);
  } else if (command == "enumerate" || command == "benchmark") {
    auto values = numbers107(rest,2);
    Count107 start=values[0], requested=values[1];
    auto cursor = index.stream(start,requested);
    Count107 actual=cursor.remaining();
    Count107 permitted=command=="enumerate"?100000:1000000;
    if(actual>permitted)throw std::invalid_argument("requested output/benchmark range exceeds CLI limit");
    out << command << "\",\"start\":"<<start<<",\"requested_limit\":"<<requested
        <<",\"total\":"<<index.count();
    if(command=="enumerate") {
      out<<",\"emitted\":"<<actual<<",\"items\":[";
      bool comma=false;
      while(!cursor.done()) {
        if(comma)out<<',';
        comma=true;
        out<<"{\"rank\":"<<cursor.id()<<",\"B\":";
        print_word107(out,cursor.word());out<<'}';
        cursor.advance();
      }
      out<<']';
    } else {
      auto began=std::chrono::steady_clock::now();
      Count107 checksum=0, processed=0;
      while(!cursor.done()) {
        auto word=cursor.word();
        if(index.rank(word)!=cursor.id())throw std::logic_error("benchmark rank disagreement");
        checksum=checksum107(checksum,cursor.id(),word);
        ++processed;cursor.advance();
      }
      double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
      out<<",\"processed\":"<<processed<<",\"seconds\":"<<seconds<<",\"checksum\":"<<checksum;
    }
  } else if (command == "roundtrip") {
    auto values=numbers107(rest,2);
    Count107 samples=values[0],seed=values[1];
    if(samples>1000000)throw std::invalid_argument("roundtrip sample limit is 1000000");
    if(samples && !index.count())throw std::invalid_argument("cannot sample an empty index");
    std::mt19937_64 random(seed);
    Count107 checksum=0;
    auto began=std::chrono::steady_clock::now();
    for(Count107 i=0;i<samples;++i) {
      Count107 id=random()%index.count();
      auto word=index.unrank(id);
      if(index.rank(word)!=id)throw std::logic_error("random rank/unrank disagreement");
      checksum=checksum107(checksum,id,word);
    }
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
    out<<"roundtrip\",\"samples\":"<<samples<<",\"seed\":"<<seed<<",\"total\":"<<index.count()
       <<",\"seconds\":"<<seconds<<",\"checksum\":"<<checksum;
  } else throw std::invalid_argument("unknown command");
  out << '}';
  return out.str();
}

static void error107(const std::exception &error) {
  // All emitted error messages are fixed library strings, never user input.
  std::cout << "{\"ok\":false,\"error\":\"" << error.what() << "\"}\n";
}

int main(int argc,char **argv) {
  try {
    if(argc<3)throw std::invalid_argument("usage: BASE WIDTH [COMMAND ...]; otherwise commands come from stdin");
    Count107 base=integer107(argv[1]),width=integer107(argv[2]);
    if(base>std::numeric_limits<unsigned>::max() || width>std::numeric_limits<unsigned>::max())
      throw std::invalid_argument("base or width exceeds supported representation");
    ChargeIndex index{unsigned(base),unsigned(width)};
    bool failed=false;
    auto execute=[&](const std::string &line) {
      try {std::cout<<command107(index,line)<<'\n'<<std::flush;}
      catch(const std::exception &error){error107(error);failed=true;}
    };
    if(argc>3) {
      std::string line;
      for(int i=3;i<argc;++i){if(i>3)line+=' ';line+=argv[i];}
      execute(line);
    } else {
      std::string line;
      while(std::getline(std::cin,line))execute(line);
    }
    return failed?2:0;
  } catch(const std::exception &error) {error107(error);return 2;}
}
