// Independent controls for the cyclic exterior graph implementation.
// Build: c++ -std=c++17 -O2 calculation/agent-113/test_exterior_cyclic.cpp -o /tmp/a113-test-exterior-cyclic
// Run:   /tmp/a113-test-exterior-cyclic
//
// Quotients preserve periodic words up to positive powers, not fixed-length
// closed-word languages. For each tested nonempty word w, periodic membership
// is decided EXACTLY: the finite relation labelled w must contain a directed
// cycle. No cutoff on the exponent of w is used.
#define A113_CYCLIC_NO_MAIN
#include "exterior_backward_cyclic.cpp"

#include <functional>
#include <random>
#include <sstream>

namespace independent_cyclic_tests {
using a113cyclic::Graph;
using a113fa::Budget;
using a113fa::Edge;
using a113fa::Label;
using a113fa::LimitReached;
using a113fa::State;
using Matrix = std::vector<uint64_t>;
using Word = std::vector<Label>;

struct Counts {
  uint64_t random_graphs=0, root_words=0, bisimulation_pairs=0;
  uint64_t pre_graphs=0, pre_words=0, tuple_words=0, tuples=0;
  uint64_t first_words=0, first_graphs=0, resource_controls=0;
} counts;

static void require(bool condition,const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}
static a113fa::Limits limits() {
  a113fa::Limits l;
  l.max_states=500000; l.max_edges=5000000;
  l.max_operations=500000000; l.seconds=180;
  return l;
}
static std::string context(const char* kind,size_t trial,const Word& word={}) {
  std::ostringstream s; s<<kind<<" trial="<<trial<<" word=";
  for (Label a:word) s<<a<<',';
  return s.str();
}
static void deduplicate(Graph& g) {
  for (auto& row:g.edges) {
    std::sort(row.begin(),row.end(),[](const Edge& a,const Edge& b) {
      return a.label!=b.label?a.label<b.label:a.to<b.to;
    });
    row.erase(std::unique(row.begin(),row.end(),[](const Edge& a,const Edge& b) {
      return a.label==b.label && a.to==b.to;
    }),row.end());
  }
}
static bool same_graph(Graph a,Graph b) {
  deduplicate(a); deduplicate(b);
  if (a.phase!=b.phase || a.edges.size()!=b.edges.size()) return false;
  for (size_t q=0;q<a.size();++q) {
    if (a.edges[q].size()!=b.edges[q].size()) return false;
    for (size_t j=0;j<a.edges[q].size();++j)
      if (a.edges[q][j].label!=b.edges[q][j].label ||
          a.edges[q][j].to!=b.edges[q][j].to) return false;
  }
  return true;
}

// All independent matrices use at most 64 vertices. Diagonals are initially
// FALSE for positive reachability; an empty walk is never a cycle witness.
static Matrix closure(Matrix relation) {
  const size_t n=relation.size();
  require(n<=64,"independent matrix domain exceeded");
  for (size_t k=0;k<n;++k)
    for (size_t i=0;i<n;++i)
      if ((relation[i]>>k)&1) relation[i]|=relation[k];
  return relation;
}
static bool has_diagonal(const Matrix& relation) {
  for (size_t q=0;q<relation.size();++q) if ((relation[q]>>q)&1) return true;
  return false;
}
static bool has_cycle(const Matrix& relation) {
  return has_diagonal(closure(relation));
}
static Matrix adjacency(const Graph& g) {
  require(g.size()<=64,"independent graph too large");
  Matrix r(g.size(),0);
  for (size_t q=0;q<g.size();++q)
    for (const Edge& e:g.edges[q]) r[q]|=uint64_t(1)<<e.to;
  return r;
}
static Matrix compose(const Matrix& a,const Matrix& b) {
  require(a.size()==b.size(),"matrix dimensions differ");
  Matrix out(a.size(),0);
  for (size_t q=0;q<a.size();++q) {
    uint64_t bits=a[q];
    while (bits) {
      unsigned j=static_cast<unsigned>(__builtin_ctzll(bits));
      bits&=bits-1; out[q]|=b[j];
    }
  }
  return out;
}
static Matrix identity(size_t n) {
  require(n<=64,"independent identity too large");
  Matrix r(n,0);
  for (size_t q=0;q<n;++q) r[q]=uint64_t(1)<<q;
  return r;
}
struct WordRelations {
  size_t n;
  std::unordered_map<Label,Matrix> letters;
  explicit WordRelations(const Graph& g):n(g.size()) {
    require(n<=64,"independent word graph too large");
    for (size_t q=0;q<n;++q) for (const Edge& e:g.edges[q]) {
      auto p=letters.emplace(e.label,Matrix(n,0));
      p.first->second[q]|=uint64_t(1)<<e.to;
    }
  }
  explicit WordRelations(size_t vertices):n(vertices) {}
  Matrix word(const Word& w) const {
    Matrix r=identity(n);
    for (Label a:w) {
      auto p=letters.find(a);
      if (p==letters.end()) return Matrix(n,0);
      r=compose(r,p->second);
    }
    return r;
  }
  bool closed(const Word& w) const { return has_diagonal(word(w)); }
  bool periodic(const Word& w) const { return has_cycle(word(w)); }
};
static Graph independent_core(const Graph& g) {
  Matrix reachable=closure(adjacency(g));
  std::vector<State> map(g.size(),a113fa::absent); Graph out;
  for (State q=0;q<g.size();++q)
    if ((reachable[q]>>q)&1) map[q]=out.add_state(g.phase[q]);
  for (State q=0;q<g.size();++q) if (map[q]!=a113fa::absent)
    for (const Edge& e:g.edges[q])
      if ((reachable[e.to]>>q)&1) out.add_edge(map[q],e.label,map[e.to]);
  deduplicate(out); return out;
}

// Greatest phase-respecting strong bisimulation, by explicit pair deletion.
// This does not use partition signatures or the production refinement code.
static std::vector<std::vector<bool>> bisimulation(const Graph& g) {
  const size_t n=g.size();
  std::vector<std::vector<bool>> r(n,std::vector<bool>(n,false));
  for (size_t a=0;a<n;++a) for (size_t b=0;b<n;++b) r[a][b]=g.phase[a]==g.phase[b];
  bool changed=true;
  auto matches=[&](size_t a,size_t b) {
    for (const Edge& x:g.edges[a]) {
      bool found=false;
      for (const Edge& y:g.edges[b])
        if (x.label==y.label && r[x.to][y.to]) { found=true; break; }
      if (!found) return false;
    }
    return true;
  };
  while (changed) {
    changed=false;
    for (size_t a=0;a<n;++a) for (size_t b=0;b<n;++b)
      if (r[a][b] && (!matches(a,b) || !matches(b,a))) {
        r[a][b]=false; changed=true;
      }
  }
  return r;
}
static Graph disjoint_union(const Graph& a,const Graph& b) {
  Graph g=a;
  for (uint32_t phase:b.phase) g.add_state(phase);
  for (State q=0;q<b.size();++q)
    for (const Edge& e:b.edges[q]) g.add_edge(a.size()+q,e.label,a.size()+e.to);
  return g;
}
static bool independent_equivalent(const Graph& a,const Graph& b) {
  auto relation=bisimulation(disjoint_union(a,b));
  for (size_t q=0;q<a.size();++q) {
    bool found=false;
    for (size_t r=0;r<b.size();++r) found=found || relation[q][a.size()+r];
    if (!found) return false;
  }
  for (size_t r=0;r<b.size();++r) {
    bool found=false;
    for (size_t q=0;q<a.size();++q) found=found || relation[q][a.size()+r];
    if (!found) return false;
  }
  return true;
}
template<class F>
static void words(const std::vector<std::vector<Label>>& domains,F visit) {
  Word word(domains.size());
  auto recurse=[&](auto&& self,size_t i)->void {
    if (i==domains.size()) { visit(word); return; }
    for (Label a:domains[i]) { word[i]=a; self(self,i+1); }
  };
  recurse(recurse,0);
}
static Graph random_graph(std::mt19937& random) {
  Graph g; const unsigned n=random()%8;
  for (unsigned q=0;q<n;++q) g.add_state(random()%3);
  for (State q=0;q<n;++q) for (State r=0;r<n;++r)
    for (Label a=0;a<2;++a) if (random()%5==0) {
      g.add_edge(q,a,r);
      if (random()%4==0) g.add_edge(q,a,r);
    }
  return g;
}
static void general_graph_controls(std::mt19937& random,Budget& budget) {
  for (size_t trial=0;trial<400;++trial) {
    Graph g=random_graph(random);
    Graph actual=a113cyclic::core(g,budget), expected=independent_core(g);
    require(same_graph(actual,expected),context("SCC core",trial));
    auto relation=bisimulation(actual);
    auto partition=a113cyclic::partition(actual,budget);
    require(partition.size()==actual.size(),context("partition size",trial));
    for (size_t a=0;a<actual.size();++a) for (size_t b=0;b<actual.size();++b)
      require((partition[a]==partition[b])==relation[a][b],context("bisimulation relation",trial));
    Graph quotient=a113cyclic::reduce(actual,budget);
    require(independent_equivalent(actual,quotient),context("quotient bisimulation",trial));
    WordRelations original(g), reduced(quotient);
    for (size_t length=1;length<=5;++length)
      words(std::vector<std::vector<Label>>(length,{0,1}),[&](const Word& w) {
        require(original.periodic(w)==reduced.periodic(w),context("periodic quotient",trial,w));
        ++counts.root_words;
      });
    Graph other=independent_core(random_graph(random));
    require(a113cyclic::equivalent(actual,other,budget)==independent_equivalent(actual,other),
            context("joint bisimulation",trial));
    ++counts.bisimulation_pairs; ++counts.random_graphs;
  }
}

// This scalar FORWARD arithmetic is independent of Engine::inverse/forward.
// PRE's input graph is a graph of inner-cut letters; its output word specifies
// outer-cut letters. The coefficient still travels forward in temporal order.
struct ScalarTile { Label inner; int next; };
static Label label(int b,int phase,int l,int h,int y) {
  return static_cast<Label>(phase*4*b+l*2*b+h*b+y);
}
static std::vector<ScalarTile> scalar_forward(int b,const std::string& g,Label old,int x) {
  int phase=old/(4*b), rest=old%(4*b), l=rest/(2*b), h=(rest/b)%2, y=rest%b;
  std::vector<ScalarTile> out;
  for (int inward=0;inward<=1;++inward) {
    if ((x+inward)/b!=h) continue;
    int low=(x+l)%b, high=(x+inward)%b;
    out.push_back({label(b,phase,(x+l)/b,inward,g[phase]=='1'?high:0),
                   low+(g[phase]=='1'?y:high)});
  }
  return out;
}
static std::vector<Label> alphabet(int b,const std::string& g,int t) {
  std::vector<Label> out;
  for (int l=0;l<2;++l) for (int h=0;h<2;++h)
    for (int y=0;y<(g[t]=='1'?b:1);++y) out.push_back(label(b,t,l,h,y));
  return out;
}
static WordRelations independent_pre_relations(const Graph& graph,int b,const std::string& g) {
  const int domain=2*b-1; WordRelations out(graph.size()*domain);
  for (int t=0;t<static_cast<int>(g.size());++t) for (Label old:alphabet(b,g,t)) {
    Matrix row(out.n,0);
    for (State q=0;q<graph.size();++q) for (int x=0;x<domain;++x)
      for (const ScalarTile& tile:scalar_forward(b,g,old,x))
        for (const Edge& e:graph.edges[q]) if (e.label==tile.inner)
          row[q*domain+x]|=uint64_t(1)<<(e.to*domain+tile.next);
    out.letters.emplace(old,std::move(row));
  }
  return out;
}
static WordRelations independent_first_relations(const Graph& graph,int b,const std::string& g) {
  const int domain=2*b-1; WordRelations out(graph.size()*domain);
  for (State q=0;q<graph.size();++q) for (int x=1;x<domain;++x) {
    int t=graph.phase[q], overflow=g[t]-'0';
    Label start=label(b,t,0,overflow,overflow?1:0);
    for (const ScalarTile& tile:scalar_forward(b,g,start,x))
      for (const Edge& e:graph.edges[q]) if (e.label==tile.inner) {
        auto p=out.letters.emplace(e.label,Matrix(out.n,0));
        p.first->second[q*domain+x]|=uint64_t(1)<<(e.to*domain+tile.next);
      }
  }
  return out;
}
static bool tuple_closed(const Graph& graph,int b,const std::string& g,const Word& w) {
  std::vector<int> coefficient(w.size(),0); bool accepted=false;
  const int domain=2*b-1;
  auto enumerate=[&](auto&& self,size_t i)->void {
    if (i<w.size()) {
      for (int x=0;x<domain;++x) { coefficient[i]=x; self(self,i+1); }
      return;
    }
    ++counts.tuples; Matrix paths=identity(graph.size());
    for (size_t t=0;t<w.size();++t) {
      Matrix step(graph.size(),0);
      for (const ScalarTile& tile:scalar_forward(b,g,w[t],coefficient[t]))
        if (tile.next==coefficient[(t+1)%w.size()])
          for (State q=0;q<graph.size();++q)
            for (const Edge& e:graph.edges[q])
              if (e.label==tile.inner) step[q]|=uint64_t(1)<<e.to;
      paths=compose(paths,step);
    }
    accepted=accepted || has_diagonal(paths);
  };
  enumerate(enumerate,0); return accepted;
}
static Graph typed_random_graph(std::mt19937& random,int b,const std::string& g) {
  Graph graph; std::vector<std::vector<State>> at(g.size());
  for (uint32_t t=0;t<g.size();++t) {
    unsigned n=1+random()%2;
    while (n--) at[t].push_back(graph.add_state(t));
  }
  for (uint32_t t=0;t<g.size();++t) for (State q:at[t])
    for (State r:at[(t+1)%g.size()]) for (Label a:alphabet(b,g,t))
      if (random()%4==0) {
        graph.add_edge(q,a,r);
        if (random()%5==0) graph.add_edge(q,a,r);
      }
  return graph;
}
static void product_controls(std::mt19937& random,Budget& budget) {
  const std::string streams[]={"00","01","10","11"};
  for (size_t trial=0;trial<80;++trial) {
    a113backward::Options o; o.base=2; o.period=2; o.g=streams[trial%4];
    o.e=std::string{char('0'+random()%2),char('0'+random()%2)}; o.limits=limits();
    Budget arithmetic_budget(o.limits); a113backward::Engine engine(o,arithmetic_budget);
    Graph graph=typed_random_graph(random,o.base,o.g);
    Graph pre=a113cyclic::preimage(graph,engine,budget);
    Graph pre_reduced=a113cyclic::reduce(pre,budget);
    Graph input_reduced=a113cyclic::reduce(a113cyclic::core(graph,budget),budget);
    Graph composed=a113cyclic::preimage(input_reduced,engine,budget);
    WordRelations oracle=independent_pre_relations(graph,o.base,o.g);
    WordRelations result(pre), quotient(pre_reduced), alternate(composed);
    for (int repetitions=1;repetitions<=2;++repetitions) {
      std::vector<std::vector<Label>> domains;
      for (int t=0;t<2*repetitions;++t) domains.push_back(alphabet(o.base,o.g,t%2));
      size_t index=0;
      words(domains,[&](const Word& w) {
        bool root=oracle.periodic(w), closed=oracle.closed(w);
        require(result.closed(w)==closed,context("exact PRE closed word",trial,w));
        require(result.periodic(w)==root,context("exact PRE periodic word",trial,w));
        require(quotient.periodic(w)==root,context("quotiented PRE word",trial,w));
        require(alternate.periodic(w)==root,context("PRE quotient composition",trial,w));
        if (repetitions==1 || index<16) {
          require(tuple_closed(graph,o.base,o.g,w)==closed,context("full coefficient tuple",trial,w));
          ++counts.tuple_words;
        }
        ++index; ++counts.pre_words;
      });
    }
    Graph first=a113cyclic::first_intersection(graph,engine,budget);
    WordRelations first_oracle=independent_first_relations(graph,o.base,o.g), first_result(first);
    Matrix aggregate(first_oracle.n,0);
    for (const auto& entry:first_oracle.letters)
      for (size_t q=0;q<aggregate.size();++q) aggregate[q]|=entry.second[q];
    require((first.size()!=0)==has_cycle(aggregate),context("positive FIRST cycle",trial));
    words({alphabet(o.base,o.g,0),alphabet(o.base,o.g,1)},[&](const Word& w) {
      require(first_oracle.periodic(w)==first_result.periodic(w),context("positive FIRST word",trial,w));
      ++counts.first_words;
    });
    ++counts.first_graphs; ++counts.pre_graphs;
  }
}
static Graph chain(size_t n) {
  Graph g;
  for (size_t q=0;q<n;++q) g.add_state(0);
  for (State q=0;q+1<n;++q) g.add_edge(q,0,q+1);
  return g;
}
template<class F>
static void must_limit(a113fa::Limits lim,F operation,const char* name,uint64_t minimum_operations=0) {
  bool limited=false; Budget budget(lim);
  try { operation(budget); }
  catch (const LimitReached&) { limited=true; }
  require(limited,std::string("resource limit silently accepted: ")+name);
  require(budget.operations>=minimum_operations,std::string("resource control did not reach intended stage: ")+name);
  ++counts.resource_controls;
}
static void explicit_controls(Budget& budget) {
  Graph two; two.add_state(0); two.add_state(0); two.add_edge(0,0,1); two.add_edge(1,0,0);
  Graph one=a113cyclic::reduce(two,budget);
  require(one.size()==1,"two-cycle quotient should have one state");
  require(!WordRelations(two).closed({0}) && WordRelations(one).closed({0}),
          "fixed-k counterexample disappeared");
  require(WordRelations(two).periodic({0}) && WordRelations(one).periodic({0}),
          "positive-power membership failed");
  require(a113cyclic::equivalent(two,one,budget),"positive joint-bisimulation control");
  Graph other; other.add_state(0); other.add_edge(0,1,0);
  require(!a113cyclic::equivalent(two,other,budget),"negative joint-bisimulation control");
  Graph recolored=one; recolored.phase[0]=1;
  require(!a113cyclic::equivalent(one,recolored,budget),"phase-colour guard failed");
  Graph empty_vertex; empty_vertex.add_state(0);
  require(a113cyclic::core(empty_vertex,budget).size()==0,"zero-length walk counted as cycle");
  require(!has_cycle(adjacency(empty_vertex)),"independent cycle convention failed");
  a113fa::Limits l=limits(); l.max_states=1;
  must_limit(l,[&](Budget& b){ (void)a113cyclic::core(two,b); },"SCC states");
  must_limit(l,[&](Budget& b){ (void)a113cyclic::equivalent(one,other,b); },"joint states");
  Graph edges=one; edges.add_edge(0,1,0); l=limits(); l.max_edges=1;
  must_limit(l,[&](Budget& b){ (void)a113cyclic::core(edges,b); },"SCC edges");
  must_limit(l,[&](Budget& b){ (void)a113cyclic::partition(edges,b); },"refinement edges");
  l=limits(); l.max_operations=60;
  must_limit(l,[&](Budget& b){ (void)a113cyclic::partition(chain(12),b); },
             "refinement operations",46);
  // Different long chains agree on shallow observations. An interrupted
  // refinement must throw, not report them equivalent from an unstable cut.
  l.max_operations=180;
  must_limit(l,[&](Budget& b){ (void)a113cyclic::equivalent(chain(12),chain(13),b); },
             "stable-only equivalence",156);
}
} // namespace independent_cyclic_tests

int main() {
  using namespace independent_cyclic_tests;
  try {
    // Keep the included CLI helpers referenced in this strict-warning build.
    // Tests never invoke the CLI or alter process resource limits.
    (void)&a113cyclic::parse_options;
    (void)&a113cyclic::solve;
    Budget budget(limits()); std::mt19937 random(0x113C24U);
    explicit_controls(budget);
    general_graph_controls(random,budget);
    product_controls(random,budget); budget.check_time();
    std::cout<<"{\"status\":\"PASS\",\"random_graphs\":"<<counts.random_graphs
             <<",\"periodic_word_checks\":"<<counts.root_words
             <<",\"joint_bisimulation_checks\":"<<counts.bisimulation_pairs
             <<",\"pre_graphs\":"<<counts.pre_graphs<<",\"pre_word_checks\":"<<counts.pre_words
             <<",\"full_tuple_word_checks\":"<<counts.tuple_words<<",\"coefficient_tuples\":"<<counts.tuples
             <<",\"first_graphs\":"<<counts.first_graphs<<",\"first_word_checks\":"<<counts.first_words
             <<",\"resource_controls\":"<<counts.resource_controls
             <<",\"fixed_k_counterexample\":true,\"periodic_membership\":\"exact_relation_cycle\"}\n";
    return 0;
  } catch (const std::exception& e) {
    std::cerr<<"test_exterior_cyclic FAILED: "<<e.what()<<'\n'; return 1;
  }
}
