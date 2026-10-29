// Agent W19: decimal two-step non-gauge multi-packet erasure.
// An exact decimal digit-array implementation; no infinite Lychrel claim.
#include <bits/stdc++.h>
using namespace std;
using Bytes=vector<uint8_t>;
static constexpr int B[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static constexpr int W[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
static constexpr int C0[]={14,9,9,0};
static constexpr int C1[]={0,14,9,0};
static Bytes half(int packets,int copies,int gap,uint32_t mask){
 Bytes h;for(int x:B)h.push_back(x);
 for(int k=0;k<copies;k++)for(int x:W)h.push_back(x);
 for(int p=0;p<packets;p++){
  const int* c=(mask&(1u<<p))?C1:C0;
  for(int j=0;j<4;j++)h.push_back(c[j]);
  if(p+1<packets)for(int k=0;k<gap;k++)for(int x:W)h.push_back(x);
 }
 return h;
}
static Bytes coefficients(int packets,int copies,int gap,uint32_t mask){
 Bytes h=half(packets,copies,gap,mask),p=h;
 for(auto it=h.rbegin();it!=h.rend();++it)p.push_back(*it);
 return p;
}
static Bytes digit_seed(const Bytes&p){
 if(p.size()%2)throw runtime_error("even pairword required");
 Bytes d(p.size());size_t m=p.size()/2;
 for(size_t j=0;j<m;j++){int x=p[j],lo=min(x,9);d[j]=lo;d[d.size()-j-1]=x-lo;}
 if(!d.back())throw runtime_error("leading zero");
 return d;
}
static Bytes step(const Bytes&d){
 Bytes out;out.reserve(d.size()+1);int carry=0;
 for(size_t i=0;i<d.size();i++){
  int v=int(d[i])+d[d.size()-1-i]+carry;
  out.push_back(v%10);carry=v/10;
 }
 if(carry)out.push_back(carry);
 return out;
}
static Bytes pairs(const Bytes&d){
 Bytes q(d.size());for(size_t j=0;j<d.size();j++)q[j]=d[j]+d[d.size()-1-j];
 return q;
}
static string key(const Bytes&d){return string(d.begin(),d.end());}
static void run(int packets,int copies,int gap){
 if(packets<1||packets>16||copies<0||gap<1)throw runtime_error("bad inputs");
 uint32_t n=1u<<packets;
 set<string> before,after_one,after_two;
 Bytes reference;size_t bytes=0;
 for(uint32_t mask=0;mask<n;mask++){
  Bytes p=coefficients(packets,copies,gap,mask);
  Bytes d=digit_seed(p);
  if(pairs(d)!=p)throw runtime_error("seed pairword mismatch");
  Bytes d1=step(d),d2=step(d1),d3=step(d2);
  bytes=d.size();
  if(d1.size()!=d.size()+1||d2.size()!=d.size()+1||d3.size()!=d.size()+2)
   throw runtime_error("unexpected overflow schedule");
  before.insert(key(p));after_one.insert(key(pairs(d1)));after_two.insert(key(pairs(d2)));
  if(mask==0)reference=d3;
  if(d3!=reference)throw runtime_error("third integer did not coalesce");
 }
 if(before.size()!=n||after_one.size()!=n||after_two.size()!=1)
   throw runtime_error("distinct non-gauge erasure family failed");
 cout<<"PASS packets="<<packets<<" gap="<<gap<<" copies="<<copies
     <<" decimal_seed_digits="<<bytes<<" distinct_t0="<<before.size()
     <<" distinct_pair_t1="<<after_one.size()<<" distinct_pair_t2="<<after_two.size()
     <<" identical_integers_t3=true\n";
}
static vector<array<int,8>> parse_rows(const string&line){
 vector<array<int,8>> out;size_t p=0;
 while((p=line.find('[',p))!=string::npos){
  size_t q=line.find(']',p);if(q==string::npos)throw runtime_error("bad phase file");
  auto chunk=line.substr(p+1,q-p-1);array<int,8> row{};stringstream ss(chunk);string token;
  for(int j=0;j<8;j++){if(!getline(ss,token,','))throw runtime_error("incomplete phase row");row[j]=stoi(token);}
  out.push_back(row);p=q+1;
 }
 return out;
}
static uint64_t fnv(const Bytes&d){
 uint64_t h=14695981039346656037ULL;
 for(auto x:d){h^=x;h*=1099511628211ULL;}return h;
}
static void run_long(int packets,int copies,int gap,int steps,const string&file){
 ifstream in(file);if(!in)throw runtime_error("cannot open phase file");
 string line1,line2;getline(in,line1);getline(in,line2);
 auto root=parse_rows(line1),bulk=parse_rows(line2);
 if(root.size()!=39||bulk.size()!=20)throw runtime_error("bad phase table counts");
 Bytes a=digit_seed(coefficients(packets,copies,gap,0));
 size_t min_front=SIZE_MAX,min_half=SIZE_MAX;int bad=0;
 for(int t=0;t<=steps;t++){
  if(a.size()%2==0&&equal(a.begin(),a.begin()+a.size()/2,a.rbegin()))
   throw runtime_error("palindrome at time "+to_string(t));
  size_t H=a.size()/2;min_half=min(min_half,H);size_t j=0;
  for(;j<H;j++){
   int expected=j<39?root[j][t%8]:bulk[(j-39)%20][t%8];
   if(int(a[j])+a[a.size()-1-j]!=expected)break;
  }
  min_front=min(min_front,j);
  if(j<200)throw runtime_error("outer 200-column guard lost at "+to_string(t));
  if(t==0||t==1000||t==10000||t==steps)
   cout<<"CHECKPOINT t="<<t<<" digits="<<a.size()<<" first_bad="<<j
       <<" fnv64="<<hex<<fnv(a)<<dec<<"\n";
  if(t<steps){
   Bytes b=step(a);int delta=int(b.size())-int(a.size());
   if(delta!=int(t%2==0))throw runtime_error("overflow schedule broke");
   a.swap(b);
  }
 }
 cout<<"LONG_PASS steps="<<steps<<" packets="<<packets<<" copies="<<copies
     <<" min_first_bad="<<min_front<<" min_half="<<min_half
     <<" palindromes="<<bad<<"\n";
}
int main(int argc,char**argv){try{
 if(argc==4)run(stoi(argv[1]),stoi(argv[2]),stoi(argv[3]));
 else if(argc==7&&string(argv[1])=="--long")
  run_long(stoi(argv[2]),stoi(argv[3]),stoi(argv[4]),stoi(argv[5]),argv[6]);
 else{cerr<<"usage: erasure PACKETS COPIES GAP | erasure --long PACKETS COPIES GAP STEPS PHASE_FILE\n";return 2;}
 return 0;
}catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
