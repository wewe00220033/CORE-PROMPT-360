<div dir="rtl">

# 🧰 `skills-pack/` — حزمة المهارات والقواعد والـ Workflows الكاملة (`v3.0`)

> **الغرض:** تجميع جميع المهارات (`24` مهارة بالكامل: `00-lock360-zero-gaps` في جذر المستودع + `23` مهارة إضافية هنا) مع مسارات العمل (`3` workflows) والقواعد (`3` rules) وقالب `GEMINI.template.md` المنظّف من أي أسرار أو مسارات شخصية، لنقل بيئة العمل كاملة لأي جهاز بضغطة زر.
> **سلسلة التوريد (`v3.0`):** قبل تثبيت الحزمة في بيئة حساسة شغّل `python3 scripts/lock360.py audit-skill skills-pack/skills` (صفر `FAIL` مطلوب؛ `WARN` يُدوَّن)، وأكمل الحكم البشري في [`references/SKILL_AUDIT_CHECKLIST.md`](../references/SKILL_AUDIT_CHECKLIST.md). الفهرس الكامل ومسار الاختيار السريع في [`references/COMPLETE_SKILLS_CATALOG.md`](../references/COMPLETE_SKILLS_CATALOG.md).

---

## 📦 محتويات الحزمة

- **المهارة المحورية في الجذر (`1`):** [`00-lock360-zero-gaps`](../SKILL.md) + [`workflows/00-lock360-zero-gaps.md`](../workflows/00-lock360-zero-gaps.md).
- **المهارات التأسيسية والهندسية المخصصة (`9` داخل `skills/`):**
  - `00-architect-sre`: دستور المعماري ومفتش الأمان والـ SRE والصمامات الـ 86.
  - `00-architectural-cards-protocol`: بروتوكول الكروت المعمارية والخلاصة المركزة المزدوجة.
  - `00-bolla-constitution`: دستور الحوكمة الهندسي الموحد (T0/T1/T2) والقوانين العشرة الذهبية.
  - `00-dual-agent-copilot`: تشغيل ومزامنة الوكلاء المتوازيين وقاموس الجودة.
  - `00-evidence-inspector`: فحص الأدلة والتحقق الإلزامي بالسطور.
  - `00-reverse-engineer`: بروتوكول تحليل واجهات المزودين (Zero-Browser HTTP).
  - `01-micro-tasker`: تقسيم المهام الصغيرة المنضبطة.
  - `02-planning-system`: قوالب وأدوات التخطيط ومتابعة التنفيذ.
  - `everything-search`: استخدام `ev` للبحث اللحظي عبر فهرس Everything (`%USERPROFILE%` معمم).
- **مهارات المراجعة والتصميم الهندسي `egm-*` (`7` داخل `skills/`):**
  - `egm-bootstrap`, `egm-brainstorm`, `egm-draft`, `egm-drift-report`, `egm-resolve`, `egm-review`, `egm-review-loop`.
- **مهارات قواعد البيانات والخدمات السحابية `neon*` (`7` داخل `skills/`):**
  - `neon`, `neon-ai-gateway`, `neon-auth`, `neon-functions`, `neon-object-storage`, `neon-postgres`, `neon-realtime`.
- **مسارات العمل الإضافية (`2` في `workflows/`):** `00-architect-sre.md` · `00-bolla-constitution.md`.
- **ملفات القواعد (`3` في `rules/`):** `arabic_keyboard_shortcuts.md` (بمسارات `%LOCALAPPDATA%` و`%APPDATA%` معمّمة) · `dastoor_bolla_architect_sre.md` · `egm_protocol.md`.
- **قالب القواعد العامة:** [`GEMINI.template.md`](./GEMINI.template.md) — منزوع التوكنات والمسارات المحلية (استبدل `<YOUR_TELEGRAM_*>` بمفاتيحك على الجهاز الجديد فقط).

---

## 🚀 التثبيت على أي جهاز جديد

- **تثبيت Lock360 فقط (الوضع الافتراضي الخفيف):** يستخدم `-All` / `--all`.
- **تثبيت الحزمة الشاملة الكاملة (`24` مهارة + `3` workflows + `3` rules + بذور `GEMINI.md` لو مش موجود):**

</div>

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\install.ps1 -All -WithPack
```

**macOS / Linux:**
```bash
bash scripts/install.sh --all --with-pack
```

<div dir="rtl">

- **ملاحظة أمان التحديث:** لو `GEMINI.md` موجود مسبقاً على جهازك، المثبّت **لا يمسح** توكناتك أو قواعدك الحالية؛ بيحدّث فقط كتلة `<!-- LOCK360_START --> ... <!-- LOCK360_END -->`، ويستخدم `GEMINI.template.md` كبداية فقط لو الملف مش موجود أصلاً.
- **إلغاء تثبيت الحزمة بأمان (يحفظ نسخة احتياطية قبل الحذف):**
  - Windows: `powershell -ExecutionPolicy Bypass -File scripts\install.ps1 -Uninstall -WithPack`
  - macOS / Linux: `bash scripts/install.sh --uninstall --with-pack`

</div>
