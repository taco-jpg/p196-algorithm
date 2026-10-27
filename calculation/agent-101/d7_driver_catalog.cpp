// Agent 101: exact SCCs and bounded driver discovery in the D7 projection.
// Reuse our reviewed factor relation without changing its frozen source.
// Every graph cycle here is projected-only: no finite B is supplied.
#define main agent101_prefix_sink_original_main
#include "prefix_center_sink.cpp"
#undef main
#include <map>
#include <numeric>
#include <set>
#include <sstream>

struct CatalogConfig {
    Options factors;
    U64 operation_limit=5000000000ULL;
    U64 driver_bytes=1048576;
    unsigned max_period=64,max_drivers=16;
    bool fixture=false,discover=false,export_core=false;
    CatalogConfig(){factors.R=3;factors.D=7;factors.seconds=1200;factors.memory=4096;}
};
struct WorkBudget {
    U64 used=0,limit;
    explicit WorkBudget(U64 n):limit(n){}
    void take(U64 n=1){if(n>limit-used)throw Limit("operation_cap");used+=n;}
};
static void catalog_timeout(int){
    const char s[]="{\"type\":\"SUMMARY\",\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
    (void)!write(STDOUT_FILENO,s,sizeof(s)-1);_exit(3);
}
static CatalogConfig catalog_parse(int argc,char** argv){CatalogConfig c;
    for(int i=1;i<argc;++i){std::string key=argv[i];
        if(key=="--scc-only"){c.discover=false;continue;}
        if(key=="--discover"){c.discover=true;continue;}
        if(key=="--export-core"){c.export_core=true;continue;}
        if(key=="--scc-fixture"){c.fixture=true;continue;}
        if(key=="--all-middles"){c.factors.even=false;continue;}
        if(i+1>=argc)throw Input("option needs a value");
        U64 n=integer(argv[++i]);
        if(key=="--prefix"){if(n>3)throw Input("prefix width must be 1..3");c.factors.R=static_cast<int>(n);}
        else if(key=="--center"){if(n>7)throw Input("center bound must be 1..7");c.factors.D=static_cast<int>(n);}
        else if(key=="--seconds"){if(n>1500)throw Input("wall limit exceeds 1500 seconds");c.factors.seconds=static_cast<unsigned>(n);}
        else if(key=="--memory-mb"){if(n>4096)throw Input("memory limit exceeds 4096 MiB");c.factors.memory=static_cast<unsigned>(n);}
        else if(key=="--operations"){if(n>1000000000000ULL)throw Input("operation cap exceeds 10^12");c.operation_limit=n;}
        else if(key=="--max-period"){if(n>64)throw Input("period cap exceeds 64");c.max_period=static_cast<unsigned>(n);}
        else if(key=="--max-drivers"){if(n>64)throw Input("driver cap exceeds 64");c.max_drivers=static_cast<unsigned>(n);}
        else if(key=="--driver-bytes"){if(n>4194304)throw Input("driver output cap exceeds 4 MiB");c.driver_bytes=n;}
        else throw Input("unknown option");
    }
    if(c.fixture&&(c.discover||c.export_core))throw Input("fixture and factor-output modes are separate");
    return c;
}

struct CompactGraph {
    std::vector<U32> original,offset,target;
    U64 full_vertices=0,full_arcs=0,peeled=0,initial_sinks=0,deleted_arcs=0;
    unsigned max_outdegree=0;
};
static CompactGraph fixture_graph(WorkBudget& budget){
    U64 n,m;if(!(std::cin>>n>>m))throw Input("fixture needs N M");
    if(n>300000||m>2000000)throw Input("fixture exceeds N=300000 or M=2000000");
    budget.take(n+m);std::vector<std::vector<U32>> rows(static_cast<std::size_t>(n));
    for(U64 j=0;j<m;++j){U64 u,v;if(!(std::cin>>u>>v)||u>=n||v>=n)throw Input("invalid fixture edge");
        rows[u].push_back(static_cast<U32>(v));}
    std::string extra;if(std::cin>>extra)throw Input("unexpected trailing fixture input");
    CompactGraph graph;graph.full_vertices=n;graph.full_arcs=m;graph.original.resize(static_cast<std::size_t>(n));
    std::iota(graph.original.begin(),graph.original.end(),0);graph.offset.reserve(static_cast<std::size_t>(n+1));
    graph.target.reserve(static_cast<std::size_t>(m));graph.offset.push_back(0);
    for(const auto& row:rows){graph.target.insert(graph.target.end(),row.begin(),row.end());
        graph.offset.push_back(static_cast<U32>(graph.target.size()));}
    return graph;
}
static CompactGraph compact_residual(const Factors& f,const CatalogConfig& c,WorkBudget& budget){
    CompactGraph graph;graph.full_vertices=f.vertices();graph.full_arcs=f.arcs();
    U64 N=graph.full_vertices;
    if(!N||N>std::numeric_limits<U32>::max())throw Limit("product vertex ID cap");
    if(5*N+(128ULL<<20)>static_cast<U64>(c.factors.memory)*1024*1024)
        throw Limit("graph arrays exceed memory budget");
    U32 nc=static_cast<U32>(f.c.size());
    std::unique_ptr<std::uint8_t[]> degree(new std::uint8_t[N]);
    std::unique_ptr<U32[]> queue(new U32[N]);U64 head=0,tail=0,arcs=0;
    for(U32 p=0;p<f.p.size();++p){budget.take(nc);
        for(U32 ci=0;ci<nc;++ci){unsigned d=f.pcount[p][0]*f.ccount[ci][0]+f.pcount[p][1]*f.ccount[ci][1];
            if(d>255)throw Limit("byte outdegree overflow");
            U32 id=p*nc+ci;degree[id]=static_cast<std::uint8_t>(d);arcs+=d;
            graph.max_outdegree=std::max(graph.max_outdegree,d);
            if(!d)queue[tail++]=id;
        }
    }
    if(arcs!=graph.full_arcs)throw std::runtime_error("factor arc total mismatch");
    graph.initial_sinks=tail;
    while(head<tail){budget.take();U32 id=queue[head++],p=id/nc,ci=id%nc;
        for(int g=0;g<2;++g){U64 count=static_cast<U64>(f.pr[g][p].size())*f.cr[g][ci].size();
            budget.take(count);graph.deleted_arcs+=count;
            for(U32 pp:f.pr[g][p])for(U32 cc:f.cr[g][ci]){U32 source=pp*nc+cc;
                if(!degree[source])throw std::runtime_error("outdegree underflow");
                if(--degree[source]==0){if(tail>=N)throw std::runtime_error("peel queue overflow");queue[tail++]=source;}
            }
        }
    }
    graph.peeled=tail;graph.original.reserve(static_cast<std::size_t>(N-tail));
    // Reuse the now-dead queue as an original-ID -> compact-ID map. It is read
    // only where degree[id]>0, so no full second index allocation is needed.
    budget.take(N);
    for(U32 id=0;id<N;++id)if(degree[id]){
        queue[id]=static_cast<U32>(graph.original.size());graph.original.push_back(id);
    }
    graph.offset.reserve(graph.original.size()+1);graph.offset.push_back(0);
    if(graph.deleted_arcs>graph.full_arcs)throw std::runtime_error("deleted arc total overflow");
    U64 live_arcs=graph.full_arcs-graph.deleted_arcs;
    if(live_arcs>std::numeric_limits<U32>::max())throw Limit("compact arc ID cap");
    graph.target.reserve(static_cast<std::size_t>(live_arcs));
    for(U32 id:graph.original){U32 p=id/nc,ci=id%nc;std::size_t before=graph.target.size();
        budget.take(static_cast<U64>(f.p[p].edges.size())*f.c[ci].edges.size());
        for(auto a:f.p[p].edges)for(auto b:f.c[ci].edges)if(a.g==b.g){U32 next=a.target*nc+b.target;
            if(degree[next])graph.target.push_back(queue[next]);
        }
        if(graph.target.size()-before!=degree[id])throw std::runtime_error("residual outdegree mismatch");
        graph.offset.push_back(static_cast<U32>(graph.target.size()));
    }
    if(graph.target.size()!=live_arcs)throw std::runtime_error("residual arc total mismatch");
    queue.reset();degree.reset();return graph;
}

struct Component {U32 size=0,min_original=std::numeric_limits<U32>::max();U64 internal=0,outgoing=0,self_loops=0;};
struct SCCResult {std::vector<U32> component;std::vector<Component> info;};
static SCCResult tarjan(const CompactGraph& graph,WorkBudget& budget){
    U32 n=static_cast<U32>(graph.original.size()),unseen=std::numeric_limits<U32>::max(),clock=0;
    SCCResult out;out.component.resize(n,unseen);
    std::vector<U32> entered(n,unseen),low(n),active;std::vector<std::uint8_t> on_stack(n,0);
    struct Frame {U32 vertex,edge;};std::vector<Frame> dfs;active.reserve(n);dfs.reserve(n);
    auto enter=[&](U32 v){budget.take();entered[v]=low[v]=clock++;on_stack[v]=1;
        active.push_back(v);dfs.push_back({v,graph.offset[v]});};
    budget.take(n);
    for(U32 start=0;start<n;++start){if(entered[start]!=unseen)continue;enter(start);
        while(!dfs.empty()){U32 u=dfs.back().vertex;
            if(dfs.back().edge<graph.offset[u+1]){budget.take();U32 v=graph.target[dfs.back().edge++];
                if(entered[v]==unseen){enter(v);continue;}
                if(on_stack[v])low[u]=std::min(low[u],entered[v]);
            }else{budget.take();
                if(low[u]==entered[u]){U32 cid=static_cast<U32>(out.info.size());Component item;
                    while(true){U32 v=active.back();active.pop_back();on_stack[v]=0;out.component[v]=cid;
                        ++item.size;item.min_original=std::min(item.min_original,graph.original[v]);if(v==u)break;}
                    out.info.push_back(item);
                }
                dfs.pop_back();if(!dfs.empty()){U32 parent=dfs.back().vertex;low[parent]=std::min(low[parent],low[u]);}
            }
        }
    }
    if(!active.empty())throw std::runtime_error("Tarjan stack did not empty");
    for(U32 u=0;u<n;++u){budget.take(graph.offset[u+1]-graph.offset[u]);
        for(U32 edge=graph.offset[u];edge<graph.offset[u+1];++edge){U32 v=graph.target[edge];auto& item=out.info[out.component[u]];
            if(out.component[u]==out.component[v])++item.internal;else ++item.outgoing;
            if(u==v)++item.self_loops;
        }
    }
    return out;
}
static bool cyclic(const Component& c){return c.size>1||c.self_loops;}
static void print_fixture(const CompactGraph& graph,const SCCResult& scc,const WorkBudget& budget){
    U64 cyclic_count=0,cyclic_vertices=0;for(const auto& item:scc.info)if(cyclic(item)){++cyclic_count;cyclic_vertices+=item.size;}
    std::cout<<"{\"type\":\"SCC_FIXTURE\",\"status\":\"COMPLETE\",\"vertices\":"<<graph.original.size()<<",\"arcs\":"<<graph.target.size()
        <<",\"components\":"<<scc.info.size()<<",\"cyclic_components\":"<<cyclic_count<<",\"cyclic_vertices\":"<<cyclic_vertices<<",\"component\":[";
    for(std::size_t i=0;i<scc.component.size();++i)std::cout<<(i?",":"")<<scc.component[i];
    std::cout<<"],\"operations\":"<<budget.used<<",\"seconds\":"<<elapsed()<<"}\n";std::cout.flush();
}
static void print_scc(const Factors& f,const CatalogConfig& c,const CompactGraph& graph,const SCCResult& scc,const WorkBudget& budget){
    std::map<U32,U32,std::greater<U32>> histogram;std::vector<U32> ranked;U64 cyclic_vertices=0,cyclic_arcs=0;
    for(U32 i=0;i<scc.info.size();++i){const auto& item=scc.info[i];++histogram[item.size];
        if(cyclic(item)){ranked.push_back(i);cyclic_vertices+=item.size;cyclic_arcs+=item.internal;}}
    std::sort(ranked.begin(),ranked.end(),[&](U32 a,U32 b){if(scc.info[a].size!=scc.info[b].size)return scc.info[a].size>scc.info[b].size;
        return scc.info[a].min_original<scc.info[b].min_original;});
    std::cout<<"{\"type\":\"SCC\",\"status\":\"COMPLETE\",\"prefix_width\":"<<c.factors.R<<",\"center_bound\":"<<c.factors.D
        <<",\"even_middle\":"<<(c.factors.even?"true":"false")<<",\"prefix_states\":"<<f.p.size()<<",\"center_states\":"<<f.c.size()
        <<",\"vertices\":"<<graph.full_vertices<<",\"arcs\":"<<graph.full_arcs<<",\"peeled\":"<<graph.peeled
        <<",\"residual_vertices\":"<<graph.original.size()<<",\"residual_arcs\":"<<graph.target.size()
        <<",\"initial_sinks\":"<<graph.initial_sinks<<",\"max_outdegree\":"<<graph.max_outdegree
        <<",\"components\":"<<scc.info.size()<<",\"cyclic_components\":"<<ranked.size()<<",\"cyclic_vertices\":"<<cyclic_vertices
        <<",\"cyclic_arcs\":"<<cyclic_arcs<<",\"size_histogram\":[";
    bool first=true;for(auto entry:histogram){if(!first)std::cout<<',';first=false;
        std::cout<<"{\"size\":"<<entry.first<<",\"count\":"<<entry.second<<'}';}
    std::cout<<"],\"largest_cyclic\":[";
    for(std::size_t i=0;i<std::min<std::size_t>(ranked.size(),32);++i){if(i)std::cout<<',';U32 cid=ranked[i];const auto& item=scc.info[cid];
        std::cout<<"{\"id\":"<<cid<<",\"size\":"<<item.size<<",\"internal_arcs\":"<<item.internal<<",\"outgoing_arcs\":"<<item.outgoing
            <<",\"self_loops\":"<<item.self_loops<<",\"min_product_id\":"<<item.min_original<<'}';}
    std::cout<<"],\"operations\":"<<budget.used<<",\"seconds\":"<<elapsed()<<",\"rss_mb\":"<<peak_mb()<<"}\n";
    std::cout.flush();
}

// The key rotates aligned (e,g) pairs, never the two streams independently.
static std::string paired(const std::string& e,const std::string& g){
    if(e.empty()||e.size()!=g.size())throw std::runtime_error("invalid driver strings");
    std::string out;for(std::size_t i=0;i<e.size();++i)out+=static_cast<char>('0'+2*(e[i]-'0')+(g[i]-'0'));return out;
}
static unsigned primitive_period(const std::string& s){
    for(unsigned p=1;p<=s.size();++p)if(s.size()%p==0){bool equal=true;
        for(std::size_t j=p;j<s.size();++j)if(s[j]!=s[j%p]){equal=false;break;}
        if(equal)return p;}
    throw std::runtime_error("missing primitive period");
}
static std::string rotation_key(const std::string& s){std::string best=s;
    for(std::size_t i=1;i<s.size();++i)best=std::min(best,s.substr(i)+s.substr(0,i));
    return best;}
static std::string primitive_key(const std::string& s){return rotation_key(s.substr(0,primitive_period(s)));}
static CycleEdge actual_edge(const Factors& f,U32 from,U32 to){U32 nc=static_cast<U32>(f.c.size());
    for(auto a:f.p[from/nc].edges)for(auto b:f.c[from%nc].edges)
        if(a.g==b.g&&a.target*nc+b.target==to)return {from,to,a.g,b.label,a.label};
    throw std::runtime_error("compact edge has no factor realization");
}
static void json_word(std::ostream& out,const Word& w){out<<'[';
    for(std::size_t i=0;i<w.size();++i)out<<(i?",":"")<<w[i];
    out<<']';}
static void print_core(const Factors& f,const CompactGraph& graph,const SCCResult& scc,const CatalogConfig& c,WorkBudget& budget){
    U64 vertices=0,arcs=0;for(const auto& item:scc.info)if(cyclic(item)){vertices+=item.size;arcs+=item.internal;}
    if(vertices>10000||arcs>50000)throw Limit("core_export_size_cap");
    U32 nc=static_cast<U32>(f.c.size());std::ostringstream out;
    out<<"{\"type\":\"CORE\",\"status\":\"COMPLETE\",\"scope\":\"internal_arcs_of_cyclic_projection_SCCs\",\"certificate\":false"
        <<",\"boundary_carry_role\":\"one_realizing_choice\",\"prefix_width\":"<<c.factors.R<<",\"center_bound\":"<<c.factors.D
        <<",\"even_middle\":"<<(c.factors.even?"true":"false")<<",\"vertex_count\":"<<vertices<<",\"edge_count\":"<<arcs<<",\"vertices\":[";
    bool first=true;for(U32 u=0;u<graph.original.size();++u)if(cyclic(scc.info[scc.component[u]])){budget.take();
        if(!first)out<<',';
        first=false;U32 id=graph.original[u];
        out<<"{\"id\":"<<id<<",\"scc\":"<<scc.component[u]<<",\"prefix\":";json_word(out,f.p[id/nc].word);
        out<<",\"C\":";json_word(out,f.c[id%nc].word);out<<",\"e\":"<<f.c[id%nc].e<<'}';}
    out<<"],\"edges\":[";first=true;U64 emitted=0;
    for(U32 u=0;u<graph.original.size();++u)if(cyclic(scc.info[scc.component[u]])){
        for(U32 j=graph.offset[u];j<graph.offset[u+1];++j){U32 v=graph.target[j];if(scc.component[u]!=scc.component[v])continue;
            budget.take();auto edge=actual_edge(f,graph.original[u],graph.original[v]);if(!first)out<<',';first=false;++emitted;
            out<<"{\"source\":"<<edge.from<<",\"target\":"<<edge.to<<",\"g\":"<<edge.g<<",\"v\":"<<edge.v
                <<",\"boundary_carry\":"<<edge.cut<<'}';}}
    out<<"]}";if(emitted!=arcs)throw std::runtime_error("core export arc count mismatch");
    std::string line=out.str();if(line.size()+1>4194304)throw Limit("core_export_byte_cap");
    std::cout<<line<<'\n';std::cout.flush();
}
static std::string driver_json(const Factors& f,const std::vector<CycleEdge>& edges,const std::string& e,const std::string& g){
    U32 nc=static_cast<U32>(f.c.size());U64 G=0,V=0;for(auto edge:edges){G+=edge.g;V+=edge.v;}
    if(G!=2*V)throw std::runtime_error("closed center length telescope failed");
    std::ostringstream out;out<<"{\"type\":\"DRIVER\",\"period\":"<<edges.size()<<",\"primitive_eg_period\":"<<primitive_period(paired(e,g))
        <<",\"e\":\""<<e<<"\",\"g\":\""<<g<<"\",\"v\":[";
    for(std::size_t i=0;i<edges.size();++i)out<<(i?",":"")<<edges[i].v;
    out<<"],\"sum_g\":"<<G<<",\"sum_v\":"<<V<<",\"certificate\":false,\"edges\":[";
    for(std::size_t i=0;i<edges.size();++i){if(i)out<<',';auto edge=edges[i];
        if(edge.to!=edges[(i+1)%edges.size()].from)throw std::runtime_error("emitted walk does not close");
        out<<"{\"prefix\":";json_word(out,f.p[edge.from/nc].word);out<<",\"C\":";json_word(out,f.c[edge.from%nc].word);
        out<<",\"e\":"<<f.c[edge.from%nc].e<<",\"g\":"<<edge.g<<",\"v\":"<<edge.v<<",\"boundary_carry\":"<<edge.cut<<",\"next_prefix\":";
        json_word(out,f.p[edge.to/nc].word);out<<",\"next_C\":";json_word(out,f.c[edge.to%nc].word);out<<'}';}
    out<<"]}";return out.str();
}
struct DiscoveryStats {
    U64 eligible_arcs=0,trials=0,return_paths=0,too_long=0,zero_growth=0;
    U64 skipped_p24=0,skipped_p42=0,duplicates=0,emitted=0,bytes=0;
    bool capped=false;std::string reason;
};
static DiscoveryStats discover(const Factors& f,const CompactGraph& graph,const SCCResult& scc,const CatalogConfig& c,WorkBudget& budget){
    DiscoveryStats stats;for(const auto& item:scc.info)if(cyclic(item))stats.eligible_arcs+=item.internal;
    // Exclusion is label-only. Repetitions/rotations of the owned paired
    // streams are skipped; other C realizations of a tried e/g are deduplicated.
    const std::string owned24=primitive_key(paired("010100110100101011001011","110001001000110001001000"));
    const std::string owned42=primitive_key(paired("010100010111000101010101011101000111010101","101000101001001010100101000101001001010100"));
    std::set<std::string> seen;U32 n=static_cast<U32>(graph.original.size()),stamp=0,nc=static_cast<U32>(f.c.size());
    std::vector<U32> visited(n,0),parent(n),queue;std::vector<unsigned> depth(n);queue.reserve(1024);
    // One shortest return for every internal arc. This is a deterministic
    // sample, not all simple cycles, and especially not all closed walks.
    for(U32 u=0;u<n;++u){U32 cid=scc.component[u];if(!cyclic(scc.info[cid]))continue;
        for(U32 arc=graph.offset[u];arc<graph.offset[u+1];++arc){U32 start=graph.target[arc];
            if(scc.component[start]!=cid)continue;
            ++stats.trials;if(++stamp==0)throw Limit("BFS stamp cap");
            queue.clear();queue.push_back(start);visited[start]=stamp;depth[start]=0;parent[start]=start;std::size_t head=0;
            while(head<queue.size()&&visited[u]!=stamp){U32 current=queue[head++];budget.take();
                if(depth[current]+1>=c.max_period)continue;
                for(U32 j=graph.offset[current];j<graph.offset[current+1];++j){budget.take();U32 next=graph.target[j];
                    if(scc.component[next]!=cid||visited[next]==stamp)continue;
                    visited[next]=stamp;parent[next]=current;depth[next]=depth[current]+1;queue.push_back(next);
                    if(next==u)break;
                }
            }
            if(visited[u]!=stamp){++stats.too_long;continue;}
            ++stats.return_paths;std::vector<U32> nodes;
            for(U32 v=u;;v=parent[v]){nodes.push_back(v);if(v==start)break;}
            std::reverse(nodes.begin(),nodes.end());nodes.insert(nodes.begin(),u);
            if(nodes.size()-1>c.max_period)throw std::runtime_error("return exceeded period bound");
            std::vector<CycleEdge> path;std::string e,g;U64 G=0;
            for(std::size_t i=0;i+1<nodes.size();++i){auto edge=actual_edge(f,graph.original[nodes[i]],graph.original[nodes[i+1]]);
                path.push_back(edge);e+=static_cast<char>('0'+f.c[edge.from%nc].e);g+=static_cast<char>('0'+edge.g);G+=edge.g;}
            if(!G){++stats.zero_growth;continue;}
            std::string pair=paired(e,g),primitive=primitive_key(pair);
            if(primitive==owned24){++stats.skipped_p24;continue;}
            if(primitive==owned42){++stats.skipped_p42;continue;}
            if(!seen.insert(rotation_key(pair)).second){++stats.duplicates;continue;}
            std::string line=driver_json(f,path,e,g);
            if(stats.emitted>=c.max_drivers||line.size()+1>c.driver_bytes-stats.bytes){
                stats.capped=true;stats.reason=stats.emitted>=c.max_drivers?"driver_count_cap":"driver_byte_cap";return stats;}
            std::cout<<line<<'\n';std::cout.flush();++stats.emitted;stats.bytes+=line.size()+1;
        }
    }
    return stats;
}
static void print_discovery_summary(const DiscoveryStats& s,const CatalogConfig& c,const WorkBudget& budget){
    std::cout<<"{\"type\":\"SUMMARY\",\"status\":\""<<(s.capped?"UNDECIDED":"CATALOG_SAMPLED")
        <<"\",\"discovery\":\"SAMPLED_DRIVER_DISCOVERY\",\"sampling_method\":\"one_shortest_return_per_internal_arc\",\"certificate\":false"
        <<",\"all_closed_walks_enumerated\":false,\"max_period\":"<<c.max_period<<",\"eligible_internal_arcs\":"<<s.eligible_arcs
        <<",\"arc_trials\":"<<s.trials<<",\"all_internal_arcs_processed\":"<<(s.trials==s.eligible_arcs&&!s.capped?"true":"false")
        <<",\"return_paths\":"<<s.return_paths<<",\"no_return_within_bound\":"<<s.too_long<<",\"zero_growth_skipped\":"<<s.zero_growth
        <<",\"known_p24_samples_skipped\":"<<s.skipped_p24<<",\"known_p42_samples_skipped\":"<<s.skipped_p42
        <<",\"duplicate_samples_skipped\":"<<s.duplicates<<",\"drivers_emitted\":"<<s.emitted<<",\"driver_bytes\":"<<s.bytes;
    if(s.capped)std::cout<<",\"reason\":\""<<s.reason<<'"';
    std::cout<<",\"operations\":"<<budget.used<<",\"seconds\":"<<elapsed()<<",\"rss_mb\":"<<peak_mb()<<"}\n";std::cout.flush();
}

int main(int argc,char** argv){started=std::chrono::steady_clock::now();
    if(argc==2&&std::string(argv[1])=="--help"){
        std::cout<<"d7_driver_catalog --scc-only|--discover [--prefix R --center D --all-middles] [--seconds N] [--memory-mb N] [--operations N]\n"
            <<"--scc-fixture reads N M then M directed pairs from stdin (N<=300000,M<=2000000).\n"
            <<"--discover supports --max-period 64 --max-drivers 16 --driver-bytes 1048576 (hard caps 64,64,4194304).\n"
            <<"--export-core emits cyclic SCC vertices/internal arcs (caps 10000 vertices,50000 arcs,4 MiB).\n"
            <<"Default R3,D7,even middle; <=1500 seconds, <=4096 MiB. SCCs exact; driver discovery is sampled.\n";return 0;}
    try{CatalogConfig c=catalog_parse(argc,argv);limits(c.factors);
        if(std::signal(SIGALRM,catalog_timeout)==SIG_ERR)throw Limit("cannot enforce wall timeout");
        WorkBudget budget(c.operation_limit);
        if(c.fixture){auto graph=fixture_graph(budget);auto scc=tarjan(graph,budget);print_fixture(graph,scc,budget);}
        else{Factors f(c.factors);auto graph=compact_residual(f,c,budget);auto scc=tarjan(graph,budget);print_scc(f,c,graph,scc,budget);
            if(c.export_core)print_core(f,graph,scc,c,budget);
            if(c.discover){auto sample=discover(f,graph,scc,c,budget);print_discovery_summary(sample,c,budget);alarm(0);return sample.capped?3:0;}}
        std::cout<<"{\"type\":\"SUMMARY\",\"status\":\"SCC_COMPLETE\",\"discovery\":\"NOT_RUN\",\"certificate\":false,\"operations\":"<<budget.used
            <<",\"seconds\":"<<elapsed()<<",\"rss_mb\":"<<peak_mb()<<"}\n";alarm(0);return 0;
    }catch(const Input& error){alarm(0);std::cerr<<error.what()<<'\n';
        std::cout<<"{\"type\":\"SUMMARY\",\"status\":\"UNDECIDED\",\"reason\":\"invalid_or_unsupported_input\"}\n";return 2;
    }catch(const Limit& error){alarm(0);std::cout<<"{\"type\":\"SUMMARY\",\"status\":\"UNDECIDED\",\"reason\":\""<<error.what()<<"\"}\n";return 3;
    }catch(const std::bad_alloc&){alarm(0);const char s[]="{\"type\":\"SUMMARY\",\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";
        (void)!write(STDOUT_FILENO,s,sizeof(s)-1);return 3;
    }catch(const std::exception& error){alarm(0);std::cerr<<error.what()<<'\n';
        std::cout<<"{\"type\":\"SUMMARY\",\"status\":\"UNDECIDED\",\"reason\":\"internal_error\"}\n";return 4;}
}
