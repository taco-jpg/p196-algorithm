from pathlib import Path
import re,csv,collections,json,sys
D=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
rows=[];hist=collections.Counter()
for u in range(30):
 f=D/f'U{u}_full.log'
 if not f.exists() or not f.stat().st_size:continue
 lines=f.read_text().strip().splitlines()
 if len(lines)!=2:raise AssertionError((u,lines))
 z=re.search(r'minLen=(\d+) maxLen=(\d+) clockBad=(\d+) provedMismatch=(\d+) UNKNOWN=(\d+)',lines[0]);assert z,(u,lines[0])
 mn,mx,bad,proven,unknown=map(int,z.groups())
 h={int(x):int(y) for x,y in re.findall(r'(\d+):(\d+)',lines[1])}
 assert sum(h.values())==proven and proven+unknown==19**5 and bad==0
 hist.update(h)
 rows.append(dict(idx=u,U=[9,2*(u//3),18-2*(u//3)][u%3:]+[9,2*(u//3),18-2*(u//3)][:u%3],confirmed=proven,unknown=unknown,minPrefix=mn,maxPrefix=mx,firstMin=min(h),firstMax=max(h),hist=h))
print('COMPLETE U',len(rows),'successfully excluded',sum(r['confirmed'] for r in rows),'unknown',sum(r['unknown'] for r in rows))
for r in rows:print('U%02d %-12s minPrefix=%3d firstMismatch=[%3d,%3d] confirmed=%d UNKNOWN=%d'%(r['idx'],str(r['U']),r['minPrefix'],r['firstMin'],r['firstMax'],r['confirmed'],r['unknown']))
print('AGGREGATE histogram',sorted(hist.items()))
(D/'summary.json').write_text(json.dumps({'rows':rows,'hist':dict(sorted(hist.items()))},indent=2))
