import json, datetime

# Append one NOTE record to r6.jsonl (status NOTE: ignored by done_tasks, which only reads COMPLETE/EMPTY/TOO_BIG rows).
rows = [json.loads(l) for l in open('r6.jsonl')]
tasks = [{'T': r['T'], 'clock': r['clock'], 'status': r['status'], 'streams': r['streams']}
         for r in rows if r['T'] in (25, 26, 27, 28)]
assert len(tasks) == 30, len(tasks)
note = {
    'status': 'NOTE',
    'kind': 'stream_list_T25_28',
    'ended': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'tasks': tasks,
    'all_streams_empty': all(not t['streams'] for t in tasks),
    'T24_0001_conclusion': (
        'COMPUTED (9-wire criterion, ROT=1, full reachable set of T=24 clock 0001). The only NEW STREAM reported is '
        '101101010010101101010010, i.e. the period-12 stream 101101010010 twice, first at height 53. '
        'No period-8 stream was reported. This is a statement about this (T, clock) and this 9-wire check only; '
        'the claim for any width was not computed.'),
}
with open('r6.jsonl', 'a') as f:
    f.write(json.dumps(note, ensure_ascii=False) + '\n')
print('appended; streams empty for all 30:', note['all_streams_empty'])
