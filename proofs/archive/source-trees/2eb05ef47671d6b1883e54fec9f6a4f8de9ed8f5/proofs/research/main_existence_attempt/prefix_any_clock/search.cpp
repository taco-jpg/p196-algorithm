#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

// Exact greatest universal trap on all canonical outer q prefixes.
// Both incoming interior carries are allowed; no overflow clock is fixed.
// A positive trap would supply a finite-prefix Lychrel certificate.
uint32_t step(uint32_t index, unsigned width, unsigned incoming) {
    std::array<unsigned, 16> q{},lo{},hi{};
    for (unsigned i=0;i<width;++i) {q[i]=index%19;index/=19;}
    unsigned c=0;
    for (unsigned i=0;i<width;++i) {
        lo[i]=(q[i]+c)%10;c=(q[i]+c)/10;
    }
    c=incoming;
    for (unsigned i=width;i-->0;) {
        hi[i]=(q[i]+c)%10;c=(q[i]+c)/10;
    }
    unsigned h=c;uint32_t result=0,power=1;
    for (unsigned i=0;i<width;++i) {
        unsigned x=lo[i]+(h ? (i==0 ? 1 : hi[i-1]) : hi[i]);
        assert(x<=18);
        result+=power*x;power*=19;
    }
    assert(result%19>0);
    return result;
}

bool safe(uint32_t index,unsigned width) {
    bool high=false,special=(index%19==11);
    for (unsigned i=0;i<width;++i) {
        unsigned q=index%19;index/=19;
        high|=q>=10;special&=(q==0 || q==11);
    }
    return high && !special;
}

void run(unsigned width) {
    auto start=std::chrono::steady_clock::now();
    const uint32_t none=std::numeric_limits<uint32_t>::max();
    uint32_t total=1;for(unsigned i=0;i<width;++i)total*=19;
    std::vector<uint32_t> head(total,none),next(2*total,none),dest(2*total,none),queue;
    std::vector<int32_t> rank(total,-1);
    std::vector<uint8_t> choice(total,0);
    queue.reserve(total);uint32_t valid=0,unsafe=0;
    for(uint32_t p=0;p<total;++p) {
        if(p%19==0){rank[p]=0;continue;}
        ++valid;
        if(!safe(p,width)){rank[p]=0;queue.push_back(p);++unsafe;}
        for(unsigned c=0;c<2;++c) {
            uint32_t e=2*p+c,v=step(p,width,c);dest[e]=v;
            next[e]=head[v];head[v]=e;
        }
    }
    for(size_t i=0;i<queue.size();++i) {
        uint32_t v=queue[i];
        for(uint32_t e=head[v];e!=none;e=next[e]) {
            uint32_t p=e/2;
            if(rank[p]<0){rank[p]=rank[v]+1;choice[p]=e%2;queue.push_back(p);}
        }
    }
    uint32_t trap=0,maxrank=0,first=none;
    for(uint32_t p=0;p<total;++p)if(p%19) {
        if(rank[p]<0){
            ++trap;first=std::min(first,p);
            assert(safe(p,width));
            assert(rank[dest[2*p]]<0 && rank[dest[2*p+1]]<0);
        } else if(rank[p]>0) {
            assert(safe(p,width));
            assert(rank[dest[2*p+choice[p]]]>=0);
            assert(rank[dest[2*p+choice[p]]]<rank[p]);
            maxrank=std::max(maxrank,static_cast<uint32_t>(rank[p]));
        } else assert(!safe(p,width));
    }
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::cout<<"{\"width\":"<<width<<",\"canonical_prefixes\":"<<valid
             <<",\"initially_unsafe\":"<<unsafe<<",\"universal_trap_size\":"<<trap
             <<",\"max_elimination_rank\":"<<maxrank<<",\"first_trap_code\":";
    if(first==none)std::cout<<"null";else std::cout<<first;
    std::cout<<",\"all_rank_or_closure_obligations_checked\":true,\"seconds\":"<<seconds<<"}"<<std::endl;
}

int main(){for(unsigned width=1;width<=5;++width)run(width);}
