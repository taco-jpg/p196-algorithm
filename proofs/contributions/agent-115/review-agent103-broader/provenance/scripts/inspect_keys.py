import gzip, json, sys
d = json.loads(gzip.decompress(open(sys.argv[1],'rb').read()))
print('top keys', [k for k in d if k!='jobs'])
for k in d:
    if k!='jobs': print(k, repr(d[k])[:300])
j = d['jobs'][16]
print('job keys', list(j.keys()))
for k,v in j.items():
    print(k, type(v).__name__, (len(v) if hasattr(v,'__len__') else ''), repr(v)[:200])
