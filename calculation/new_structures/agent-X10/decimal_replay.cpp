// Fully independent ordinary decimal digit-array reverse-and-add, all digits checked against
// the separate symbolic 4-sheet oracle at EVERY STEP; no GMP/no decimal parsing needed.
// g++ -std=c++17 -O3 decimal_replay.cpp -o decimal_replay
#define main four_sheet_engine_main
#include "four_sheet_fast.cpp"
#undef main
#include <stdexcept>
static string expected(const S& p,int q,int r){
    static const int coef[4][2]={{0,0},{1,0},{2,1},{3,1}};
    int top=3*q+r+p[3].end();
    string v(top+1,'0');
    for(int k=0;k<4;k++){
       int shift=coef[k][0]*q+coef[k][1]*r;
       for(int j=0;j<p[k].length();j++){
          int exp=shift+p[k].start+j;
          if(exp<0||exp>top)throw runtime_error("out-of-range exponent");
          char &dst=v[top-exp];
          if(dst!='0'&&p[k].d[j])throw runtime_error("overlap");
          if(p[k].d[j])dst='0'+p[k].d[j];
       }
    }
    if(v[0]=='0')throw runtime_error("leading zero");
    return v;
}
static string raa(const string&s){
    int carry=0;int n=(int)s.size();string t(n,'0');
    for(int i=n-1;i>=0;--i){
        int x=(s[i]-'0')+(s[n-1-i]-'0')+carry;
        t[i]=(char)('0'+x%10);carry=x/10;
    }
    if(carry)t.insert(t.begin(),(char)('0'+carry));
    return t;
}
// Exact concrete-parameter guard; unlike a uniform q,r>=G bound, it also
// admits r<0 when q+r is still a sufficiently wide middle gap.
static bool actual_gap_guard(const S&x,int q,int r){
    const int bases[4]={0,q,2*q+r,3*q+r};
    for(int k=0;k<4;k++)
        if(!x[k].empty()&&bases[k]+x[k].start<0)return false;
    for(int k=0;k<3;k++)
        if(!x[k].empty()&&!x[k+1].empty()&&
           bases[k+1]+x[k+1].start<=bases[k]+x[k].end())return false;
    return !x[3].empty();
}
static bool ispal(const string&s){
    for(int i=0,j=(int)s.size()-1;i<j;i++,j--)if(s[i]!=s[j])return false;
    return true;
}
int main(int argc,char**argv){
    if(argc<4){cerr<<"Usage: ./decimal_replay steps q r [continue_after_guard]\n";return 2;}
    int T=atoi(argv[1]),q=atoi(argv[2]),r=atoi(argv[3]);bool past=argc>4;
    S x;x[0]={0,{5,7}};x[1]={0,{7,3}};x[2]={};x[3]={0,{8,8}};
    string actual=expected(x,q,r);
    int G=0,matched=0,nonpal=0,first_mismatch=-1,first_guard=-1;
    for(int t=0;t<=T;t++){
        G=max(G,needed_G(x));
        if(!actual_gap_guard(x,q,r)&&first_guard==-1)first_guard=t;
        bool ok=true;
        try{ok=(expected(x,q,r)==actual);}catch(const exception& e){ok=false;}
        if(ok)matched++;
        if(!ok&&first_mismatch==-1)first_mismatch=t;
        if(!ispal(actual))nonpal++;
        if(t==0||t==88||t==264||t==1000||t==5000||t==10000||t==20000||t==T){
           cout<<"t="<<t<<" digits="<<actual.size()<<" G="<<G<<" shape="<<ok<<" nonpal="<<!ispal(actual)<<"\n";
        }
        if(!ok&&!past)break;
        if(t<T){actual=raa(actual);x=evolve(x);}
    }
    cout<<"SUMMARY steps="<<T<<" q="<<q<<" r="<<r<<" matched="<<matched<<" nonpal="<<nonpal<<" guard_exit="<<first_guard<<" first_mismatch="<<first_mismatch<<" final_bound="<<G<<"\n";
    return (first_mismatch==-1&&nonpal==T+1)?0:1;
}
