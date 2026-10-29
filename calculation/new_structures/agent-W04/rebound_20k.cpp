// W04 independent decimal rebound ordinary digit-vector reverse-add, no carry transducer.
// Usage: ./independent_20k M N STEPS MIN_RUN
#include <bits/stdc++.h>
using namespace std;
static vector<uint8_t> make_seed(int m,int n){
 vector<int> H; H.insert(H.end(),{11,9,8,17});H.insert(H.end(),m,8);H.push_back(17);H.push_back(7);H.insert(H.end(),n,16);H.push_back(8);
 const int k=H.size();vector<uint8_t> d(2*k);
 for(int i=0;i<k;i++){int x=H[i],high=min(9,x);d[i]=x-high;d[2*k-1-i]=high;}
 if(d.back()==0)throw runtime_error("zero leading digit");
 return d;
}
static bool has_ordered_bands(const vector<uint8_t>&d,int a,int b,int threshold,int& Alen,int& Blen){
 const int h=(d.size()+1)/2;
 // O(n) dynamic max for B over suffix, ensuring runs occur in order.
 vector<int> bs(h+1,0),suffix(h+1,0);
 for(int i=h-1;i>=0;i--){int x=int(d[i])+int(d[d.size()-1-i]);bs[i]=x==b?bs[i+1]+1:0;suffix[i]=max(bs[i],suffix[i+1]);}
 int run=0;
 for(int i=0;i<h;i++){
   int x=int(d[i])+int(d[d.size()-1-i]);run=(x==a?run+1:0);
   if(run>=threshold && suffix[i+1]>=threshold){Alen=max(Alen,run); Blen=max(Blen,suffix[i+1]);}
 }
 return Alen>=threshold && Blen>=threshold;
}

struct Band {int pos=-1, len=0;};
static Band longest_run(const vector<uint8_t>&d,int target){
 Band best;int run=0;
 for(int i=0;i<(int)(d.size()+1)/2;i++){
  int x=int(d[i])+int(d[d.size()-1-i]);
  if(x==target)run++; else run=0;
  if(run>best.len){best.pos=i-run+1;best.len=run;}
 }
 return best;
}
static bool pump_both(const vector<uint8_t>&d,const vector<uint8_t>&out,
                      const vector<uint8_t>&c,int a,int b,int A,int B,
                      int&olapA,int&olapB,int&odd){
 const int q=d.size();
 Band p=longest_run(d,a),r=longest_run(d,b);
 Band P=longest_run(out,A),R=longest_run(out,B);
 if(p.pos<0||P.pos<0||r.pos<0||R.pos<0 ||p.pos+p.len>r.pos||P.pos+P.len>R.pos)return false;
 auto witness=[&](Band x,Band y,int&olap)->bool{
  int begin=max(x.pos,y.pos),end=min(x.pos+x.len,y.pos+y.len);
  olap=max(0,end-begin);
  for(int i=begin;i<end && i<(q+1)/2;i++){
   // Finite two-ended carry-transducer state before / after column i.
   // First digit after overflow is handled in the outer finite root;
   // all pump sites are strictly internal to a uniform band.
   int previous=(i==0?-1:out[q-i]);
   int next_previous=out[q-i-1];
   if(int(c[i])==int(c[i+1]) && int(c[q-i])==int(c[q-i-1]) && previous==next_previous)
     return true;
  }
  return false;
 };
 odd=0;
 for(int i=0;i<(q+1)/2;i++)odd+=(int(d[i])+int(d[q-1-i]))%2;
 return odd>0 && witness(p,P,olapA) && witness(r,R,olapB);
}
int main(int argc,char**argv){
 if(argc!=5){cerr<<"USAGE M N STEPS MIN_RUN\n";return 1;}
 int m=stoi(argv[1]),n=stoi(argv[2]),steps=stoi(argv[3]),minrun=stoi(argv[4]);
 vector<uint8_t>d=make_seed(m,n);const int A[6]={8,16,14,10,2,4},B[6]={16,14,10,2,4,8};
 uint64_t hsh=1469598103934665603ULL;int minA=INT_MAX,minB=INT_MAX,minOlA=INT_MAX,minOlB=INT_MAX,minOdd=INT_MAX;
 for(int t=0;t<=steps;t++){
   if(d.empty() || d.back()==0){cerr<<"NONCANONICAL "<<t<<"\n";return 2;}
   bool pal=true;for(int i=0,j=(int)d.size()-1;i<j;i++,j--){if(d[i]!=d[j]){pal=false;break;}}
   if(pal){cerr<<"PALINDROME "<<t<<"\n";return 3;}
   int la=0,lb=0;
   if(!has_ordered_bands(d,A[t%6],B[t%6],minrun,la,lb)){
     cerr<<"BAND_SHAPE_FAIL t="<<t<<" A="<<la<<" B="<<lb<<"\n";return 4;
   }
   minA=min(minA,la);minB=min(minB,lb);
   int currentOdd=0;
   for(int i=0;i<(int)(d.size()+1)/2;i++)currentOdd+=(int(d[i])+int(d[d.size()-1-i]))%2;
   if(currentOdd==0){cerr<<"NO_ODD_COEFFICIENT "<<t<<"\n";return 6;}
   minOdd=min(minOdd,currentOdd);
   hsh^=uint64_t(t);hsh*=1099511628211ULL;
   hsh^=uint64_t(d.size());hsh*=1099511628211ULL;
   hsh^=uint64_t(la);hsh*=1099511628211ULL;
   hsh^=uint64_t(lb);hsh*=1099511628211ULL;
   if(t%5000==0||t==steps){
     uint64_t numeric=1469598103934665603ull;
     for(auto it=d.rbegin();it!=d.rend();++it){numeric^=uint8_t('0'+*it);numeric*=1099511628211ull;}
     cout<<"CHECKPOINT "<<t<<" digits="<<d.size()<<" A="<<la<<" B="<<lb<<" digest="<<hex<<hsh<<" numeric_fnv="<<numeric<<dec<<"\n"<<flush;
   }
   if(t==steps)break;
   vector<uint8_t>next;next.resize(d.size());int carry=0;int q=d.size();
   vector<uint8_t> carries(q+1);carries[0]=0;
   for(int i=0;i<q;i++){int z=int(d[i])+int(d[q-1-i])+carry;next[i]=z%10;carry=z/10;carries[i+1]=carry;}
   if(carry)next.push_back(carry);
   int oA=0,oB=0,odd=0;
   if(!pump_both(d,next,carries,A[t%6],B[t%6],A[(t+1)%6],B[(t+1)%6],oA,oB,odd)){
     cerr<<"INDEPENDENT_COUNTER_PUMP_FAIL t="<<t<<" overlapA="<<oA<<" overlapB="<<oB<<" odd="<<odd<<"\n";return 5;
   }
   minOlA=min(minOlA,oA);minOlB=min(minOlB,oB);minOdd=min(minOdd,odd);
   d.swap(next);
 }
 cout<<"COMPUTED 20000 shape-and-nonpalindrome states="<<steps+1<<" m="<<m<<" n="<<n<<" minA="<<minA<<" minB="<<minB<<" minOverlapA="<<minOlA<<" minOverlapB="<<minOlB<<" minOdd="<<minOdd<<" final_digits="<<d.size()<<" digest="<<hex<<hsh<<dec<<"\n";
}
