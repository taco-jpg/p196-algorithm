'use strict';

// Agent #118 independent JavaScript seven-column inverse/rank replay.

// Finite computation only; not a Lean proof or claim about all-time 196.

const K = 7;

function key(d){return String.fromCharCode(...d.map(x=>65+x))}

function digits(w){return Array.from(w,ch=>ch.charCodeAt(0)-65)}

function exactShortForward(w){
  const s=digits(w), norm=[];let carry=0;
  for(const v of s){const u=v+carry;norm.push(u%10);carry=Math.floor(u/10);}
  if(carry)norm.push(carry);
  return key(norm.map((v,i)=>v+norm[norm.length-1-i]));
}

function possibleLongForward(w){
  const s=digits(w),k=s.length,lo=[];let carry=0;
  for(const v of s){let t=v+carry;lo.push(t%10);carry=Math.floor(t/10);}
  const result=new Set();
  for(let e=0;e<2;e++){
    let h=new Array(k);carry=e;
    for(let i=k-1;i>=0;i--){let z=s[i]+carry;h[i]=z%10;carry=Math.floor(z/10);}
    if(carry)result.add(key([lo[0]+1,...Array.from({length:k-1},(_,j)=>lo[j+1]+h[j])]));
    else result.add(key(lo.map((v,i)=>v+h[i])));
  }
  return result;
}

function shortPredecessors(k){
  const index=new Map();let sourceCount=0;
  function add(s){sourceCount++;const w=key(s),dest=exactShortForward(w);if(!index.has(dest))index.set(dest,new Set());index.get(dest).add(w);}
  add; for(let n=1;n<k;n++){
    if(n===1){for(let c=2;c<=18;c+=2)add([c]);continue;}
    const l=Math.floor(n/2),freedom=l-1;
    for(let a=1;a<=18;a++)
      for(let v=0;v<19**freedom;v++){
        let rem=v,tail=new Array(freedom);
        for(let i=freedom-1;i>=0;i--){tail[i]=rem%19;rem=Math.floor(rem/19);}
        const left=[a,...tail];
        if(n%2===0)add([...left,...left.slice().reverse()]);
        else for(let c=0;c<=18;c+=2)add([...left,c,...left.slice().reverse()]);
      }
  }
  return {index,sourceCount};
}

function initialWords(pref,k){
  let d=Array.from(pref,ch=>Number(ch)),D=d.length;
  if(D<3||D>k||d[0]<1||d[0]>9)throw Error("invalid prefix");
  let longer=new Set(),shorter=new Set();
  for(let v=0;v<10**(k-D);v++){
    let tail=String(v).padStart(k-D,"0").split("").map(Number);
    longer.add(key([...d,...tail]));
  }
  for(let n=D;n<k;n++){
    let half=Math.ceil(n/2);
    for(let v=0;v<10**half;v++){
      let h=String(v).padStart(half,"0").split("").map(Number);
      let p=[...h,...h.slice(0,Math.floor(n/2)).reverse()];
      if(p.slice(0,D).every((x,i)=>x===d[i])&&(n%2===0||p[Math.floor(n/2)]%2===0))shorter.add(key(p));
    }
  }
  return {longer,shorter,all:new Set([...longer,...shorter])};
}

function invertLongFactory(k){
  const tab=new Map(),memo=new Map();
  for(let p=0;p<=18;p++)for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
    const opts=[];for(let s=0;s<=18;s++){
      const xo=Math.floor((s+x)/10),yo=Math.floor((s+y)/10);
      if((s+x)%10+(s+y)%10===p)opts.push([s,xo,yo]);
    }
    tab.set(`${p},${x},${y}`,opts);
  }
  return function invert(pw){
    if(memo.has(pw))return memo.get(pw);
    const p=digits(pw);
    if(p.length!==k||p.some(v=>v<0||v>18))return new Set();
    let states=[["",0,0]];
    for(let i=0;i<k;i++){
      const next=new Map();
      for(const [w,x,needed] of states)for(let yin=0;yin<=1;yin++){
        for(const [s,xo,yo] of tab.get(`${p[i]},${x},${yin}`)){
          if(i===0&&s===0)continue;
          if(yo!==needed)continue;
          const row=[w+String.fromCharCode(65+s),xo,yin];
          next.set(row.join("|"),row);
        }
      }
      states=[...next.values()];
    }
    const ans=new Set(states.map(st=>st[0]));
    if(p[0]>=1&&p[0]<=10){
      for(let x1=0;x1<=1;x1++){
        const s0=p[0]-1+10*x1;
        if(s0<1||s0>18)continue;
        let g=[];for(let yin=0;yin<=1;yin++)
          if(Math.floor((s0+yin)/10)===1)g.push([String.fromCharCode(65+s0),x1,yin]);
        for(let i=1;i<k;i++){
          const next=new Map();
          for(const [w,x,y_prev] of g){
            const hp=(w.charCodeAt(w.length-1)-65+y_prev)%10;
            const low=p[i]-hp;
            if(low<0||low>9)continue;
            for(let xo=0;xo<=1;xo++){
              const s=low+10*xo-x;
              if(s<0||s>18)continue;
              for(let yin=0;yin<=1;yin++){
                if(Math.floor((s+yin)/10)!==y_prev)continue;
                const row=[w+String.fromCharCode(65+s),xo,yin];
                next.set(row.join("|"),row);
              }
            }
          }
          g=[...next.values()];
        }
        for(const [w] of g)ans.add(w);
      }
    }
    memo.set(pw,ans);return ans;
  };
}

function sharedCertificate(prefixes=["5523","5524"]){
  const k=K,t0=Date.now(),rootsBy=new Map();
  for(const pref of prefixes)rootsBy.set(pref,initialWords(pref,k));
  const initialUnion=new Set([...rootsBy.values()].flatMap(x=>[...x.all]));
  const {index:shortIndex,sourceCount}=shortPredecessors(k);
  if(sourceCount!==10467)throw Error("bad count short sources "+sourceCount);
  const inv=invertLongFactory(k),seen=new Set(initialUnion),todo=[...seen],parents=new Map(),children=new Map();
  let longEdges=0,shortEdges=0;
  while(todo.length){
    const p=todo.pop(),ps=new Set(shortIndex.get(p)||[]);
    if(p.length===k)for(const s of inv(p))ps.add(s);
    parents.set(p,ps);
    for(const q of ps){
      if(q.length===k){if(!possibleLongForward(q).has(p))throw Error("invalid long edge");longEdges++;}
      else{if(exactShortForward(q)!==p)throw Error("invalid short edge");shortEdges++;}
      if(!children.has(q))children.set(q,[]);
      children.get(q).push(p);
      if(!seen.has(q)){
        seen.add(q);todo.push(q);
        if(seen.size>700000)throw Error("CAP");
      }
    }
  }
  const rem=new Map([...parents].map(([p,ps])=>[p,ps.size]));
  let queue=[...rem].filter(([p,v])=>v===0).map(([p])=>p);
  const rank=new Map(queue.map(p=>[p,0]));
  for(let i=0;i<queue.length;i++){
    const q=queue[i];
    for(const p of children.get(q)||[]){
      rem.set(p,rem.get(p)-1);
      if(rem.get(p)===0){
        rank.set(p,1+Math.max(...[...parents.get(p)].map(s=>rank.get(s))));
        queue.push(p);
      }
    }
  }
  if(rank.size!==seen.size)throw Error("cyclic");
  for(const [p,ps] of parents)for(const q of ps)
    if(!(rank.get(q)<rank.get(p)))throw Error("rank defect");
  const closureOf=(roots)=>{
    const all=new Set(roots),stack=[...all];
    while(stack.length)for(const q of parents.get(stack.pop())){
      if(!all.has(q)){all.add(q);stack.push(q);}
    }
    return all;
  };
  const closures=new Map([...rootsBy].map(([p,v])=>[p,closureOf(v.all)]));
  const keys=[...closures.keys()];
  const overlap=keys.length===2?[...closures.get(keys[0])].filter(s=>closures.get(keys[1]).has(s)).length:0;
  const distribution={};
  for(const r of rank.values())distribution[r]=(distribution[r]||0)+1;
  const perPrefix={};
  for(const [pref,v] of rootsBy){
    let max=-1;for(const row of v.all)max=Math.max(max,rank.get(row));
    perPrefix[pref]={initial_long:v.longer.size,initial_short:v.shorter.size,closure_nodes:closures.get(pref).size,initial_max_rank:max,method_bound:max+1};
  }
  return {status:"ACYCLIC",evidence:"INDEPENDENT JAVASCRIPT FINITE REPLAY; NOT LEAN CHECKED",prefixes,k,initial_union:initialUnion.size,short_sources:sourceCount,closure_total:seen.size,closure_long:[...seen].filter(w=>w.length===k).length,closure_short:[...seen].filter(w=>w.length<k).length,all_edges:longEdges+shortEdges,long_edges:longEdges,short_edges:shortEdges,rank_max_entire_graph:Math.max(...rank.values()),rank_distribution:distribution,shared_overlap_nodes:overlap,by_prefix:perPrefix,runtime_ms:Date.now()-t0};
}

if (typeof require !== 'undefined' && require.main === module) {

  const p = process.argv.slice(2).filter(s => /^[1-9][0-9]{3}$/.test(s));

  console.log(JSON.stringify(sharedCertificate(p.length ? p : ['5523','5524']),null,2));

}
