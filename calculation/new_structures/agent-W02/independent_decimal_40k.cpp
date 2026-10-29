// Independent ordinary-decimal-digit replay for W02 frontier fixture.
// Does not import local carry maps or lattice-transition logic.
#include <bits/stdc++.h>
using namespace std;
using u8=uint8_t;
static const int B[34]={2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11}; 
static const int W[9]={1,10,8,5,9,16,0,9,11};
static const int A[11]={6,1,0,1,11,14,10,6,11,16,1};
static const int K[11]={16,0,9,11,1,10,8,5,14,18,0};
vector<u8> seed(int n,const int *symbol){
    vector<u8> pair(n),d(n);
    for(int i=0;i<n/2;i++)pair[i]=pair[n-1-i]=(i<34?B[i]:W[(i-34)%9]);
    if(symbol)for(int j=0;j<11;j++)pair[13998+j]=pair[n-1-13998-j]=symbol[j];
    for(int i=0;i<n/2;i++){int v=pair[i],hi=min(v,9);d[i]=v-hi;d[n-1-i]=hi;}
    assert(d.back()!=0);
    return d;
}
void add_reverse(vector<u8>&d){
    size_t n=d.size();const vector<u8> old=d;int carry=0;
    for(size_t i=0;i<n;i++){int r=old[i]+old[n-1-i]+carry;d[i]=r%10;carry=r/10;}
    if(carry)d.push_back(carry);
}
struct Delta {int lo,hi,edge,pen;uint64_t hash;};
Delta summary(const vector<u8>&ref,const vector<u8>&trial){
    if(ref.size()!=trial.size())throw runtime_error("length mismatch");
    size_t n=ref.size();uint64_t h=14695981039346656037ULL;int lo=-1,hi=-1,edge=-1;
    for(int i=0;i<(int)n/2;i++){
        int v=int(trial[i])+trial[n-1-i];int r=int(ref[i])+ref[n-1-i];
        int delta=v-r;assert(-18<=delta&&delta<=18);
        h=(h^uint8_t(delta+18))*1099511628211ULL;
        if(delta){if(lo==-1)lo=i;hi=i;edge=v;}
    }
    return {lo,hi,edge,int(trial[hi-1])+trial[n-hi],h};
}
bool pal(const vector<u8>&d){return equal(d.begin(),d.begin()+d.size()/2,d.rbegin());}
int main(int argc,char**argv){
    if(argc<2){cerr<<"usage: ./independent_decimal path/to/front_trace.tsv [steps]\n";return 2;}
    ifstream in(argv[1]);if(!in){cerr<<"fixture missing\n";return 2;}
    int steps=argc>2?atoi(argv[2]):5000;
    string header;getline(in,header);
    if(header!="step len Aleft Aright Aedge Apen AfHash Bleft Bright Bedge Bpen BfHash"){cerr<<"wrong header\n";return 2;}
    vector<u8> bg=seed(100000,nullptr),a=seed(100000,A),b=seed(100000,K);
    for(int t=0;t<=steps;t++){
        int time,len,alo,ahi,ae,apen,blo,bhi,be,bpen;uint64_t ah,bh;
        if(!(in>>time>>len>>alo>>ahi>>ae>>apen>>ah>>blo>>bhi>>be>>bpen>>bh)){cerr<<"missing trace step "<<t<<"\n";return 1;}
        if(time!=t||len!=(int)bg.size()||a.size()!=bg.size()||b.size()!=bg.size()){
            cerr<<"bad length/schedule step="<<t<<"\n";return 1;
        }
        if(pal(bg)||pal(a)||pal(b)){cerr<<"palindrome at "<<t<<"\n";return 1;}
        auto da=summary(bg,a),db=summary(bg,b);
        if(da.lo!=alo||da.hi!=ahi||da.edge!=ae||da.pen!=apen||da.hash!=ah||db.lo!=blo||db.hi!=bhi||db.edge!=be||db.pen!=bpen||db.hash!=bh){
            cerr<<"FULL_DELTA_HASH_MISMATCH t="<<t<<"\n";return 1;
        }
        if(t<steps){add_reverse(bg);add_reverse(a);add_reverse(b);}
    }
    cout<<"INDEPENDENT_DECIMAL_PASS steps="<<steps<<" states_checked="<<(steps+1)*3<<" all_full_delta_hashes_match no_palindromes\n";
}
