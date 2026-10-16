#!/usr/bin/env node
'use strict';

// Independent replay of the full persisted k=7 rank witness for Agent #118.
// This is a finite computation check, not Lean and not a result about P196.
function checkWitness(raw, h) {
  const {key,digits,invertLongFactory,shortPredecessors,initialWords,
         exactShortForward,possibleLongForward} = h;
  if (raw.charCodeAt(raw.length-1)!==10) throw Error('Missing final newline');
  const rows=raw.trimEnd().split('\n');
  const ranks=new Map();
  let previous=null;
  for(const row of rows){
    const match=/^([0-9]+(?:,[0-9]+)*):([0-9]+)$/.exec(row);
    if(!match)throw Error('Malformed witness row '+row);
    const d=match[1].split(',').map(Number), v=Number(match[2]);
    if(d.length<1||d.length>7||d[0]<1||d[0]>18||
       d.some(x=>x<0||x>18||!Number.isInteger(x))||v<0||!Number.isInteger(v))
      throw Error('Bad digit/rank '+row);
    if(d.length<7){
      if(d.some((x,i)=>x!==d[d.length-1-i])||(d.length%2===1 && d[Math.floor(d.length/2)]%2))
        throw Error('Noncanonical short word');
    }
    const w=key(d);
    if(previous!==null && !(previous<w))throw Error('Unsorted/duplicate row');
    previous=w;
    ranks.set(w,v);
  }
  if(ranks.size!==72052)throw Error('Wrong witness size');
  const longPred=invertLongFactory(7), short=shortPredecessors(7);
  if(short.sourceCount!==10467)throw Error('Short universe incomplete');
  let longEdges=0,shortEdges=0,longNodes=0,shortNodes=0,maxRank=0;
  const hist={};
  for(const [w,r] of ranks){
    const d=digits(w);
    if(d.length===7)longNodes++;else shortNodes++;
    hist[r]=(hist[r]||0)+1;
    maxRank=Math.max(maxRank,r);
    const preds=new Set(short.index.get(w)||[]);
    if(d.length===7)for(const p of longPred(w))preds.add(p);
    let maxPrior=-1;
    for(const p of preds){
      const prior=ranks.get(p);
      if(prior===undefined)throw Error('Missing full inverse '+p+' -> '+w);
      if(!(prior<r))throw Error('Rank descent violated: '+p+' -> '+w);
      maxPrior=Math.max(maxPrior,prior);
      if(p.length===7){
        if(!possibleLongForward(p).has(w))throw Error('Bad long inverse');
        longEdges++;
      }else{
        if(exactShortForward(p)!==w)throw Error('Bad short inverse');
        shortEdges++;
      }
    }
    if(r!==maxPrior+1)throw Error('Incorrect rank recurrence');
  }
  const byPrefix={};
  for(const prefix of ['5523','5524']){
    const init=initialWords(prefix,7);
    if(init.longer.size!==1000||init.shorter.size!==0)throw Error('Bad target initials');
    let maxInit=0;
    for(const w of init.all){
      if(!ranks.has(w))throw Error('Missing initial row');
      maxInit=Math.max(maxInit,ranks.get(w));
    }
    if(maxInit!==6)throw Error('Unexpected initial rank');
    byPrefix[prefix]={initial_rows:init.all.size,max_rank:maxInit,method_bound:maxInit+1};
  }
  if(longNodes!==72044||shortNodes!==8||longEdges!==98227||
     shortEdges!==8||maxRank!==6)throw Error('Wrong graph totals');
  return {status:'PASS_FINITE_NOT_LEAN',rows:ranks.size,longNodes,shortNodes,
          longEdges,shortEdges,totalEdges:longEdges+shortEdges,
          rankHistogram:hist,maxRank,byPrefix};
}

if(typeof require!=='undefined' && require.main===module){
  const fs=require('node:fs'), path=require('node:path'),crypto=require('node:crypto');
  const raw=fs.readFileSync(process.argv[2]||path.join(__dirname,'ranked_rows.tsv'),'utf8');
  const got=crypto.createHash('sha256').update(raw,'utf8').digest('hex');
  if(got!=='21786466cfa8796c72d7623c50c8e413b721c88e8cbdebc9bee124441e22a1ec')
    throw Error('SHA-256 mismatch: '+got);
  const result=checkWitness(raw,require('./verify_union.js'));
  console.log(JSON.stringify({...result,sha256:got},null,2));
}
if(typeof module!=='undefined'&&module.exports)module.exports={checkWitness};
