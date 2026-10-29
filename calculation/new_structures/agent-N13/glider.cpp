#include <bits/stdc++.h>
using namespace std;
using V=vector<uint8_t>;
static const int PATH[]={17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13};
static const int CYC[]={17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13};
V init(int half,int replacement){V a(2*half);for(int j=0;j<half;j++){
 int q=j<39?PATH[j]:CYC[(j-39)%20];if(replacement && j>=half-replacement)q=(7*j+11)%19;
 a[j]=min(q,9);a[2*half-1-j]=q-a[j];}return a;}
V next(const V&a){V b(a.size()+1);int carry=0;for(size_t j=0;j<a.size();j++){
 int q=a[j]+a[a.size()-1-j]+carry;b[j]=q%10;carry=q/10;
 }if(carry)b[a.size()]=carry;else b.pop_back();return b;}
int firstDifferentPair(const V&a,const V&b){int j=0;for(;j<int(min(a.size(),b.size())/2);j++)if(a[j]+a[a.size()-1-j]!=b[j]+b[b.size()-1-j])break;return j;}
struct Snap{V a,b;int front;};
int main(int argc,char**argv){int half=argc>1?stoi(argv[1]):5200,steps=argc>2?stoi(argv[2]):20000,patch=argc>3?stoi(argv[3]):100;
 int begin=argc>4?stoi(argv[4]):1000; int rmin=-100,rmax=74;
 V a=init(half,0),b=init(half,patch);deque<Snap> prior;long count=0;int firstBad=-1;
 vector<int> fail75;long badWrong19=0;
 for(int t=0;t<=steps;t++){
   int f=firstDifferentPair(a,b);
   if(t>=begin && t>=88){
     auto &p=prior[prior.size()-88];
     if(f!=p.front-20 || int(a.size())-int(p.a.size())!=44 || int(b.size())-int(p.b.size())!=44){cerr<<"incorrect front/length t="<<t<<"\n";return 2;}
     for(int r=rmin;r<=rmax;r++){
       int j=f+r,k=p.front+r;
       if(j<0 || k<0 || j>=int(a.size())/2 || k>=int(p.a.size())/2){cerr<<"position out of range\n";return 2;}
       if(a[j]!=p.a[k] || b[j]!=p.b[k] || a[a.size()-1-j]!=p.a[p.a.size()-1-k] || b[b.size()-1-j]!=p.b[p.b.size()-1-k]){
         if(firstBad<0)firstBad=t;
       }
       count+=4;
     }
     int r=75,j=f+r,k=p.front+r;
     bool same=(a[j]==p.a[k] && b[j]==p.b[k] && a[a.size()-1-j]==p.a[p.a.size()-1-k] && b[b.size()-1-j]==p.b[p.b.size()-1-k]);
     if(!same && fail75.size()<30)fail75.push_back(t);
     int wrong=k-1;
     if(j>=0 && wrong>=0 && a[j]!=p.a[wrong])badWrong19++;
   }
   prior.push_back({a,b,f});if(prior.size()>89)prior.pop_front();
   if(t<steps){a=next(a);b=next(b);}
 }
 cout<<"half="<<half<<" steps="<<steps<<" patch="<<patch<<" begin="<<begin<<" digit_checks="<<count
 <<" first_bad="<<firstBad<<" wrong_offset19_failures="<<badWrong19<<" r75_failures=";
 for(int t:fail75){cout<<t<<",";}cout<<"\n";
 if(firstBad>=0)return 1;
 cout<<"SHEARED_TWO_END_GLIDER_WINDOW_PASS\n";
}
