#!/usr/bin/env python3
"""verify_repo.py - stdlib-only repository hygiene checks.

Runs from any cwd (repo root is derived from __file__).
Prints ASCII-only PASS/FAIL/SKIP lines and exits 1 when any check FAILs.
"""
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_REL = "scripts/verify_repo.py"

TEXT_EXTS = {".md", ".sh", ".py", ".yml", ".yaml", ".snippet", ".mdc",
             ".gitattributes", ".gitignore"}
TEXT_NAMES = {"VERSION", "LICENSE", ".gitattributes", ".gitignore"}

RESULTS = []  # (status, check, message)


def report(status, check, msg):
    RESULTS.append((status, check, msg))
    print("[%s] (%s) %s" % (status, check, msg))


def collect_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)


def is_text(rel):
    base = os.path.basename(rel)
    ext = os.path.splitext(base)[1].lower()
    return base in TEXT_NAMES or ext in TEXT_EXTS


def is_ps1(rel):
    return rel.lower().endswith(".ps1")


def read_bytes(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return fh.read()


def read_text(rel):
    return read_bytes(rel).decode("utf-8", errors="replace")


# ---------------------------------------------------------------- (a) BOM
def check_bom(files):
    bad = 0
    checked = 0
    for rel in files:
        if not is_text(rel):
            continue
        checked += 1
        if read_bytes(rel).startswith(b"\xef\xbb\xbf"):
            bad += 1
            report("FAIL", "a", "BOM present: %s" % rel)
    if not bad:
        report("PASS", "a", "no BOM in %d text files" % checked)
    return bad


# ---------------------------------------------------------------- (b) EOL
def check_eol(files):
    bad = 0
    checked = 0
    for rel in files:
        if not (is_text(rel) or is_ps1(rel)):
            continue
        checked += 1
        data = read_bytes(rel)
        crlf = data.count(b"\r\n")
        cr = data.count(b"\r")
        lf = data.count(b"\n")
        if is_ps1(rel):
            pure_lf = (cr == 0)
            pure_crlf = (crlf == lf and cr == crlf and lf > 0)
            if not (pure_lf or pure_crlf):
                bad += 1
                report("FAIL", "b", "mixed EOL in %s (crlf=%d lone_cr=%d lone_lf=%d)"
                       % (rel, crlf, cr - crlf, lf - crlf))
        else:
            if cr != 0:
                bad += 1
                report("FAIL", "b", "CR found in %s (expected pure LF; crlf=%d lone_cr=%d)"
                       % (rel, crlf, cr - crlf))
    if not bad:
        report("PASS", "b", "EOL policy OK for %d files" % checked)
    return bad


# ---------------------------------------------------------------- (c) ASCII
def check_ps1_ascii():
    rel = "scripts/install.ps1"
    if not os.path.isfile(os.path.join(ROOT, rel)):
        report("SKIP", "c", "%s not found" % rel)
        return 0
    data = read_bytes(rel)
    offenders = [i for i, b in enumerate(data) if b > 0x7F]
    if offenders:
        line = data[:offenders[0]].count(b"\n") + 1
        report("FAIL", "c", "%s is not 7-bit ASCII (%d non-ASCII bytes, first at line %d)"
               % (rel, len(offenders), line))
        return 1
    report("PASS", "c", "%s is 7-bit ASCII" % rel)
    return 0


# ---------------------------------------------------------------- (d) forbidden
def forbidden_patterns():
    # Regexes are assembled from string pieces so this file never matches itself.
    pats = [
        ("machine-path-win-users", r"C:\\Us" + r"ers\\"),
        ("machine-path-mac-users", "/Us" + "ers/"),
        ("machine-path-home", r"(?<!~)/ho" + r"me/[a-z]+/"),
        ("owner-name", "Zi" + "zo"),
        ("project-drive", r"D:\\S" + "MS"),
        ("owner-codename", "PHOE" + "NIX"),
        ("brain-id", "115a5" + "a36"),
        ("brain-path", "antigra" + r"vity[\\/]brain"),
        ("secret-openai", r"(?<![A-Za-z0-9])sk-[A-Za-z0-9]{10,}"),
        ("secret-github", r"ghp_[A-Za-z0-9]{20,}"),
        ("secret-bearer", r"Bearer\s+[A-Za-z0-9._-]{16,}"),
        ("secret-bot-token", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
        ("secret-api-key", r"api[_-]?key\s*[:=]\s*\S{8,}"),
        ("leak-4096", "40" + "96"),
        ("leak-24kb", "24" + "KB"),
        ("leak-frida", "fri" + "da"),
        ("leak-lsposed", "LSPo" + "sed"),
        ("leak-floodwait", "Flood" + "Wait"),
        ("leak-authkey", "Auth" + "Key"),
        ("leak-session", r"\.sess" + r"ion\b"),
        ("leak-telegram", "Tele" + "gram"),
    ]
    compiled = []
    for name, pat in pats:
        flags = re.I if name == "secret-api-key" else 0
        compiled.append((name, re.compile(pat, flags)))
    return compiled


SIBLING_SKILLS = [
    "00-reverse-engineer", "00-bolla-constitution", "00-architect-sre",
    "01-micro-tasker", "02-planning-system", "00-evidence-inspector",
    "egm-review", "everything-search",
]
SIBLING_WHITELIST = ("SKILL.md", "workflows/00-lock360-zero-gaps.md")


def check_forbidden(files):
    bad = 0
    pats = forbidden_patterns()
    sibling_re = re.compile("|".join(re.escape(s) for s in SIBLING_SKILLS))
    scanned = 0
    for rel in files:
        if rel == SELF_REL:
            continue
        scanned += 1
        text = read_text(rel)
        lines = text.split("\n")
        for lineno, line in enumerate(lines, 1):
            for name, rx in pats:
                if rx.search(line):
                    bad += 1
                    report("FAIL", "d", "%s:%d forbidden pattern [%s]" % (rel, lineno, name))
            if rel not in SIBLING_WHITELIST and sibling_re.search(line):
                bad += 1
                report("FAIL", "d", "%s:%d sibling skill name allowed only in SKILL.md / workflows/00-lock360-zero-gaps.md"
                       % (rel, lineno))
    if not bad:
        report("PASS", "d", "no forbidden patterns in %d files" % scanned)
    return bad


# ---------------------------------------------------------------- (e) links
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")


def check_links(files):
    bad = 0
    checked = 0
    for rel in files:
        if not rel.lower().endswith(".md"):
            continue
        base_dir = os.path.dirname(os.path.join(ROOT, rel))
        in_fence = False
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            clean = CODE_SPAN_RE.sub("", line)
            for m in LINK_RE.finditer(clean):
                target = m.group(1)
                low = target.lower()
                if low.startswith(("http://", "https://", "mailto:")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                target = urllib.parse.unquote(target)
                checked += 1
                resolved = os.path.normpath(os.path.join(base_dir, target))
                if not os.path.exists(resolved):
                    bad += 1
                    report("FAIL", "e", "%s:%d broken link -> %s" % (rel, lineno, m.group(1)))
    if not bad:
        report("PASS", "e", "%d relative markdown links resolve" % checked)
    return bad


# ---------------------------------------------------------------- (f) version
VERSION_RE = re.compile(r"\bv2\.\d+\b")


def check_version(files):
    vpath = os.path.join(ROOT, "VERSION")
    if not os.path.isfile(vpath):
        report("FAIL", "f", "VERSION file missing")
        return 1
    ver = read_text("VERSION").strip()
    if not VERSION_RE.fullmatch(ver):
        report("FAIL", "f", "VERSION content is not vMAJOR.MINOR: %r" % ver)
        return 1
    bad = 0
    hits = 0
    for rel in files:
        if not (is_text(rel) or is_ps1(rel)):
            continue
        if rel == "gist/04-CHANGELOG.md" or rel.startswith("archive/"):
            continue
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            for m in VERSION_RE.finditer(line):
                hits += 1
                if m.group(0) != ver:
                    bad += 1
                    report("FAIL", "f", "%s:%d version %s != VERSION %s"
                           % (rel, lineno, m.group(0), ver))
    if not bad:
        report("PASS", "f", "%d version mentions match VERSION=%s" % (hits, ver))
    return bad


# ---------------------------------------------------------------- (g) placeholders
def placeholder_patterns():
    return [
        ("arabic-placeholder", re.compile("<\u0636" + "\u0639_")),
        ("git-c-ellipsis", re.compile("git -C " + r"\.\.\.")),
        ("todo-line", re.compile(r"^\s*TO" + "DO:")),
    ]


def check_placeholders(files):
    bad = 0
    pats = placeholder_patterns()
    scanned = 0
    for rel in files:
        if not (is_text(rel) or is_ps1(rel)):
            continue
        scanned += 1
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            for name, rx in pats:
                if rx.search(line):
                    bad += 1
                    report("FAIL", "g", "%s:%d placeholder [%s]" % (rel, lineno, name))
    if not bad:
        report("PASS", "g", "no placeholders in %d files" % scanned)
    return bad


# ---------------------------------------------------------------- (h) bash -n
def find_bash():
    cands = []
    w = shutil.which("bash")
    if w:
        cands.append(w)
    cands.append(os.path.join("C:\\Program Files", "Git", "bin", "bash.exe"))
    for c in cands:
        if not os.path.isfile(c):
            continue
        try:
            p = subprocess.run([c, "-c", "exit 0"], cwd=ROOT,
                               capture_output=True, timeout=30)
        except Exception:
            continue
        if p.returncode == 0:
            return c
    return None


def check_bash_syntax():
    rel = "scripts/install.sh"
    if not os.path.isfile(os.path.join(ROOT, rel)):
        report("SKIP", "h", "%s not found" % rel)
        return 0
    bash = find_bash()
    if not bash:
        report("SKIP", "h", "no working bash found (PATH or Git for Windows); bash -n skipped")
        return 0
    try:
        p = subprocess.run([bash, "-n", rel], cwd=ROOT, capture_output=True,
                           text=True, timeout=60)
    except Exception as exc:
        report("FAIL", "h", "bash -n could not run: %s" % exc)
        return 1
    if p.returncode != 0:
        err = (p.stderr or p.stdout or "").strip().replace("\n", " | ")
        report("FAIL", "h", "bash -n %s failed (rc=%d): %s" % (rel, p.returncode, err))
        return 1
    report("PASS", "h", "bash -n %s OK (%s)" % (rel, bash))
    return 0


# ---------------------------------------------------------------- (i) workflows
def check_workflows(files):
    bad = 0
    checked = 0
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    for rel in files:
        if not rel.startswith(".github/workflows/"):
            continue
        if not rel.lower().endswith((".yml", ".yaml")):
            continue
        checked += 1
        text = read_text(rel)
        if "\t" in text:
            bad += 1
            report("FAIL", "i", "%s contains tab characters" % rel)
        if not re.search(r"^on:", text, re.M):
            bad += 1
            report("FAIL", "i", "%s missing top-level 'on:'" % rel)
        if not re.search(r"^jobs:", text, re.M):
            bad += 1
            report("FAIL", "i", "%s missing top-level 'jobs:'" % rel)
        if yaml is not None:
            try:
                doc = yaml.safe_load(text)
                if not isinstance(doc, dict):
                    bad += 1
                    report("FAIL", "i", "%s does not parse to a mapping" % rel)
            except Exception as exc:
                bad += 1
                report("FAIL", "i", "%s YAML parse error: %s" % (rel, str(exc).replace("\n", " ")))
    if checked == 0:
        report("SKIP", "i", "no workflow files under .github/workflows")
        return 0
    if not bad:
        extra = "PyYAML full parse" if yaml is not None else "PyYAML unavailable, structural checks only"
        report("PASS", "i", "%d workflow files OK (%s)" % (checked, extra))
    return bad


# ---------------------------------------------------------------- (j) tables
def check_md_tables(files):
    bad = 0
    checked = 0
    for rel in files:
        if not rel.lower().endswith(".md"):
            continue
        checked += 1
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            if line.lstrip().startswith("|"):
                bad += 1
                report("FAIL", "j", "%s:%d markdown table row" % (rel, lineno))
    if not bad:
        report("PASS", "j", "0 markdown table rows in %d .md files" % checked)
    return bad


# ---------------------------------------------------------------- main
def main():
    print("verify_repo: root=%s" % ROOT)
    files = collect_files()
    print("verify_repo: %d files (excluding .git)" % len(files))
    fails = 0
    fails += check_bom(files)
    fails += check_eol(files)
    fails += check_ps1_ascii()
    fails += check_forbidden(files)
    fails += check_links(files)
    fails += check_version(files)
    fails += check_placeholders(files)
    fails += check_bash_syntax()
    fails += check_workflows(files)
    fails += check_md_tables(files)
    n_pass = sum(1 for s, _, _ in RESULTS if s == "PASS")
    n_fail = sum(1 for s, _, _ in RESULTS if s == "FAIL")
    n_skip = sum(1 for s, _, _ in RESULTS if s == "SKIP")
    print("SUMMARY: PASS=%d FAIL=%d SKIP=%d" % (n_pass, n_fail, n_skip))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
