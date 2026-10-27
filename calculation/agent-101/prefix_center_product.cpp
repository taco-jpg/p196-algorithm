// Agent 101: finite prefix/center overapproximation, not a certificate checker.
// Build: c++ -O3 -std=c++17 -Wall -Wextra -pedantic prefix_center_product.cpp -o /tmp/a101_product
// Run:   /tmp/a101_product --center 6 --prefix 2
// Each run enumerates ALL legal symmetric neutral-pair trims. A projected cycle
// is not a finite B cycle and is never reported as a decimal certificate.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using U32 = std::uint32_t;
using U64 = std::uint64_t;
using Word = std::vector<int>;

struct Limited : std::runtime_error { using std::runtime_error::runtime_error; };
struct Budget {
    double seconds = 1200.0;
    U64 bytes = 4096ULL << 20;
    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    double elapsed() const {
        return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    }
    void check() const { if (elapsed() > seconds) throw Limited("time limit"); }
    void memory(U64 need) const { if (need > bytes) throw Limited("memory estimate exceeds limit"); }
};

static U64 power19(int n) {
    U64 q = 1;
    while (n--) {
        if (q > std::numeric_limits<U64>::max()/19) throw Limited("state-count overflow");
        q *= 19;
    }
    return q;
}
static void print_word(const Word& w) {
    std::cout << '[';
    for (std::size_t j=0;j<w.size();++j) std::cout << (j ? "," : "") << w[j];
    std::cout << ']';
}
static std::pair<Word,int> normalize(const Word& w, int carry) {
    Word d;
    for (int x:w) { d.push_back((x+carry)%10); carry=(x+carry)/10; }
    return {d,carry};
}

struct PrefixEdge { U32 dest; int gamma, boundary; };
struct CenterEdge { U32 dest; int trim; };
struct PrefixBack { U32 source; int boundary; };
struct CenterBack { U32 source; int trim; };
struct Center { Word word; int entry; };

struct Model {
    int R, D;
    U32 np=0, nc=0;
    std::vector<Word> prefix;
    std::vector<std::vector<PrefixEdge>> pe;
    std::vector<std::vector<PrefixBack>> pb[2];
    std::vector<Center> center;
    std::vector<std::vector<CenterEdge>> ce[2];
    std::vector<std::vector<CenterBack>> cb[2];
    std::vector<U64> coff, neutral;
    U64 memory_estimate=0;

    Model(int r,int d,Budget& budget):R(r),D(d),coff(d+2),neutral(d+1) {
        const U64 pcount=18*power19(R-1);
        for (int m=1;m<=D;++m) {
            const int h=(m+1)/2;
            U64 n=0; for(int j=0;j<h;++j)n=19*n+9;
            neutral[m]=n;
            coff[m+1]=coff[m]+power19(h)-1;
        }
        const U64 ccount=coff[D+1];
        if (pcount>std::numeric_limits<U32>::max() ||
            ccount>std::numeric_limits<U32>::max() ||
            pcount*ccount>std::numeric_limits<U32>::max())
            throw Limited("product needs more than 32-bit vertex IDs");
        np=static_cast<U32>(pcount); nc=static_cast<U32>(ccount);
        // Conservative allowance for both graph arrays and precomputed local
        // vectors/words. The large graph itself never stores adjacency lists.
        memory_estimate=8*pcount*ccount + 1024*(pcount+ccount) + (16ULL<<20);
        budget.memory(memory_estimate);
        prefix.resize(np); pe.resize(np);
        for(int g=0;g<2;++g)pb[g].resize(np);
        for(U32 p=0;p<np;++p) {
            if ((p&16383)==0)budget.check();
            Word a(R); U32 k=p;
            for(int j=R-1;j>0;--j){a[j]=k%19;k/=19;}
            a[0]=static_cast<int>(k)+1; prefix[p]=a;
            for(int boundary=0;boundary<=1;++boundary) {
                Word high(R+1),low(R+1),out(R); high[R]=boundary;
                for(int j=R-1;j>=0;--j)high[j]=(a[j]+high[j+1])/10;
                for(int j=0;j<R;++j)low[j+1]=(a[j]+low[j])/10;
                const int g=high[0];
                for(int j=0;j<R;++j)
                    out[j]=(a[j]+low[j])%10 + (g ? (j==0?1:(a[j-1]+high[j])%10)
                                                               : (a[j]+high[j+1])%10);
                if(out[0]<1 || out[0]>18)throw std::runtime_error("invalid exterior head");
                U32 target=out[0]-1;
                for(int j=1;j<R;++j) {
                    if(out[j]<0 || out[j]>18)throw std::runtime_error("invalid prefix coefficient");
                    target=19*target+out[j];
                }
                bool duplicate=false;
                for(auto q:pe[p]) if(q.dest==target && q.gamma==g)duplicate=true;
                if(!duplicate) {
                    pe[p].push_back({target,g,boundary});
                    pb[g][target].push_back({p,boundary});
                }
            }
        }
        center.reserve(nc);
        for(int m=1;m<=D;++m) {
            int h=(m+1)/2;
            for(U64 code=0;code<power19(h);++code) {
                if((code&16383)==0)budget.check();
                if(code==neutral[m])continue; // All-9 transmits carry, never flips it.
                U64 k=code; Word c(m);
                for(int j=h-1;j>=0;--j){c[j]=k%19;k/=19;}
                for(int j=0;j<m/2;++j)c[m-1-j]=c[j];
                int entry=-1,choices=0;
                for(int e=0;e<2;++e)if(normalize(c,e).second==1-e){entry=e;++choices;}
                if(choices!=1)throw std::runtime_error("center carry uniqueness failed");
                center.push_back({c,entry});
            }
        }
        if(center.size()!=nc)throw std::runtime_error("center index construction failed");
        for(int g=0;g<2;++g){ce[g].resize(nc);cb[g].resize(nc);}
        for(U32 c=0;c<nc;++c) {
            if((c&16383)==0)budget.check();
            const auto& src=center[c]; const Word digits=normalize(src.word,src.entry).first;
            for(int g=0;g<2;++g) {
                Word d=digits;if(g)d.push_back(9*src.entry);
                Word raw(d.size());
                for(std::size_t j=0;j<d.size();++j)raw[j]=d[j]+d[d.size()-1-j];
                for(int v=0;2*v<static_cast<int>(raw.size());++v) {
                    int m=static_cast<int>(raw.size())-2*v;
                    if(m<=D) {
                        U64 code=0; for(int j=0;j<(m+1)/2;++j)code=19*code+raw[v+j];
                        if(code!=neutral[m]) {
                            U32 target=static_cast<U32>(coff[m]+code-(code>neutral[m]));
                            if(target>=nc)throw std::runtime_error("invalid center target index");
                            ce[g][c].push_back({target,v}); cb[g][target].push_back({c,v});
                        }
                    }
                    if(m<2 || raw[v]!=9 || raw[raw.size()-1-v]!=9)break;
                }
            }
        }
    }

    template<class F>void edges(U32 vertex,F emit)const {
        U32 p=vertex/nc,c=vertex%nc;
        for(auto a:pe[p])for(auto b:ce[a.gamma][c])
            emit(a.dest*nc+b.dest,a.gamma,b.trim,a.boundary);
    }
};

static void projected_cycle(const Model& m,const std::vector<U32>& degree,
                            Budget& budget,U64 available_bytes) {
    struct BackStep { U32 state,pred; int g,v,h; };
    U32 current=0;while(current<degree.size() && degree[current]==0)++current;
    if(current==degree.size())throw std::runtime_error("empty residual");
    std::unordered_map<U32,std::size_t> seen;
    std::vector<BackStep> path;
    while(!seen.count(current)) {
        budget.check();
        // Explicit conservative upper bound on this sparse walk's storage.
        if(96ULL*(path.size()+1)>available_bytes)throw Limited("witness memory limit");
        seen[current]=path.size();
        U32 p=current/m.nc,c=current%m.nc,pred=0;
        int found_g=-1,found_v=0,found_h=0;
        for(int g=0;g<2 && found_g<0;++g) {
            for(auto a:m.pb[g][p]) {
                for(auto b:m.cb[g][c]) {
                    U32 q=a.source*m.nc+b.source;
                    if(degree[q]){pred=q;found_g=g;found_v=b.trim;found_h=a.boundary;break;}
                }
                if(found_g>=0)break;
            }
        }
        if(found_g<0)throw std::runtime_error("residual vertex lacks residual predecessor");
        path.push_back({current,pred,found_g,found_v,found_h});current=pred;
    }
    const std::size_t begin=seen.at(current);
    U64 growth=0,trims=0;
    for(std::size_t j=begin;j<path.size();++j){growth+=path[j].g;trims+=path[j].v;}
    std::cout<<"{\"projected_cycle\":true,\"certificate\":false,\"period\":"<<path.size()-begin
             <<",\"sum_g\":"<<growth<<",\"sum_v\":"<<trims<<",\"edges\":[";
    for(std::size_t j=path.size();j-- >begin;) {
        const auto z=path[j];
        if(j+1<path.size())std::cout<<',';
        const U32 sp=z.pred/m.nc,sc=z.pred%m.nc,tp=z.state/m.nc,tc=z.state%m.nc;
        std::cout<<"{\"prefix\":";print_word(m.prefix[sp]);
        std::cout<<",\"C\":";print_word(m.center[sc].word);
        std::cout<<",\"e\":"<<m.center[sc].entry<<",\"g\":"<<z.g<<",\"v\":"<<z.v
                 <<",\"boundary_carry\":"<<z.h<<",\"next_prefix\":";print_word(m.prefix[tp]);
        std::cout<<",\"next_C\":";print_word(m.center[tc].word);std::cout<<'}';
    }
    std::cout<<"]}\n";
}

int main(int argc,char**argv) {
    Budget budget;int R=2,D=5;
    try {
        for(int i=1;i<argc;++i) {
            const std::string a=argv[i];
            if(a=="--help") {
                std::cout<<"Usage: prefix_center_product --center D --prefix R "
                            "[--seconds 1200] [--memory-mb 4096]\n"
                            "R=1..3, D=1..10. Caps produce UNDECIDED, never an exclusion.\n";
                return 0;
            }
            if(i+1==argc)throw std::runtime_error("option requires a value");
            const std::string value=argv[++i];std::size_t consumed=0;
            U64 n=std::stoull(value,&consumed);
            if(consumed!=value.size() || value.empty() || value[0]=='-' || n==0)
                throw std::runtime_error("expected a positive integer option value");
            if(a=="--prefix") {if(n>3)throw std::runtime_error("prefix must be 1..3");R=static_cast<int>(n);}
            else if(a=="--center") {if(n>10)throw std::runtime_error("center must be 1..10");D=static_cast<int>(n);}
            else if(a=="--seconds") {if(n>1800)throw std::runtime_error("maximum run is 1800 seconds");budget.seconds=static_cast<double>(n);}
            else if(a=="--memory-mb") {if(n>8192)throw std::runtime_error("maximum memory budget is 8192 MiB");budget.bytes=n<<20;}
            else throw std::runtime_error("unknown option: "+a);
        }
        Model m(R,D,budget);
        const U32 n=m.np*m.nc;
        std::vector<U32> degree(n,0),queue;queue.reserve(n);
        U64 edges=0,growth_edges=0;U32 max_degree=0;
        for(U32 s=0;s<n;++s) {
            if((s&65535)==0)budget.check();
            m.edges(s,[&](U32 target,int g,int,int) {
                if(degree[target]==std::numeric_limits<U32>::max())throw std::runtime_error("indegree overflow");
                max_degree=std::max(max_degree,++degree[target]);++edges;growth_edges+=g;
            });
        }
        for(U32 s=0;s<n;++s)if(degree[s]==0)queue.push_back(s);
        const U64 initial_zero=queue.size();std::size_t front=0;
        while(front<queue.size()) {
            if((front&65535)==0)budget.check();
            U32 s=queue[front++];
            m.edges(s,[&](U32 target,int,int,int) {
                if(degree[target]==0)throw std::runtime_error("indegree underflow");
                if(--degree[target]==0)queue.push_back(target);
            });
        }
        U64 remaining=n-queue.size();
        std::cout<<"{\"status\":\""<<(remaining?"CYCLIC_PROJECTION":"ACYCLIC")<<"\",\"prefix\":"<<R
                 <<",\"max_center\":"<<D<<",\"prefix_states\":"<<m.np<<",\"center_states\":"<<m.nc
                 <<",\"vertices\":"<<n<<",\"edges\":"<<edges<<",\"growth_edges\":"<<growth_edges
                 <<",\"max_indegree\":"<<max_degree<<",\"initial_zero_indegree\":"<<initial_zero
                 <<",\"peeled\":"<<queue.size()<<",\"residual\":"<<remaining
                 <<",\"memory_estimate_bytes\":"<<m.memory_estimate<<",\"seconds\":"<<budget.elapsed()<<"}\n";
        std::cout.flush();
        if(remaining) {
            std::vector<U32>().swap(queue);
            U64 used=m.memory_estimate-4ULL*n;
            projected_cycle(m,degree,budget,budget.bytes-used);
        }
        return 0;
    } catch(const Limited& ex) {
        std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\""<<ex.what()<<"\",\"seconds\":"<<budget.elapsed()<<"}\n";
        return 3;
    } catch(const std::bad_alloc&) {
        std::cout<<"{\"status\":\"UNDECIDED\",\"reason\":\"allocation failure\"}\n";return 3;
    } catch(const std::exception& ex) {
        std::cerr<<"ERROR: "<<ex.what()<<'\n';return 2;
    }
}
