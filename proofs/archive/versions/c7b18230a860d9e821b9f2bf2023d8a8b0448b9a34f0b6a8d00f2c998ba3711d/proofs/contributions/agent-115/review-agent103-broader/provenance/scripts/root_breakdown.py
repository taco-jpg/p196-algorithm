import gzip, json, sys
J = {j['id']: j for j in json.loads(gzip.decompress(open(sys.argv[1],'rb').read()))['jobs']}
for i in (16, 17):
    j = J[i]; w = j['component_weights']; r = j['weighted_sink_ranks']
    top = max(range(len(r)), key=lambda c: r[c])
    succ = {}
    for a, b in j['condensation_edges']: succ.setdefault(a, []).append(b)
    path = [top]
    while succ.get(path[-1]):
        path.append(max(succ[path[-1]], key=lambda c: r[c]))
        if r[path[-2]] != w[path[-2]] + r[path[-1]]: break
    print(i, 'ncomp', len(w), 'max rank', r[top], 'cyclic', j['cyclic_components'],
          'children', [(l['component'], l['child_job']) for l in j['children']],
          'critical path (comp,weight)', [(c, w[c]) for c in path], 'sum', sum(w[c] for c in path))
