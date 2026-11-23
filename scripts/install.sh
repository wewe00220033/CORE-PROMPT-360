#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="00-lock360-zero-gaps"
TARGET_ROOT="${HOME}/.gemini"
WITH_WORKFLOW=0
WITH_RULE=0
UNINSTALL=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all) WITH_WORKFLOW=1; WITH_RULE=1 ;;
    --with-workflow) WITH_WORKFLOW=1 ;;
    --with-rule) WITH_RULE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --target)
      shift
      [ "$#" -gt 0 ] || { echo "error: --target requires a path" >&2; exit 2; }
      TARGET_ROOT="$1"
      ;;
    -h|--help)
      echo "Usage: bash scripts/install.sh [--all | --with-workflow | --with-rule | --uninstall] [--target DIR]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
  shift
done

SKILL_DST="${TARGET_ROOT}/config/skills/${SKILL_NAME}"
WF_DST="${TARGET_ROOT}/config/workflows/00-lock360-zero-gaps.md"
GEMINI_FILE="${TARGET_ROOT}/GEMINI.md"

update_gemini_block() {
  local mode="$1" # install | remove
  python3 - "$GEMINI_FILE" "$mode" <<'PY'
import os, re, shutil, sys

path, mode = sys.argv[1], sys.argv[2]
start = "<!-- LOCK360_START -->"
end = "<!-- LOCK360_END -->"
snippet = """<!-- LOCK360_START -->
## 🔒 بروتوكول التقفيل الشامل 360° (Lock360 v2.3)

- **المصدر الموحد:** `00-lock360-zero-gaps` (`~/.gemini/config/skills/00-lock360-zero-gaps/SKILL.md` · `gist/01-CORE-PROMPT-360-v2.md` · `workflows/00-lock360-zero-gaps.md`).
- **`L1 Auto-Guard` (`P` تلقائياً بعد الأعمال غير التافهة):** راجع المتبقي/الحدود، أمان التسليم والتزامن، الدليل القاطع بعد آخر تعديل، واسأل المستخدم عن أي غموض بدل التخمين.
- **`L2 / L3`:** عند طلب قفّل 360 / بالضبة والمفتاح / 1600°-10000° / `/lock360` حمّل المهارة ونفّذ الترس المناسب (`S / M / L`)، مع الالتزام بقاعدة `RTL-Safe` (بلا جداول `| col |` في الشات).
<!-- LOCK360_END -->"""

existing = ""
if os.path.isfile(path):
    with open(path, "r", encoding="utf-8") as fh:
        existing = fh.read().replace("\r\n", "\n")
elif mode == "remove":
    sys.exit(0)

sc = len(re.findall(re.escape(start), existing))
ec = len(re.findall(re.escape(end), existing))
if sc != ec or sc > 1:
    sys.stderr.write(f"Refusing to modify {path}: malformed LOCK360 markers (start={sc}, end={ec})\n")
    sys.exit(3)

if os.path.isfile(path):
    shutil.copy2(path, path + ".bak")

pattern = re.compile(r"\n*" + re.escape(start) + r".*?" + re.escape(end) + r"\n*", re.S)
if sc == 1:
    if mode == "remove":
        out = pattern.sub("\n", existing).strip() + "\n"
    else:
        out = pattern.sub("\n\n" + snippet + "\n", existing)
elif mode == "install":
    out = (existing.rstrip() + "\n\n" if existing.strip() else "") + snippet + "\n"
else:
    sys.exit(0)

os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
tmp = f"{path}.tmp-{os.getpid()}"
with open(tmp, "wb") as fh:
    fh.write(out.encode("utf-8"))
os.replace(tmp, path)
PY
}

validate_gemini_markers() {
  command -v python3 >/dev/null 2>&1 || { echo "error: python3 required for --with-rule/--all/--uninstall" >&2; exit 2; }
  [ -f "$GEMINI_FILE" ] || return 0
  python3 - "$GEMINI_FILE" <<'PY'
import re, sys
p = sys.argv[1]
txt = open(p, "r", encoding="utf-8").read().replace("\r\n", "\n")
sc = len(re.findall(re.escape("<!-- LOCK360_START -->"), txt))
ec = len(re.findall(re.escape("<!-- LOCK360_END -->"), txt))
if sc != ec or sc > 1:
    sys.stderr.write(f"Refusing to modify {p}: malformed LOCK360 markers (start={sc}, end={ec})\n")
    sys.exit(3)
PY
}

if [ "$UNINSTALL" -eq 1 ]; then
  validate_gemini_markers
  if [ -d "$SKILL_DST" ]; then
    BAK="${TARGET_ROOT}/.backup_lock360_uninstall_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BAK"
    cp -R "$SKILL_DST" "${BAK}/${SKILL_NAME}"
    echo "[lock360] Backed up skill before uninstall (preserves Extension Slots): ${BAK}/${SKILL_NAME}"
    rm -rf "$SKILL_DST"
  fi
  rm -f "$WF_DST"
  update_gemini_block "remove"
  echo "[lock360] Uninstalled cleanly from: $TARGET_ROOT"
  exit 0
fi

if [ "$WITH_RULE" -eq 1 ]; then
  validate_gemini_markers
fi

if [ -d "$SKILL_DST" ]; then
  BAK="${TARGET_ROOT}/.backup_lock360_$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$BAK"
  cp -R "$SKILL_DST" "${BAK}/${SKILL_NAME}"
  echo "[lock360] Backed up existing skill to: ${BAK}/${SKILL_NAME}"
fi

mkdir -p "$SKILL_DST"
cp "$REPO_ROOT/SKILL.md" "$SKILL_DST/SKILL.md"
[ -f "$REPO_ROOT/README.md" ] && cp "$REPO_ROOT/README.md" "$SKILL_DST/README.md"
rm -rf "$SKILL_DST/gist" "$SKILL_DST/references"
cp -R "$REPO_ROOT/gist" "$SKILL_DST/gist"
cp -R "$REPO_ROOT/references" "$SKILL_DST/references"
echo "[lock360] Installed skill to: $SKILL_DST"

if [ "$WITH_WORKFLOW" -eq 1 ] && [ -f "$REPO_ROOT/workflows/00-lock360-zero-gaps.md" ]; then
  mkdir -p "$(dirname "$WF_DST")"
  cp "$REPO_ROOT/workflows/00-lock360-zero-gaps.md" "$WF_DST"
  echo "[lock360] Installed workflow to: $WF_DST"
fi

if [ "$WITH_RULE" -eq 1 ]; then
  update_gemini_block "install"
  echo "[lock360] Updated LOCK360 rule block in: $GEMINI_FILE"
fi

echo "[lock360] Done."
