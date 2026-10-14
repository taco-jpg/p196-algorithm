// Exact affine-length periodic-word arithmetic; independent of big integers.
// Every branch is valid for all m above an explicitly accumulated threshold.
// This finite block-code exclusion is not a decimal Lychrel existence proof.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

struct Seg { std::vector<int> p; int a,b; };
using Word=std::vector<Seg>;
static int mod(int a,int b) { int c=a%b; return c<0?c+b:c; }
static int floordiv(int a,int b) { return (a-mod(a,b))/b; }
static int positive(int a,int b) { assert(a>0); return floordiv(-b,a)+1; }

static std::vector<int> primitive(const std::vector<int>& p) {
    for(int d=1;d<=(int)p.size();++d) {
        if(p.size()%d) continue;
        bool yes=true;
        for(int i=d;i<(int)p.size();++i) if(p[i]!=p[i%d]) {yes=false;break;}
        if(yes) return std::vector<int>(p.begin(),p.begin()+d);
    }
    std::abort();
}
static void append(Word& out,const std::vector<int>& pp,int a,int b) {
    if(a==0 && b==0) return;
    std::vector<int> p=primitive(pp);
    assert(a>=0 && a%(int)p.size()==0);
    if(!out.empty() && out.back().p.size()==p.size()) {
        Seg& old=out.back();
        int shift=mod(old.b,p.size());
        bool yes=true;
        for(int i=0;i<(int)p.size();++i) if(old.p[(i+shift)%p.size()]!=p[i]) {yes=false;break;}
        if(yes) {old.a+=a;old.b+=b;return;}
    }
    out.push_back({std::move(p),a,b});
}
static std::pair<int,int> minimum(const Seg& x,const Seg& y,int& M) {
    int da=x.a-y.a,db=x.b-y.b;
    if(da>0) {M=std::max(M,positive(da,db));return {y.a,y.b};}
    if(da<0) {M=std::max(M,positive(-da,-db));return {x.a,x.b};}
    return db<=0?std::make_pair(x.a,x.b):std::make_pair(y.a,y.b);
}
static bool drop(Seg& s,int a,int b) {
    if(s.a==a && s.b==b) return false;
    assert(a%(int)s.p.size()==0);
    int shift=mod(b,s.p.size());
    std::rotate(s.p.begin(),s.p.begin()+shift,s.p.end());
    s.a-=a;s.b-=b;
    return true;
}
static Word reverse_word(const Word& w) {
    Word out;
    for(auto it=w.rbegin();it!=w.rend();++it) {
        Seg s=*it;
        for(int i=0;i<(int)s.p.size();++i) s.p[i]=it->p[mod(it->b-1-i,it->p.size())];
        out.push_back(std::move(s));
    }
    return out;
}
static Word add_word(const Word& w,int& M) {
    Word right=reverse_word(w),out;
    unsigned i=0,j=0;
    Seg x=w[0],y=right[0];
    int c=0;
    while(true) {
        auto [a,b]=minimum(x,y,M);
        if(!a) {
            assert(b>0);
            std::vector<int> digits;
            for(int r=0;r<b;++r) {
                int total=x.p[r%x.p.size()]+y.p[r%y.p.size()]+c;
                digits.push_back(total%10);c=total/10;
            }
            append(out,digits,0,b);
        } else {
            int period=std::lcm(x.p.size(),y.p.size());
            assert(a%period==0);
            M=std::max(M,positive(a,b-period));
            std::vector<int> first,stable;
            for(int r=0;r<period;++r) {
                int total=x.p[r%x.p.size()]+y.p[r%y.p.size()]+c;
                first.push_back(total%10);c=total/10;
            }
            int fixed=c;
            for(int r=0;r<period;++r) {
                int total=x.p[r%x.p.size()]+y.p[r%y.p.size()]+c;
                stable.push_back(total%10);c=total/10;
            }
            assert(c==fixed);
            append(out,first,0,period);
            append(out,stable,a,b-period);
            for(int r=0;r<mod(b,period);++r) {
                int total=x.p[r%x.p.size()]+y.p[r%y.p.size()]+c;
                c=total/10;
            }
        }
        if(!drop(x,a,b)) {++i;if(i<w.size()) x=w[i];}
        if(!drop(y,a,b)) {++j;if(j<right.size()) y=right[j];}
        if(i==w.size() || j==right.size()) {assert(i==w.size()&&j==right.size());break;}
    }
    if(c) append(out,{c},0,1);
    return out;
}
static bool eventually_equal(const Word& left,const Word& right,int& M) {
    unsigned i=0,j=0;
    Seg x=left[0],y=right[0];
    while(true) {
        auto [a,b]=minimum(x,y,M);
        int period=std::lcm(x.p.size(),y.p.size());
        int count;
        if(a) {M=std::max(M,positive(a,b-period+1));count=period;}
        else {assert(b>0);count=std::min(period,b);}
        for(int r=0;r<count;++r) if(x.p[r%x.p.size()]!=y.p[r%y.p.size()]) return false;
        if(!drop(x,a,b)) {++i;if(i<left.size()) x=left[i];}
        if(!drop(y,a,b)) {++j;if(j<right.size()) y=right[j];}
        if(i==left.size() || j==right.size()) return i==left.size()&&j==right.size();
    }
}
static Word encoded(int a,int b,int k,int shift=0) {
    std::vector<int>A(k),B(k);
    for(int i=0;i<k;++i) {A[i]=a%10;a/=10;B[i]=b%10;b/=10;}
    Word out;
    append(out,A,k,k*shift);append(out,B,0,k);append(out,A,0,k);
    append(out,B,k,k*shift);append(out,A,0,k);append(out,B,0,k);
    return out;
}
static std::string expand(const Word& w,int m) {
    std::string out;
    for(auto&s:w) {
        int n=s.a*m+s.b;assert(n>0);
        for(int i=0;i<n;++i) out+='0'+s.p[i%s.p.size()];
    }
    std::reverse(out.begin(),out.end());return out;
}
static std::string numeric_step(const std::string& s) {
    std::string out;int c=0;
    for(int i=s.size()-1;i>=0;--i) {
        int z=s[i]+s[s.size()-1-i]-2*'0'+c;out+='0'+z%10;c=z/10;
    }
    if(c) out+='0'+c;
    std::reverse(out.begin(),out.end());return out;
}
struct Result {int M=3,steps=0,segments=0;std::vector<int>hits;};
static Result check_code(int a,int b,int k,bool validate) {
    Word w=encoded(a,b,k),target=encoded(a,b,k,1);
    Result res;res.segments=w.size();
    for(int t=1;t<=10*k+4;++t) {
        Word before;
        if(validate) before=w;
        w=add_word(w,res.M);
        if(validate) for(int m:{res.M,res.M+1,res.M+7})
            assert(numeric_step(expand(before,m))==expand(w,m));
        if(eventually_equal(w,target,res.M)) res.hits.push_back(t);
        res.segments=std::max(res.segments,(int)w.size());
        int slope=0,width=0;
        for(auto&s:w) {slope+=s.a;width+=s.b;}
        assert(slope==2*k);
        res.steps=t;
        if(width>6*k) break;
    }
    return res;
}
int main(int argc,char**argv) {
    int maxk=argc>1?std::atoi(argv[1]):4;
    bool validate=argc>2 && std::string(argv[2])=="validate";
    bool allpairs=argc>3 && std::string(argv[3])=="all";
    assert(maxk>=1 && maxk<=5);
    std::cout << "{\n  \"claim\":\"exact eventual periodic-block exclusion; no decimal witness\",\n"
              << "  \"validated_numerically\":" << (validate?"true":"false")
              << ",\n  \"all_pairs\":" << (allpairs?"true":"false") << ",\n  \"widths\":[\n";
    int Q=1;
    for(int k=1;k<=maxk;++k) {
        Q*=10;
        auto start=std::chrono::steady_clock::now();
        unsigned long long tested=0;
        int maxM=3,maxsteps=0,maxsegments=0;
        std::array<int,2> threshold_example={0,0};
        std::vector<std::array<int,3>> hits;
        for(int b=Q/10;b<Q;++b) {
            int a0=allpairs?0:mod(-(Q%99)*b,99);
            int inc=allpairs?1:99;
            for(int a=a0;a<Q;a+=inc) {
                Result r=check_code(a,b,k,validate);
                ++tested;
                if(r.M>maxM) {maxM=r.M;threshold_example={a,b};}
                maxsteps=std::max(maxsteps,r.steps);
                maxsegments=std::max(maxsegments,r.segments);
                for(int t:r.hits) hits.push_back({a,b,t});
            }
        }
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout << "    {\"k\":" << k << ",\"tested\":" << tested
                  << ",\"uniform_threshold\":" << maxM << ",\"maximum_steps\":" << maxsteps
                  << ",\"maximum_segments\":" << maxsegments
                  << ",\"threshold_example\":[" << threshold_example[0] << ',' << threshold_example[1]
                  << "],\"eventual_returns\":[";
        bool first=true;
        for(auto h:hits) {
            if(!first) std::cout << ',';first=false;
            std::cout << '[' << h[0] << ',' << h[1] << ',' << h[2] << ']';
        }
        std::cout << "],\"seconds\":" << sec << '}' << (k==maxk?"\n":",\n") << std::flush;
    }
    std::cout << "  ]\n}\n";
}
