#!/usr/bin/env python3
"""verify_repo.py - stdlib-only repository hygiene checks.

Runs from any cwd (repo root is derived from __file__).
Prints ASCII-only PASS/FAIL/SKIP lines and exits 1 when any check FAILs.

Usage:
  python3 scripts/verify_repo.py                    run every check
  python3 scripts/verify_repo.py --update-manifest  rewrite MANIFEST.sha256, then run every check

MANIFEST.sha256 digests are computed over EOL-normalized bytes (CRLF -> LF) for
text files, including *.ps1 which git checks out as CRLF on Windows, so the
manifest verifies identically on Windows, Linux and macOS.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_REL = "scripts/verify_repo.py"
MANIFEST_REL = "MANIFEST.sha256"

TEXT_EXTS = {".md", ".sh", ".py", ".yml", ".yaml", ".snippet", ".mdc",
             ".json", ".svg", ".txt", ".gitattributes", ".gitignore"}
# Test fixtures intentionally contain tables, placeholders and old version strings
# (red-green mutations) - they are exempt from (f)(g)(j) only; (a)(b)(d) stay strict.
FIXTURES_PREFIX = "tests/fixtures/"


def is_fixture(rel):
    return rel.startswith(FIXTURES_PREFIX)
TEXT_NAMES = {"VERSION", "LICENSE", ".gitattributes", ".gitignore", MANIFEST_REL}

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


def is_pack_asset(rel):
    return (rel.startswith("skills-pack/skills/")
            or rel.startswith("skills-pack/workflows/")
            or rel.startswith("skills-pack/rules/"))


def is_pack_md(rel):
    return is_pack_asset(rel) or rel == "skills-pack/GEMINI.template.md"


# ---------------------------------------------------------------- (d) forbidden
SAFE_APIKEY_ENV_RE = re.compile(r"api[_-]?key\s*[:=]\s*(?:process\.env\.|os\.environ|env\.|\$\{|<\w)", re.I)


def universal_forbidden_patterns():
    # Enforced across 100% of tracked files including skills-pack/.
    pats = [
        ("machine-path-win-users", r"C:\\+Us" + r"ers\\"),
        ("machine-path-mac-users", "/Us" + "ers/"),
        ("machine-path-home", r"(?<!~)/ho" + r"me/[a-z]+/"),
        ("owner-name", "Zi" + "zo"),
        ("project-drive", r"D:\\+S" + "MS"),
        ("project-codename", "hRh" + "R"),
        ("owner-codename", "PHOE" + "NIX"),
        ("brain-id", "115a5" + "a36"),
        ("brain-path", "antigra" + r"vity[\\/]brain"),
        ("secret-openai", r"(?<![A-Za-z0-9])sk-[A-Za-z0-9]{10,}"),
        ("secret-github", r"ghp_[A-Za-z0-9]{20,}"),
        ("secret-bearer", r"Bearer\s+[A-Za-z0-9._-]{16,}"),
        ("secret-bot-token", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
        ("personal-tg-chat", "11242" + "47595"),
        ("personal-tg-bot", "sheets2025" + "from_bot"),
        ("secret-api-key", r"api[_-]?key\s*[:=]\s*\S{8,}"),
    ]
    compiled = []
    for name, pat in pats:
        flags = re.I if name == "secret-api-key" else 0
        compiled.append((name, re.compile(pat, flags)))
    return compiled


def core_forbidden_patterns():
    # Enforced only on Lock360 core (outside skills-pack/).
    pats = [
        ("leak-4096", "40" + "96"),
        ("leak-24kb", "24" + "KB"),
        ("leak-frida", "fri" + "da"),
        ("leak-lsposed", "LSPo" + "sed"),
        ("leak-floodwait", "Flood" + "Wait"),
        ("leak-authkey", "Auth" + "Key"),
        ("leak-session", r"\.sess" + r"ion\b"),
        ("leak-telegram", "Tele" + "gram"),
    ]
    return [(name, re.compile(pat)) for name, pat in pats]


SIBLING_SKILLS = [
    "00-reverse-engineer", "00-bolla-constitution", "00-architect-sre",
    "00-architectural-cards-protocol", "00-dual-agent-copilot",
    "01-micro-tasker", "02-planning-system", "00-evidence-inspector",
    "egm-bootstrap", "egm-brainstorm", "egm-draft", "egm-drift-report",
    "egm-resolve", "egm-review", "egm-review-loop", "everything-search",
    "neon-ai-gateway", "neon-auth", "neon-functions", "neon-object-storage",
    "neon-postgres", "neon-realtime",
]
SIBLING_WHITELIST = (
    "SKILL.md",
    "workflows/00-lock360-zero-gaps.md",
    "skills-pack/README.md",
    ".github/workflows/verify.yml",
    "references/COMPLETE_SKILLS_CATALOG.md",
)


def check_forbidden(files):
    bad = 0
    uni_pats = universal_forbidden_patterns()
    core_pats = core_forbidden_patterns()
    sibling_re = re.compile("|".join(re.escape(s) for s in SIBLING_SKILLS))
    scanned = 0
    for rel in files:
        # The manifest is pure hex digests: random hex can collide with digit-only
        # leak patterns, so it is excluded here and verified by check (k) instead.
        if rel in (SELF_REL, MANIFEST_REL):
            continue
        scanned += 1
        text = read_text(rel)
        in_pack = rel.startswith("skills-pack/")
        lines = text.split("\n")
        for lineno, line in enumerate(lines, 1):
            for name, rx in uni_pats:
                if name == "secret-api-key" and SAFE_APIKEY_ENV_RE.search(line):
                    continue
                if rx.search(line):
                    bad += 1
                    report("FAIL", "d", "%s:%d forbidden pattern [%s]" % (rel, lineno, name))
            if not in_pack:
                for name, rx in core_pats:
                    if rx.search(line):
                        bad += 1
                        report("FAIL", "d", "%s:%d forbidden pattern [%s]" % (rel, lineno, name))
                if rel not in SIBLING_WHITELIST and sibling_re.search(line):
                    bad += 1
                    report("FAIL", "d", "%s:%d sibling skill name not allowed outside whitelist"
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
        if not rel.lower().endswith(".md") or is_pack_md(rel):
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
VERSION_RE = re.compile(r"\bv\d+\.\d+\b")
# Arabic label "<al-isdar>:" optionally followed by markdown emphasis / backtick,
# then a bare "2.x" or "3.x" (or v2.x/v3.x). Catches unprefixed versions that VERSION_RE misses.
VERSION_LABEL_RE = re.compile(
    "\u0627\u0644\u0625\u0635\u062f\u0627\u0631:[\\s*`]*(v?)([23]\\.\\d+)\\b")


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
    label_hits = 0
    for rel in files:
        if not (is_text(rel) or is_ps1(rel)):
            continue
        if rel == "gist/04-CHANGELOG.md" or rel.startswith("archive/") or is_pack_asset(rel) or is_fixture(rel):
            continue
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            for m in VERSION_RE.finditer(line):
                hits += 1
                if m.group(0) != ver:
                    bad += 1
                    report("FAIL", "f", "%s:%d version %s != VERSION %s"
                           % (rel, lineno, m.group(0), ver))
            for m in VERSION_LABEL_RE.finditer(line):
                if m.group(1) == "v":
                    continue  # already counted by VERSION_RE above
                label_hits += 1
                found = "v" + m.group(2)
                if found != ver:
                    bad += 1
                    report("FAIL", "f", "%s:%d unprefixed version label %s != VERSION %s"
                           % (rel, lineno, m.group(2), ver))
    if not bad:
        report("PASS", "f", "%d version mentions (+%d label-only) match VERSION=%s"
               % (hits, label_hits, ver))
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
        if not (is_text(rel) or is_ps1(rel)) or is_fixture(rel):
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
def load_yaml_module():
    try:
        import yaml  # type: ignore
        return yaml
    except Exception:
        return None


def check_workflows(files):
    bad = 0
    checked = 0
    yaml = load_yaml_module()
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
        if not rel.lower().endswith(".md") or is_pack_md(rel) or is_fixture(rel):
            continue
        checked += 1
        for lineno, line in enumerate(read_text(rel).split("\n"), 1):
            if line.lstrip().startswith("|"):
                bad += 1
                report("FAIL", "j", "%s:%d markdown table row" % (rel, lineno))
    if not bad:
        report("PASS", "j", "0 markdown table rows in %d .md files" % checked)
    return bad


# ---------------------------------------------------------------- (k) manifest
MANIFEST_LINE_RE = re.compile(r"^([0-9a-f]{64})  (\S.*)$")


def git_file_list():
    """Tracked + untracked-but-not-ignored files via git; None when git is unusable."""
    git = shutil.which("git")
    if not git or not os.path.isdir(os.path.join(ROOT, ".git")):
        return None
    names = set()
    for args in (["ls-files", "-z"],
                 ["ls-files", "-z", "--others", "--exclude-standard"]):
        try:
            p = subprocess.run([git] + args, cwd=ROOT, capture_output=True, timeout=60)
        except Exception:
            return None
        if p.returncode != 0:
            return None
        for raw in p.stdout.split(b"\0"):
            if raw:
                names.add(raw.decode("utf-8", errors="replace").replace("\\", "/"))
    return names


def manifest_files():
    names = git_file_list()
    if names is None:
        names = set(collect_files())
    out = []
    for rel in sorted(names):
        if rel == MANIFEST_REL or rel.startswith(".git/") or "/__pycache__/" in rel:
            continue
        if os.path.isfile(os.path.join(ROOT, rel)):
            out.append(rel)
    return out


def manifest_digest(rel):
    data = read_bytes(rel)
    if is_text(rel) or is_ps1(rel):
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def write_manifest():
    lines = ["%s  %s" % (manifest_digest(rel), rel) for rel in manifest_files()]
    path = os.path.join(ROOT, MANIFEST_REL)
    tmp = "%s.tmp-%d" % (path, os.getpid())
    with open(tmp, "wb") as fh:
        fh.write(("\n".join(lines) + "\n").encode("utf-8"))
    os.replace(tmp, path)
    print("verify_repo: wrote %s (%d entries, EOL-normalized sha256)" % (MANIFEST_REL, len(lines)))
    return len(lines)


def check_manifest():
    if not os.path.isfile(os.path.join(ROOT, MANIFEST_REL)):
        report("FAIL", "k", "%s missing (run: python3 scripts/verify_repo.py --update-manifest)"
               % MANIFEST_REL)
        return 1
    bad = 0
    listed = {}
    for lineno, line in enumerate(read_text(MANIFEST_REL).split("\n"), 1):
        if not line.strip():
            continue
        m = MANIFEST_LINE_RE.match(line)
        if not m:
            bad += 1
            report("FAIL", "k", "%s:%d malformed line (expected '<sha256>  <path>')"
                   % (MANIFEST_REL, lineno))
            continue
        if m.group(2) in listed:
            bad += 1
            report("FAIL", "k", "%s:%d duplicate entry %s" % (MANIFEST_REL, lineno, m.group(2)))
        listed[m.group(2)] = m.group(1)
    expected = dict((rel, manifest_digest(rel)) for rel in manifest_files())
    for rel in sorted(listed):
        if rel not in expected:
            bad += 1
            report("FAIL", "k", "%s listed in manifest but absent from the tree" % rel)
        elif listed[rel] != expected[rel]:
            bad += 1
            report("FAIL", "k", "%s sha256 mismatch (manifest %s.. != tree %s..)"
                   % (rel, listed[rel][:12], expected[rel][:12]))
    for rel in sorted(expected):
        if rel not in listed:
            bad += 1
            report("FAIL", "k", "%s present in tree but not listed in %s" % (rel, MANIFEST_REL))
    if bad:
        report("FAIL", "k", "manifest drift: re-run with --update-manifest after reviewing the diff")
    else:
        report("PASS", "k", "%s verifies %d files (EOL-normalized sha256)"
               % (MANIFEST_REL, len(expected)))
    return bad


# ---------------------------------------------------------------- (l) issue templates
ISSUE_FORM_TYPES = ("markdown", "textarea", "input", "dropdown", "checkboxes")


def check_issue_templates(files):
    bad = 0
    checked = 0
    yaml = load_yaml_module()
    for rel in files:
        if not rel.startswith(".github/ISSUE_TEMPLATE/"):
            continue
        if not rel.lower().endswith((".yml", ".yaml")):
            continue
        checked += 1
        text = read_text(rel)
        base = os.path.basename(rel)
        if "\t" in text:
            bad += 1
            report("FAIL", "l", "%s contains tab characters" % rel)
        if base == "config.yml":
            if not re.search(r"^blank_issues_enabled:", text, re.M):
                bad += 1
                report("FAIL", "l", "%s missing top-level 'blank_issues_enabled:'" % rel)
        else:
            for key in ("name", "description", "body"):
                if not re.search(r"^%s:" % key, text, re.M):
                    bad += 1
                    report("FAIL", "l", "%s missing top-level '%s:'" % (rel, key))
            if not re.search(r"^\s+-\s+type:\s*(%s)\b" % "|".join(ISSUE_FORM_TYPES), text, re.M):
                bad += 1
                report("FAIL", "l", "%s has no issue-form element under body" % rel)
        if yaml is not None:
            try:
                doc = yaml.safe_load(text)
                if not isinstance(doc, dict):
                    bad += 1
                    report("FAIL", "l", "%s does not parse to a mapping" % rel)
                elif base != "config.yml" and not isinstance(doc.get("body"), list):
                    bad += 1
                    report("FAIL", "l", "%s 'body' is not a list" % rel)
            except Exception as exc:
                bad += 1
                report("FAIL", "l", "%s YAML parse error: %s" % (rel, str(exc).replace("\n", " ")))
    pr_tpl = ".github/PULL_REQUEST_TEMPLATE.md"
    has_pr = os.path.isfile(os.path.join(ROOT, pr_tpl))
    if checked == 0:
        report("SKIP", "l", "no issue templates under .github/ISSUE_TEMPLATE")
        return 0
    if not has_pr:
        bad += 1
        report("FAIL", "l", "%s missing" % pr_tpl)
    if not bad:
        extra = "PyYAML full parse" if yaml is not None else "structural checks only"
        report("PASS", "l", "%d issue templates + PR template OK (%s)" % (checked, extra))
    return bad


# ---------------------------------------------------------------- (m) lock360 engine
def check_lock360_engine():
    rel = "scripts/lock360.py"
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        report("SKIP", "m", "%s not found" % rel)
        return 0
    bad = 0
    oks = []
    runs = (
        (["--selftest"], "selftest"),
        (["eval"], "eval"),
        (["audit-skill", ".", "--strict"], "audit-skill core"),
        (["audit-skill", "skills-pack/skills"], "audit-skill pack"),
    )
    for args, label in runs:
        try:
            p = subprocess.run([sys.executable, "-X", "utf8", path] + args, cwd=ROOT,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=300)
        except Exception as exc:
            bad += 1
            report("FAIL", "m", "lock360.py %s could not run: %s" % (label, exc))
            continue
        summary = ""
        for line in (p.stdout or "").strip().split("\n")[::-1]:
            if "lock360 " in line and (line.startswith("lock360 ") or "audit-skill" in line):
                summary = line.strip().split("\u2014")[-1].strip() if "audit-skill" in line else line.strip()
                summary = ("%s: %s" % (label, summary)) if "audit-skill" in line else summary
                break
        if p.returncode != 0:
            bad += 1
            fails = [l.strip() for l in (p.stdout or "").split("\n") if l.startswith("[FAIL]")]
            report("FAIL", "m", "lock360.py %s rc=%d: %s" % (label, p.returncode,
                   " | ".join(fails[:5]) or (p.stderr or "").strip()[-300:]))
        else:
            oks.append(summary or ("%s rc=0" % label))
    if not bad:
        report("PASS", "m", "lock360.py OK: %s" % " | ".join(oks))
    return bad


# ---------------------------------------------------------------- (n) deploy gate doc wiring
def check_deploy_wiring():
    rel = "references/RELEASE_DEPLOY_ROLLBACK.md"
    if not os.path.isfile(os.path.join(ROOT, rel)):
        report("FAIL", "n", "%s missing" % rel)
        return 1
    txt = read_text(rel)
    bad = 0
    for needle in ("deploy-gate", "F-DEPLOY-GATE", "GO / NO-GO / ROLLBACK"):
        if needle not in txt:
            bad += 1
            report("FAIL", "n", "%s missing required wiring token %r" % (rel, needle))
    for doc_rel in ("SKILL.md", "README.md"):
        if "RELEASE_DEPLOY_ROLLBACK.md" not in read_text(doc_rel):
            bad += 1
            report("FAIL", "n", "%s does not reference %s" % (doc_rel, rel))
    if not bad:
        report("PASS", "n", "%s wired to deploy-gate, F-DEPLOY-GATE, SKILL.md and README.md" % rel)
    return bad


# ---------------------------------------------------------------- (o) clean lexicon (zero legacy metaphors)
def check_clean_lexicon(files):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import lock360  # local engine source of truth
    bad = 0
    scanned = 0
    for rel in files:
        if not (is_text(rel) or is_ps1(rel)):
            continue
        if rel in (SELF_REL, MANIFEST_REL, "scripts/lock360.py", "gist/04-CHANGELOG.md"):
            continue
        if rel.startswith("archive/") or rel.startswith("skills-pack/skills/"):
            continue
        scanned += 1
        hits = lock360.find_legacy_lexicon(read_text(rel))
        if hits:
            bad += 1
            report("FAIL", "o", "%s contains legacy/obsolete lexicon: %s" % (rel, ", ".join(hits[:4])))
    if not bad:
        report("PASS", "o", "clean lexicon verified across %d files (fixtures & eval included)" % scanned)
    return bad


# ---------------------------------------------------------------- (p) eval coverage gate
def check_eval_coverage():
    import json
    cases_rel = "tests/eval_cases.json"
    if not os.path.isfile(os.path.join(ROOT, cases_rel)):
        report("FAIL", "p", "%s missing" % cases_rel)
        return 1
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import lock360
    spec = json.loads(read_text(cases_rel))
    cases = spec.get("cases", [])
    covered = set()
    for c in cases:
        exp = c.get("expect", {})
        covered.update(exp.get("must_include", []))
    required = ([c["id"] for c in lock360.CHECKS]
                + [cid for cid, _, _ in lock360.QA_CHECKS]
                + [code for code, _, _ in lock360.DEPLOY_CHECKS]
                + list(lock360.SKILL_AUDIT_CHECKS))
    # SA-OVERTRIGGER and SA-SIZE are tested via negative assertions / dedicated checks
    missing = [cid for cid in required if cid not in covered and cid not in ("SA-OVERTRIGGER", "SA-SIZE", "DG-01")]
    bad = 0
    if len(cases) < 150:
        bad += 1
        report("FAIL", "p", "eval_cases.json has %d cases < 150 minimum" % len(cases))
    if missing:
        bad += 1
        report("FAIL", "p", "check IDs missing red-green coverage in eval_cases.json: %s" % ", ".join(missing))
    if not bad:
        report("PASS", "p", "eval coverage OK (%d cases covering %d check IDs)" % (len(cases), len(covered)))
    return bad


# ---------------------------------------------------------------- (q) v3 core & v2 stub
def check_v3_core_and_redirect():
    v3_rel = "gist/01-CORE-PROMPT-360-v3.md"
    v2_rel = "gist/01-CORE-PROMPT-360-v2.md"
    bad = 0
    if not os.path.isfile(os.path.join(ROOT, v3_rel)):
        bad += 1
        report("FAIL", "q", "%s missing" % v3_rel)
    else:
        t3 = read_text(v3_rel)
        for req in ("3.15", "3.16", "Q-Contract", "القارئ"):
            if req not in t3:
                bad += 1
                report("FAIL", "q", "%s missing %r" % (v3_rel, req))
    if not os.path.isfile(os.path.join(ROOT, v2_rel)):
        bad += 1
        report("FAIL", "q", "%s redirect stub missing" % v2_rel)
    else:
        t2 = read_text(v2_rel)
        lines2 = t2.strip().split("\n")
        if len(lines2) > 10 or "01-CORE-PROMPT-360-v3.md" not in t2:
            bad += 1
            report("FAIL", "q", "%s must be a <=10-line redirect stub pointing to v3" % v2_rel)
    if not bad:
        report("PASS", "q", "%s verified + %s is valid redirect stub" % (v3_rel, v2_rel))
    return bad


# ---------------------------------------------------------------- main
USAGE = "usage: verify_repo.py [--update-manifest] [-h]"


def main(argv):
    update = False
    for arg in argv:
        if arg == "--update-manifest":
            update = True
        elif arg in ("-h", "--help"):
            print(USAGE)
            return 0
        else:
            print("verify_repo: unknown option %r" % arg)
            print(USAGE)
            return 2
    print("verify_repo: root=%s" % ROOT)
    if update:
        write_manifest()
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
    fails += check_manifest()
    fails += check_issue_templates(files)
    fails += check_lock360_engine()
    fails += check_deploy_wiring()
    fails += check_clean_lexicon(files)
    fails += check_eval_coverage()
    fails += check_v3_core_and_redirect()
    n_pass = sum(1 for s, _, _ in RESULTS if s == "PASS")
    n_fail = sum(1 for s, _, _ in RESULTS if s == "FAIL")
    n_skip = sum(1 for s, _, _ in RESULTS if s == "SKIP")
    print("SUMMARY: PASS=%d FAIL=%d SKIP=%d" % (n_pass, n_fail, n_skip))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
