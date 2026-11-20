#!/usr/bin/env python3
"""Check Zstack skills: frontmatter, unique names, and cross-file references.

Skills are installed side by side in one skills directory, so a reference
`../<skill>/<path>` is resolved against the skill named <skill>, wherever it
lives in this repository.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


skills = {}
for md in sorted(ROOT.glob("*/**/skills/*/SKILL.md")):
    d = md.parent
    fm = frontmatter(md)
    rel = md.relative_to(ROOT)
    if fm is None:
        errors.append(f"{rel}: missing frontmatter")
        continue
    name = fm.get("name", "")
    if name != d.name:
        errors.append(f"{rel}: name '{name}' does not match directory '{d.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"{rel}: name '{name}' is not lowercase-hyphen")
    if not fm.get("description"):
        errors.append(f"{rel}: empty description")
    if name in skills:
        errors.append(f"{rel}: duplicate name, also {skills[name].relative_to(ROOT)}")
    skills[name] = d
    if fm.get("disable-model-invocation") == "true":
        oy = d / "agents" / "openai.yaml"
        if not oy.exists() or "allow_implicit_invocation: false" not in oy.read_text():
            errors.append(f"{rel}: manual-only skill lacks agents/openai.yaml "
                          "with allow_implicit_invocation: false")

ref_re = re.compile(r"`((?:\.\./)?[A-Za-z0-9_./<>-]+\.(?:md|yaml))`")
for name, d in skills.items():
    for md in d.rglob("*.md"):
        for ref in ref_re.findall(md.read_text(encoding="utf-8")):
            if "<" in ref:
                continue
            if ref.startswith("../"):
                parts = ref[3:].split("/", 1)
                target = skills.get(parts[0])
                path = target / parts[1] if target and len(parts) == 2 else None
            elif "/" in ref and ref.split("/", 1)[0] in ("playbooks", "principles", "references", "agents"):
                path = d / ref
            else:
                continue  # project file such as docs/devel/foo.rst
            if path is None or not path.exists():
                errors.append(f"{md.relative_to(ROOT)}: broken reference {ref}")

# Skill names mentioned in backticks must exist when they look like ours.
mention_re = re.compile(r"`((?:z|qemu|linux)-[a-z-]+)`")
for name, d in skills.items():
    for md in d.rglob("*.md"):
        for m in mention_re.findall(md.read_text(encoding="utf-8")):
            if m not in skills and m not in ("linux-kernel-development", "qemu-codebase"):
                errors.append(f"{md.relative_to(ROOT)}: unknown skill `{m}`")

for e in errors:
    print("ERROR", e)
print(f"{len(skills)} skills checked, {len(errors)} errors")
sys.exit(1 if errors else 0)
