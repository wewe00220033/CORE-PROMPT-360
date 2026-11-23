#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="00-lock360-zero-gaps"
TARGET_ROOT="${HOME}/.gemini"
WITH_WORKFLOW=0
WITH_RULE=0
WITH_PACK=0
UNINSTALL=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all) WITH_WORKFLOW=1; WITH_RULE=1 ;;
    --with-workflow) WITH_WORKFLOW=1 ;;
    --with-rule) WITH_RULE=1 ;;
    --with-pack) WITH_PACK=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --target)
      shift
      [ "$#" -gt 0 ] || { echo "error: --target requires a path" >&2; exit 2; }
      TARGET_ROOT="$1"
      ;;
    -h|--help)
      echo "Usage: bash scripts/install.sh [--all | --with-workflow | --with-rule] [--with-pack] [--uninstall] [--target DIR]"
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

# Portable form when TargetRoot is the default (~/.gemini); absolute SKILL.md path otherwise.
DEFAULT_ROOT="${HOME%/}/.gemini"
if [ "${TARGET_ROOT%/}" = "$DEFAULT_ROOT" ]; then
  SNIPPET_SKILL_PATH="~/.gemini/config/skills/${SKILL_NAME}/SKILL.md"
else
  SNIPPET_SKILL_PATH="${SKILL_DST}/SKILL.md"
fi

# Python is required only for --with-rule/--all/--uninstall; resolved BEFORE any copy (no half-install).
PY=""
require_python() {
  # Try python3 then python; keep the first one that actually runs (skips broken launchers / store stubs).
  local cand
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 \
       && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 6) else 1)' >/dev/null 2>&1; then
      PY="$(command -v "$cand")"
      return 0
    fi
  done
  echo "error: a working Python >= 3.6 (python3 or python) is required for --with-rule/--all/--uninstall" >&2
  exit 2
}

update_gemini_block() {
  local mode="$1" # install | remove
  "$PY" - "$GEMINI_FILE" "$mode" "$SNIPPET_SKILL_PATH" <<'PY'
import os, re, shutil, sys

path, mode, skill_path = sys.argv[1], sys.argv[2], sys.argv[3]
start = "<!-- LOCK360_START -->"
end = "<!-- LOCK360_END -->"
snippet = """<!-- LOCK360_START -->
## 🔒 بروتوكول التقفيل الشامل 360° (Lock360 v2.5)

- **المصدر الموحد:** `00-lock360-zero-gaps` (`__LOCK360_SKILL_PATH__` · `gist/01-CORE-PROMPT-360-v2.md` · `workflows/00-lock360-zero-gaps.md`).
- **`L1 Auto-Guard` (`P` تلقائياً بعد الأعمال غير التافهة):** راجع المتبقي/الحدود، أمان التسليم والتزامن، الدليل القاطع بعد آخر تعديل، واسأل المستخدم عن أي غموض بدل التخمين.
- **`L2 / L3`:** عند طلب قفّل 360 / بالضبة والمفتاح / 1600°-10000° / `/lock360` حمّل المهارة ونفّذ الترس المناسب (`S / M / L`)، مع الالتزام بقاعدة `RTL-Safe` (بلا جداول `| col |` في الشات).
<!-- LOCK360_END -->"""
snippet = snippet.replace("__LOCK360_SKILL_PATH__", skill_path)

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
  require_python
  [ -f "$GEMINI_FILE" ] || return 0
  "$PY" - "$GEMINI_FILE" <<'PY'
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

PACK_ROOT="${REPO_ROOT}/skills-pack"

install_pack() {
  if [ ! -d "$PACK_ROOT" ]; then
    echo "error: skills-pack directory not found at $PACK_ROOT" >&2
    exit 2
  fi
  local bak_root="${TARGET_ROOT}/.backup_lock360_pack_$(date +%Y%m%d_%H%M%S)"
  local bak_used=0
  local skills_dst_root="${TARGET_ROOT}/config/skills"
  local wf_dst_root="${TARGET_ROOT}/config/workflows"
  local rules_dst_root="${TARGET_ROOT}/config/rules"
  local sc=0 wc=0 rc=0

  if [ -d "${PACK_ROOT}/skills" ]; then
    mkdir -p "$skills_dst_root"
    for d in "${PACK_ROOT}/skills"/*/; do
      [ -d "$d" ] || continue
      local name; name="$(basename "${d%/}")"
      local dst="${skills_dst_root}/${name}"
      if [ -d "$dst" ]; then
        mkdir -p "${bak_root}/skills"
        cp -R "$dst" "${bak_root}/skills/${name}"
        bak_used=1
        rm -rf "$dst"
      fi
      cp -R "${d%/}" "$dst"
      sc=$((sc + 1))
    done
  fi

  if [ -d "${PACK_ROOT}/workflows" ]; then
    mkdir -p "$wf_dst_root"
    for f in "${PACK_ROOT}/workflows"/*; do
      [ -f "$f" ] || continue
      local name; name="$(basename "$f")"
      local dst="${wf_dst_root}/${name}"
      if [ -f "$dst" ]; then
        mkdir -p "${bak_root}/workflows"
        cp "$dst" "${bak_root}/workflows/${name}"
        bak_used=1
      fi
      cp "$f" "$dst"
      wc=$((wc + 1))
    done
  fi

  if [ -d "${PACK_ROOT}/rules" ]; then
    mkdir -p "$rules_dst_root"
    for f in "${PACK_ROOT}/rules"/*; do
      [ -f "$f" ] || continue
      local name; name="$(basename "$f")"
      local dst="${rules_dst_root}/${name}"
      if [ -f "$dst" ]; then
        mkdir -p "${bak_root}/rules"
        cp "$dst" "${bak_root}/rules/${name}"
        bak_used=1
      fi
      cp "$f" "$dst"
      rc=$((rc + 1))
    done
  fi

  [ "$bak_used" -eq 1 ] && echo "[lock360] Backed up existing pack targets to: $bak_root"
  echo "[lock360] Installed skills-pack: skills=${sc} workflows=${wc} rules=${rc}"

  if [ "$WITH_RULE" -eq 1 ] && [ -f "${PACK_ROOT}/GEMINI.template.md" ]; then
    if [ ! -f "$GEMINI_FILE" ]; then
      mkdir -p "$(dirname "$GEMINI_FILE")"
      cp "${PACK_ROOT}/GEMINI.template.md" "$GEMINI_FILE"
      echo "[lock360] Seeded new GEMINI.md from sanitized skills-pack/GEMINI.template.md"
    else
      echo "[lock360] Existing GEMINI.md preserved (sanitized template available at skills-pack/GEMINI.template.md)"
    fi
  fi
}

uninstall_pack() {
  if [ ! -d "$PACK_ROOT" ]; then
    echo "[lock360] Warning: skills-pack not found in repo; skipping pack uninstall."
    return 0
  fi
  local bak_root="${TARGET_ROOT}/.backup_lock360_pack_uninstall_$(date +%Y%m%d_%H%M%S)"
  local bak_used=0
  local skills_dst_root="${TARGET_ROOT}/config/skills"
  local wf_dst_root="${TARGET_ROOT}/config/workflows"
  local rules_dst_root="${TARGET_ROOT}/config/rules"

  if [ -d "${PACK_ROOT}/skills" ]; then
    for d in "${PACK_ROOT}/skills"/*/; do
      [ -d "$d" ] || continue
      local name; name="$(basename "${d%/}")"
      local dst="${skills_dst_root}/${name}"
      if [ -d "$dst" ]; then
        mkdir -p "${bak_root}/skills"
        cp -R "$dst" "${bak_root}/skills/${name}"
        bak_used=1
        rm -rf "$dst"
      fi
    done
  fi

  if [ -d "${PACK_ROOT}/workflows" ]; then
    for f in "${PACK_ROOT}/workflows"/*; do
      [ -f "$f" ] || continue
      local name; name="$(basename "$f")"
      local dst="${wf_dst_root}/${name}"
      if [ -f "$dst" ]; then
        mkdir -p "${bak_root}/workflows"
        cp "$dst" "${bak_root}/workflows/${name}"
        bak_used=1
        rm -f "$dst"
      fi
    done
  fi

  if [ -d "${PACK_ROOT}/rules" ]; then
    for f in "${PACK_ROOT}/rules"/*; do
      [ -f "$f" ] || continue
      local name; name="$(basename "$f")"
      local dst="${rules_dst_root}/${name}"
      if [ -f "$dst" ]; then
        mkdir -p "${bak_root}/rules"
        cp "$dst" "${bak_root}/rules/${name}"
        bak_used=1
        rm -f "$dst"
      fi
    done
  fi

  [ "$bak_used" -eq 1 ] && echo "[lock360] Backed up and removed skills-pack targets (backup: $bak_root)"
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
  [ "$WITH_PACK" -eq 1 ] && uninstall_pack
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

if [ "$WITH_PACK" -eq 1 ]; then
  install_pack
fi

if [ "$WITH_RULE" -eq 1 ]; then
  update_gemini_block "install"
  echo "[lock360] Updated LOCK360 rule block in: $GEMINI_FILE"
fi

echo "[lock360] Done."
