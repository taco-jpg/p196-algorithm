// Backward closed-walk graphs for every positive repetition of an E/G driver.
// Full phase-coloured strong bisimulation preserves closed-walk languages up
// to powers of whole words. It does NOT preserve counts at a fixed repetition.
// Reuse our independently tested scalar tiles and CLI/resource definitions.
#define main a113_backward_regular_dependency_main
#include "exterior_backward_regular.cpp"
#undef main

namespace a113cyclic {
using a113fa::Budget;
using a113fa::State;
using a113fa::Label;
using a113fa::Edge;
using a113fa::LimitReached;
using a113backward::Engine;
using a113backward::Options;
constexpr State absent=a113fa::absent;

struct Graph {
  std::vector<std::vector<Edge>> edges;
  std::vector<uint32_t> phase;
  State add_state(uint32_t t) {
    if (edges.size()>=absent) throw LimitReached("graph index capacity");
    State q=edges.size(); edges.emplace_back(); phase.push_back(t); return q;
  }
  void add_edge(State q,Label a,State to) {
    if (q>=size() || to>=size()) throw std::invalid_argument("graph edge bounds");
    edges[q].push_back({a,to});
  }
  size_t size() const { return edges.size(); }
  size_t edge_count() const {
    size_t result=0; for (const auto& row:edges) result+=row.size(); return result;
  }
};
static Graph allocate(size_t n,Budget& budget) {
  budget.observe(n,0); // enforce the state/index cap BEFORE allocating the graph
  Graph result; result.edges.resize(n); result.phase.resize(n); return result;
}
void validate(const Graph& graph,Budget& budget) {
  if (graph.phase.size()!=graph.size()) throw std::invalid_argument("graph phase vector size");
  budget.observe(graph.size(),0); size_t edges=0;
  for (const auto& row:graph.edges) for (const Edge& edge:row) {
    budget.tick(); if (edge.to>=graph.size()) throw std::invalid_argument("graph target index");
    ++edges;
  }
  budget.observe(graph.size(),edges);
}
static void unique_rows(Graph& graph,Budget& budget) {
  size_t count=0;
  for (auto& row:graph.edges) {
    std::sort(row.begin(),row.end(),[&](const Edge& a,const Edge& b){budget.tick();return a<b;});
    row.erase(std::unique(row.begin(),row.end()),row.end()); count+=row.size();
  }
  budget.observe(graph.size(),count);
}

// Keep exactly edges lying on nonempty directed cycles. Kosaraju's two
// passes use explicit stacks; surviving vertices retain ascending old order.
Graph core(const Graph& graph,Budget& budget) {
  validate(graph,budget); size_t n=graph.size();
  std::vector<std::vector<State>> reverse(n);
  for (State q=0;q<n;++q) for (const Edge& edge:graph.edges[q]) {
    budget.tick(); reverse[edge.to].push_back(q);
  }
  std::vector<uint8_t> seen(n,0); std::vector<State> finish; finish.reserve(n);
  for (State q=0;q<n;++q) if (!seen[q]) {
    std::vector<std::pair<State,size_t>> stack{{q,0}}; seen[q]=1;
    while (!stack.empty()) {
      budget.tick(); auto& frame=stack.back();
      if (frame.second==graph.edges[frame.first].size()) {
        finish.push_back(frame.first); stack.pop_back(); continue;
      }
      State next=graph.edges[frame.first][frame.second++].to;
      if (!seen[next]) { seen[next]=1; stack.push_back({next,0}); }
    }
  }
  std::vector<State> component(n,absent); std::vector<size_t> component_size;
  for (auto it=finish.rbegin();it!=finish.rend();++it) if (component[*it]==absent) {
    State id=component_size.size(); component_size.push_back(0);
    std::vector<State> stack{*it}; component[*it]=id;
    while (!stack.empty()) {
      State q=stack.back(); stack.pop_back(); ++component_size[id]; budget.tick();
      for (State prior:reverse[q]) {
        budget.tick(); if (component[prior]==absent) { component[prior]=id; stack.push_back(prior); }
      }
    }
  }
  std::vector<State> map(n,absent); Graph result;
  for (State q=0;q<n;++q) {
    budget.tick(); bool live=component_size[component[q]]>1;
    for (const Edge& edge:graph.edges[q]) { budget.tick(); if (edge.to==q) live=true; }
    if (live) { budget.observe(result.size()+1,0); map[q]=result.add_state(graph.phase[q]); }
  }
  size_t edges=0;
  for (State q=0;q<n;++q) if (map[q]!=absent) for (const Edge& edge:graph.edges[q]) {
    budget.tick();
    if (component[q]==component[edge.to]) {
      if (map[edge.to]==absent) throw std::logic_error("cyclic component lost a target");
      budget.observe(result.size(),edges+1);
      result.edges[map[q]].push_back({edge.label,map[edge.to]}); ++edges;
    }
  }
  unique_rows(result,budget); return result;
}

// Monotone partition refinement to the FULL strong-bisimulation fixed point.
// Keeping the previous class in each signature prevents any class merging;
// equality of successive class counts therefore proves stabilization.
std::vector<State> partition(const Graph& graph,Budget& budget) {
  validate(graph,budget); size_t n=graph.size();
  if (!n) return {};
  std::vector<State> classes(n),next(n);
  std::unordered_map<uint32_t,State> phase_class;
  for (State q=0;q<n;++q) {
    budget.tick(); auto found=phase_class.emplace(graph.phase[q],phase_class.size());
    classes[q]=found.first->second;
  }
  size_t count=phase_class.size();
  while (true) {
    budget.check_time();
    std::unordered_map<std::vector<uint64_t>,State,a113fa::VectorHash> signatures;
    for (State q=0;q<n;++q) {
      budget.tick(); std::vector<uint64_t> signature; signature.reserve(graph.edges[q].size()+1);
      for (const Edge& edge:graph.edges[q]) {
        budget.tick(); signature.push_back((static_cast<uint64_t>(edge.label)<<32)|classes[edge.to]);
      }
      std::sort(signature.begin(),signature.end(),[&](uint64_t a,uint64_t b){budget.tick();return a<b;});
      signature.erase(std::unique(signature.begin(),signature.end()),signature.end());
      signature.insert(signature.begin(),classes[q]);
      auto found=signatures.emplace(std::move(signature),signatures.size());
      next[q]=found.first->second;
    }
    size_t new_count=signatures.size();
    if (new_count<count) throw std::logic_error("partition refinement merged old classes");
    classes.swap(next);
    if (new_count==count) { budget.check_time(); return classes; }
    count=new_count;
  }
}

Graph reduce(const Graph& graph,Budget& budget) {
  auto classes=partition(graph,budget);
  if (classes.empty()) return {};
  size_t count=static_cast<size_t>(*std::max_element(classes.begin(),classes.end()))+1;
  Graph result=allocate(count,budget); std::vector<uint8_t> assigned(count,0); size_t edges=0;
  // Union ALL member edges. The result does not rely on selecting a lucky
  // class representative, including when tested on nondeterministic graphs.
  for (State q=0;q<graph.size();++q) {
    budget.tick(); State c=classes[q];
    if (assigned[c] && result.phase[c]!=graph.phase[q]) throw std::logic_error("mixed phase bisimulation class");
    assigned[c]=1; result.phase[c]=graph.phase[q];
    for (const Edge& edge:graph.edges[q]) {
      budget.tick(); budget.observe(result.size(),edges+1);
      result.edges[c].push_back({edge.label,classes[edge.to]}); ++edges;
    }
  }
  unique_rows(result,budget); return result;
}

bool equivalent(const Graph& a,const Graph& b,Budget& budget) {
  validate(a,budget); validate(b,budget);
  if (a.size()>budget.limits.max_states-b.size()) throw LimitReached("joint graph state cap");
  size_t n=a.size()+b.size(),edges=a.edge_count()+b.edge_count();
  budget.observe(n,edges); Graph both=allocate(n,budget);
  for (State q=0;q<a.size();++q) { budget.tick(); both.phase[q]=a.phase[q]; both.edges[q]=a.edges[q]; }
  for (State q=0;q<b.size();++q) {
    budget.tick(); State target=a.size()+q; both.phase[target]=b.phase[q];
    for (const Edge& edge:b.edges[q]) {
      budget.tick(); both.edges[target].push_back({edge.label,static_cast<State>(a.size()+edge.to)});
    }
  }
  auto classes=partition(both,budget); std::vector<uint8_t> coverage(n,0);
  for (State q=0;q<n;++q) { budget.tick(); coverage[classes[q]]|=q<a.size()?1:2; }
  for (uint8_t mask:coverage) { budget.tick(); if (mask && mask!=3) return false; }
  budget.check_time(); return true;
}

static void typed(const Graph& graph,Engine& engine,Budget& budget) {
  validate(graph,budget);
  for (State q=0;q<graph.size();++q) {
    budget.tick();
    if (graph.phase[q]>=static_cast<uint32_t>(engine.p)) throw std::invalid_argument("graph phase outside unit period");
    for (const Edge& edge:graph.edges[q]) {
      budget.tick();
      if (engine.decode(edge.label).phase!=static_cast<int>(graph.phase[q]) ||
          graph.phase[edge.to]!=(graph.phase[q]+1)%engine.p)
        throw std::invalid_argument("edge does not advance its labelled phase");
    }
  }
}
static Graph boundary(Engine& engine,Budget& budget,bool terminal) {
  Graph result=allocate(engine.p,budget); budget.observe(engine.p,engine.p);
  for (int t=0;t<engine.p;++t) {
    budget.tick(); int e=engine.o.e[t]-'0',g=engine.o.g[t]-'0';
    result.phase[t]=t;
    Label label=terminal?engine.label(t,e,1-e,g?(engine.b-1)*e:0):engine.label(t,0,g,g?1:0);
    result.edges[t].push_back({label,static_cast<State>((t+1)%engine.p)});
  }
  return result;
}
static Graph tile_product(const Graph& graph,Engine& engine,Budget& budget,bool backward,bool positive) {
  typed(graph,engine,budget);
  size_t domain=engine.domain;
  if (graph.size()>budget.limits.max_states/domain) throw LimitReached("tile product state cap");
  size_t n=graph.size()*domain; Graph result=allocate(n,budget); size_t edges=0;
  for (State q=0;q<graph.size();++q) for (int x=0;x<engine.domain;++x) {
    budget.tick(); State current=q*domain+x; result.phase[current]=graph.phase[q];
    if (positive && x==0) continue;
    for (const Edge& edge:graph.edges[q]) {
      budget.tick();
      const auto& relation=backward?engine.inverse(edge.label):engine.forward(edge.label);
      for (const auto& tile:relation[x]) {
        budget.tick(); if (positive && tile.next==0) continue;
        budget.observe(n,edges+1);
        result.edges[current].push_back({tile.output,static_cast<State>(edge.to*domain+tile.next)}); ++edges;
      }
    }
  }
  return result;
}
Graph preimage(const Graph& graph,Engine& engine,Budget& budget) {
  return tile_product(graph,engine,budget,true,false);
}
Graph physical_first(Engine& engine,Budget& budget) {
  Graph raw=tile_product(boundary(engine,budget,false),engine,budget,false,true);
  return reduce(core(raw,budget),budget);
}

// Equal-phase synchronous product, then discard all edges outside cycles.
// Only pairs with matching phase are allocated. In the P24 driver the reduced
// FIRST graph has one vertex per phase, avoiding an unnecessary 19-fold product.
Graph intersection(const Graph& a,const Graph& b,Budget& budget) {
  validate(a,budget); validate(b,budget);
  std::unordered_map<uint32_t,std::vector<State>> by_phase;
  std::vector<State> rank(b.size());
  for (State q=0;q<b.size();++q) {
    budget.tick(); auto& row=by_phase[b.phase[q]]; rank[q]=row.size(); row.push_back(q);
  }
  std::vector<size_t> offset(a.size()); size_t n=0;
  for (State q=0;q<a.size();++q) {
    budget.tick(); offset[q]=n; auto found=by_phase.find(a.phase[q]);
    size_t add=found==by_phase.end()?0:found->second.size();
    if (add>budget.limits.max_states-n) throw LimitReached("intersection product state cap");
    n+=add;
  }
  Graph result=allocate(n,budget); size_t edges=0;
  for (State q=0;q<a.size();++q) {
    auto group=by_phase.find(a.phase[q]); if (group==by_phase.end()) continue;
    auto left=a.edges[q];
    std::sort(left.begin(),left.end(),[&](const Edge& x,const Edge& y){budget.tick();return x<y;});
    for (State r:group->second) {
      budget.tick(); State current=offset[q]+rank[r]; result.phase[current]=a.phase[q];
      auto right=b.edges[r];
      std::sort(right.begin(),right.end(),[&](const Edge& x,const Edge& y){budget.tick();return x<y;});
      size_t i=0,j=0;
      while (i<left.size() && j<right.size()) {
        budget.tick();
        if (left[i].label<right[j].label) { ++i; continue; }
        if (right[j].label<left[i].label) { ++j; continue; }
        size_t iend=i+1,jend=j+1;
        while (iend<left.size() && left[iend].label==left[i].label) ++iend;
        while (jend<right.size() && right[jend].label==right[j].label) ++jend;
        for (size_t ai=i;ai<iend;++ai) for (size_t bj=j;bj<jend;++bj) {
          budget.tick(); State x=left[ai].to,y=right[bj].to;
          if (a.phase[x]!=b.phase[y]) continue;
          budget.observe(n,edges+1);
          result.edges[current].push_back({left[ai].label,static_cast<State>(offset[x]+rank[y])}); ++edges;
        }
        i=iend; j=jend;
      }
    }
  }
  return core(result,budget);
}
Graph first_intersection(const Graph& graph,Engine& engine,Budget& budget) {
  return intersection(graph,physical_first(engine,budget),budget);
}

static std::vector<Label> cycle_word(const Graph& graph,Budget& budget) {
  State start=absent;
  for (State q=0;q<graph.size();++q) if (graph.phase[q]==0) { start=q; break; }
  if (start==absent) throw std::logic_error("nonempty typed cycle graph lacks phase zero");
  std::vector<State> parent(graph.size(),absent),queue{start};
  std::vector<Label> letter(graph.size()); parent[start]=start;
  for (size_t i=0;i<queue.size();++i) {
    State q=queue[i]; budget.tick();
    for (const Edge& edge:graph.edges[q]) {
      budget.tick();
      if (edge.to==start) {
        std::vector<Label> word{edge.label};
        for (State here=q;here!=start;here=parent[here]) word.push_back(letter[here]);
        std::reverse(word.begin(),word.end()); return word;
      }
      if (parent[edge.to]==absent) { parent[edge.to]=q; letter[edge.to]=edge.label; queue.push_back(edge.to); }
    }
  }
  throw std::logic_error("cyclic core vertex has no return path");
}
static void dump(const Graph& graph,Engine& engine,int depth,Budget& budget) {
  typed(graph,engine,budget); std::ostringstream text;
  text<<"{\"event\":\"dump\",\"format\":\"p196-exterior-cyclic-v1\",\"direction\":\"backward\""
      <<",\"role\":\"frontier\",\"semantics\":\"closed walks up to whole-word powers\""
      <<",\"fixed_repetition_counts_available\":false,\"base\":"<<engine.b
      <<",\"e\":"<<a113backward::quoted(engine.o.e)<<",\"g\":"<<a113backward::quoted(engine.o.g)
      <<",\"depth\":"<<depth<<",\"phase\":[";
  for (State q=0;q<graph.size();++q) { budget.tick(); if (q) text<<','; text<<graph.phase[q]; }
  text<<"],\"transitions\":[";
  for (State q=0;q<graph.size();++q) {
    if (q) text<<',';
    text<<'[';
    for (size_t j=0;j<graph.edges[q].size();++j) {
      budget.tick(); if (j) text<<',';
      text<<'['<<graph.edges[q][j].label<<','<<graph.edges[q][j].to<<']';
    }
    text<<']';
  }
  text<<"]}"; budget.check_time(); std::cout<<text.str()<<'\n'<<std::flush; budget.check_time();
}
static Options parse_options(int argc,char** argv) {
  Options options=a113backward::parse(argc,argv);
  auto supplied=[&](const char* flag) {
    for (int i=4;i<argc;i+=2) if (std::string(argv[i])==flag) return true;
    return false;
  };
  if (!supplied("--states")) options.limits.max_states=1000000;
  if (!supplied("--edges")) options.limits.max_edges=20000000;
  if (!supplied("--ops")) options.limits.max_operations=1000000000;
  return options;
}
static int solve(const Options& options) {
  Budget budget(options.limits); Engine engine(options,budget);
  Graph graph=boundary(engine,budget,true),first;
  if (options.dump_depth<0) {
    first=physical_first(engine,budget);
    std::cout<<"{\"event\":\"physical_first_graph\",\"vertices\":"<<first.size()
             <<",\"edges\":"<<first.edge_count()<<"}\n"<<std::flush;
    if (!first.size()) {
      budget.check_time();
      std::cout<<"{\"status\":\"NO_EXTERIORS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\""
               <<",\"reason\":\"empty_positive_first_graph\"}\n"; return 0;
    }
  }
  for (int depth=0;depth<=options.depth;++depth) {
    // The terminal constant-(b-1) column self-loop survives every PRE layer.
    // An empty backward graph therefore signals an implementation error.
    if (!graph.size()) throw std::logic_error("terminal neutral word vanished from backward graph");
    std::cout<<"{\"event\":\"backward_graph\",\"depth\":"<<depth<<",\"vertices\":"<<graph.size()
             <<",\"edges\":"<<graph.edge_count()<<",\"operations\":"<<budget.operations
             <<",\"rss_mib\":"<<a113backward::rss_mib()<<"}\n"<<std::flush;
    if (options.dump_depth==depth) {
      dump(graph,engine,depth,budget);
      std::cout<<"{\"status\":\"DUMPED\",\"no_exclusion_claim\":true}\n"; return 0;
    }
    if (options.dump_depth<0) {
      Graph hit=intersection(graph,first,budget);
      std::cout<<"{\"event\":\"first_cycle_intersection\",\"depth\":"<<depth
               <<",\"empty\":"<<(hit.size()?"false":"true")<<",\"vertices\":"<<hit.size()
               <<",\"edges\":"<<hit.edge_count()<<"}\n"<<std::flush;
      if (hit.size()) {
        auto word=cycle_word(hit,budget);
        if (word.empty() || word.size()%engine.p) throw std::logic_error("candidate cycle has invalid temporal length");
        budget.check_time();
        std::cout<<"{\"status\":\"RECONSTRUCTION_REQUIRED\",\"reason\":\"positive_first_cycle\""
                 <<",\"depth\":"<<depth<<",\"padded_columns\":"<<depth+1
                 <<",\"quotient_cycle_laps\":"<<word.size()/engine.p
                 <<",\"power_lifting_may_be_required\":true,\"word\":[";
        for (size_t i=0;i<word.size();++i) { if (i) std::cout<<','; std::cout<<word[i]; }
        std::cout<<"]}\n"; return 0;
      }
    }
    if (depth==options.depth) break;
    Graph raw=preimage(graph,engine,budget),useful=core(raw,budget),next=reduce(useful,budget);
    if (!next.size()) throw std::logic_error("terminal neutral word vanished from graph preimage");
    bool same=options.dump_depth<0 && equivalent(graph,next,budget);
    std::cout<<"{\"event\":\"preimage_graph\",\"from_depth\":"<<depth
             <<",\"raw_vertices\":"<<raw.size()<<",\"raw_edges\":"<<raw.edge_count()
             <<",\"core_vertices\":"<<useful.size()<<",\"core_edges\":"<<useful.edge_count()
             <<",\"quotient_vertices\":"<<next.size()<<",\"quotient_edges\":"<<next.edge_count()
             <<",\"full_bisimulation_checked\":"<<(options.dump_depth<0?"true":"false")
             <<",\"same\":"<<(same?"true":"false")<<"}\n"<<std::flush;
    if (same) {
      budget.check_time();
      std::cout<<"{\"status\":\"NO_EXTERIORS_ALL_REPETITIONS\",\"classification\":\"COMPUTED\""
               <<",\"reason\":\"full_strong_bisimulation_fixed_point\",\"depth\":"<<depth
               <<",\"unit_period\":"<<engine.p<<",\"operations\":"<<budget.operations<<"}\n"; return 0;
    }
    graph=std::move(next);
  }
  budget.check_time();
  std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"backward_graph_depth_limit\",\"depth\":"<<options.depth<<"}\n";
  return 3;
}
} // namespace a113cyclic

#ifndef A113_CYCLIC_NO_MAIN
int main(int argc,char** argv) {
  using a113backward::quoted;
  try {
    auto options=a113cyclic::parse_options(argc,argv); a113backward::resources(options);
    int status=a113cyclic::solve(options); alarm(0); return status;
  } catch (const std::invalid_argument& e) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":"<<quoted(e.what())<<"}\n"; return 2;
  } catch (const std::out_of_range&) {
    alarm(0); std::cout<<"{\"status\":\"INVALID\",\"reason\":\"integer_range\"}\n"; return 2;
  } catch (const a113fa::LimitReached& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":"<<quoted(e.what())<<"}\n"; return 3;
  } catch (const std::bad_alloc&) {
    alarm(0); const char text[]="{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";
    (void)!write(1,text,sizeof(text)-1); return 3;
  } catch (const std::exception& e) {
    alarm(0); std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\",\"detail\":"<<quoted(e.what())<<"}\n";
    return 4;
  }
}
#endif
