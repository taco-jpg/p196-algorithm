// Agent 118: all positive block counts for decimal saturated exterior returns.
// Automata operations: pinned Agent118 PR399 center_regular.cpp, reused below.
// Arithmetic tiles: pinned Agent108 PR386, itself derived from original bauto.
// No repeated-block equality of e or B is imposed.  Only the overflow clock
// has period four.  Terminal words outside the three known p12 e languages are
// reconstructed and replayed before a NEW_DRIVER completion can be printed.
#include "regular118_core.hpp"
#include "tiles108_core.hpp"
#include <functional>
#include <iostream>

namespace BREG118 {
using namespace REG118;
using Tile = Tiles108::Tile;
using Table = array<Tiles108::Local, 2560>;
static Table reverseTiles;
static const char* activeStage = "initialization";

const array<Label, 3> KNOWN{2469, 2409, 90};  // L masks 5,9,10; each whole cycle separately

void checkSymbol(Label symbol) {
  if (symbol >= 2560) undecided118("exterior_regular_bad_symbol");
}
bool terminal(Label symbol) { checkSymbol(symbol); return Tiles108::terminal_symbol(symbol); }

DFA words(const vector<Label>& alphabet, int blocks, Budget& budget) {
  DFA out; budget.state(blocks ? size_t(blocks) + 1 : 2);
  out.q.resize(blocks ? size_t(blocks) + 1 : 2); uint64_t edges = 0;
  for (size_t q = 0; q + 1 < out.q.size(); ++q) for (Label a : alphabet) {
    checkSymbol(a); budget.edge(++edges); out.q[q].arcs.push_back({a, Id(q + 1)});
  }
  out.q.back().accept = true;
  if (!blocks) for (Label a : alphabet) { budget.edge(++edges); out.q.back().arcs.push_back({a, 1}); }
  for (State& q : out.q) sort(q.arcs.begin(), q.arcs.end());
  return out;
}

DFA knownLanguage(Budget& budget) {
  DFA out; budget.state(10); out.q.resize(10);
  for (int first = 0; first < 3; ++first) {
    out.q[0].arcs.push_back({KNOWN[first], Id(1 + 3 * first + 1)});
    for (int position = 0; position < 3; ++position) {
      State& q = out.q[1 + 3 * first + position]; q.accept = position == 0;
      q.arcs.push_back({KNOWN[(first + position) % 3], Id(1 + 3 * first + (position + 1) % 3)});
    }
  }
  sort(out.q[0].arcs.begin(), out.q[0].arcs.end()); budget.edge(12); return out;
}

Id advance(const DFA& dfa, Id q, Label a) {
  if (q == DEAD) return DEAD;
  const vector<Arc>& arcs = dfa.q[q].arcs;
  auto it = lower_bound(arcs.begin(), arcs.end(), Arc{a, 0});
  return it != arcs.end() && it->first == a ? it->second : DEAD;
}

DFA badSeed(const DFA& allowed, int blocks, Budget& budget) {
  vector<Label> alphabet;
  for(int s=0;s<2560;++s)if(terminal(s))alphabet.push_back(s);
  DFA candidate=words(alphabet,blocks,budget),out;
  vector<pair<Id,Id>> product;unordered_map<uint64_t,Id> known;
  auto intern=[&](Id x,Id y){
    uint64_t key=(uint64_t(x)<<32)|y;auto found=known.find(key);if(found!=known.end())return found->second;
    budget.state(out.q.size()+1);Id id=out.q.size();known.emplace(key,id);product.push_back({x,y});
    bool accept=candidate.q[x].accept&&!(y!=DEAD&&allowed.q[y].accept);
    out.q.push_back({accept,{}});return id;
  };
  out.start=intern(candidate.start,allowed.start);uint64_t edges=0;
  for(size_t i=0;i<out.q.size();++i){
    auto p=product[i];vector<Arc>arcs;
    for(Arc a:candidate.q[p.first].arcs){
      Id target=intern(a.second,advance(allowed,p.second,a.first));budget.edge(++edges);arcs.push_back({a.first,target});
    }
    out.q[i].arcs=std::move(arcs);
  }
  return minimize(out,budget);
}

DFA residueLanguage(Budget& budget){
  // Agent2's existing necessary exterior digit-sum return test, applied ONLY
  // at a neutral terminal.  A four-bit L block maps s to 7*s+6-2*a modulo9,
  // a=8*L0+4*L1+2*L2+L3.  Alpha cycles through1,7,4; beta is0..8.
  // The identity state accepts.  Intersection with positive Bad excludesepsilon.
  DFA out;budget.state(27);out.q.resize(27);uint64_t edges=0;
  for(int phase=0;phase<3;++phase)for(int beta=0;beta<9;++beta){
    State&q=out.q[9*phase+beta];q.accept=beta%(phase==0?9:3)==0;
    for(int s=0;s<2560;++s)if(terminal(s)){
      int a=8*(s&1)+4*((s>>1)&1)+2*((s>>2)&1)+((s>>3)&1);
      int nextBeta=((7*beta+6-2*a)%9+9)%9;
      budget.edge(++edges);q.arcs.push_back({Label(s),Id(9*((phase+1)%3)+nextBeta)});
    }
  }
  return out;
}

DFA intersectLanguage(const DFA&left,const DFA&right,Budget&budget){
  DFA out;vector<pair<Id,Id>>product;unordered_map<uint64_t,Id>known;
  auto intern=[&](Id x,Id y){
    uint64_t key=(uint64_t(x)<<32)|y;auto found=known.find(key);if(found!=known.end())return found->second;
    budget.state(out.q.size()+1);Id id=out.q.size();known.emplace(key,id);product.push_back({x,y});
    out.q.push_back({left.q[x].accept&&right.q[y].accept,{}});return id;
  };
  out.start=intern(left.start,right.start);uint64_t edges=0;
  for(size_t k=0;k<out.q.size();++k){
    auto p=product[k];const auto&a=left.q[p.first].arcs;const auto&b_=right.q[p.second].arcs;
    size_t i=0,j=0;vector<Arc>arcs;
    while(i<a.size()&&j<b_.size()){
      budget.tick();
      if(a[i].first<b_[j].first)++i;
      else if(b_[j].first<a[i].first)++j;
      else{Id next=intern(a[i].second,b_[j].second);budget.edge(++edges);arcs.push_back({a[i].first,next});++i;++j;}
    }
    out.q[k].arcs=std::move(arcs);
  }
  return minimize(out,budget);
}

vector<Label> intersectionWord(const DFA& left,const DFA& right,Budget& budget){
  activeStage="language_intersection";
  struct Pair{Id left,right,parent;Label letter;};vector<Pair>queue;unordered_set<uint64_t>seen;
  auto add=[&](Id x,Id y,Id parent,Label letter){
    uint64_t key=(uint64_t(x)<<32)|y;
    if(seen.insert(key).second){budget.state(queue.size()+1);queue.push_back({x,y,parent,letter});}
  };
  add(left.start,right.start,DEAD,0);
  for(size_t k=0;k<queue.size();++k){
    Pair p=queue[k];budget.tick();
    if(left.q[p.left].accept&&right.q[p.right].accept){
      vector<Label>word;for(Id q=k;queue[q].parent!=DEAD;q=queue[q].parent)word.push_back(queue[q].letter);
      reverse(word.begin(),word.end());return word;
    }
    const auto&a=left.q[p.left].arcs;const auto&b_=right.q[p.right].arcs;size_t i=0,j=0;
    while(i<a.size()&&j<b_.size()){
      budget.tick();
      if(a[i].first<b_[j].first)++i;
      else if(b_[j].first<a[i].first)++j;
      else{add(a[i].second,b_[j].second,k,a[i].first);++i;++j;}
    }
  }
  return {};
}

struct Product { Id old; int required, initial; };
struct Image {
  const Table& table; Budget& budget; const DFA& input; bool first, prune;
  Image(const Table& t, Budget& b_, const DFA& d, bool f, bool p)
    : table(t), budget(b_), input(d), first(f), prune(p) {}
  DFA run(ImageStats& stats) {
    activeStage="image_nfa";
    if (input.q.empty() || input.start >= input.q.size() || input.q[input.start].accept)
      undecided118("exterior_regular_invalid_input_start");
    NFA nfa; vector<Product> product; unordered_map<uint64_t, Id> known;
    vector<uint32_t> masks(input.q.size(), UINT32_MAX);
    auto possible = [&](Id old, int required, int initial) {
      if (!prune || (input.q[old].accept && required == initial)) return true;
      if (masks[old] == UINT32_MAX) {
        uint32_t mask = 0;
        for (Arc a : input.q[old].arcs) {
          checkSymbol(a.first);
          for (int port = 0; port < 19; ++port) for (const Tile& t : table[a.first][port]) {
            budget.tick(); if (!first || t.positive) mask |= uint32_t(1) << port;
          }
        }
        masks[old] = mask;
      }
      return bool(masks[old] & (uint32_t(1) << required));
    };
    auto intern = [&](Id old, int required, int initial) -> Id {
      budget.tick();
      if (old >= input.q.size() || required < 0 || required >= 19 || initial < 0 || initial >= 19)
        undecided118("exterior_regular_bad_product");
      uint64_t key = uint64_t(old) * 361 + 19 * required + initial;
      auto found = known.find(key); if (found != known.end()) return found->second;
      budget.state(nfa.q.size() + 1); Id id = nfa.q.size();
      known.emplace(key, id); product.push_back({old, required, initial});
      nfa.q.push_back({input.q[old].accept && required == initial, {}}); return id;
    };
    for (int a = 0; a < 19; ++a) if (possible(input.start, a, a)) nfa.starts.push_back(intern(input.start, a, a));
    uint64_t edges = 0;
    for (size_t i = 0; i < nfa.q.size(); ++i) {
      Product p = product[i]; vector<Arc> arcs;
      for (Arc a : input.q[p.old].arcs) {
        checkSymbol(a.first); budget.tick();
        for (const Tile& t : table[a.first][p.required]) {
          budget.tick(); if (first && !t.positive) continue;
          // Intermediate accepted input words may continue with unclosed ports.
          // Whole-word acceptance, not each block boundary, enforces closure.
          if (!possible(a.second, t.right, p.initial)) continue;
          Id next = intern(a.second, t.right, p.initial);
          budget.edge(++edges); arcs.push_back({Label(t.out), next});
        }
      }
      sort(arcs.begin(), arcs.end()); arcs.erase(unique(arcs.begin(), arcs.end()), arcs.end());
      nfa.q[i].arcs = std::move(arcs);
    }
    stats.nfa = nfa.q.size(); stats.nfaEdges = edgeCount(nfa.q);
    activeStage="trim_nfa";
    NFA live = trimNfa(nfa, budget); stats.live = live.q.size();
    nfa = NFA(); product.clear(); product.shrink_to_fit(); known.clear(); known.rehash(0);
    activeStage="determinize";
    DFA dfa = determinize(live, budget); stats.dfaRaw = dfa.q.size();
    activeStage="minimize";
    return minimize(dfa, budget);
  }
};

struct TerminalResult { vector<Label> known, bad; };
TerminalResult terminalSearch(const DFA& input, const DFA& allowed, Budget& budget) {
  activeStage="terminal_intersection";
  struct Pair { Id input, allowed, parent; Label letter; };
  vector<Pair> queue; unordered_set<uint64_t> seen;
  auto add = [&](Id x, Id y, Id parent, Label letter) {
    uint64_t key = (uint64_t(x) << 32) | y;
    if (seen.insert(key).second) { budget.state(queue.size() + 1); queue.push_back({x,y,parent,letter}); }
  };
  auto word = [&](Id q) {
    vector<Label> out;
    for (; queue[q].parent != DEAD; q = queue[q].parent) out.push_back(queue[q].letter);
    reverse(out.begin(), out.end()); return out;
  };
  add(input.start, allowed.start, DEAD, 0); TerminalResult result;
  for (size_t k = 0; k < queue.size(); ++k) {
    Pair p = queue[k]; budget.tick();
    if (input.q[p.input].accept) {
      bool known = p.allowed != DEAD && allowed.q[p.allowed].accept;
      if (!known) { result.bad = word(k); return result; }
      if (result.known.empty()) result.known = word(k);
    }
    for (Arc a : input.q[p.input].arcs) if (terminal(a.first)) {
      budget.tick(); add(a.second, advance(allowed, p.allowed, a.first), k, a.first);
    }
  }
  return result;
}

vector<Count> lengthCounts(const DFA& dfa, int maximum, Budget& budget) {
  activeStage="length_counts";
  vector<Count> answer(maximum + 1), current(dfa.q.size()); current[dfa.start].value = 1;
  for (int n = 1; n <= maximum; ++n) {
    vector<Count> next(dfa.q.size());
    for (size_t q = 0; q < dfa.q.size(); ++q) if (current[q].value)
      for (Arc a : dfa.q[q].arcs) { budget.tick(); REG118::plus(next[a.second], current[q]); }
    current.swap(next);
    for (size_t q = 0; q < dfa.q.size(); ++q) if (dfa.q[q].accept) REG118::plus(answer[n], current[q]);
  }
  return answer;
}

vector<vector<Label>> decode(const DFA& dfa, int length, size_t cap, Budget& budget) {
  if (length < 1 || length > 128) undecided118("exterior_regular_export_length");
  vector<vector<Count>> suffix(length + 1, vector<Count>(dfa.q.size()));
  for (size_t q = 0; q < dfa.q.size(); ++q) suffix[0][q].value = dfa.q[q].accept;
  for (int n = 1; n <= length; ++n) for (size_t q = 0; q < dfa.q.size(); ++q)
    for (Arc a : dfa.q[q].arcs) { budget.tick(); REG118::plus(suffix[n][q], suffix[n-1][a.second]); }
  Count total = suffix[length][dfa.start];
  if (!total.exact || total.value > cap) undecided118("exterior_regular_export_cap");
  vector<vector<Label>> out; vector<Label> prefix;
  function<void(Id,int)> visit = [&](Id q, int remaining) {
    if (!remaining) { if (dfa.q[q].accept) out.push_back(prefix); return; }
    for (Arc a : dfa.q[q].arcs) if (suffix[remaining-1][a.second].value) {
      budget.tick(); prefix.push_back(a.first); visit(a.second, remaining-1); prefix.pop_back();
    }
  };
  visit(dfa.start, length);
  if (out.size() != total.value) undecided118("exterior_regular_export_count_mismatch");
  return out;
}

void printWords(const vector<vector<Label>>& list) {
  cout << '[';
  for (size_t i = 0; i < list.size(); ++i) {
    if (i) cout << ','; cout << '[';
    for (size_t j = 0; j < list[i].size(); ++j) { if (j) cout << ','; cout << list[i][j]; }
    cout << ']';
  }
  cout << "]\n" << flush;
}

pair<vector<Label>, vector<int>> predecessor(const DFA& input, const vector<Label>& target,
                                            bool first, const Table& table, Budget& budget) {
  activeStage="witness_predecessor";
  size_t n = target.size();
  if (!n || n > 2048) undecided118("exterior_regular_witness_word_cap");
  vector<Label> previous(n); vector<int> column(4*n);
  // The four-component key is exact; width is a true language position here.
  set<array<uint32_t,4>> failed;
  function<bool(size_t,Id,int,int)> visit = [&](size_t position, Id q, int required, int initial) {
    budget.tick();
    if (position == n) return input.q[q].accept && required == initial;
    array<uint32_t,4> key{uint32_t(position), q, uint32_t(required), uint32_t(initial)};
    if (failed.count(key)) return false;
    for (Arc a : input.q[q].arcs) {
      checkSymbol(a.first);
      for (const Tile& tile : table[a.first][required]) {
        budget.tick();
        if (Label(tile.out) != target[position] || (first && !tile.positive)) continue;
        if (visit(position + 1, a.second, tile.right, initial)) {
          previous[position] = a.first;
          for (int r = 0; r < 4; ++r) column[4*position+r] = tile.coefficients[r];
          return true;
        }
      }
    }
    budget.state(failed.size() + 1); failed.insert(key); return false;
  };
  for (int initial = 0; initial < 19; ++initial)
    if (visit(0, input.start, initial, initial)) return {previous,column};
  undecided118("exterior_regular_missing_predecessor");
}

pair<vector<int>,int> norm(const vector<int>& word, int carry) {
  vector<int> digits;
  for (int x : word) {
    if (x < 0 || x > 18) undecided118("exterior_regular_bad_witness_coefficient");
    digits.push_back((x + carry) % 10); carry = (x + carry) / 10;
  }
  return {digits,carry};
}
vector<vector<int>> replay(const vector<Label>& terminalWord, const vector<vector<int>>& columns) {
  size_t period = 4 * terminalWord.size(); vector<vector<int>> exterior(period);
  for (const vector<int>& column : columns) {
    if (column.size() != period) undecided118("exterior_regular_column_width");
    for (size_t t = 0; t < period; ++t) exterior[t].push_back(column[t]);
  }
  for (vector<int>& word : exterior) while (!word.empty() && word.back() == 9) word.pop_back();
  for (size_t t = 0; t < period; ++t) {
    const vector<int>& word = exterior[t];
    if (!word.empty() && word[0] == 0) undecided118("exterior_regular_zero_witness_head");
    auto forward = norm(word,0); int e = forward.second;
    int expected = (terminalWord[t/4] >> (t%4)) & 1;
    if (e != expected) undecided118("exterior_regular_witness_e_mismatch");
    vector<int> reverseWord(word.rbegin(),word.rend()); auto reverse = norm(reverseWord,1-e);
    if (reverse.second != int(t%4==0)) undecided118("exterior_regular_witness_g_mismatch");
    vector<int> left = forward.first, right(reverse.first.rbegin(),reverse.first.rend());
    if (reverse.second) { left.push_back(9*(1-e)); right.insert(right.begin(),1); }
    if (left.size() != right.size()) undecided118("exterior_regular_witness_width_mismatch");
    vector<int> next; for (size_t i = 0; i < left.size(); ++i) next.push_back(left[i]+right[i]);
    while (!next.empty() && next.back() == 9) next.pop_back();
    if (next != exterior[(t+1)%period]) undecided118("exterior_regular_witness_transition_mismatch");
  }
  return exterior;
}

struct Engine {
  Budget budget; int layers = 80, fixedBlocks = 0, exportLayer = -1, slice = 0;
  bool prune = true, stopKnown = false, wantWitness = false, backward = false, residueSeed = false;
  Engine() { budget.states=500000; budget.edges=5000000; budget.operations=100000000; }
  const char* scope() const { return fixedBlocks ? "fixed_G_control" : "all_G_all_widths"; }
  void diagnostic(int depth, const DFA& dfa, const ImageStats& stats, const TerminalResult& terminals) {
    vector<Count> counts = lengthCounts(dfa,8,budget);
    printf("BREG_LAYER width=%d nfa=%zu nfa_live=%zu nfa_edges=%llu dfa_raw=%zu dfa=%zu edges=%llu "
           "known=%d bad=%d ops=%llu",depth,stats.nfa,stats.live,(unsigned long long)stats.nfaEdges,
           stats.dfaRaw,dfa.q.size(),(unsigned long long)edgeCount(dfa.q),int(!terminals.known.empty()),
           int(!terminals.bad.empty()),(unsigned long long)budget.used);
    for (int n=1;n<=8;++n) printf(" count%d=%s",n,decimal(counts[n].value).c_str());
    printf("\n"); fflush(stdout);
  }
  void printHit(const vector<Label>& word,int width,const char* kind) {
    printf("BREG_HIT kind=%s width=%d blocks=%zu period=%zu symbols=",kind,width,word.size(),4*word.size());
    for(size_t i=0;i<word.size();++i) printf("%s%llu",i?",":"",(unsigned long long)word[i]);
    printf(" e="); for(Label s:word) for(int r=0;r<4;++r) printf("%d",int((s>>r)&1));
    printf("\n"); fflush(stdout);
  }
  void witness(const vector<DFA>& history,const vector<Label>& terminalWord,int width) {
    if (terminalWord.size()*size_t(width)*4 > budget.edges) undecided118("exterior_regular_witness_size_cap");
    vector<Label> current=terminalWord; vector<vector<int>> columns;
    for(int k=width;k>=1;--k) {
      auto step=predecessor(history[k-1],current,k==1,Tiles108::tiles,budget);
      current=std::move(step.first); columns.push_back(std::move(step.second));
    }
    if(current.size()!=terminalWord.size()||!all_of(current.begin(),current.end(),[](Label a){return a==272;}))
      undecided118("exterior_regular_witness_initial_mismatch");
    reverse(columns.begin(),columns.end()); auto exterior=replay(terminalWord,columns);
    printf("BREG_WITNESS verified=1 width=%d blocks=%zu period=%zu",width,terminalWord.size(),exterior.size());
    for(size_t t=0;t<exterior.size();++t) {
      printf(" B%zu=[",t); for(size_t i=0;i<exterior[t].size();++i)printf("%s%d",i?",":"",exterior[t][i]); printf("]");
    }
    printf("\n"); fflush(stdout);
  }
  void backwardWitness(const vector<DFA>& history,const DFA& physical,const DFA& allowed,
                       const vector<Label>& firstWord,int depth){
    if(firstWord.size()*size_t(depth+1)*4>budget.edges)undecided118("exterior_regular_witness_size_cap");
    auto first=predecessor(physical,firstWord,true,Tiles108::tiles,budget);
    if(first.first.size()!=firstWord.size()||!all_of(first.first.begin(),first.first.end(),[](Label a){return a==272;}))
      undecided118("exterior_regular_backward_initial_mismatch");
    vector<vector<int>>columns{std::move(first.second)};vector<Label>current=firstWord;
    for(int k=depth;k>=1;--k){
      auto step=predecessor(history[k-1],current,false,reverseTiles,budget);
      current=std::move(step.first);columns.push_back(std::move(step.second));
    }
    Id q=allowed.start;
    for(Label a:current){if(!terminal(a))undecided118("exterior_regular_backward_nonterminal");q=advance(allowed,q,a);}
    if(q!=DEAD&&allowed.q[q].accept)undecided118("exterior_regular_backward_known_target");
    printHit(current,depth+1,"outside_known_p12");auto exterior=replay(current,columns);
    printf("BREG_WITNESS verified=1 width=%d blocks=%zu period=%zu",depth+1,current.size(),exterior.size());
    for(size_t t=0;t<exterior.size();++t){
      printf(" B%zu=[",t);for(size_t i=0;i<exterior[t].size();++i)printf("%s%d",i?",":"",exterior[t][i]);printf("]");
    }
    printf("\n");fflush(stdout);
  }
  void runBackward(){
    // Exact generic preimages.  Agent103 independently applies the same
    // relational method to its fixed-G6 task; this mode keeps ALL G at once.
    DFA allowed=knownLanguage(budget),physical=words({272},fixedBlocks,budget);
    ImageStats firstStats;DFA first=Image(Tiles108::tiles,budget,physical,true,prune).run(firstStats);
    DFA expected=words({65,337},fixedBlocks,budget);vector<Label>difference;bool acceptsLeft=false;
    activeStage="language_equivalence";
    if(!equivalent(first,expected,budget,difference,acceptsLeft))undecided118("exterior_regular_FIRST_language_mismatch");
    DFA seed=badSeed(allowed,fixedBlocks,budget);
    if(residueSeed)seed=intersectLanguage(seed,residueLanguage(budget),budget);
    vector<DFA>history;history.push_back(std::move(seed));ImageStats stats;
    printf("BREG_INIT mode=backward scope=%s blocks=%d prune=%d residue_seed=%d\n",scope(),fixedBlocks,int(prune),int(residueSeed));
    printf("BREG_FIRST exact_language_verified=1\n");fflush(stdout);
    for(int depth=0;;++depth){
      const DFA&current=history.back();
      if(exportLayer==depth){printWords(decode(current,slice,1000000,budget));return;}
      vector<Label>hit=intersectionWord(current,first,budget);
      diagnostic(depth,current,stats,TerminalResult());
      if(!hit.empty()){
        printf("BREG_CONNECTION depth=%d width=%d blocks=%zu\n",depth,depth+1,hit.size());fflush(stdout);
        backwardWitness(history,physical,allowed,hit,depth);
        printf("BREG_DONE status=new_driver mode=backward scope=%s width=%d blocks=%zu verified=1 residue_seed=%d ops=%llu\n",
               scope(),depth+1,hit.size(),int(residueSeed),(unsigned long long)budget.used);return;
      }
      if(depth>=1&&history[depth-1].q.size()==current.q.size()&&edgeCount(history[depth-1].q)==edgeCount(current.q)){
        activeStage="language_equivalence";
        if(equivalent(history[depth-1],current,budget,difference,acceptsLeft)){
          printf("BREG_DONE status=known_drivers_only mode=backward scope=%s fixed_at=%d final_index=%d residue_seed=%d "
                 "first_intersection_empty=1 terminal_seed_excludes_known=1 ops=%llu peak_states=%llu peak_edges=%llu\n",
                 scope(),depth-1,depth,int(residueSeed),(unsigned long long)budget.used,(unsigned long long)budget.peakStates,
                 (unsigned long long)budget.peakEdges);return;
        }
      }
      if(depth>=layers)undecided118("exterior_regular_layer_limit");
      printf("BREG_BUILD direction=backward from_depth=%d\n",depth);fflush(stdout);
      ImageStats nextStats;DFA next=Image(reverseTiles,budget,current,false,prune).run(nextStats);
      // K is subtracted only in Q0.  Never remove known words from a preimage.
      history.push_back(std::move(next));stats=nextStats;
    }
  }
  void run() {
    if(backward){runBackward();return;}
    DFA allowed=knownLanguage(budget); vector<DFA> history{words({272},fixedBlocks,budget)};
    vector<uint64_t> edges{edgeCount(history[0].q)}; ImageStats stats; bool knownEver=false;
    printf("BREG_INIT mode=forward scope=%s blocks=%d prune=%d\n",scope(),fixedBlocks,int(prune)); fflush(stdout);
    for(int depth=0;;++depth) {
      const DFA& current=history.back();
      if(exportLayer==depth) { printWords(decode(current,slice,1000000,budget)); return; }
      TerminalResult terminals=terminalSearch(current,allowed,budget);
      diagnostic(depth,current,stats,terminals);
      if(!terminals.bad.empty()) {
        printHit(terminals.bad,depth,"outside_known_p12"); witness(history,terminals.bad,depth);
        printf("BREG_DONE status=new_driver mode=forward scope=%s width=%d blocks=%zu verified=1 ops=%llu\n",
               scope(),depth,terminals.bad.size(),(unsigned long long)budget.used); return;
      }
      if(!terminals.known.empty()) {
        if(!knownEver)printHit(terminals.known,depth,"known_p12"); knownEver=true;
        if(stopKnown) {
          if(wantWitness)witness(history,terminals.known,depth);
          printf("BREG_DONE status=known_driver_control mode=forward scope=%s width=%d blocks=%zu verified=%d ops=%llu\n",
                 scope(),depth,terminals.known.size(),int(wantWitness),(unsigned long long)budget.used); return;
        }
      }
      if(depth>=1) {
        for(int old=depth-1;old>=1;--old) {
          // Size filtering can only miss a repeat; the actual stopping check is
          // exact language equality, with implicit rejecting sinks included.
          if(history[old].q.size()!=current.q.size() || edges[old]!=edges.back())continue;
          vector<Label> difference; bool acceptsLeft=false;
          activeStage="language_equivalence";
          if(equivalent(history[old],current,budget,difference,acceptsLeft)) {
            printf("BREG_DONE status=%s mode=forward scope=%s cycle_start=%d period=%d terminal_checks=%d "
                   "known_seen=%d ops=%llu peak_states=%llu peak_edges=%llu\n",knownEver?"known_drivers_only":"no_exterior",
                   scope(),old,depth-old,depth+1,int(knownEver),(unsigned long long)budget.used,
                   (unsigned long long)budget.peakStates,(unsigned long long)budget.peakEdges); return;
          }
        }
      }
      if(depth>=layers)undecided118("exterior_regular_layer_limit");
      printf("BREG_BUILD from_width=%d\n",depth); fflush(stdout);
      ImageStats nextStats; DFA next=Image(Tiles108::tiles,budget,current,depth==0,prune).run(nextStats);
      if(depth==0) {
        DFA exactFirst=words({65,337},fixedBlocks,budget); vector<Label> difference; bool acceptsLeft=false;
        if(!equivalent(exactFirst,next,budget,difference,acceptsLeft))undecided118("exterior_regular_FIRST_language_mismatch");
        printf("BREG_FIRST exact_language_verified=1\n"); fflush(stdout);
      }
      history.push_back(std::move(next)); edges.push_back(edgeCount(history.back().q)); stats=nextStats;
    }
  }
};

void auditTiles() {
  uint64_t count=0,positive=0,live=0;
  for(int s=0;s<2560;++s) {
    bool active=false; set<int> targets;
    for(int left=0;left<19;++left)for(const Tile&t:Tiles108::tiles[s][left]) {
      ++count;positive+=t.positive;active=true;checkSymbol(t.out);
      if(t.right<0||t.right>18||t.coefficients[0]!=left||!targets.insert(t.out).second)
        undecided118("exterior_regular_tile_table_mismatch");
    }
    live+=active;
  }
  if(count!=48640||positive!=41856||live!=2000)undecided118("exterior_regular_tile_count_mismatch");
}

void dumpTiles() {
  vector<array<int,9>> rows;
  for(int s=0;s<2560;++s)for(int left=0;left<19;++left)for(const Tile&t:Tiles108::tiles[s][left])
    rows.push_back({s,t.out,left,t.right,int(t.positive),t.coefficients[0],t.coefficients[1],t.coefficients[2],t.coefficients[3]});
  sort(rows.begin(),rows.end());
  for(const auto&row:rows){for(size_t k=0;k<row.size();++k){if(k)cout<<' ';cout<<row[k];}cout<<'\n';}
}

DFA finiteInput(int blocks,Budget& budget) {
  uint64_t count;if(!(cin>>count)||count>100000)undecided118("exterior_regular_finite_input_count");
  vector<map<Label,Id>> trie(1); vector<bool> accepting(1,false);uint64_t edges=0;
  for(uint64_t i=0;i<count;++i){Id q=0;for(int p=0;p<blocks;++p){
    Label a;if(!(cin>>a))undecided118("exterior_regular_missing_finite_symbol");checkSymbol(a);
    auto it=trie[q].find(a);
    if(it==trie[q].end()){
      budget.state(trie.size()+1);Id next=trie.size();trie[q].emplace(a,next);
      trie.emplace_back();accepting.push_back(false);budget.edge(++edges);q=next;
    }else q=it->second;
  }accepting[q]=true;}
  string extra;if(cin>>extra)undecided118("exterior_regular_trailing_finite_input");
  DFA dfa;dfa.q.resize(trie.size());
  for(size_t i=0;i<trie.size();++i){dfa.q[i].accept=accepting[i];dfa.q[i].arcs=vector<Arc>(trie[i].begin(),trie[i].end());}
  return minimize(dfa,budget);
}

int main118(int argc,char**argv) {
  Tiles108::build_tiles();auditTiles();Engine engine;
  for(int s=0;s<2560;++s)for(int left=0;left<19;++left)for(const Tile&t:Tiles108::tiles[s][left])
    reverseTiles[t.out][left].push_back({s,t.right,t.coefficients,t.positive});
  if(argc==2&&string(argv[1])=="--tiles"){dumpTiles();return 0;}
  if(argc==4&&string(argv[1])=="--image"){
    long long blocks=number118(argv[2]),first=number118(argv[3]);
    if(blocks<1||blocks>32||(first!=0&&first!=1))undecided118("exterior_regular_bad_image_options");
    DFA input=finiteInput(blocks,engine.budget);ImageStats stats;
    DFA out=Image(Tiles108::tiles,engine.budget,input,first,true).run(stats);
    printWords(decode(out,blocks,1000000,engine.budget));return 0;
  }
  if(argc==3&&string(argv[1])=="--reverse-image"){
    long long blocks=number118(argv[2]);if(blocks<1||blocks>32)undecided118("exterior_regular_bad_image_options");
    DFA input=finiteInput(blocks,engine.budget);ImageStats stats;
    DFA out=Image(reverseTiles,engine.budget,input,false,true).run(stats);
    printWords(decode(out,blocks,1000000,engine.budget));return 0;
  }
  set<string>seen;
  for(int i=1;i<argc;++i){string flag=argv[i];if(!seen.insert(flag).second)undecided118("duplicate_exterior_regular_option");
    auto value=[&](){if(++i>=argc)undecided118("missing_exterior_regular_option_value");long long n=number118(argv[i]);if(n<1)undecided118("nonpositive_exterior_regular_limit");return uint64_t(n);};
    if(flag=="--layers"){auto n=value();if(n>10000)undecided118("unsupported_exterior_regular_layers");engine.layers=n;}
    else if(flag=="--states"){engine.budget.states=value();if(engine.budget.states>10000000)undecided118("unsupported_exterior_regular_states");}
    else if(flag=="--edges"){engine.budget.edges=value();if(engine.budget.edges>100000000)undecided118("unsupported_exterior_regular_edges");}
    else if(flag=="--ops")engine.budget.operations=value();
    else if(flag=="--fixed-blocks"){auto n=value();if(n>128)undecided118("unsupported_exterior_regular_blocks");engine.fixedBlocks=n;}
    else if(flag=="--slice"){auto n=value();if(n>128)undecided118("unsupported_exterior_regular_slice");engine.slice=n;}
    else if(flag=="--export-layer"){if(++i>=argc)undecided118("missing_export_layer");long long n=number118(argv[i]);if(n<0||n>10000)undecided118("unsupported_export_layer");engine.exportLayer=n;}
    else if(flag=="--no-prune")engine.prune=false;
    else if(flag=="--stop-at-known")engine.stopKnown=true;
    else if(flag=="--witness")engine.wantWitness=true;
    else if(flag=="--backward")engine.backward=true;
    else if(flag=="--residue-seed")engine.residueSeed=true;
    else undecided118("unsupported_exterior_regular_option");
  }
  if((engine.exportLayer>=0)!=(engine.slice>0)||engine.exportLayer>engine.layers)undecided118("invalid_exterior_regular_export_options");
  if(engine.stopKnown&&!engine.fixedBlocks)undecided118("known_stop_requires_fixed_control");
  if(engine.stopKnown&&engine.backward)undecided118("known_stop_requires_forward_control");
  if(engine.residueSeed&&!engine.backward)undecided118("residue_seed_requires_backward");
  engine.run();return 0;
}
}  // namespace BREG118

int main(int argc,char**argv){
  try{return BREG118::main118(argc,argv);}
  catch(const exception&error){fprintf(stderr,"UNDECIDED %s stage=%s\n",error.what(),BREG118::activeStage);return 2;}
  catch(...){fprintf(stderr,"UNDECIDED unexpected_exception\n");return 2;}
}
