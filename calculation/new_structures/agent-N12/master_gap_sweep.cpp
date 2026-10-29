// Exact master-orbit transfer for a family of central-padding seeds.
// This is a finite-horizon experiment, NOT a decimal Lychrel proof.
#include <bits/stdc++.h>
using namespace std;
using D=vector<uint8_t>;
D seed(int gap){string s="39"+string(gap,'0')+"43";D x;for(auto it=s.rbegin();it!=s.rend();++it)x.push_back(*it-'0');return x;}
void step(D& d){int n=(int)d.size(),carry=0;D e(n+1);for(int i=0;i<n;i++){int a=d[i]+d[n-1-i]+carry;e[i]=a%10;carry=a/10;}if(carry)e[n]=carry;else e.pop_back();d.swap(e);}
int width(const D&d){int n=d.size();for(int j=n/2-1;j>=0;j--)if(d[j]+d[n-j-1])return j+1;return 0;}
int zeros(const D&d){return int(d.size())-2*width(d);}
int mismatch(const D&d){int n=d.size();for(int j=0;j<n/2;j++)if(d[j]!=d[n-1-j])return j;return -1;}
D unpad(const D &m,int delta){
 int n=(int)m.size(),right=(n-delta+1)/2;
 if(delta<0||n-delta<4||right<0||right+delta>n)abort();
 for(int j=right;j<right+delta;j++)if(m[j]!=0){cerr<<"unpad_nonzero\n";abort();}
 D s;s.reserve(n-delta);
 s.insert(s.end(),m.begin(),m.begin()+right);
 s.insert(s.end(),m.begin()+right+delta,m.end());
 return s;
}
int main(int argc,char**argv){
 int maxk=argc>1?atoi(argv[1]):256,limit=argc>2?atoi(argv[2]):52000,guard=argc>3?atoi(argv[3]):100;
 if(maxk<0||maxk>2000||limit<51000||guard<10)return 2;
 D master=seed(31000+maxk);
 vector<D>x(maxk+1);
 vector<int> activation(maxk+1,-1),firstzero(maxk+1,-1),firstpal(maxk+1,-1),maxwitness(maxk+1,0),finalz(maxk+1,-999);
 int activated=0,max_master_mismatch=0;
 for(int t=0;t<=limit;t++){
  int zm=zeros(master),mm=mismatch(master);
  if(mm<0){cerr<<"master palindrome at t="<<t<<"\n";return 5;}
  max_master_mismatch=max(max_master_mismatch,mm);
  for(int k=0;k<=maxk;k++){
   int delta=maxk-k;
   if(activation[k]<0&&zm<=delta+guard){
    if(zm-delta<4){cerr<<"padding guard violated t="<<t<<" k="<<k<<"\n";return 3;}
    x[k]=unpad(master,delta);
    if(zeros(x[k])!=zm-delta){cerr<<"bad unpadding\n";return 3;}
    activation[k]=t;activated++;maxwitness[k]=max_master_mismatch;
   }
   if(activation[k]>=0&&firstzero[k]<0){
    int z=zeros(x[k]);finalz[k]=z;
    if(z==0)firstzero[k]=t;
    int w=mismatch(x[k]);
    if(w<0&&firstpal[k]<0)firstpal[k]=t;
    maxwitness[k]=max(w,maxwitness[k]);
   }
  }
  if(t<limit){step(master);for(int k=0;k<=maxk;k++)if(activation[k]>=0&&firstzero[k]<0)step(x[k]);}
 }
 if(activated!=maxk+1){cerr<<"not all activated "<<activated<<"\n";return 4;}
 cout<<"k,gap,activation,first_zero,first_pal,max_mismatch_index_through_collision,final_z\n";
 for(int k=0;k<=maxk;k++)
  cout<<k<<','<<31000+k<<','<<activation[k]<<','<<firstzero[k]<<','<<firstpal[k]<<','<<maxwitness[k]<<','<<finalz[k]<<'\n';
}
