"""GitHub Actions transport for the kit's explicit atomic tag/delete operations.

Content review and build checks were waived by the repository owner.
This adapter preserves exact SHA leases, ancestry and excluded branch guards.
"""
import json
import os
import subprocess
import sys

plan = json.load(open(sys.argv[1], encoding='utf-8'))
def git(*args):
    return subprocess.check_output(['git', *args], stderr=subprocess.STDOUT).decode()
def refs():
    result = {}
    for line in git('ls-remote', 'origin').splitlines():
        sha, name = line.split('\t', 1)
        if name.startswith(('refs/heads/', 'refs/tags/')) and not name.endswith('^{}'):
            result[name] = sha
    return result
def require(ok, message):
    if not ok:
        raise RuntimeError(message)

main = 'refs/heads/main'
commit = os.environ['GITHUB_SHA']
expected = dict(plan['remote_branch_tags'])
expected[main] = commit
retire = plan['retirement_candidates']
tags = plan['preservation_tags']
excluded = plan['excluded_heads']
current = refs()
if all(ref not in current for ref in retire) and all(current.get(tags[ref]) == sha for ref, sha in retire.items()):
    require(current.get(main) == commit, 'Main changed; stop.')
    require(all(current.get(ref) == sha for ref, sha in excluded.items()), 'Excluded branch changed.')
    print('Retirement already completed for this exact migration.')
    sys.exit(0)
for ref, sha in retire.items():
    require(ref != main and ref not in excluded, 'Protected branch in retirement list.')
    require(current.get(ref) == sha, 'Branch head changed: '+ref)
    git('merge-base', '--is-ancestor', sha, commit)
existing_tags = {tag: current[tag] for tag in tags.values() if tag in current}
require(all(existing_tags.get(tags[ref], sha) == sha for ref, sha in retire.items()), 'Conflicting preservation tag.')
expected.update(existing_tags)
require(current == expected, 'Remote refs changed outside this migration; stop.')
missing = [f'{sha}:{tags[ref]}' for ref, sha in retire.items() if tags[ref] not in current]
if missing:
    print(git('push', '--atomic', '--porcelain', 'origin', *missing))
current = refs()
expected.update({tags[ref]: sha for ref, sha in retire.items()})
require(current == expected, 'Preservation tags or remote refs differ; no deletion.')
args = ['push', '--atomic', '--porcelain']
args += [f'--force-with-lease={ref}:{sha}' for ref, sha in retire.items()]
args += ['origin'] + [':'+ref for ref in retire]
print(git(*args))
after = refs()
require(after == {ref: sha for ref, sha in expected.items() if ref not in retire}, 'Unexpected final refs.')
heads = {ref: sha for ref, sha in after.items() if ref.startswith('refs/heads/')}
require(set(heads) == set(excluded) | {main}, 'Unexpected remaining branches.')
print(json.dumps({'published_commit': commit, 'before': len(retire)+len(excluded)+1,
                  'after': len(heads), 'remaining_heads': heads,
                  'preserved_tags': len(tags), 'review_and_build_checks': 'WAIVED_BY_OWNER'}, indent=2))
