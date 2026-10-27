// Independent language controls for exterior_invariant.hpp. The expected
// languages use explicit finite sets or separately specified infinite DFAs.
// No regular.hpp, production minimizer, or bounded-word approximation is used.
// Build: c++ -O2 -std=c++17 calculation/agent-111/exterior_invariant_selftest.cpp -o /tmp/a111_exterior_test
// Run: /tmp/a111_exterior_test [finite_random_cases=800]
#include "exterior_invariant.hpp"
#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <optional>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Symbol = uint64_t;
using Word = std::vector<Symbol>;
using Words = std::set<Word>;
using Rows = std::map<Symbol,std::vector<a111x::Row>>;

struct Counts {
  uint64_t inclusion=0, intersection=0, cyclic=0, cyclic_intersections=0, product_states=0;
  uint64_t shortest_witnesses=0, epsilon_witnesses=0, replayed_rows=0;
  uint64_t finite_images=0, raw_row_tuples=0, closed_row_tuples=0, image_words=0;
  uint64_t infinite_cases=0, first_languages=0, corrupted_invariants=0;
  uint64_t changed_relations=0, dual_obligations=0, transpose_cases=0, cap_cases=0, invalid_cases=0;
};
static void require(bool good,const std::string& message) {
  if (!good) throw std::runtime_error(message);
}
static Symbol symbol(uint32_t type,uint32_t value) {
  return (uint64_t(type)<<32)|value;
}
static std::string show(const Word& w) {
  std::ostringstream out;out<<'[';
  for(size_t i=0;i<w.size();++i) out<<(i?",":"")<<w[i];
  return out.str()+']';
}

// Independent partial DFA. Missing letters enter a rejecting sink only in the
// product oracle; accepting states retain all of their outgoing transitions.
struct Ref {
  size_t start=0;
  std::vector<std::map<Symbol,size_t>> next{{}};
  std::vector<bool> accept{false};
  size_t add(bool final=false) {next.emplace_back();accept.push_back(final);return next.size()-1;}
};
static a111x::DFA core(const Ref& r) {
  a111x::DFA d;d.start=a111x::State(r.start);d.nodes.resize(r.next.size());
  for(size_t i=0;i<r.next.size();++i) {
    d.nodes[i].accept=r.accept[i];
    for(auto [x,q]:r.next[i]) d.nodes[i].edges.push_back({x,a111x::State(q)});
  }
  return d;
}
static Ref reference(const a111x::DFA& d) {
  Ref r;
  if(d.nodes.empty()) {require(d.start==0,"invalid empty DFA from core");return r;}
  r.start=d.start;r.next.assign(d.nodes.size(),{});r.accept.assign(d.nodes.size(),false);
  require(r.start<r.next.size(),"invalid DFA start from core");
  for(size_t i=0;i<d.nodes.size();++i) {
    r.accept[i]=d.nodes[i].accept;
    for(auto [x,q]:d.nodes[i].edges) {
      require(q<r.next.size(),"invalid DFA target from core");
      auto added=r.next[i].emplace(x,q);
      require(added.second||added.first->second==q,"conflicting DFA from core");
    }
  }
  return r;
}
static bool accepted(const Ref& r,const Word& w) {
  size_t q=r.start;
  for(Symbol x:w) {auto it=r.next[q].find(x);if(it==r.next[q].end())return false;q=it->second;}
  return r.accept[q];
}
static Ref trie(const Words& words) {
  Ref r;
  for(const Word& w:words) {
    size_t q=0;
    for(Symbol x:w) {
      auto it=r.next[q].find(x);
      if(it==r.next[q].end()) {size_t to=r.add();r.next[q][x]=to;q=to;} else q=it->second;
    }
    r.accept[q]=true;
  }
  return r;
}
static Ref all_words(const std::set<Symbol>& alphabet,bool epsilon=true) {
  Ref r;r.accept[0]=epsilon;
  if(epsilon) for(Symbol x:alphabet) r.next[0][x]=0;
  else {r.add(true);for(Symbol x:alphabet){r.next[0][x]=1;r.next[1][x]=1;}}
  return r;
}
static Ref powers(const Word& w) {
  require(!w.empty(),"empty reference power block");Ref r;
  for(size_t i=0;i<w.size();++i)r.add(i+1==w.size());
  for(size_t i=0;i<w.size();++i)r.next[i][w[i]]=i+1;
  r.next[w.size()][w[0]]=1;return r;
}

// Exact all-length inclusion/intersection oracle, with a shortest witness.
// This independently traverses a product of ordinary partial DFAs. It never
// asks the implementation under test to minimize or decide either language.
static std::optional<Word> witness(const Ref& left,const Ref& right,
                                  bool intersection,Counts& count) {
  struct Visit{size_t a,b,parent;Symbol letter;};
  const size_t none=std::numeric_limits<size_t>::max();
  std::vector<Visit> queue{{left.start,right.start,none,0}};
  std::map<std::pair<size_t,size_t>,size_t> seen;seen[{left.start,right.start}]=0;
  auto final=[](const Ref& r,size_t q){return q<r.next.size()&&r.accept[q];};
  auto step=[](const Ref& r,size_t q,Symbol x){
    if(q==r.next.size())return q;
    auto it=r.next[q].find(x);return it==r.next[q].end()?r.next.size():it->second;
  };
  for(size_t h=0;h<queue.size();++h) {
    require(queue.size()<1000000,"independent product budget exceeded");
    const auto v=queue[h];++count.product_states;
    bool good=final(left,v.a)&&(intersection?final(right,v.b):!final(right,v.b));
    if(good) {
      Word w;
      for(size_t p=h;queue[p].parent!=none;p=queue[p].parent)w.push_back(queue[p].letter);
      std::reverse(w.begin(),w.end());
      require(accepted(left,w)&&(intersection?accepted(right,w):!accepted(right,w)),
              "reference product produced an invalid witness");
      return w;
    }
    std::set<Symbol> letters;
    if(v.a<left.next.size())for(auto [x,q]:left.next[v.a])letters.insert(x);
    if(v.b<right.next.size())for(auto [x,q]:right.next[v.b])letters.insert(x);
    for(Symbol x:letters) {
      size_t a=step(left,v.a,x),b=step(right,v.b,x);
      if(seen.emplace(std::make_pair(a,b),queue.size()).second)queue.push_back({a,b,h,x});
    }
  }
  return std::nullopt;
}
static void equivalent(const Ref& a,const Ref& b,Counts& count,const std::string& name) {
  auto ab=witness(a,b,false,count),ba=witness(b,a,false,count);
  require(!ab&&!ba,name+" differs at "+(ab?show(*ab):(ba?show(*ba):"[]")));
}

// Independent epsilon-closure/subset construction, used only to audit FIRST
// constructors against hand-specified infinite languages. The production
// verifier instead uses direct products and no determinizer/minimizer.
static Ref nfa_reference(const a111x::NFA& nfa) {
  auto closure=[&](std::set<size_t> states) {
    std::vector<size_t> stack(states.begin(),states.end());
    for(size_t i=0;i<stack.size();++i) {
      require(stack[i]<nfa.nodes.size(),"invalid NFA state from constructor");
      for(auto q:nfa.nodes[stack[i]].epsilon) {
        require(q<nfa.nodes.size(),"invalid NFA epsilon target from constructor");
        if(states.insert(q).second)stack.push_back(q);
      }
    }
    return states;
  };
  std::set<size_t> initial(nfa.starts.begin(),nfa.starts.end());initial=closure(initial);
  std::vector<std::set<size_t>> subsets{initial};
  std::map<std::set<size_t>,size_t> ids;ids[initial]=0;Ref r;
  for(size_t at=0;at<subsets.size();++at) {
    require(subsets.size()<50000,"independent subset-oracle budget exceeded");
    auto current=subsets[at];std::map<Symbol,std::set<size_t>> moves;
    for(size_t q:current) {
      r.accept[at]=r.accept[at]||nfa.nodes[q].accept;
      for(auto [x,to]:nfa.nodes[q].edges) {
        require(to<nfa.nodes.size(),"invalid NFA symbol target from constructor");
        moves[x].insert(to);
      }
    }
    for(auto& [x,to]:moves) {
      auto next=closure(to);auto added=ids.emplace(next,subsets.size());
      if(added.second){subsets.push_back(next);r.add();}
      r.next[at][x]=added.first->second;
    }
  }
  return r;
}
static void check_result(const a111x::Result& result,const Ref& source,const Ref& target,
                         bool intersection,Counts& count,const std::string& label) {
  auto expected=witness(source,target,intersection,count);
  require(result.ok==!expected,label+" wrong boolean outcome");
  if(expected) {
    require(accepted(source,result.word)&&
            (intersection?accepted(target,result.word):!accepted(target,result.word)),
            label+" invalid counterexample "+show(result.word));
    require(result.word.size()==expected->size(),label+" counterexample is not shortest");
    ++count.shortest_witnesses;if(result.word.empty())++count.epsilon_witnesses;
  }
}
static void ordinary(const a111x::NFA& source,const Ref& expected_source,
                     const Ref& target,Counts& count) {
  auto candidate=core(target);
  auto inclusion=a111x::included(source,candidate);
  check_result(inclusion,expected_source,target,false,count,"NFA inclusion");++count.inclusion;
  auto separation=a111x::disjoint(source,candidate);
  check_result(separation,expected_source,target,true,count,"NFA intersection");++count.intersection;
}
static void ordinary(const Ref& source,const Ref& target,Counts& count) {
  auto result=a111x::included(core(source),core(target));
  check_result(result,source,target,false,count,"DFA inclusion");++count.inclusion;
}

static const std::vector<a111x::Row>& relation_row(const Rows& rows,Symbol x) {
  static const std::vector<a111x::Row> empty;
  auto it=rows.find(x);return it==rows.end()?empty:it->second;
}
static bool same_row(const a111x::Row& a,const a111x::Row& b) {
  return a.incoming==b.incoming&&a.output==b.output&&a.outgoing==b.outgoing;
}
static a111x::Result cyclic(const a111x::DFA& source,const Ref& expected_image,
                            const Ref& target,const Rows& rows,Counts& count,
                            bool intersection=false) {
  auto local=[&](Symbol x)->const std::vector<a111x::Row>&{return relation_row(rows,x);};
  auto result=intersection?a111x::cyclic_image_disjoint(source,core(target),local):
                           a111x::cyclic_image_included(source,core(target),local);
  check_result(result,expected_image,target,intersection,count,
               intersection?"cyclic image intersection":"cyclic image inclusion");
  if(!result.ok) {
    require(!result.word.empty()&&result.input.size()==result.word.size()&&
            result.rows.size()==result.word.size(),"cyclic witness has wrong nonempty arity");
    require(accepted(reference(source),result.input),"cyclic witness input not accepted");
    for(size_t i=0;i<result.word.size();++i) {
      const auto& row=result.rows[i];const auto& allowed=relation_row(rows,result.input[i]);
      require(std::any_of(allowed.begin(),allowed.end(),[&](const auto& r){return same_row(row,r);}),
              "cyclic witness used absent local row");
      require(row.output==result.word[i]&&
              row.outgoing==result.rows[(i+1)%result.rows.size()].incoming,
              "cyclic witness output or final-to-first carry mismatch");
      ++count.replayed_rows;
    }
  }
  ++count.cyclic;if(intersection)++count.cyclic_intersections;return result;
}
static Words explicit_image(const Words& source,const Rows& rows,Counts& count) {
  Words image;
  for(const auto& w:source) {
    if(w.empty())continue;
    std::vector<a111x::Row> selected(w.size());
    std::function<void(size_t)> visit=[&](size_t at) {
      if(at==w.size()) {
        ++count.raw_row_tuples;
        for(size_t i=0;i<w.size();++i)
          if(selected[i].outgoing!=selected[(i+1)%w.size()].incoming)return;
        Word out;for(const auto& r:selected)out.push_back(r.output);
        image.insert(std::move(out));++count.closed_row_tuples;return;
      }
      for(const auto& r:relation_row(rows,w[at])){selected[at]=r;visit(at+1);}
    };
    visit(0);
  }
  ++count.finite_images;count.image_words+=image.size();return image;
}
static Ref random_dfa(std::mt19937_64& rng,const std::set<Symbol>& alphabet,size_t states) {
  Ref r;while(r.next.size()<states)r.add();r.start=rng()%states;
  for(size_t q=0;q<states;++q) {
    r.accept[q]=rng()%3==0;
    for(Symbol x:alphabet)if(rng()%3!=0)r.next[q][x]=rng()%states;
  }
  return r;
}
static Rows random_rows(std::mt19937_64& rng,const Words& source,bool force_loop) {
  Rows rows;for(const auto& w:source)for(Symbol x:w)rows[x];
  for(auto& [x,list]:rows) {
    for(unsigned i=0,end=rng()%4;i<end;++i)
      list.push_back({rng()%2?-7:5,symbol(rng()%3,rng()%3),rng()%2?-7:5});
    if(force_loop)list.push_back({-7,symbol(uint32_t(x>>32),0),-7});
    if(!list.empty()&&rng()%3==0)list.push_back(list.front());
  }
  return rows;
}

static void finite_tests(std::mt19937_64& rng,size_t rounds,Counts& count) {
  std::set<Symbol> alphabet;
  for(uint32_t t=0;t<3;++t)for(uint32_t x=0;x<3;++x)alphabet.insert(symbol(t,x));
  for(size_t iteration=0;iteration<rounds;++iteration) {
    Words input;
    for(unsigned k=0,end=1+rng()%9;k<end;++k) {
      Word w(rng()%5);for(auto& x:w)x=symbol(rng()%3,rng()%3);input.insert(std::move(w));
    }
    if(iteration%4==0){input.insert({symbol(0,0),symbol(1,0)});input.insert({symbol(0,1),symbol(1,1)});}
    auto source=core(trie(input));Rows rows=random_rows(rng,input,iteration%2==0);
    Ref expected=trie(explicit_image(input,rows,count));
    cyclic(source,expected,expected,rows,count);
    cyclic(source,expected,expected,rows,count,true);
    cyclic(source,expected,Ref{},rows,count);
    cyclic(source,expected,Ref{},rows,count,true);
    Ref target=random_dfa(rng,alphabet,1+rng()%5);
    cyclic(source,expected,target,rows,count);
    cyclic(source,expected,target,rows,count,true);
    Rows changed=random_rows(rng,input,iteration%2!=0);
    Ref expected_changed=trie(explicit_image(input,changed,count));
    cyclic(source,expected_changed,expected,changed,count);
    cyclic(source,expected_changed,expected,changed,count,true);++count.changed_relations;
  }
  // One-letter closure must match its own incoming/outgoing boundary.
  const Symbol x=symbol(UINT32_MAX,UINT32_MAX);
  Words input{Word{},Word{x}};
  Rows rows{{x,{{-7,11,5},{5,12,-7},{-7,13,-7},{-7,13,-7}}}};
  Ref image=trie(explicit_image(input,rows,count));
  equivalent(image,trie(Words{Word{13}}),count,"K1 closure expected language");
  cyclic(core(trie(input)),image,Ref{},rows,count);
  cyclic(core(trie(input)),image,image,rows,count,true);
  cyclic(core(trie(Words{Word{}})),Ref{},Ref{},rows,count);
  cyclic(core(trie(Words{Word{}})),Ref{},trie(Words{Word{}}),rows,count,true);
}

static Ref binary_closed_paths() {
  Ref r;for(int i=0;i<4;++i)r.add();
  for(unsigned first=0;first<2;++first)for(unsigned next=0;next<2;++next)
    r.next[0][2*first+next]=1+2*first+next;
  for(unsigned first=0;first<2;++first)for(unsigned need=0;need<2;++need) {
    size_t q=1+2*first+need;r.accept[q]=first==need;
    for(unsigned next=0;next<2;++next)r.next[q][2*need+next]=1+2*first+next;
  }
  return r;
}
static Ref two_blocks(Symbol a,Symbol b,Symbol c,Symbol d,bool mixed_cross=false) {
  Ref r;r.add(true);r.add();r.add();
  r.next[0]={{a,2},{c,3}};r.next[1]=r.next[0];r.next[2][b]=1;r.next[3][d]=1;
  if(mixed_cross)r.next[2][d]=1;
  return r;
}
static Ref separate_block_powers(Symbol a,Symbol b,Symbol c,Symbol d) {
  Ref r;r.add();r.add(true);r.add();r.add(true);
  r.next[0]={{a,1},{c,3}};r.next[1][b]=2;r.next[2][a]=1;
  r.next[3][d]=4;r.next[4][c]=3;return r;
}
static void first_and_infinite_tests(Counts& count) {
  const Symbol A=symbol(100,0),B=symbol(101,0);
  const Symbol a=symbol(0,1),b=symbol(1,1),c=symbol(0,2),d=symbol(1,2);
  auto root=a111x::positive_powers(Word{A,B});
  equivalent(reference(root),powers(Word{A,B}),count,"ROOT positive powers");
  Rows first{{A,{{0,a,1},{0,c,2}}},{B,{{1,b,0},{2,d,0}}}};
  Ref full=two_blocks(a,b,c,d),individual=separate_block_powers(a,b,c,d);
  cyclic(root,full,full,first,count);++count.infinite_cases;
  auto mixed=cyclic(root,full,individual,first,count);++count.infinite_cases;
  require(!mixed.ok&&mixed.word.size()==4,"FIRST mixed-block failure must have length four");
  ++count.corrupted_invariants;

  auto first_blocks=a111x::positive_blocks({Word{a,b},Word{c,d},Word{a,b}});
  equivalent(nfa_reference(first_blocks),full,count,"FIRST union positive closure");
  ordinary(first_blocks,full,individual,count);ordinary(first_blocks,full,full,count);
  ++count.first_languages;

  // Complete three-obligation certificate model: FIRST, generic preservation,
  // and a correlated terminal word whose letters are individually possible.
  Rows identity{{a,{{-17,a,-17}}},{b,{{-17,b,-17}}},
                {c,{{-17,c,-17}}},{d,{{-17,d,-17}}}};
  cyclic(core(full),full,full,identity,count);++count.infinite_cases;
  auto terminal=a111x::positive_blocks({Word{a,d}});
  ordinary(terminal,powers(Word{a,d}),full,count);
  Ref contaminated=two_blocks(a,b,c,d,true);
  auto collision=a111x::disjoint(terminal,core(contaminated));
  check_result(collision,powers(Word{a,d}),contaminated,true,count,"corrupted terminal invariant");
  require(!collision.ok&&collision.word.size()==2,"terminal corruption not detected");
  ++count.corrupted_invariants;++count.intersection;
  Rows changed=identity;changed[a]={{-17,c,-17}};
  // The changed language is (cb|cd)+, specified directly.
  Ref changed_image;changed_image.add(true);changed_image.add();
  changed_image.next[0][c]=2;changed_image.next[1][c]=2;
  changed_image.next[2]={{b,1},{d,1}};
  auto closure_failure=cyclic(core(full),changed_image,full,changed,count);
  require(!closure_failure.ok&&closure_failure.word.size()==2,"generic closure corruption missed");
  ++count.infinite_cases;++count.changed_relations;++count.corrupted_invariants;

  // All nonempty closed binary edge paths; input also accepts epsilon, which
  // must be dropped without destroying nonempty loops through its start.
  Ref source=all_words({A});Rows binary{{A,{{0,0,0},{0,1,1},{1,2,0},{1,3,1},{0,0,0}}}};
  Ref closed=binary_closed_paths();auto source_core=core(source);
  cyclic(source_core,closed,closed,binary,count);++count.infinite_cases;
  cyclic(source_core,closed,all_words({0,1,2,3},false),binary,count);++count.infinite_cases;
  cyclic(source_core,closed,trie(Words{Word{}}),binary,count);++count.infinite_cases;
  Ref damaged=closed;damaged.next[0].erase(0);
  cyclic(source_core,closed,damaged,binary,count);++count.infinite_cases;++count.corrupted_invariants;

  // Arbitrary signed int32 endpoints, including both extrema. Only alternating
  // rows close, so the image is (ab)+ union (ba)+, never a singleton letter.
  Rows extremes{{A,{{INT32_MIN,a,INT32_MAX},{INT32_MAX,b,INT32_MIN}}}};
  Ref alternating=separate_block_powers(a,b,b,a);
  cyclic(source_core,alternating,alternating,extremes,count);++count.infinite_cases;
  cyclic(source_core,alternating,alternating,extremes,count,true);++count.infinite_cases;
  auto excluded=cyclic(source_core,alternating,Ref{},extremes,count);++count.infinite_cases;
  require(!excluded.ok&&excluded.word.size()==2,"signed boundary closure has wrong shortest length");

  // Acceptance of a prefix is not permission to stop exploring continuations.
  Rows same{{A,{{5,a,5}}}};Ref nonempty=powers(Word{a});
  auto continuation=cyclic(source_core,nonempty,trie(Words{Word{a}}),same,count);
  require(!continuation.ok&&continuation.word.size()==2,"accepted prefix hid continuation");
  ++count.infinite_cases;++count.corrupted_invariants;
  auto later_intersection=cyclic(source_core,nonempty,trie(Words{Word{a,a}}),same,count,true);
  require(!later_intersection.ok&&later_intersection.word.size()==2,
          "accepted source prefix hid later cyclic intersection");
  ++count.infinite_cases;

  // Variable-length FIRST blocks with an accepting prefix of another block.
  auto variable=a111x::positive_blocks({Word{a},Word{b,b},Word{a}});
  Ref variable_expected;variable_expected.add(true);variable_expected.add();
  variable_expected.next[0]={{a,1},{b,2}};variable_expected.next[1]=variable_expected.next[0];
  variable_expected.next[2][b]=1;
  equivalent(nfa_reference(variable),variable_expected,count,"variable FIRST closure");
  ordinary(variable,variable_expected,trie(Words{Word{a},Word{b,b}}),count);++count.first_languages;
  auto prefix=a111x::positive_blocks({Word{a,b},Word{a,b,b}});
  Ref prefix_expected;prefix_expected.add();prefix_expected.add(true);prefix_expected.add(true);
  prefix_expected.next[0][a]=1;prefix_expected.next[1][b]=2;
  prefix_expected.next[2]={{a,1},{b,3}};prefix_expected.next[3][a]=1;
  equivalent(nfa_reference(prefix),prefix_expected,count,"prefix FIRST blocks");
  ordinary(prefix,prefix_expected,prefix_expected,count);++count.first_languages;
}

static void nfa_tests(std::mt19937_64& rng,Counts& count) {
  const Symbol a=11,b=12;
  // A longer epsilon route and a one-symbol route reach the same accepting
  // product state. Proper 0-1 distances must return epsilon, not the letter.
  a111x::NFA epsilon;epsilon.nodes.resize(4);epsilon.starts={0,0};
  epsilon.nodes[0].edges={{a,1}};epsilon.nodes[0].epsilon={2};
  epsilon.nodes[2].epsilon={3};epsilon.nodes[3].epsilon={2,1};epsilon.nodes[1].accept=true;
  Ref expected=trie(Words{Word{},Word{a}}),reject_all=all_words({a,b});reject_all.accept[0]=false;
  ordinary(epsilon,expected,reject_all,count);ordinary(epsilon,expected,all_words({a,b}),count);
  ordinary(epsilon,expected,trie(Words{Word{}}),count);
  equivalent(nfa_reference(epsilon),expected,count,"epsilon-cycle reference");

  a111x::NFA prefix;prefix.nodes.resize(3);prefix.starts={0};
  prefix.nodes[0].edges={{a,1},{a,1}};prefix.nodes[1].accept=true;
  prefix.nodes[1].edges={{b,2}};prefix.nodes[2].accept=true;
  Ref prefix_language=trie(Words{Word{a},Word{a,b}});
  ordinary(prefix,prefix_language,trie(Words{Word{a}}),count);
  ordinary(prefix,prefix_language,trie(Words{Word{a,b}}),count);
  ordinary(powers(Word{a}),trie(Words{Word{a}}),count);
  ordinary(powers(Word{b}),powers(Word{a}),count);

  for(size_t iteration=0;iteration<240;++iteration) {
    size_t depth=1+rng()%4,width=3;
    a111x::NFA nfa;nfa.nodes.resize((depth+1)*width);nfa.starts={0,1,0};
    for(size_t level=0;level<=depth;++level)for(size_t j=0;j<width;++j) {
      auto& node=nfa.nodes[level*width+j];node.accept=rng()%3==0;
      if(level==depth)continue;
      for(unsigned k=0,end=rng()%6;k<end;++k) {
        auto target=a111x::State((level+1)*width+rng()%width);
        if(rng()%3==0)node.epsilon.push_back(target);
        else node.edges.push_back({symbol(rng()%2,rng()%3),target});
      }
    }
    Words words;Word word;
    std::function<void(size_t,size_t)> enumerate=[&](size_t q,size_t traversed) {
      require(traversed<=depth,"finite epsilon-NFA enumeration exceeded DAG depth");
      if(nfa.nodes[q].accept)words.insert(word);
      for(auto target:nfa.nodes[q].epsilon)enumerate(target,traversed+1);
      for(auto [x,target]:nfa.nodes[q].edges){word.push_back(x);enumerate(target,traversed+1);word.pop_back();}
    };
    for(auto start:nfa.starts)enumerate(start,0);
    Ref language=trie(words);equivalent(nfa_reference(nfa),language,count,"finite NFA paths");
    std::set<Symbol> alphabet;for(const auto& w:words)for(Symbol x:w)alphabet.insert(x);
    Ref target=random_dfa(rng,alphabet,1+rng()%5);
    ordinary(nfa,language,target,count);
  }
  ordinary(a111x::NFA{},Ref{},Ref{},count);
  ordinary(a111x::positive_blocks({Word{a}}),powers(Word{a}),trie(Words{Word{}}),count);
}

// Relational inversion exchanges old and output symbols. Coefficient ports
// stay in their original left-to-right orientation; no word is reversed.
static Rows transposed(const Rows& forward,bool incorrectly_swap_ports=false) {
  Rows inverse;
  for(const auto& [old_symbol,rows]:forward)for(const auto& row:rows)
    inverse[row.output].push_back(incorrectly_swap_ports?
        a111x::Row{row.outgoing,old_symbol,row.incoming}:
        a111x::Row{row.incoming,old_symbol,row.outgoing});
  return inverse;
}
static void dual_tests(Counts& count) {
  Word old_word{symbol(10,0),symbol(11,1),symbol(UINT32_MAX,2)};
  Word new_word{symbol(20,0),symbol(21,1),symbol(22,2)};
  const int32_t ports[3]={-7,5,INT32_MAX};Rows forward;
  for(size_t i=0;i<3;++i)
    forward[old_word[i]]={{ports[i],new_word[i],ports[(i+1)%3]}};
  auto old_source=core(powers(old_word)),new_source=core(powers(new_word));
  Ref old_language=powers(old_word),new_language=powers(new_word);
  cyclic(old_source,new_language,new_language,forward,count,true);
  Rows reverse=transposed(forward),wrong=transposed(forward,true);
  cyclic(new_source,old_language,old_language,reverse,count);
  auto backward_hit=cyclic(new_source,old_language,old_language,reverse,count,true);
  require(!backward_hit.ok&&backward_hit.word.size()==3,
          "correct transpose lost its three-symbol predecessor");
  auto wrong_empty=cyclic(new_source,Ref{},old_language,wrong,count,true);
  require(wrong_empty.ok,"port-reversed relation should have no path in this fixed phase order");
  // The same distinction is checked by literal finite row enumeration.
  Words literal{new_word};
  require(explicit_image(literal,reverse,count)==Words{old_word},"transpose finite oracle");
  require(explicit_image(literal,wrong,count).empty(),"port reversal finite oracle");
  count.transpose_cases+=2;count.infinite_cases+=4;

  // Complete dual certificate model. Forward: a->a, b->t, c->b, t->t.
  // Terminal=t+, backward invariant K={b,c,t}+, FIRST=a+. A proper inverse
  // has Pre(K)=K, whereas omitting c would make a false closure certificate.
  const Symbol a=101,b=102,c=103,t=104;
  Rows transitions{{a,{{0,a,0}}},{b,{{0,t,0}}},{c,{{0,b,0}}},{t,{{0,t,0}}}};
  Rows predecessors=transposed(transitions);
  Ref K=all_words({b,c,t},false),first_language=powers(Word{a});
  auto terminal=a111x::positive_blocks({Word{t}});
  auto first_source=core(first_language);
  auto terminal_included=a111x::included(terminal,core(K));
  check_result(terminal_included,powers(Word{t}),K,false,count,"dual Terminal subset K");
  ++count.inclusion;++count.dual_obligations;
  auto closure=cyclic(core(K),K,K,predecessors,count);
  require(closure.ok,"valid backward invariant failed preservation");++count.dual_obligations;
  auto first_separated=cyclic(first_source,first_language,K,transitions,count,true);
  require(first_separated.ok,"valid backward invariant intersects FIRST");++count.dual_obligations;

  Ref omitted=all_words({b,t},false);
  auto missing_predecessor=cyclic(core(omitted),K,omitted,predecessors,count);
  require(!missing_predecessor.ok&&missing_predecessor.word.size()==1,
          "backward invariant omitting a predecessor was accepted");
  ++count.dual_obligations;++count.corrupted_invariants;
  Ref missing_terminal=all_words({b,c},false);
  auto terminal_failure=a111x::included(terminal,core(missing_terminal));
  check_result(terminal_failure,powers(Word{t}),missing_terminal,false,count,"dual missing terminal");
  require(!terminal_failure.ok,"backward invariant omitting Terminal was accepted");
  ++count.inclusion;++count.dual_obligations;++count.corrupted_invariants;
  Ref contaminated=all_words({a,b,c,t},false);
  auto first_failure=cyclic(first_source,first_language,contaminated,transitions,count,true);
  require(!first_failure.ok&&first_failure.word.size()==1,
          "backward invariant containing FIRST was accepted");
  ++count.dual_obligations;++count.corrupted_invariants;
  Rows changed=transitions;changed[a]={{0,b,0}};
  auto signature_failure=cyclic(first_source,powers(Word{b}),K,changed,count,true);
  require(!signature_failure.ok&&signature_failure.word.size()==1,
          "cyclic intersection retained a stale FIRST signature");
  ++count.changed_relations;++count.dual_obligations;count.infinite_cases+=5;
}

static void guard_tests(Counts& count) {
  auto invalid=[&](const std::function<void()>& f) {
    bool rejected=false;try{f();}catch(const std::invalid_argument&){rejected=true;}
    require(rejected,"malformed input did not throw invalid_argument");++count.invalid_cases;
  };
  auto valid=core(powers(Word{1,2}));
  invalid([&]{auto bad=valid;bad.start=uint32_t(bad.nodes.size());a111x::included(bad,valid);});
  invalid([&]{auto bad=valid;bad.nodes[0].edges={{1,999}};a111x::included(valid,bad);});
  invalid([&]{auto bad=valid;bad.nodes[0].edges={{1,0},{1,1}};a111x::included(valid,bad);});
  invalid([&]{a111x::DFA bad;bad.start=1;a111x::included(valid,bad);});
  invalid([&]{a111x::NFA n;n.starts={0};a111x::included(n,valid);});
  invalid([&]{a111x::NFA n;n.nodes.resize(1);n.starts={0};n.nodes[0].epsilon={1};a111x::included(n,valid);});
  invalid([&]{a111x::positive_blocks({});});
  invalid([&]{a111x::positive_blocks({Word{}});});
  invalid([&]{a111x::positive_blocks({Word{1},Word{}});});
  auto capped=[&](const std::function<void()>& f) {
    bool rejected=false;try{f();}catch(const a111x::Limit&){rejected=true;}
    require(rejected,"resource cap did not throw dedicated Limit");++count.cap_cases;
  };
  auto source=core(powers(Word{1,2,3})),target=core(all_words({1,2,3}));
  a111x::Limits limit;limit.states=1;capped([&]{a111x::included(source,target,limit);});
  limit=a111x::Limits{};limit.edges=1;capped([&]{a111x::included(source,target,limit);});
  limit=a111x::Limits{};limit.work=1;capped([&]{a111x::included(source,target,limit);});
  Rows rows{{1,{{-5,1,-5}}},{2,{{-5,2,-5}}},{3,{{-5,3,-5}}}};
  auto local=[&](Symbol x)->const std::vector<a111x::Row>&{return relation_row(rows,x);};
  limit=a111x::Limits{};limit.states=1;
  capped([&]{a111x::cyclic_image_included(source,target,local,limit);});
  capped([&]{a111x::cyclic_image_disjoint(source,target,local,limit);});
  limit=a111x::Limits{};limit.edges=1;
  capped([&]{a111x::cyclic_image_disjoint(source,target,local,limit);});
  limit=a111x::Limits{};limit.work=1;
  capped([&]{a111x::cyclic_image_disjoint(source,target,local,limit);});
}

int main(int argc,char** argv) {
  try {
    size_t rounds=argc>1?std::stoul(argv[1]):800;
    require(argc<=2&&rounds<=10000,"usage: exterior_invariant_selftest [finite_random_cases<=10000]");
    std::mt19937_64 rng(11124349);Counts count;
    first_and_infinite_tests(count);nfa_tests(rng,count);finite_tests(rng,rounds,count);
    dual_tests(count);guard_tests(count);
    std::cout<<"EXTERIOR_INVARIANT_CONTROLS PASS finite_random_cases="<<rounds
      <<" inclusion_checks="<<count.inclusion<<" intersection_checks="<<count.intersection
      <<" cyclic_checks="<<count.cyclic<<" cyclic_intersections="<<count.cyclic_intersections
      <<" product_states="<<count.product_states
      <<" shortest_witnesses="<<count.shortest_witnesses<<" epsilon_witnesses="<<count.epsilon_witnesses
      <<" replayed_rows="<<count.replayed_rows<<" finite_images="<<count.finite_images
      <<" raw_row_tuples="<<count.raw_row_tuples<<" closed_row_tuples="<<count.closed_row_tuples
      <<" image_words="<<count.image_words<<" infinite_cases="<<count.infinite_cases
      <<" first_languages="<<count.first_languages<<" corrupted_invariants="<<count.corrupted_invariants
      <<" changed_relations="<<count.changed_relations<<" dual_obligations="<<count.dual_obligations
      <<" transpose_cases="<<count.transpose_cases<<" invalid_cases="<<count.invalid_cases
      <<" cap_cases="<<count.cap_cases<<'\n';return 0;
  }catch(const std::exception& error){std::cerr<<"EXTERIOR_INVARIANT_CONTROLS FAIL: "<<error.what()<<'\n';return 1;}
}
