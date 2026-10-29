// Independent GMP verification of the 161-site moving macrofront
// in the finite decimal orbit N225, compared at temporal lag 88.
#include <gmpxx.h>
#include <algorithm>
#include <deque>
#include <iostream>
#include <string>
using namespace std;
const string entrance[]={
"H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D",
"8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB",
"H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4",
"8E8438GGCD99B9BC949B5397A498C98G8E7339A",
"H8H86HDE680040459A92B6IF09IH49ICI8F6791",
"8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA",
"HDEEAA6049H08899A1149HBBE0IF69I56GA68E1",
"8C9A62764E788GI90225E7A4759FCG8EBD87ED6"};
const string lattice[]={
"H31DHBE3I12073ECF97D","CB45CA78CA327A8895HB",
"639B51FH5174F0HGIBF4","A9D1767ED68BA68FGB8A",
"2073ECF97DH31DHBE3I1","327A8895HBCB45CA78CA",
"74F0HGIBF4639B51FH51","8BA68FGB8AA9D1767ED6"};
const string alphabet="0123456789ABCDEFGHI";
struct Snapshot{int t,front;string motif;};
int main(){
 string seed;if(!(cin>>seed))return 2;
 mpz_class n(seed,10);deque<Snapshot> history;
 int checked=0,failFront=0,failMotif=0,firstBreak=-1;
 int breakF0=-1,breakF1=-1,breakMatch=-1,minMatch=999;
 for(int t=0;t<=20000;t++){
  string s=n.get_str(10);int m=s.size(),half=m/2;
  auto pairAt=[&](int i){return (s[i]-'0')+(s[m-1-i]-'0');};
  int f=0;
  while(f<half){
   int want=alphabet.find(f<39?entrance[t%8][f]:lattice[t%8][(f-39)%20]);
   if(pairAt(f)!=want)break;
   f++;
  }
  string motif;
  for(int j=0;j<240&&f+j<half;j++)motif+=alphabet[pairAt(f+j)];
  if(t==2000||t==10000||t==19000||t==19722||t==19723||t==20000)
   cout<<"checkpoint t="<<t<<" frontier="<<f<<" motif32="<<motif.substr(0,32)<<"\n";
  if(history.size()==88){
   const auto&prev=history.front();
   int equal=0;
   while(equal<(int)min(prev.motif.size(),motif.size())&&prev.motif[equal]==motif[equal])equal++;
   if(prev.t>=2000&&prev.t<=19722){
    checked++;
    if(f!=prev.front-20)failFront++;
    if(equal<161)failMotif++;
    minMatch=min(minMatch,equal);
   }
   if(prev.t>=2000&&firstBreak<0&&(f!=prev.front-20||equal<161)){
    firstBreak=prev.t;breakF0=prev.front;breakF1=f;breakMatch=equal;
   }
   history.pop_front();
  }
  history.push_back({t,f,move(motif)});
  if(t==20000)break;
  string rev(s.rbegin(),s.rend());n+=mpz_class(rev,10);
 }
 cout<<"GLIDER checked="<<checked<<" front_fail="<<failFront<<" motif_fail="<<failMotif
     <<" min_motif_match="<<minMatch<<" first_break_t="<<firstBreak
     <<" front_before="<<breakF0<<" front_after="<<breakF1<<" matched="<<breakMatch<<"\n";
 return !(checked==17723&&failFront==0&&failMotif==0&&minMatch>=161&&firstBreak==19723);
}