#!/usr/bin/env node
/* Independent BigInt / textual-decimal replay, no Python imports or proof shortcuts.
   The complete record is checked, not merely accepted as input. FINITE only. */
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const filename = process.argv[2] || 'finite_evidence.json';
const raw = readFileSync(filename);
const j = JSON.parse(raw.toString('utf8'));
const r=3, p=1, u=1, v=7, L=2*r+7;
const q = Array.from({length:L},(_,i) =>
  [0,1,2*r+5,2*r+6].includes(i) ? p :
  [r+1,r+5].includes(i) ? u :
  [r+2,r+4].includes(i) ? u+v :
  i===r+3 ? 2*v : 0);
assert.deepEqual(q,j.initial_pair_word_low_to_high);
assert.equal(q.length,13);
const choices = [];
for(let i=0;i<Math.floor(L/2);i++) {
  const a=[];
  for(let lo=0;lo<=9;lo++) {
    const hi=q[i]-lo;
    if(hi>=0 && hi<=9 && (i!==0 || hi>0))a.push([lo,hi]);
  }
  choices.push(a);
}
assert.deepEqual(choices.map(x=>x.length),[1,2,1,1,2,9]);
const all=[];
function generate(i,pairs) {
  if(i===choices.length) {
    const d=Array(L).fill(0);
    for(let k=0;k<pairs.length;k++) {
      d[k]=pairs[k][0];
      d[L-1-k]=pairs[k][1];
    }
    d[Math.floor(L/2)]=q[Math.floor(L/2)]/2;
    assert.ok(d[L-1]>0);
    assert.ok(d.every((x,k)=>q[k]===x+d[L-1-k]));
    let n=0n;
    for(let k=0;k<L;k++)n += BigInt(d[k])*10n**BigInt(k);
    assert.equal(n.toString().length,L);
    all.push(n);
    return;
  }
  for(const pair of choices[i])generate(i+1,[...pairs,pair]);
}
generate(0,[]);
all.sort((a,b)=>a<b?-1:a>b?1:0);
assert.equal(all.length,36);
assert.deepEqual(all.map(x=>x.toString()),j.canonical_integer_seeds_as_decimal_strings);
const listDigest=createHash('sha256').update(all.map(x=>x.toString()).join('\n')+'\n').digest('hex');
assert.equal(listDigest,j.seed_list_sha256);
const direct=n=>n+BigInt(n.toString().split('').reverse().join(''));
const isPalindrome=n=> {const s=n.toString();return s===s.split('').reverse().join('')};
let shared=[];
for(const n0 of all){
  const seq=[n0];
  for(let t=1;t<=11;t++)seq.push(direct(seq.at(-1)));
  assert.ok(seq.slice(1,11).every(x=>!isPalindrome(x)));
  assert.ok(isPalindrome(seq[11]));
  if(shared.length===0)shared=seq;
  else assert.deepEqual(seq.slice(1),shared.slice(1));
}
assert.deepEqual(shared.map(x=>x.toString()), j.representative_orbit_times_0_to_11);
assert.equal(shared[11].toString(),'8819059559509188');
assert.equal(j.positive_time_first_palindrome,11);
assert.equal(j.all_canonical_integer_seeds_agree_after_one_step,true);
console.log(`INDEPENDENT NODE PASS: ${all.length} canonical seeds; 11 transitions; palindrome ${shared[11]}`);
console.log(`BYTE SHA256=${createHash('sha256').update(raw).digest('hex')}`);
