#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="00-lock360-zero-gaps"
TARGET_ROOT="${HOME}/.gemini"
OPENCODE_ROOT="${XDG_CONFIG_HOME:-${HOME}/.config}/opencode"
WITH_WORKFLOW=0
WITH_RULE=0
WITH_PACK=0
WITH_OPENCODE=0
UNINSTALL=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all) WITH_WORKFLOW=1; WITH_RULE=1 ;;
    --with-workflow) WITH_WORKFLOW=1 ;;
    --with-rule) WITH_RULE=1 ;;
    --with-pack) WITH_PACK=1 ;;
    --opencode) WITH_OPENCODE=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --target)
      shift
      [ "$#" -gt 0 ] || { echo "error: --target requires a path" >&2; exit 2; }
      TARGET_ROOT="$1"
      ;;
    --opencode-root)
      shift
      [ "$#" -gt 0 ] || { echo "error: --opencode-root requires a path" >&2; exit 2; }
      OPENCODE_ROOT="$1"
      ;;
    -h|--help)
      echo "Usage: bash scripts/install.sh [--all | --with-workflow | --with-rule] [--with-pack] [--opencode] [--uninstall] [--target DIR] [--opencode-root DIR]"
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
OC_SKILL_DST="${OPENCODE_ROOT}/skills/${SKILL_NAME}"
OC_AGENTS_FILE="${OPENCODE_ROOT}/AGENTS.md"

# Portable form when TargetRoot is the default (~/.gemini); absolute SKILL.md path otherwise.
DEFAULT_ROOT="${HOME%/}/.gemini"
if [ "${TARGET_ROOT%/}" = "$DEFAULT_ROOT" ]; then
  SNIPPET_SKILL_PATH="~/.gemini/config/skills/${SKILL_NAME}/SKILL.md"
else
  SNIPPET_SKILL_PATH="${SKILL_DST}/SKILL.md"
fi
DEFAULT_OC_ROOT="${HOME%/}/.config/opencode"
if [ "${OPENCODE_ROOT%/}" = "$DEFAULT_OC_ROOT" ]; then
  OC_SNIPPET_SKILL_PATH="~/.config/opencode/skills/${SKILL_NAME}/SKILL.md"
else
  OC_SNIPPET_SKILL_PATH="${OC_SKILL_DST}/SKILL.md"
fi

# Python is required only for --with-rule/--all/--opencode/--uninstall; resolved BEFORE any copy (no half-install).
PY=""
require_python() {
  [ -n "$PY" ] && return 0
  # Try python3 then python; keep the first one that actually runs (skips broken launchers / store stubs).
  local cand
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 \
       && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 6) else 1)' >/dev/null 2>&1; then
      PY="$(command -v "$cand")"
      return 0
    fi
  done
  echo "error: a working Python >= 3.6 (python3 or python) is required for --with-rule/--all/--opencode/--uninstall" >&2
  exit 2
}

# update_marker_block FILE MODE SKILL_PATH  (MODE: install | remove)
# Only the <!-- LOCK360_START --> ... <!-- LOCK360_END --> block is touched; every other line is preserved.
update_marker_block() {
  local file="$1" mode="$2" skill_path="$3"
  require_python
  "$PY" - "$file" "$mode" "$skill_path" <<'PY'
import os, re, shutil, sys

path, mode, skill_path = sys.argv[1], sys.argv[2], sys.argv[3]
start = "<!-- LOCK360_START -->"
end = "<!-- LOCK360_END -->"
snippet = """<!-- LOCK360_START -->
## 🔒 بروتوكول التقفيل الشامل 360° (Lock360 v3.1)

- **المصدر الموحد:** `00-lock360-zero-gaps` (`__LOCK360_SKILL_PATH__` · `gist/01-CORE-PROMPT-360-v3.md` · `workflows/00-lock360-zero-gaps.md`).
- **`L1 Auto-Guard` (`P` تلقائياً بعد الأعمال غير التافهة):** راجع المتبقي/الحدود، أمان التسليم والتزامن، الدليل القاطع بعد آخر تعديل، واسأل المستخدم عن أي غموض بدل التخمين.
- **`L2 / L3`:** عند طلب قفّل 360 / بالضبة والمفتاح / 1600°-10000° / `/lock360` حمّل المهارة ونفّذ الترس المناسب (`S / M / L`)، ومرّر المخرج على `scripts/lock360.py audit` قبل الإغلاق، مع الالتزام بقاعدة `RTL-Safe` (بلا جداول `| col |` في الشات).
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

# validate_markers FILE - refuse early when the marker pair is malformed.
validate_markers() {
  local file="$1"
  require_python
  [ -f "$file" ] || return 0
  "$PY" - "$file" <<'PY'
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

# prune_backups DIR PREFIX [KEEP=2] - keep only newest backups matching PREFIX*.
prune_backups() {
  local dir="$1" prefix="$2" keep="${3:-2}"
  [ -d "$dir" ] || return 0
  local i=0 d
  while IFS= read -r d; do
    [ -d "$d" ] || continue
    i=$((i + 1))
    if [ "$i" -gt "$keep" ]; then
      rm -rf "$d"
      echo "[lock360] Pruned old backup: $(basename "$d")"
    fi
  done < <(find "$dir" -maxdepth 1 -mindepth 1 -type d -name "${prefix}*" 2>/dev/null | sort -r)
  return 0
}

# copy_skill_payload DST - SKILL.md, README.md, gist/, references/, prompts/, scripts/lock360.py, tests/.
copy_skill_payload() {
  local dst="$1"
  mkdir -p "$dst"
  cp "$REPO_ROOT/SKILL.md" "$dst/SKILL.md"
  [ -f "$REPO_ROOT/README.md" ] && cp "$REPO_ROOT/README.md" "$dst/README.md"
  rm -rf "$dst/gist" "$dst/references" "$dst/prompts" "$dst/scripts" "$dst/tests"
  cp -R "$REPO_ROOT/gist" "$dst/gist"
  cp -R "$REPO_ROOT/references" "$dst/references"
  [ -d "$REPO_ROOT/prompts" ] && cp -R "$REPO_ROOT/prompts" "$dst/prompts"
  [ -d "$REPO_ROOT/tests" ] && cp -R "$REPO_ROOT/tests" "$dst/tests"
  if [ -f "$REPO_ROOT/scripts/lock360.py" ]; then
    mkdir -p "$dst/scripts"
    cp "$REPO_ROOT/scripts/lock360.py" "$dst/scripts/lock360.py"
    chmod +x "$dst/scripts/lock360.py" 2>/dev/null || true
  fi
  return 0
}

# backup_dir SRC_DIR BAK_ROOT - copy an existing install aside before touching it.
backup_dir() {
  local src="$1" bak="$2"
  mkdir -p "$bak"
  cp -R "$src" "${bak}/${SKILL_NAME}"
  return 0
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

  if [ "$bak_used" -eq 1 ]; then
    echo "[lock360] Backed up existing pack targets to: $bak_root"
  fi
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
  return 0
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

  if [ "$bak_used" -eq 1 ]; then
    echo "[lock360] Backed up and removed skills-pack targets (backup: $bak_root)"
  fi
  return 0
}

# OpenCode: skill under <root>/skills/<name>, marker block in <root>/AGENTS.md. Never touches opencode.json / cli.json.
install_opencode() {
  validate_markers "$OC_AGENTS_FILE"
  if [ -d "$OC_SKILL_DST" ]; then
    local bak="${OPENCODE_ROOT}/.backup_lock360_opencode_$(date +%Y%m%d_%H%M%S)"
    backup_dir "$OC_SKILL_DST" "$bak"
    echo "[lock360] Backed up existing OpenCode skill to: ${bak}/${SKILL_NAME}"
  fi
  copy_skill_payload "$OC_SKILL_DST"
  echo "[lock360] Installed OpenCode skill to: $OC_SKILL_DST"
  update_marker_block "$OC_AGENTS_FILE" "install" "$OC_SNIPPET_SKILL_PATH"
  echo "[lock360] Updated LOCK360 block in: $OC_AGENTS_FILE (opencode.json / cli.json untouched)"
  return 0
}

uninstall_opencode() {
  validate_markers "$OC_AGENTS_FILE"
  if [ -d "$OC_SKILL_DST" ]; then
    local bak="${OPENCODE_ROOT}/.backup_lock360_opencode_uninstall_$(date +%Y%m%d_%H%M%S)"
    backup_dir "$OC_SKILL_DST" "$bak"
    echo "[lock360] Backed up OpenCode skill before uninstall: ${bak}/${SKILL_NAME}"
    rm -rf "$OC_SKILL_DST"
  fi
  update_marker_block "$OC_AGENTS_FILE" "remove" "$OC_SNIPPET_SKILL_PATH"
  echo "[lock360] Removed LOCK360 block from: $OC_AGENTS_FILE (other lines preserved)"
  return 0
}

if [ "$UNINSTALL" -eq 1 ]; then
  validate_markers "$GEMINI_FILE"
  if [ -d "$SKILL_DST" ]; then
    BAK="${TARGET_ROOT}/.backup_lock360_uninstall_$(date +%Y%m%d_%H%M%S)"
    backup_dir "$SKILL_DST" "$BAK"
    echo "[lock360] Backed up skill before uninstall (preserves Extension Slots): ${BAK}/${SKILL_NAME}"
    rm -rf "$SKILL_DST"
  fi
  rm -f "$WF_DST"
  if [ "$WITH_PACK" -eq 1 ]; then
    uninstall_pack
  fi
  if [ "$WITH_OPENCODE" -eq 1 ]; then
    uninstall_opencode
  fi
  update_marker_block "$GEMINI_FILE" "remove" "$SNIPPET_SKILL_PATH"
  prune_backups "$TARGET_ROOT" ".backup_lock360_uninstall_20"
  prune_backups "$TARGET_ROOT" ".backup_lock360_pack_uninstall_20"
  prune_backups "$OPENCODE_ROOT" ".backup_lock360_opencode_uninstall_20"
  echo "[lock360] Uninstalled cleanly from: $TARGET_ROOT"
  exit 0
fi

if [ "$WITH_RULE" -eq 1 ]; then
  validate_markers "$GEMINI_FILE"
fi
if [ "$WITH_OPENCODE" -eq 1 ]; then
  validate_markers "$OC_AGENTS_FILE"
fi

if [ -d "$SKILL_DST" ]; then
  BAK="${TARGET_ROOT}/.backup_lock360_$(date +%Y%m%d_%H%M%S)"
  backup_dir "$SKILL_DST" "$BAK"
  echo "[lock360] Backed up existing skill to: ${BAK}/${SKILL_NAME}"
fi

copy_skill_payload "$SKILL_DST"
echo "[lock360] Installed skill to: $SKILL_DST"

if [ "$WITH_WORKFLOW" -eq 1 ] && [ -f "$REPO_ROOT/workflows/00-lock360-zero-gaps.md" ]; then
  mkdir -p "$(dirname "$WF_DST")"
  cp "$REPO_ROOT/workflows/00-lock360-zero-gaps.md" "$WF_DST"
  echo "[lock360] Installed workflow to: $WF_DST"
fi

if [ "$WITH_PACK" -eq 1 ]; then
  install_pack
fi

if [ "$WITH_OPENCODE" -eq 1 ]; then
  install_opencode
fi

if [ "$WITH_RULE" -eq 1 ]; then
  update_marker_block "$GEMINI_FILE" "install" "$SNIPPET_SKILL_PATH"
  echo "[lock360] Updated LOCK360 rule block in: $GEMINI_FILE"
fi

prune_backups "$TARGET_ROOT" ".backup_lock360_20"
prune_backups "$TARGET_ROOT" ".backup_lock360_pack_20"
prune_backups "$OPENCODE_ROOT" ".backup_lock360_opencode_20"
echo "[lock360] Done."
