"""Independent verification helpers; no mathematical proof authorship.

Derived from the preserved successful spectral audit infrastructure. The public
namespace is Agent14.Carryfree, and literal axiom parsing permits apostrophes in
declaration names. Wrapped axiom arrays remain supported.
"""
from datetime import datetime, timezone
import hashlib
import json
import re

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def masked_source(text):
    """Mask strings and nested comments for lexical source checks."""
    result = []
    index = 0
    depth = 0
    quoted = False
    while index < len(text):
        pair = text[index:index + 2]
        char = text[index]
        if depth:
            if pair == "/-":
                depth += 1
                result.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            if char == "\\":
                result.extend("  ")
                index += 2
            else:
                quoted = char != '"'
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            result.extend("  ")
            index += 2
        elif pair == "--":
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            result.extend(" " * (end - index))
            index = end
        elif char == '"':
            quoted = True
            result.append(" ")
            index += 1
        else:
            result.append(char)
            index += 1
    if depth or quoted:
        raise ValueError("Unterminated source comment or string")
    return "".join(result)


def declared_public_names(module, code):
    """Enumerate explicit public declarations in the inspected new namespace."""
    namespaces = re.findall(r"^\s*namespace\s+(\S+)\s*$", code, re.M)
    if namespaces != ["Agent14.Carryfree"]:
        raise ValueError("Unexpected namespace organization in " + module)
    stripped = re.sub(r"@\[[^\]]*\]", "", code)
    pattern = re.compile(
        r"^\s*((?:(?:private|protected|noncomputable|partial|unsafe)\s+)*)"
        r"(theorem|lemma|def|abbrev|opaque|structure|inductive)\s+([A-Za-z_][\w']*)",
        re.M,
    )
    names = []
    for modifiers, kind, name in pattern.findall(stripped):
        if "private" not in modifiers.split():
            names.append({"name": "Agent14.Carryfree." + name,
                          "source_kind": kind, "module": module})
    if not names or len({record["name"] for record in names}) != len(names):
        raise ValueError("Missing or duplicate public declarations in " + module)
    return names


def axiom_list(text):
    if not text.startswith("[") or not text.endswith("]"):
        raise ValueError("Malformed axiom output: " + text)
    return [part.strip() for part in text[1:-1].split(",") if part.strip()]


def parse_safe_audit(audit_log):
    """Read Lean's pretty-printed axiom arrays, including wrapped lines."""
    pattern = re.compile(r"^SAFE_CONSTANT (\S+) (\S+) (\S+) : (\[[^\]]*\])$", re.M)
    constants = [{"module": mod, "kind": kind, "name": name, "axioms": axiom_list(axs)}
                 for mod, kind, name, axs in pattern.findall(audit_log)]
    summary_pattern = re.compile(r"^FULL_SAFE_AUDIT safe=(\d+) theorem=(\d+) definition=(\d+) opaque=(\d+) other=(\d+) unsafe=(\d+) partial=(\d+) union=(\[[^\]]*\])$", re.M)
    summaries = summary_pattern.findall(audit_log)
    if len(summaries) != 1 or int(summaries[0][0]) != len(constants) or not constants:
        raise ValueError("Safe audit output is absent or incomplete")
    if len({rec["name"] for rec in constants}) != len(constants):
        raise ValueError("Duplicate audited constants")
    keys = ["safe", "theorem", "definition", "opaque", "other", "unsafe", "partial"]
    summary = dict(zip(keys, map(int, summaries[0][:7])))
    summary["axiom_union"] = axiom_list(summaries[0][7])
    unsafe = re.findall(r"^INVENTORY_UNSAFE (\S+) (\S+) (\S+)$", audit_log, re.M)
    partial = re.findall(r"^INVENTORY_PARTIAL (\S+) (\S+) (\S+)$", audit_log, re.M)
    if len(unsafe) != summary["unsafe"] or len(partial) != summary["partial"]:
        raise ValueError("Unsafe or partial inventory count mismatch")
    for kind in ["theorem", "definition", "opaque"]:
        if sum(rec["kind"] == kind for rec in constants) != summary[kind]:
            raise ValueError("Safe audit category count mismatch")
    if sum(rec["kind"] not in {"theorem", "definition", "opaque"} for rec in constants) != summary["other"]:
        raise ValueError("Other safe declaration count mismatch")
    observed_union = {axiom for rec in constants for axiom in rec["axioms"]}
    if observed_union - ALLOWED or observed_union != set(summary["axiom_union"]):
        raise ValueError("Disallowed or inconsistent safe axiom union")
    return constants, summary, unsafe, partial


def parse_public_axioms(public_log, public_names):
    """Require one literal #print axioms result for every explicit public name."""
    records = {}
    pattern = re.compile(r"^'(.+)' (?:does not depend on any axioms|depends on axioms: (\[[^\]]*\]))$", re.M)
    for match in pattern.finditer(public_log):
        name, axioms = match.groups()
        if name in records:
            raise ValueError("Duplicate public axiom report")
        records[name] = axiom_list(axioms) if axioms else []
    if set(records) != set(public_names):
        raise ValueError("Public #print axioms reports do not cover the complete explicit declaration list")
    if any(set(axioms) - ALLOWED for axioms in records.values()):
        raise ValueError("Disallowed public theorem or definition axiom")
    return records


def safe_audit_source(order, roots):
    return ("\n".join("import " + name for name in roots) + "\nimport Lean\n"
            "open Lean Elab Command\n"
            "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
            "run_cmd do\n  let env ← getEnv\n  let selected : List String := "
            + json.dumps(order) + "\n" + r'''
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut safeCount := 0
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut opaqueCount := 0
  let mut otherCount := 0
  let mut unsafeCount := 0
  let mut partialCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        let kind : String := match info with
          | .axiomInfo _ => "axiom"
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
          | .quotInfo _ => "quotient"
        if info.isUnsafe then
          unsafeCount := unsafeCount + 1
          logInfo m!"INVENTORY_UNSAFE {mod} {kind} {name}"
        else if info.isPartial then
          partialCount := partialCount + 1
          logInfo m!"INVENTORY_PARTIAL {mod} {kind} {name}"
        else
          if kind == "axiom" then
            throwError m!"CUSTOM_SAFE_AXIOM {mod} {name}"
          safeCount := safeCount + 1
          if kind == "theorem" then theoremCount := theoremCount + 1
          else if kind == "definition" then definitionCount := definitionCount + 1
          else if kind == "opaque" then opaqueCount := opaqueCount + 1
          else otherCount := otherCount + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {kind} {name} : {axl}"
          logInfo m!"SAFE_CONSTANT {mod} {kind} {name} : {axl}"
  logInfo m!"FULL_SAFE_AUDIT safe={safeCount} theorem={theoremCount} definition={definitionCount} opaque={opaqueCount} other={otherCount} unsafe={unsafeCount} partial={partialCount} union={union}"
''')


