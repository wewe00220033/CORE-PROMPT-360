<div dir="rtl">

# 🔒 CORE-PROMPT-360 — بروتوكول التقفيل الشامل 360° بالضبة والمفتاح (`v2.7` — 🐜🪰 Ant & Fly Hermetic Edition)

> **مستودع جاهز كـ Skill محمولة + نواة برومبت عالمية + محرك تحقق حتمي** لنقل منهجية `Lock360 v2.7` إلى **أي جهاز** (Windows / macOS / Linux) وأي أداة ذكاء اصطناعي (Antigravity / OpenCode / Claude / Gemini / ChatGPT / DeepSeek / أي موديل ضعيف).
> **الجديد في Ant & Fly Hermetic Edition:** الموديل هو الحلّال و`scripts/lock360.py` هو المُحقِّق — 🐜 **مصيدة النمل** تلتقط الثغرات الأرضية الدقيقة في المخرج (مرحلة غائبة، جدول، ثقة في المكان الغلط، سر)، و🪰 **شبكة الدبان** تصطاد الانحراف في الجو (مجاملة، تبرير بدل دليل، نجاح كاذب، تخفيض ترس صامت)، مع مفتاح لهجة بشري/هندسي تلقائي وبوستر للموديلات الضعيفة.
> *(ملاحظة: هذا الدليل خاص بالتثبيت والنشر على الأجهزة عبر Git؛ لاستخدام البرومبت بالنسخ اليدوي المباشر اقرأ [`gist/00-README.md`](./gist/00-README.md)).*

---

## 🌟 إيه اللي جوه الحزمة؟

- **`SKILL.md` (`00-lock360-zero-gaps`):** المحوّل القياسي للأتراس ومستويات التشغيل (`L1/L2/L3 ↔ P/S/M/L`) — يشتغل فوراً بمجرد وجود المجلد في مسار المهارات.
- **`gist/`:** النواة المحمولة المكتفية بذاتها ([`01-CORE-PROMPT-360-v2.md`](./gist/01-CORE-PROMPT-360-v2.md)) بـ `14` مرحلة + بوابة الصدق المضادة للمجاملة `[✅/⚠️/❓]` + `Explicit Non-Goals` + فيزياء الواقع والميكانيكا + نوع الباب + `Kill Switch / Pre-Mortem` + `8` أسئلة تصيّد سريعة + [`02-LENSES.md`](./gist/02-LENSES.md) (7 عدسات تخصصية) + [`03-EXAMPLES.md`](./gist/03-EXAMPLES.md) + [`04-CHANGELOG.md`](./gist/04-CHANGELOG.md).
- **`references/`:** مراجع `L3` التقنية ([`DOMAIN_MATRICES.md`](./references/DOMAIN_MATRICES.md)، [`ADVERSARIAL_CHECKLIST_360.md`](./references/ADVERSARIAL_CHECKLIST_360.md)، [`LOCK360_TEMPLATES.md`](./references/LOCK360_TEMPLATES.md)) + مراجع `v2.7`: كتالوج النملة والدبانة [`ANT_AND_FLY_TRAPS.md`](./references/ANT_AND_FLY_TRAPS.md) · قاموس اللهجة [`TONE_GLOSSARY.md`](./references/TONE_GLOSSARY.md) · خريطة جميع الحالات [`ALL_CASES_COVERAGE_MAP.md`](./references/ALL_CASES_COVERAGE_MAP.md) · [`EVAL_AND_GUARDRAILS.md`](./references/EVAL_AND_GUARDRAILS.md) · [`THREAT_MODEL_AND_SAFETY.md`](./references/THREAT_MODEL_AND_SAFETY.md) · [`SOURCES_AND_INSPIRATIONS.md`](./references/SOURCES_AND_INSPIRATIONS.md).
- **`workflows/00-lock360-zero-gaps.md`:** سير عمل `/lock360`.
- **`scripts/`:** المحرك الحتمي [`lock360.py`](./scripts/lock360.py) (`route` · `audit` · `skeleton` · `catalog` · `eval` — stdlib فقط) + مثبّت آمن لـ Windows ([`install.ps1`](./scripts/install.ps1)) وmacOS/Linux ([`install.sh`](./scripts/install.sh)) مع النسخ الاحتياطي وإلغاء التثبيت ودعم OpenCode + أداة الفحص [`verify_repo.py`](./scripts/verify_repo.py).
- **`tests/`:** [`eval_cases.json`](./tests/eval_cases.json) — 69 حالة اختبار أحمر-أخضر للمحرك (توجيه، ترقية، لهجة، منع الإفراط في التشغيل، كل نملة ودبانة) + فكستشرات `S/M/L/P`.
- **`prompts/`:** كتل نسخ جاهزة لكل ترس + `/patch-360` ([`QUICK-START.md`](./prompts/QUICK-START.md)) + بوستر الموديلات الضعيفة [`WEAK-MODEL-BOOSTER.md`](./prompts/WEAK-MODEL-BOOSTER.md) (`CORE-MINI` + هيكل + تمريرة تحقق مستقلة + إصلاح محدود).
- **`platforms/`:** تعليمات التثبيت على OpenCode / Claude Code / Codex / Cursor / Windsurf / ChatGPT / أي AI ([`platforms/README.md`](./platforms/README.md)).
- **`skills-pack/`:** حزمة الترحيل الكاملة لأي جهاز جديد — تضم الـ `23` مهارة المكمّلة (`24` مهارة إجمالاً مع `00-lock360-zero-gaps`) + `workflows` + `rules` + قالب `GEMINI.template.md` منظّف من أي أسرار ([`skills-pack/README.md`](./skills-pack/README.md)).
- **`archive/`:** النص الأصلي `v1.x` للرجوع التاريخي فقط ([`archive/README.md`](./archive/README.md)).
- **`CONTRIBUTING.md` + `.github/`:** دليل المساهمة `RTL-Safe` ([`CONTRIBUTING.md`](./CONTRIBUTING.md)) + قوالب Issues (`bug_report` / `feature_or_lens`) وقالب Pull Request مع قائمة تحقق إلزامية.
- **`MANIFEST.sha256`:** بصمات `SHA-256` لكل الملفات المتتبعة ([`MANIFEST.sha256`](./MANIFEST.sha256)) محسوبة على نهايات أسطر موحّدة فتتطابق على Windows وLinux/macOS، ويفحصها `verify_repo.py` آلياً.

---

## 🚀 طرق التثبيت والاستخدام على أي جهاز

### 1️⃣ التثبيت المباشر كـ Skill في Antigravity (أمر واحد — يعمل فوراً)

> مهم: نحدّد اسم المجلد `00-lock360-zero-gaps` صراحةً عشان يطابق `name` داخل `SKILL.md`:

</div>

**Windows (PowerShell):**
```powershell
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git "$env:USERPROFILE\.gemini\config\skills\00-lock360-zero-gaps"
```

**macOS / Linux:**
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/.gemini/config/skills/00-lock360-zero-gaps
```

*(للتحديث لاحقاً على نفس الجهاز — Windows: `git -C "$env:USERPROFILE\.gemini\config\skills\00-lock360-zero-gaps" pull` · macOS/Linux: `git -C ~/.gemini/config/skills/00-lock360-zero-gaps pull`).*

> *ملاحظة: اختر **طريقة 1** أو **طريقة 2** فقط على الجهاز الواحد لتفادي نسختين لنفس المهارة.*

<div dir="rtl">

---

### 2️⃣ التثبيت الكامل مع `/lock360` والقاعدة العالمية المختصرة (`GEMINI.md`)

لو عايز تثبّت الـ Skill + الوورك فلو + الـ 4 أسطر الدائمة في `GEMINI.md` بشكل آمن (يحفظ نسخة احتياطية `.bak` ومش بيلمس أي قواعد تانية ليك):

</div>

**Windows (PowerShell):**
```powershell
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git "$HOME\CORE-PROMPT-360"
# تثبيت Lock360 فقط:
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -All
# أو تثبيت الحزمة الكاملة (24 مهارة + workflows + rules + قالب GEMINI.md):
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -All -WithPack
```
*(لإلغاء التثبيت بأمان لاحقاً: أضف `-Uninstall` ومعه `-WithPack` لو ثبتّ الحزمة الكاملة)*

**macOS / Linux:**
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
# تثبيت Lock360 فقط:
bash ~/CORE-PROMPT-360/scripts/install.sh --all
# أو تثبيت الحزمة الكاملة (24 مهارة + workflows + rules + قالب GEMINI.md):
bash ~/CORE-PROMPT-360/scripts/install.sh --all --with-pack
```
*(لإلغاء التثبيت لاحقاً: أضف `--uninstall` ومعه `--with-pack` لو ثبتّ الحزمة الكاملة)*

**OpenCode (أي نظام) — المهارة في `~/.config/opencode/skills/` + كتلة `AGENTS.md` دون لمس `opencode.json`:**
```bash
bash ~/CORE-PROMPT-360/scripts/install.sh --opencode            # أو أضفه إلى --all
bash ~/CORE-PROMPT-360/scripts/install.sh --uninstall --opencode
```
```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -OpenCode
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -Uninstall -OpenCode
```
*(الحمولة المثبّتة: `SKILL.md` · `gist/` · `references/` · `prompts/` · `scripts/lock360.py` — تفاصيل في [`platforms/opencode/README.md`](./platforms/opencode/README.md))*

<div dir="rtl">

---

### 3️⃣ التثبيت داخل مشروع واحد فقط (`.agents/skills/`)

</div>

```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git .agents/skills/00-lock360-zero-gaps
```

<div dir="rtl">

---

### 4️⃣ الاستخدام المباشر في ChatGPT / Claude / DeepSeek / Gemini Web

انسخ محتوى [`gist/01-CORE-PROMPT-360-v2.md`](./gist/01-CORE-PROMPT-360-v2.md) أو وجّه أي ذكاء اصطناعي لرابط `raw` المثبّت على الإصدار `v2.7`:

</div>

- **Core Prompt (`v2.7`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.7/gist/01-CORE-PROMPT-360-v2.md`
- **Plugin Lenses:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.7/gist/02-LENSES.md`
- **Examples (`P/S/M/L`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.7/gist/03-EXAMPLES.md`
- **Prompt Guide:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.7/gist/00-README.md`
- **كتل نسخ جاهزة (`P/S/M/L` + `/patch-360`):** [`prompts/QUICK-START.md`](./prompts/QUICK-START.md)

<div dir="rtl">

---

### 5️⃣ التثبيت على المنصات الأخرى (OpenCode / Claude Code / Cursor / ChatGPT)

نفس القاعدة ذات الأسطر الأربعة معبّأة بصيغة كل أداة (`AGENTS.md` · `CLAUDE.md` · `.cursor/rules/*.mdc` · Custom Instructions) في [`platforms/README.md`](./platforms/README.md). والنص الأصلي `v1.x` محفوظ للرجوع التاريخي في [`archive/README.md`](./archive/README.md).

---

### 6️⃣ التحقق والتكامل المستمر (`Verify / CI`)

![verify](https://github.com/wewe00220033/CORE-PROMPT-360/actions/workflows/verify.yml/badge.svg)

أداة فحص بـ Python القياسية فقط ([`scripts/verify_repo.py`](./scripts/verify_repo.py)) تتأكد من: لا BOM، نهايات أسطر LF، `install.ps1` بـ ASCII، صفر أسرار أو مسارات أجهزة، سلامة الروابط النسبية، تطابق الإصدار مع `VERSION` (حتى صيغة `الإصدار: 2.x` بدون `v`)، صفر جداول Markdown، صحة `install.sh` و`.github/workflows/*.yml` وقوالب `.github/ISSUE_TEMPLATE/*.yml`، ومطابقة بصمات [`MANIFEST.sha256`](./MANIFEST.sha256)، ونجاح `lock360.py --selftest` و`eval` (69 حالة). نفس الفحص + `eval` + round-trip لـ `--opencode` يعمل على Ubuntu **و**Windows + تثبيت/إلغاء تثبيت كامل على كليهما تلقائياً في [`.github/workflows/verify.yml`](./.github/workflows/verify.yml).

</div>

**macOS / Linux:**
```bash
python3 scripts/verify_repo.py
# بعد تعديل أي ملف متتبع — حدّث البصمات ثم افحص:
python3 scripts/verify_repo.py --update-manifest
```

**Windows (PowerShell):**
```powershell
python -X utf8 scripts\verify_repo.py
# بعد تعديل أي ملف متتبع — حدّث البصمات ثم افحص:
python -X utf8 scripts\verify_repo.py --update-manifest
```

<div dir="rtl">

---

### 7️⃣ المساهمة (`Issues / Pull Requests`)

[![contributing](https://img.shields.io/badge/contributing-guide-blue)](./CONTRIBUTING.md) [![issues](https://img.shields.io/github/issues/wewe00220033/CORE-PROMPT-360)](https://github.com/wewe00220033/CORE-PROMPT-360/issues) [![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

عايز تقترح عدسة جديدة أو إصلاحاً أو منصة أو ترقية `/patch-360` من تجربة حية؟ اقرأ [`CONTRIBUTING.md`](./CONTRIBUTING.md) (القواعد غير القابلة للكسر: `RTL-Safe` · صفر أسرار · إصدار واحد · `MANIFEST.sha256` محدّث)، ثم افتح [Issue](https://github.com/wewe00220033/CORE-PROMPT-360/issues/new/choose) بالقالب المناسب أو Pull Request يمر بقائمة التحقق والفاحص.

</div>

<div dir="rtl">

---

## 🎚️ ملخص التفعيل والأتراس السريع

- **`🔍 P` (`L1 Auto-Guard`):** بوابة فحص ما بعد المهام غير التافهة (المتبقي والثغرات · أمان التسليم والتزامن · الدليل بعد آخر تعديل · بوابة الاستيضاح).
- **`⚡ S`:** قرار يومي قابل للرجوع (<= 450 كلمة تقريباً).
- **`🔧 M`:** مشروع أو خطة متوسطة (`L2 Full Lock360`).
- **`🏰 L` (`1600° / 10000°`):** نظام حرج أو قرار مصيري (الـ 14 مرحلة كاملة + العدسات + المراجع التقنية).

---

## 🐜🪰 المحرك الحتمي في 30 ثانية (`scripts/lock360.py`)

- **`route`:** `python3 scripts/lock360.py route --text "قفّل 360 على ..."` ⬅ الترس والمستوى واللهجة والعدسات بنفس قواعد `SKILL.md` حرفياً.
- **`audit`:** `python3 scripts/lock360.py audit --output <رد_الموديل> --gear <P/S/M/L> [--request <الطلب>]` ⬅ 🐜 نمل · 🪰 دبان · 🦟 ناموس؛ 🔴 يمنع الإغلاق، 🟠 يُقبل مع ذكره في `3.14`.
- **`skeleton`** للموديلات الضعيفة · **`eval`** لاختبارات `tests/eval_cases.json` · **`catalog --md`** يولّد [`ANT_AND_FLY_TRAPS.md`](./references/ANT_AND_FLY_TRAPS.md).

---

## 🧭 حدود الصدق (مهم)

- Lock360 يرفع التغطية والتحقق إلى أقصى درجة عملية، لكنه **لا يدّعي كمالاً مطلقاً** خارج نطاق الأدلة والمعطيات المتاحة — ولا يوجد نظام بشري أو آلي يضمن صفر ثغرات في كل مستقبل ممكن.
- الصياغة الصحيحة للإغلاق: *"تم التقفيل بأقصى تحقق ممكن ضمن النطاق والأدلة المتاحة"* — لا *"مضمون 100%"* (المحرك يرفض الثانية بفحص `F-ABSOLUTE-CLAIM`).
- أي بند `❓ مجهول` جوهري يتوقف عنده التنفيذ حتى يُسأل المستخدم أو يتوفر دليل.

---

## 📜 الترخيص (`License`)

منشور بموجب ترخيص [`MIT License`](./LICENSE).

</div>
