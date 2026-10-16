from pathlib import Path, PurePosixPath
import hashlib, io, json, os, stat, tarfile

root = Path('/dev/shm/p196-agent17-pr147-semantics-0abe')
archive = root.with_suffix('.tar.xz')
report = root.parent / (root.name + '-archive-verification.json')

if archive.exists() or report.exists():
    raise SystemExit('Refusing to overwrite an existing archive or verification report')
if not stat.S_ISDIR(root.lstat().st_mode):
    raise SystemExit('Source root is not a regular directory')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshot():
    entries = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current = Path(current)
        for name in directories:
            child = current / name
            if not stat.S_ISDIR(child.lstat().st_mode):
                raise ValueError('Non-directory entry among source directories: ' + str(child))
        for name in files:
            child = current / name
            st = child.lstat()
            if not stat.S_ISREG(st.st_mode):
                raise ValueError('Nonregular source entry: ' + str(child))
            relative = child.relative_to(root).as_posix()
            member_name = root.name + '/' + relative
            if member_name in entries:
                raise ValueError('Duplicate source member name: ' + member_name)
            data = child.read_bytes()
            if len(data) != st.st_size:
                raise ValueError('Source file size changed during snapshot: ' + relative)
            entries[member_name] = {'bytes': len(data), 'sha256': digest(data)}
    return dict(sorted(entries.items()))

before = snapshot()
manifest_file = root / 'REVIEW-FILES.json'
old_manifest = json.loads(manifest_file.read_text())
expected_old_names = {root.name + '/' + name for name in old_manifest}
actual_without_manifest = set(before) - {root.name + '/REVIEW-FILES.json'}
if expected_old_names != actual_without_manifest:
    raise ValueError('Existing REVIEW-FILES.json member set mismatch')
for relative, expected in old_manifest.items():
    if before[root.name + '/' + relative] != expected:
        raise ValueError('Existing REVIEW-FILES.json byte identity mismatch: ' + relative)

with archive.open('xb') as archive_output:
    with tarfile.open(fileobj=archive_output, mode='w:xz', preset=6, format=tarfile.PAX_FORMAT) as package:
        for member_name, expected in before.items():
            relative = member_name[len(root.name) + 1:]
            source = root / relative
            data = source.read_bytes()
            if {'bytes': len(data), 'sha256': digest(data)} != expected:
                raise ValueError('Source changed before archival: ' + relative)
            info = tarfile.TarInfo(member_name)
            info.size = len(data)
            info.mode = stat.S_IMODE(source.stat().st_mode)
            info.mtime = int(source.stat().st_mtime)
            info.uid = 0
            info.gid = 0
            info.uname = ''
            info.gname = ''
            package.addfile(info, io.BytesIO(data))

seen = {}
with tarfile.open(archive, mode='r:xz') as package:
    for member in package:
        name = member.name
        parsed = PurePosixPath(name)
        if not member.isreg():
            raise ValueError('Nonregular archive member: ' + name)
        if name in seen:
            raise ValueError('Duplicate archive member: ' + name)
        if parsed.is_absolute() or '..' in parsed.parts or parsed.as_posix() != name:
            raise ValueError('Unsafe or noncanonical member name: ' + name)
        if name not in before:
            raise ValueError('Unexpected archive member: ' + name)
        content = package.extractfile(member)
        if content is None:
            raise ValueError('Missing regular-member data: ' + name)
        data = content.read()
        actual = {'bytes': len(data), 'sha256': digest(data)}
        if member.size != actual['bytes'] or actual != before[name]:
            raise ValueError('Archive/source byte identity mismatch: ' + name)
        seen[name] = actual
if set(seen) != set(before):
    raise ValueError('Missing archive members')
after = snapshot()
if after != before:
    raise ValueError('Original source bytes changed during packaging')

archive_bytes = archive.read_bytes()
result = {
    'status': 'PASS',
    'operation': 'Lossless preservation packaging only; no Lean or mathematical review executed',
    'source_directory': str(root),
    'archive': {'path': str(archive), 'bytes': len(archive_bytes), 'sha256': digest(archive_bytes), 'format': 'tar.xz'},
    'member_count': len(seen),
    'source_bytes': sum(record['bytes'] for record in before.values()),
    'exact_member_names_sizes_and_sha256_match': True,
    'duplicate_members': 0,
    'nonregular_members': 0,
    'source_entries_regular_files_only': True,
    'original_source_bytes_unchanged': True,
    'existing_review_manifest_verified': True,
    'includes_review_files_manifest': root.name + '/REVIEW-FILES.json' in seen,
    'archive_contains_directory_records': False,
    'members': seen,
}
with report.open('x') as output:
    output.write(json.dumps(result, indent=2) + '\n')
report_bytes = report.read_bytes()
print(json.dumps({
    'status': result['status'],
    'archive': result['archive'],
    'member_count': result['member_count'],
    'source_bytes': result['source_bytes'],
    'verification_report': {'path': str(report), 'bytes': len(report_bytes), 'sha256': digest(report_bytes)},
    'original_review': before[root.name + '/REVIEW.md'],
}, indent=2))
