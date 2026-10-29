// Independent physical decimal witness for the W30 arbitrary-clock safety gap.
// Node >= 18: node check_w30_one_step.mjs
import assert from 'node:assert/strict';

const rev = s => [...s].reverse().join('');
function sumDecimal(a, b) { // grade-school decimal addition; independent of BigInt
  let i = a.length - 1, j = b.length - 1, c = 0, out = '';
  while (i >= 0 || j >= 0 || c) {
    const z = (i >= 0 ? a.charCodeAt(i--) - 48 : 0) +
              (j >= 0 ? b.charCodeAt(j--) - 48 : 0) + c;
    out = String(z % 10) + out;
    c = Math.floor(z / 10);
  }
  return out.replace(/^0+(?=\d)/, '');
}
function pairword(s) { // least-significant digit first
  return [...s].reverse().map((x, i) => Number(x) + Number(s[i]));
}
function run(k) {
  const n = '1' + '0'.repeat(5 * k) + '3' + '78876'.repeat(k) + '0';
  const expected = '1' + '67887'.repeat(k) + '6' + '78876'.repeat(k) + '1';
  const normal = sumDecimal(n, rev(n));
  const big = (BigInt(n) + BigInt(rev(n))).toString();
  assert.equal(normal, expected, 'schoolbook, k=' + k);
  assert.equal(big, expected, 'BigInt, k=' + k);
  assert.equal(expected, rev(expected), 'palindrome, k=' + k);
  assert.notEqual(n, rev(n), 'initial nonpalindrome, k=' + k);
  assert.equal(normal.length, n.length, 'overflow gamma=0, k=' + k);
  const P = pairword(n);
  assert.equal(P.length, 10*k+3);
  assert.equal(P[0],1); assert.equal(P[P.length-1],1);
  const row=[6,7,8,8,7];
  for(let j=0;j<10*k+1;j++) assert.equal(P[j+1], row[j%5], 'row at k=' + k + ', j=' + j);
}
for(let k=1;k<=100;k++) run(k);
for(const k of [300,1000]) run(k);
console.log('PASS: 102 canonical decimal witnesses; independent BigInt and schoolbook sums; gamma=0; exact W30 row; one-step palindrome.');
