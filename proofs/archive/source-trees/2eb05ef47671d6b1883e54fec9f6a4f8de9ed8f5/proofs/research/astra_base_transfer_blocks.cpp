// Exhaustive necessary-condition test for stationary binary-to-decimal blocks.
// No decimal Lychrel existence claim. Digits are stored least significant first.
// Compile: g++ -O3 -std=c++17 astra_base_transfer_blocks.cpp -o /tmp/astra_blocks
// Run: /tmp/astra_blocks [maximum block width, default 4] [source m, default 3]
#include <array>
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using Word = std::vector<unsigned char>;

static Word encode(int a, int b, int k, int m) {
    std::string sa=std::to_string(a), sb=std::to_string(b);
    sa=std::string(k-sa.size(),'0')+sa;
    sb=std::string(k-sb.size(),'0')+sb;
    std::string x=sb+sa;
    for(int i=0;i<m;++i) x+=sb;
    x+=sa+sb;
    for(int i=0;i<m;++i) x+=sa;
    Word ans;
    for(auto it=x.rbegin();it!=x.rend();++it) ans.push_back(*it-'0');
    return ans;
}

static bool palindrome(const Word& a) {
    return std::equal(a.begin(),a.end(),a.rbegin());
}

static void step(Word& a, Word& work) {
    const int n=a.size();
    work.resize(n);
    int c=0;
    for(int i=0;i<n;++i) {
        int s=a[i]+a[n-1-i]+c;
        work[i]=s%10;
        c=s/10;
    }
    if(c) work.push_back(c);
    a.swap(work);
}

int main(int argc,char**argv) {
    const int maxk=argc>1?std::atoi(argv[1]):4;
    const int m=argc>2?std::atoi(argv[2]):3;
    if(maxk<1 || maxk>5 || m<3 || m>1000) return 2;
    std::cout << "{\n  \"claim\":\"finite necessary-condition block-code check; no decimal witness\",\n"
              << "  \"m\":" << m << ",\n  \"widths\":[\n";
    int Q=1;
    for(int k=1;k<=maxk;++k) {
        auto start=std::chrono::steady_clock::now();
        Q*=10;
        unsigned long long tested=0,initial_pals=0,hit_pals=0,returns=0,safe_returns=0;
        unsigned long long overshoots=0,at_bound=0;
        int longest=0;
        std::vector<std::array<int,4>> hits;
        Word n,work,target;
        for(int b=Q/10;b<Q;++b) {
            // Necessary for a return family at all m: a+Q*b == 0 (mod 99).
            int a0=(-(Q%99)*b)%99;
            if(a0<0) a0+=99;
            for(int a=a0;a<Q;a+=99) {
                ++tested;
                n=encode(a,b,k,m);
                target=encode(a,b,k,m+1);
                bool seen_pal=palindrome(n);
                initial_pals+=seen_pal;
                const int bound=10*k+4;
                bool overshot=false;
                for(int t=1;t<=bound;++t) {
                    step(n,work);
                    if(palindrome(n)) seen_pal=true;
                    if(n==target) {
                        ++returns;
                        safe_returns+=!seen_pal;
                        hits.push_back({a,b,t,seen_pal?1:0});
                    }
                    if(n.size()>target.size()) {
                        ++overshoots;
                        longest=std::max(longest,t);
                        overshot=true;
                        break;
                    }
                }
                hit_pals+=seen_pal;
                if(!overshot) ++at_bound;
            }
        }
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout << "    {\"k\":" << k << ",\"tested\":" << tested
                  << ",\"initial_palindromes\":" << initial_pals
                  << ",\"ever_palindrome_in_test\":" << hit_pals
                  << ",\"returns\":" << returns << ",\"safe_returns\":" << safe_returns
                  << ",\"width_overshoots\":" << overshoots
                  << ",\"still_at_or_below_target_at_bound\":" << at_bound
                  << ",\"maximum_overshoot_step\":" << longest
                  << ",\"seconds\":" << sec << ",\"hits\":[";
        bool first=true;
        for(auto h:hits) {
            if(!first) std::cout << ',';
            first=false;
            std::cout << '[' << h[0] << ',' << h[1] << ',' << h[2] << ',' << h[3] << ']';
        }
        std::cout << "]}" << (k==maxk?"\n":",\n") << std::flush;
    }
    std::cout << "  ]\n}\n";
}
