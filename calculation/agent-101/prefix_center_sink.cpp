// Agent 101: independently implemented decimal prefix/center sink peeling.
// Agent 6 owns the primary R=3,D=7 research result; this is a second-author check.
// No product arcs are stored. Incoming factor lists drive outdegree deletion.
// A surviving projected cycle is NOT a finite B cycle or a decimal certificate.
#include <algorithm>
#include <array>
#include <chrono>
#include <csignal>
#include <cstdint>
#include <iostream>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <sys/resource.h>
#include <unistd.h>

using U32=std::uint32_t;
using U64=std::uint64_t;
using Word=std::vector<int>;
struct Input:std::runtime_error{using std::runtime_error::runtime_error;};
struct Limit:std::runtime_error{using std::runtime_error::runtime_error;};
struct Options {int R=0,D=0;bool even=true,dump=false,describe=false;
    unsigned seconds=1200,memory=4096,witness_cap=100000;};
struct Edge {U32 target;int g,label;}; // label: exterior cut carry, or center trim v.
struct State {Word word;int e=-1;std::vector<Edge> edges;};
static std::chrono::steady_clock::time_point started;
static double elapsed(){return std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();}
static long peak_mb(){struct rusage r;getrusage(RUSAGE_SELF,&r);
#ifdef __APPLE__
    return r.ru_maxrss/1048576;
#else
    return r.ru_maxrss/1024;
#endif
}
static void deadline(int){const char s[]="{\"status\":\"UNDECIDED\",\"reason\":\"wall_timeout\"}\n";
    (void)!write(STDOUT_FILENO,s,sizeof(s)-1);_exit(3);}
static U64 integer(const char* text){std::string s(text);std::size_t end=0;
    if(s.empty()||s.find_first_not_of("0123456789")!=std::string::npos)throw Input("expected positive integer");
    U64 n;try{n=std::stoull(s,&end);}catch(const std::out_of_range&){throw Input("integer outside uint64 range");}
    if(!n||end!=s.size())throw Input("expected positive integer");
    return n;}
static Options parse(int argc,char** argv){Options o;
    for(int i=1;i<argc;++i){std::string key=argv[i];
        if(key=="--all-middles"){o.even=false;continue;}
        if(key=="--dump-factors"){o.dump=true;continue;}
        if(key=="--describe"){o.describe=true;continue;}
        if(i+1>=argc)throw Input("option needs a value");
        U64 n=integer(argv[++i]);
        if(key=="--prefix"){if(n>3)throw Input("prefix width must be 1..3");o.R=static_cast<int>(n);}
        else if(key=="--center"){if(n>7)throw Input("center bound must be 1..7");o.D=static_cast<int>(n);}
        else if(key=="--seconds"){if(n>1800)throw Input("wall limit exceeds 1800 seconds");o.seconds=static_cast<unsigned>(n);}
        else if(key=="--memory-mb"){if(n>8192)throw Input("memory limit exceeds 8192 MiB");o.memory=static_cast<unsigned>(n);}
        else if(key=="--witness-cap"){if(n>1000000)throw Input("witness cap exceeds 1000000");o.witness_cap=static_cast<unsigned>(n);}
        else throw Input("unknown option");
    }
    if(!o.R||!o.D)throw Input("explicit --prefix R and --center D are required");
    if(o.dump&&o.describe)throw Input("choose one factor output mode");
    return o;
}
static void limits(const Options& o){struct rlimit prior;
    if(getrlimit(RLIMIT_AS,&prior))throw Limit("cannot inspect address-space limit");
    rlim_t want=static_cast<rlim_t>(o.memory)*1024*1024;
    if(prior.rlim_max!=RLIM_INFINITY)want=std::min(want,prior.rlim_max);
    struct rlimit lim={want,prior.rlim_max};if(setrlimit(RLIMIT_AS,&lim))throw Limit("cannot enforce address-space limit");
    if(std::signal(SIGALRM,deadline)==SIG_ERR)throw Limit("cannot enforce wall timeout");
    alarm(o.seconds);
}
static U64 pow19(int n){U64 r=1;while(n--)r*=19;return r;}
static U64 code(const Word& w){U64 r=w.size();for(int x:w)r=(r<<5)|static_cast<U64>(x);return r;}
static void word(const Word& w){std::cout<<'[';for(std::size_t i=0;i<w.size();++i)std::cout<<(i?",":"")<<w[i];std::cout<<']';}
static std::pair<Word,int> norm(const Word& w,int carry){Word d;d.reserve(w.size());
    for(int x:w){int s=x+carry;d.push_back(s%10);carry=s/10;}return {d,carry};}

struct Factors {
    std::vector<State> p,c;
    std::vector<std::array<unsigned,2>> pcount,ccount;
    std::vector<std::vector<U32>> pr[2],cr[2];
    U64 pe[2]={0,0},ce[2]={0,0};
    Factors(const Options& o){
        const U32 np=static_cast<U32>(18*pow19(o.R-1));p.resize(np);pcount.resize(np);
        for(U32 id=0;id<np;++id){Word a(o.R);U32 q=id;
            for(int j=o.R-1;j>0;--j){a[j]=q%19;q/=19;}a[0]=static_cast<int>(q)+1;p[id].word=a;
            // Sentinel 0/18 forces the cut reverse carry to 0/1. Whole-word
            // column normalization independently implements the local relation.
            for(int cut=0;cut<2;++cut){Word b=a;b.push_back(cut?18:0);auto low=norm(b,0);
                if(low.second!=cut)throw std::runtime_error("sentinel carry mismatch");
                std::reverse(b.begin(),b.end());auto high=norm(b,1-cut);int g=high.second;
                Word target(o.R);int n=static_cast<int>(b.size());
                for(int j=0;j<o.R;++j)target[j]=low.first[j]+(g?(j?high.first[n-j]:1):high.first[n-1-j]);
                if(target[0]<1||target[0]>18)throw std::runtime_error("invalid projected head");
                U32 ti=target[0]-1;for(int j=1;j<o.R;++j){if(target[j]<0||target[j]>18)throw std::runtime_error("invalid prefix digit");ti=19*ti+target[j];}
                bool duplicate=false;for(auto edge:p[id].edges)if(edge.target==ti&&edge.g==g)duplicate=true;
                if(!duplicate)p[id].edges.push_back({ti,g,cut});
            }
        }
        std::unordered_map<U64,U32> center_id;
        for(int m=1;m<=o.D;++m){int half=(m+1)/2;
            for(U64 h=0;h<pow19(half);++h){U64 q=h;Word w(m);
                for(int j=half-1;j>=0;--j){w[j]=q%19;q/=19;}
                if(o.even&&(m%2)&&w[half-1]%2)continue;
                for(int j=0;j<m/2;++j)w[m-1-j]=w[j];
                int entry=-1,count=0;
                for(int e=0;e<2;++e)if(norm(w,e).second==1-e){entry=e;++count;}
                if(!count)continue;
                if(count!=1)throw std::runtime_error("center entry not unique");
                U32 id=static_cast<U32>(c.size());if(!center_id.emplace(code(w),id).second)throw std::runtime_error("center key collision");
                c.push_back({w,entry,{}});
            }
        }
        ccount.resize(c.size());
        for(U32 id=0;id<c.size();++id){auto d=norm(c[id].word,c[id].e).first;
            for(int g=0;g<2;++g){Word z=d;if(g)z.push_back(9*c[id].e);Word raw(z.size());
                for(std::size_t j=0;j<z.size();++j)raw[j]=z[j]+z[z.size()-1-j];
                for(int v=0;2*v<static_cast<int>(raw.size());++v){int m=static_cast<int>(raw.size())-2*v;
                    if(m<=o.D){Word target(raw.begin()+v,raw.end()-v);auto it=center_id.find(code(target));
                        if(it!=center_id.end())c[id].edges.push_back({it->second,g,v});}
                    if(m<2||raw[v]!=9||raw[raw.size()-1-v]!=9)break;
                }
            }
        }
        for(int g=0;g<2;++g){pr[g].resize(p.size());cr[g].resize(c.size());}
        for(U32 id=0;id<p.size();++id)for(auto edge:p[id].edges){pr[edge.g][edge.target].push_back(id);++pcount[id][edge.g];++pe[edge.g];}
        for(U32 id=0;id<c.size();++id)for(auto edge:c[id].edges){cr[edge.g][edge.target].push_back(id);++ccount[id][edge.g];++ce[edge.g];}
    }
    U64 vertices()const{return static_cast<U64>(p.size())*c.size();}
    U64 arcs()const{return pe[0]*ce[0]+pe[1]*ce[1];}
};

static void metadata(const Factors& f,const Options& o){std::cout<<"{\"kind\":\"metadata\",\"prefix_width\":"<<o.R
    <<",\"center_bound\":"<<o.D<<",\"even_middle\":"<<(o.even?"true":"false")<<",\"prefix_states\":"<<f.p.size()
    <<",\"center_states\":"<<f.c.size()<<",\"vertices\":"<<f.vertices()<<",\"arcs\":"<<f.arcs()
    <<",\"prefix_edges\":["<<f.pe[0]<<','<<f.pe[1]<<"],\"center_edges\":["<<f.ce[0]<<','<<f.ce[1]<<"]}\n";}
static void dump(const Factors& f,const Options& o){
    if(f.p.size()+f.c.size()>200000)throw Limit("factor export exceeds 200000 local states");
    metadata(f,o);
    for(int kind=0;kind<2;++kind){const auto& states=kind?f.c:f.p;
        for(U32 id=0;id<states.size();++id){std::cout<<"{\"kind\":\""<<(kind?"center":"prefix")<<"\",\"id\":"<<id<<",\"word\":";word(states[id].word);
            if(kind)std::cout<<",\"e\":"<<states[id].e;
            std::cout<<",\"edges\":[";
            for(std::size_t j=0;j<states[id].edges.size();++j){auto edge=states[id].edges[j];if(j)std::cout<<',';
                std::cout<<"{\"target\":";word(states[edge.target].word);std::cout<<",\"g\":"<<edge.g<<",\""<<(kind?"v":"boundary_carry")<<"\":"<<edge.label<<'}';}
            std::cout<<"]}\n";
        }
    }
}

struct CycleEdge {U32 from,to;int g,v,cut;};
static std::vector<CycleEdge> cycle(const Factors& f,const std::uint8_t* degree,const Options& o){
    const U32 nc=f.c.size(),n=static_cast<U32>(f.vertices());U32 current=0;while(current<n&&!degree[current])++current;
    if(current==n)throw std::runtime_error("cycle extraction without residual");
    std::unordered_map<U32,std::size_t> position;std::vector<CycleEdge> path;
    while(!position.count(current)){
        if(path.size()>=o.witness_cap)throw Limit("projected witness path cap");
        position[current]=path.size();
        bool found=false;U32 pi=current/nc,ci=current%nc;
        for(auto a:f.p[pi].edges){for(auto b:f.c[ci].edges){if(a.g!=b.g)continue;U32 target=a.target*nc+b.target;
                if(degree[target]){path.push_back({current,target,a.g,b.label,a.label});current=target;found=true;break;}}
            if(found)break;}
        if(!found)throw std::runtime_error("sink residual lacks residual successor");
    }
    return std::vector<CycleEdge>(path.begin()+position.at(current),path.end());
}
static void print_cycle(const Factors& f,const std::vector<CycleEdge>& path){U32 nc=f.c.size();U64 G=0,V=0;
    for(auto edge:path){G+=edge.g;V+=edge.v;}
    std::cout<<",\"projected_cycle\":{\"certificate\":false,\"period\":"<<path.size()<<",\"sum_g\":"<<G<<",\"sum_v\":"<<V<<",\"edges\":[";
    for(std::size_t j=0;j<path.size();++j){auto edge=path[j];if(j)std::cout<<',';
        std::cout<<"{\"prefix\":";word(f.p[edge.from/nc].word);std::cout<<",\"C\":";word(f.c[edge.from%nc].word);
        std::cout<<",\"e\":"<<f.c[edge.from%nc].e<<",\"g\":"<<edge.g<<",\"v\":"<<edge.v<<",\"boundary_carry\":"<<edge.cut<<",\"next_prefix\":";
        word(f.p[edge.to/nc].word);std::cout<<",\"next_C\":";word(f.c[edge.to%nc].word);std::cout<<'}';}
    std::cout<<"]}";
}

static void solve(const Factors& f,const Options& o){U64 N=f.vertices();
    if(N==0||N>=static_cast<U64>(std::numeric_limits<U32>::max())+1)throw Limit("vertex IDs exceed uint32 range");
    U64 array_bytes=5*N;
    if(array_bytes+(64ULL<<20)>static_cast<U64>(o.memory)*1024*1024)throw Limit("graph arrays exceed memory budget");
    const U32 nc=f.c.size();std::unique_ptr<std::uint8_t[]> degree(new std::uint8_t[N]);
    std::unique_ptr<U32[]> queue(new U32[N]);U64 tail=0,head=0,arcs=0;unsigned maximum=0;
    for(U32 p=0;p<f.p.size();++p)for(U32 c=0;c<nc;++c){
        unsigned d=f.pcount[p][0]*f.ccount[c][0]+f.pcount[p][1]*f.ccount[c][1];
        if(d>255)throw Limit("byte outdegree overflow");
        U32 id=p*nc+c;degree[id]=static_cast<std::uint8_t>(d);arcs+=d;
        maximum=std::max(maximum,d);if(!d)queue[tail++]=id;
    }
    if(arcs!=f.arcs())throw std::runtime_error("independent arc totals disagree");
    U64 initial_sinks=tail;
    while(head<tail){U32 target=queue[head++],p=target/nc,c=target%nc;
        for(int g=0;g<2;++g)for(U32 parent_p:f.pr[g][p])for(U32 parent_c:f.cr[g][c]){
            U32 source=parent_p*nc+parent_c;if(!degree[source])throw std::runtime_error("outdegree underflow");
            if(--degree[source]==0){if(tail>=N)throw std::runtime_error("queue overflow");queue[tail++]=source;}
        }
    }
    U64 residual=N-tail;queue.reset();std::vector<CycleEdge> witness;if(residual)witness=cycle(f,degree.get(),o);
    std::cout<<"{\"status\":\""<<(residual?"CYCLIC_PROJECTION":"ACYCLIC")<<"\",\"algorithm\":\"sink_peeling\",\"prefix_width\":"<<o.R
        <<",\"center_bound\":"<<o.D<<",\"even_middle\":"<<(o.even?"true":"false")<<",\"prefix_states\":"<<f.p.size()<<",\"center_states\":"<<f.c.size()
        <<",\"vertices\":"<<N<<",\"arcs\":"<<arcs<<",\"peeled\":"<<tail<<",\"residual\":"<<residual<<",\"initial_sinks\":"<<initial_sinks
        <<",\"max_outdegree\":"<<maximum<<",\"graph_array_bytes\":"<<array_bytes<<",\"seconds\":"<<elapsed()<<",\"rss_mb\":"<<peak_mb();
    if(residual)print_cycle(f,witness);
    std::cout<<"}\n";
}

int main(int argc,char** argv){started=std::chrono::steady_clock::now();
    if(argc==2&&std::string(argv[1])=="--help"){std::cout<<"prefix_center_sink --prefix R --center D [--all-middles] [--dump-factors|--describe] [--seconds N] [--memory-mb N] [--witness-cap N]\n"
        <<"R=1..3,D=1..7; odd middle coefficients are even unless --all-middles.\n";return 0;}
    try{Options o=parse(argc,argv);limits(o);Factors f(o);
        if(o.dump)dump(f,o);else if(o.describe)metadata(f,o);else solve(f,o);alarm(0);return 0;}
    catch(const Input& ex){alarm(0);std::cerr<<ex.what()<<'\n';std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"invalid_or_unsupported_input\"}\n";return 2;}
    catch(const Limit& ex){alarm(0);std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<ex.what()<<"\"}\n";return 3;}
    catch(const std::bad_alloc&){alarm(0);const char s[]="{\"status\":\"UNDECIDED\",\"reason\":\"memory_limit\"}\n";(void)!write(STDOUT_FILENO,s,sizeof(s)-1);return 3;}
    catch(const std::exception& ex){alarm(0);std::cerr<<ex.what()<<'\n';std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"internal_error\"}\n";return 4;}
}
