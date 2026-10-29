#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){int Q=argc>1?atoi(argv[1]):47,T=argc>2?atoi(argv[2]):100000;vector<unsigned char>d;d.push_back(6);d.insert(d.end(),2*Q,9);d.push_back(1);if(argc>3){string seed=argv[3];if(seed.empty()||seed[0]=='0'||seed.find_first_not_of("0123456789")!=string::npos){cerr<<"invalid seed\n";return 2;}d.clear();for(auto it=seed.rbegin();it!=seed.rend();++it)d.push_back(*it-'0');}long long ov=0,noodd=0,out16=0,out32=0;int maxodd=0,firstOut16=-1,firstOut32=-1,firstNoOdd=-1,firstPalindrome=-1;
for(int t=0;t<=T;t++){
 int n=d.size(),i=0;for(;i<n/2;i++)if((d[i]+d[n-1-i])&1)break;
 if(i==n/2){noodd++;if(firstNoOdd<0)firstNoOdd=t;bool pal=true;for(int k=0;k<n/2;k++)if(d[k]!=d[n-1-k]){pal=false;break;}if(pal){firstPalindrome=t;break;}}
 else {maxodd=max(maxodd,i);if(i>=16){out16++;if(firstOut16<0)firstOut16=t;}if(i>=32){out32++;if(firstOut32<0)firstOut32=t;}}
 if(t%10000==0||t==T)cout<<"CHECK t="<<t<<" digits="<<n<<" oddIndex="<<i<<" overflow="<<ov<<" noOdd="<<noodd<<"\n";
 if(t==T)break;
 vector<unsigned char>o(n);int c=0;for(int j=0;j<n;j++){int s=d[j]+d[n-1-j]+c;o[j]=s%10;c=s/10;}if(c){o.push_back(1);ov++;}d.swap(o);
}
cout<<"SUMMARY T="<<T<<" finalN="<<d.size()<<" overflow="<<ov<<" maxOdd="<<maxodd<<" noOdd="<<noodd<<" firstNoOdd="<<firstNoOdd<<" out16="<<out16<<" firstOut16="<<firstOut16<<" out32="<<out32<<" firstOut32="<<firstOut32<<" palindrome="<<firstPalindrome<<"\n";
}
