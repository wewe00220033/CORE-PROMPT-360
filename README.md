<div dir="rtl">

# 🔒 CORE-PROMPT-360 — بروتوكول التقفيل الشامل 360° بالضبة والمفتاح (`v3.1` — Clear-Architecture Edition)

> **مستودع جاهز كـ Skill محمولة + نواة برومبت عالمية + محرك تحقق حتمي** لنقل منهجية `Lock360 v3.1` إلى **أي جهاز** (Windows / macOS / Linux) وأي أداة ذكاء اصطناعي (Antigravity / OpenCode / Claude / Gemini / ChatGPT / DeepSeek / أي موديل ضعيف).
> **الجديد في Clear-Architecture Edition (`v3.1`):** توحيد معيار نظافة المهارات (إلغاء الاستثناء المزدوج وتنظيف `skills-pack/`)، ترقية الموجه للحالات اليومية والبطاقات والـ Luhn + مفاتيح المزودين (`AIza/gsk_/hf_`), رفع ميزانية الترس `M` إلى `6` أسطر، وتقليم النسخ الاحتياطية وتوافق Windows `python -X utf8` مع `152` حالة اختبار فوق معمارية الـ `16` مرحلة و`Q-Contract` و`deploy-gate`.
> *(ملاحظة: هذا الدليل خاص بالتثبيت والنشر على الأجهزة عبر Git؛ لاستخدام البرومبت بالنسخ اليدوي المباشر اقرأ [`gist/00-README.md`](./gist/00-README.md)).*

---

## 🌟 إيه اللي جوه الحزمة؟

- **`SKILL.md` (`00-lock360-zero-gaps`):** المحوّل القياسي للأتراس ومستويات التشغيل (`L1/L2/L3 ↔ P/S/M/L`) — يشتغل فوراً بمجرد وجود المجلد في مسار المهارات.
- **`gist/`:** النواة المحمولة [`01-CORE-PROMPT-360-v3.md`](./gist/01-CORE-PROMPT-360-v3.md) *(و[`v2.md`](./gist/01-CORE-PROMPT-360-v2.md) كـ Redirect Stub للتوافق)* بـ `16` مرحلة + بوابة الصدق `[✅/⚠️/❓]` + ملف القارئ الثلاثي + `Q-Contract` + الناقد `3.15` والملخص `3.16` + [`02-LENSES.md`](./gist/02-LENSES.md) *(عدسة 5 معزولة ولا تُحمَّل إلا عند الطلب الديني)* + [`03-EXAMPLES.md`](./gist/03-EXAMPLES.md) + [`04-CHANGELOG.md`](./gist/04-CHANGELOG.md).
- **`references/`:** مراجع `L3` التقنية ([`DOMAIN_MATRICES.md`](./references/DOMAIN_MATRICES.md)، [`ADVERSARIAL_CHECKLIST_360.md`](./references/ADVERSARIAL_CHECKLIST_360.md)، [`LOCK360_TEMPLATES.md`](./references/LOCK360_TEMPLATES.md)) + مراجع المحرك الحتمي: كتالوج الفحص [`ANT_AND_FLY_TRAPS.md`](./references/ANT_AND_FLY_TRAPS.md) · قاموس اللهجة [`TONE_GLOSSARY.md`](./references/TONE_GLOSSARY.md) · خريطة جميع الحالات [`ALL_CASES_COVERAGE_MAP.md`](./references/ALL_CASES_COVERAGE_MAP.md) · [`EVAL_AND_GUARDRAILS.md`](./references/EVAL_AND_GUARDRAILS.md) · [`THREAT_MODEL_AND_SAFETY.md`](./references/THREAT_MODEL_AND_SAFETY.md) · [`SOURCES_AND_INSPIRATIONS.md`](./references/SOURCES_AND_INSPIRATIONS.md) + النشر والحوادث وسلسلة التوريد: [`RELEASE_DEPLOY_ROLLBACK.md`](./references/RELEASE_DEPLOY_ROLLBACK.md) · [`INCIDENT_RECOVERY_AND_RUNBOOKS.md`](./references/INCIDENT_RECOVERY_AND_RUNBOOKS.md) · [`SKILL_AUDIT_CHECKLIST.md`](./references/SKILL_AUDIT_CHECKLIST.md) · [`COMPLETE_SKILLS_CATALOG.md`](./references/COMPLETE_SKILLS_CATALOG.md).
- **`workflows/00-lock360-zero-gaps.md`:** سير عمل `/lock360`.
- **`scripts/`:** المحرك الحتمي [`lock360.py`](./scripts/lock360.py) (`route` · `audit` · `qa-audit` · `qa-ledger` · `deploy-gate` · `audit-skill` · `runbook` · `skeleton` · `catalog` · `eval` — stdlib فقط) + مثبّت آمن لـ Windows ([`install.ps1`](./scripts/install.ps1)) وmacOS/Linux ([`install.sh`](./scripts/install.sh)) + أداة الفحص [`verify_repo.py`](./scripts/verify_repo.py).
- **`tests/`:** [`eval_cases.json`](./tests/eval_cases.json) — `152` حالة اختبار أحمر-أخضر (توجيه اليوميات والبوتات، ترس، قارئ، لغة نظيفة، مفاتيح وأرقام بطاقات Luhn، تناقضات `SC-1..6`، جولات `Q-*` الـ 12، بوابة النشر `DG-01..07`، تدقيق المهارات `SA-*`، واحتواء الحوادث) + فكستشرات `S/M/L/P/QA/Deploy`. *(تُنسخ أيضاً مع المهارة المثبّتة ليعمل `eval` من أي مكان).*
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

انسخ محتوى [`gist/01-CORE-PROMPT-360-v3.md`](./gist/01-CORE-PROMPT-360-v3.md) أو وجّه أي ذكاء اصطناعي لرابط `raw` المثبّت على الإصدار `v3.1`:

</div>

- **Core Prompt (`v3.1`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/01-CORE-PROMPT-360-v3.md`
- **Plugin Lenses:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/02-LENSES.md`
- **Examples (`P/S/M/L/Q-Contract`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/03-EXAMPLES.md`
- **Prompt Guide:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/00-README.md`
- **كتل نسخ جاهزة (`P/S/M/L` + `/patch-360`):** [`prompts/QUICK-START.md`](./prompts/QUICK-START.md)

<div dir="rtl">

---

### 5️⃣ التثبيت على المنصات الأخرى (OpenCode / Claude Code / Cursor / ChatGPT)

نفس القاعدة ذات الأسطر الأربعة معبّأة بصيغة كل أداة (`AGENTS.md` · `CLAUDE.md` · `.cursor/rules/*.mdc` · Custom Instructions) في [`platforms/README.md`](./platforms/README.md). والنص الأصلي `v1.x` محفوظ للرجوع التاريخي في [`archive/README.md`](./archive/README.md).

---

### 6️⃣ التحقق والتكامل المستمر (`Verify / CI`)

![verify](https://github.com/wewe00220033/CORE-PROMPT-360/actions/workflows/verify.yml/badge.svg)

أداة فحص بـ Python القياسية فقط ([`scripts/verify_repo.py`](./scripts/verify_repo.py)) تتحقق من `17` بوابة `(a)..(q)`: لا BOM، نهايات أسطر LF، `install.ps1` بـ ASCII، صفر أسرار أو مسارات أجهزة، سلامة الروابط النسبية، تطابق الإصدار مع `VERSION` (حتى صيغة `الإصدار: 3.x` بدون `v`)، صفر جداول Markdown، صحة `install.sh` و`.github/workflows/*.yml` وقوالب `.github/ISSUE_TEMPLATE/*.yml`، بصمات [`MANIFEST.sha256`](./MANIFEST.sha256)، نظافة اللغة من مسميات `v2`/الموروث خارج عدسة 5 والأرشيف، واكتمال التغطية في `eval` (`152` حالة) و`--selftest` و`audit-skill . --strict` و`audit-skill skills-pack/skills` و`deploy-gate`. نفس الفحوص تعمل على Ubuntu **و**Windows تلقائياً في [`.github/workflows/verify.yml`](./.github/workflows/verify.yml).

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
- **`⚡ S`:** قرار يومي قابل للرجوع (`8` مراحل · سقف `<= 350` كلمة).
- **`🔧 M`:** مشروع أو خطة متوسطة (`14` مرحلة بميزانية `<= 6` أسطر لكل مرحلة وسطى + `3.15` الناقد + `3.16` الخلاصة).
- **`🏰 L` (`1600° / 10000°`):** نظام حرج أو قرار مصيري (الـ `16` مرحلة كاملة + العدسات + المراجع التقنية).

---

## 🛡️ المحرك الحتمي في 30 ثانية (`scripts/lock360.py`)

- **`route`:** `python3 scripts/lock360.py route --text "قفّل 360 على ..."` ⬅ الترس والمستوى واللهجة وملف القارئ والعدسات بنفس قواعد `SKILL.md` حرفياً.
- **`audit`:** `python3 scripts/lock360.py audit --output <رد_الموديل> --gear <P/S/M/L> [--request <الطلب>]` ⬅ **`🔎 الفحص الهيكلي (A)` · `🧭 كشف الانحراف (F)` · `💬 تنبيهات الضجيج (M)`** (بما فيها `F-SELF-CONTRADICTION · SC-1..6`)؛ 🔴 يمنع الإغلاق، 🟠 يُقبل مع ذكره في `3.14`.
- **`qa-audit` & `qa-ledger`** (`Q-Contract`): `qa-ledger --prev <السابق>` ثم `qa-audit --output <رد_المتابعة> --prev <السابق> [--request <رد_المستخدم>]` ⬅ بوابة الفهم التفاعلية (`12` فحصاً `Q-*` + بوابة `HOLD / GO` + `Echo + إعادة شرح بمثال`).
- **`deploy-gate`:** `python3 scripts/lock360.py deploy-gate --output <خطة_النشر>` ⬅ البوابة السباعية (`DG-01..07`) وفحص `F-DEPLOY-GATE` في [`RELEASE_DEPLOY_ROLLBACK.md`](./references/RELEASE_DEPLOY_ROLLBACK.md).
- **`audit-skill`:** `python3 scripts/lock360.py audit-skill <مجلد_المهارة | SKILL.md | مجلد_مهارات> [--strict]` ⬅ 🛡️ تدقيق سلسلة التوريد ونظافة الواجهة (`SA-LEGACY-LEXICON`) — الحكم البشري في [`SKILL_AUDIT_CHECKLIST.md`](./references/SKILL_AUDIT_CHECKLIST.md)، والفهرس في [`COMPLETE_SKILLS_CATALOG.md`](./references/COMPLETE_SKILLS_CATALOG.md).
- **`runbook`:** `python3 scripts/lock360.py runbook [--severity S1|S2|S3] [--title "..."]` ⬅ 🚨 كتيّب حوادث `RTL-Safe` حتمي (`F-INCIDENT-CONTAINMENT`).
- **`skeleton`** للموديلات الضعيفة · **`eval`** لاختبارات `tests/eval_cases.json` (`152` حالة) · **`catalog --md`** يولّد [`ANT_AND_FLY_TRAPS.md`](./references/ANT_AND_FLY_TRAPS.md). *(ملحوظة لنظام Windows: استخدم `python -X utf8` بدلاً من `python3` لتفادي اختصار Store الوهمي).*

---

## 🧭 حدود الصدق (مهم)

- Lock360 يرفع التغطية والتحقق إلى أقصى درجة عملية، لكنه **لا يدّعي كمالاً مطلقاً** خارج نطاق الأدلة والمعطيات المتاحة — ولا يوجد نظام بشري أو آلي يضمن صفر ثغرات في كل مستقبل ممكن.
- الصياغة الصحيحة للإغلاق: *"تم التقفيل بأقصى تحقق ممكن ضمن النطاق والأدلة المتاحة"* — لا *"مضمون 100%"* (المحرك يرفض الثانية بفحص `F-ABSOLUTE-CLAIM`).
- أي بند `❓ مجهول` جوهري يتوقف عنده التنفيذ حتى يُسأل المستخدم أو يتوفر دليل.

---

## 📜 الترخيص (`License`)

منشور بموجب ترخيص [`MIT License`](./LICENSE).

</div>
