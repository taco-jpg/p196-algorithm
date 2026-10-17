from pathlib import Path, PurePosixPath
import base64, gzip, hashlib, io, json, tarfile

ANCHORS = json.loads(r"""{
  "base64": {
    "git_blob_sha1": "58c19d1545db5ea21139ac2a4526ac20dd1e1bf2",
    "name": "agent17-pr175-pr176.tar.gz.b64",
    "sha256": "200c815ce9d3a12d71f8363858b737966d266e1b14228841a23d6895f33f516a",
    "size": 8054704
  },
  "gzip": {
    "git_blob_sha1": "265afa64952df26bcb9a33aa61d7ee7dd05eb411",
    "name": "agent17-pr175-pr176.tar.gz",
    "sha256": "9416d672ed55836491df6ecb29aaee609dc20ba2a4e538a973b441ac79e4978b",
    "size": 6041027
  },
  "internal_manifest": {
    "git_blob_sha1": "e69872f8f569867129f727ad65f52a6a96c192b0",
    "sha256": "97d51764714bdb431c1e523dfeff09d552c8f9cfbb52a51c4e34814ae1f108b9",
    "size": 311935
  },
  "member_count": 926,
  "parts": [
    {
      "git_blob_sha1": "1f9981e13bf3ecf241a6a5a95fb15a83dc997f0f",
      "name": "agent17-pr175-pr176.part001.b64",
      "sha256": "5c1de1279bd7ccc4a3aeacb6fca9ca2eb2f2f3c3fe8562bcf9d85251e8edb620",
      "size": 700000
    },
    {
      "git_blob_sha1": "f827e78b595d3ae9e1014efed3a0051470f207dc",
      "name": "agent17-pr175-pr176.part002.b64",
      "sha256": "19bf3cfc45b88fa7901814d4ac4a7cf7914d055da689f1ae1c8083812fce9360",
      "size": 700000
    },
    {
      "git_blob_sha1": "bd6c2382e007ddfac85afd79cdf07eb6da0bfea7",
      "name": "agent17-pr175-pr176.part003.b64",
      "sha256": "0967e26b67e5a18e639197583079355723e0969180d7c2bdf722cec65a6ee273",
      "size": 700000
    },
    {
      "git_blob_sha1": "6c082634f8fe86a1a4b5a5d3bc2c11f01a5c460d",
      "name": "agent17-pr175-pr176.part004.b64",
      "sha256": "6a7a7a02e9094dbc44c40533e79272b4876de0bdd338fc842adae1ebdd97f4cc",
      "size": 700000
    },
    {
      "git_blob_sha1": "e9e316820895fe8f6b5398351317e3c88d19e9cf",
      "name": "agent17-pr175-pr176.part005.b64",
      "sha256": "12650e4ce40ec6c3cf17b61e6369537ee647bf69f7b4369dcc9f4155297e7eb8",
      "size": 700000
    },
    {
      "git_blob_sha1": "00fc89b6e8db6289200efe29c7e5c1c31f4b2624",
      "name": "agent17-pr175-pr176.part006.b64",
      "sha256": "8ab2452e00701e46a0d493ada7616ba548642dc17bbb1706653c15d33f71574f",
      "size": 700000
    },
    {
      "git_blob_sha1": "0d93b4d7d23767651df371c71ee1a2e44a566094",
      "name": "agent17-pr175-pr176.part007.b64",
      "sha256": "8d251560d2ef60623663e1da5d5c3066563c17279ad1180b5967688eab7438d5",
      "size": 700000
    },
    {
      "git_blob_sha1": "008bb5028e4b6f5713ad5488d76e576450ab6d4d",
      "name": "agent17-pr175-pr176.part008.b64",
      "sha256": "7ddbbc46b74deb4163117c7ebb4c2cf1bedf90804f5da667c8fa4cbecebbb657",
      "size": 700000
    },
    {
      "git_blob_sha1": "f41cef1b5d5c1a300b6c55cb5f98fb628d2b6622",
      "name": "agent17-pr175-pr176.part009.b64",
      "sha256": "3de6e780466ade001d02db92303e75f13fb590686db14ef05ce34a56d9070143",
      "size": 700000
    },
    {
      "git_blob_sha1": "c8a1970b63caed800301ac4842b4076169b290cb",
      "name": "agent17-pr175-pr176.part010.b64",
      "sha256": "db9dc0239bcdda7bf0b6e370cc7e5eeed201fbc87de6b85376186afb5706438e",
      "size": 700000
    },
    {
      "git_blob_sha1": "a2321e057242c0ebbc4dfd5a25e42af1ee1d99a1",
      "name": "agent17-pr175-pr176.part011.b64",
      "sha256": "0351f7c67455bbc6d8b080ebdce7f7f67fc13c782b2f9da728c3fd4a3f618bb2",
      "size": 700000
    },
    {
      "git_blob_sha1": "2a187fbb4edd604d072c0b2e6fd64cf58bc3d0cb",
      "name": "agent17-pr175-pr176.part012.b64",
      "sha256": "c65ef9024be59a0913bc1585212996449f25495a6b679219e6d35f494822ab89",
      "size": 354704
    }
  ],
  "tar": {
    "git_blob_sha1": "b44e57fcd5506bff1e27580d421968cb03aa5dd6",
    "name": "agent17-pr175-pr176.tar",
    "sha256": "8a171a190a823c2793ac0c688adc160d1b2888907840c4fc32cd9a0da9965243",
    "size": 44861440
  }
}
""")
DESTINATION = Path("restored-agent17-pr175-pr176")
MANIFEST = "metadata/INTERNAL_MANIFEST.json"

def identity(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()}

def require(condition, message):
    if not condition:
        raise SystemExit(message)

chunks = []
for part in ANCHORS["parts"]:
    chunk = Path(part["name"]).read_bytes()
    require(identity(chunk) == {k: part[k] for k in ("size", "sha256", "git_blob_sha1")}, "Part identity mismatch: " + part["name"])
    require(len(chunk) <= 700000, "Oversized part")
    chunks.append(chunk)
encoded = b"".join(chunks)
require(identity(encoded) == {k: ANCHORS["base64"][k] for k in ("size", "sha256", "git_blob_sha1")}, "Combined base64 identity mismatch")
compressed = base64.b64decode(encoded, validate=True)
require(base64.b64encode(compressed) == encoded, "Noncanonical base64")
require(identity(compressed) == {k: ANCHORS["gzip"][k] for k in ("size", "sha256", "git_blob_sha1")}, "Gzip identity mismatch")
require(compressed[:4] == b"\x1f\x8b\x08\x00" and compressed[4:8] == b"\0" * 4, "Unexpected gzip header")
raw = gzip.decompress(compressed)
require(identity(raw) == {k: ANCHORS["tar"][k] for k in ("size", "sha256", "git_blob_sha1")}, "Tar identity mismatch")

payloads = {}
with tarfile.open(fileobj=io.BytesIO(raw), mode="r:", encoding="utf-8") as archive:
    for member in archive.getmembers():
        name = member.name
        pieces = name.split("/")
        require(bool(name) and not name.startswith("/") and "\\" not in name and ":" not in name, "Unsafe member path")
        require(not any(ord(c) < 32 or ord(c) == 127 for c in name), "Control character in path")
        require(len(pieces) > 1 and pieces[0] in {"pr175", "pr176", "metadata"} and all(p not in {"", ".", ".."} for p in pieces), "Unsafe path components")
        require(PurePosixPath(name).as_posix() == name and name not in payloads, "Noncanonical or duplicate path")
        require(member.type == tarfile.REGTYPE and not member.linkname and not member.sparse, "Nonregular member")
        require(member.uid == member.gid == member.mtime == 0 and not member.uname and not member.gname, "Unexpected metadata")
        require(member.mode in {0o644, 0o755}, "Unsafe file mode")
        require(not (set(member.pax_headers) - {"path"}) and member.pax_headers.get("path", name) == name, "Unexpected PAX metadata")
        stream = archive.extractfile(member)
        require(stream is not None, "Missing member stream")
        content = stream.read()
        require(len(content) == member.size, "Incorrect member length")
        payloads[name] = (content, member.mode)
require(len(payloads) == ANCHORS["member_count"], "Wrong member count")
require(list(payloads) == sorted(payloads, key=lambda name: name.encode("utf-8")), "Wrong member ordering")
require(MANIFEST in payloads, "Missing internal manifest")
manifest_bytes = payloads[MANIFEST][0]
require(identity(manifest_bytes) == ANCHORS["internal_manifest"], "Internal manifest identity mismatch")
manifest = json.loads(manifest_bytes)
require((json.dumps(manifest, sort_keys=True, ensure_ascii=True, indent=2) + "\n").encode("ascii") == manifest_bytes, "Noncanonical manifest")
require(manifest.get("schema") == "agent17.delivery.internal-manifest.v1", "Unknown manifest schema")
rows = [{"path": name, "mode": mode, **identity(content)} for name, (content, mode) in payloads.items() if name != MANIFEST]
require(manifest.get("manifest_excludes_only") == [MANIFEST] and manifest.get("members") == rows and manifest.get("member_count_excluding_manifest") == len(rows), "Incomplete or mismatched internal manifest")

# Extraction starts only after the outer archive and every logical member pass.
require(not DESTINATION.exists() and not DESTINATION.is_symlink(), "Recovery directory already exists")
DESTINATION.mkdir(mode=0o700)
for name, (content, mode) in payloads.items():
    target = DESTINATION.joinpath(*name.split("/"))
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    require(not any(parent.is_symlink() for parent in target.parents), "Symlink in extraction path")
    with target.open("xb") as stream:
        stream.write(content)
    target.chmod(mode)
    require(target.read_bytes() == content, "Recovered content mismatch: " + name)
print(json.dumps({"status": "PASSED", "member_count": len(payloads), "manifest_rows": len(rows), "destination": str(DESTINATION), "author_scripts_executed": False}, sort_keys=True))
