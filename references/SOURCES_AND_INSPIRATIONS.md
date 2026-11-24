# 📚 المصادر والإلهامات — Sources & Inspirations (`v2.9`)

> **السياسة:** نأخذ **الأفكار العامة** ونعيد صياغتها بلغتنا داخل سياق Lock360؛ صفر نسخ حرفي لنص أو كود محمي؛ نذكر المصدر عند اقتباس هيكل أو فكرة مميزة؛ وأي مهارة أو أداة خارجية تُراجع أمنياً قبل الدمج (سلسلة التوريد). كل بند أدناه يذكر **أين دخل** في `v2.9`.

---

## 1) السلامة الهندسية والمنظمات عالية الموثوقية

- **James Reason — نموذج الجبنة السويسرية (`Human Error`, 1990; `Managing the Risks of Organizational Accidents`, 1997):** الحوادث = اصطفاف أعطال نشطة مع **شروط كامنة** موجودة قبل الحادث عبر طبقات دفاع متعددة. ⬅ سطر *"سجل الشروط الكامنة"* في `3.7` + الفحصان `A-LATENT` و`A-DEPTH-1`.
- **Nancy Leveson — MIT STPA (`Engineering a Safer World`, 2011; `STPA Handbook`, 2018):** السلامة مشكلة تحكم؛ **أفعال التحكم غير الآمنة** 4 أنماط: لم يُقدَّم / قُدِّم بشكل غير آمن / توقيت أو ترتيب خاطئ / توقف مبكراً أو استمر طويلاً. ⬅ تصنيف مصيدة النمل: `A-STAGE-MISSING` (1) · `A-STAGE-EMPTY` (2) · `A-ORDER`, `A-CONF-DUP` (3) · `F-GEAR-DOWNSHIFT` (4).
- **Karl Weick & Kathleen Sutcliffe — HRO (`Managing the Unexpected`, 2001/2015):** الانشغال بالفشل، رفض التبسيط، الحساسية للعمليات، الالتزام بالمرونة، الاحترام للخبرة لا للرتبة. ⬅ رفض التبسيط = `F-GEAR-DOWNSHIFT`؛ احترام الخبرة = `F-EXPERT-ESCALATION` كفحص حتمي لا توصية.
- **AIAG & VDA — `FMEA Handbook` (2019):** الخطورة × الاحتمال × **صعوبة الاكتشاف**، واستبدال `RPN` بـ **أولوية الفعل `AP (H/M/L)`** لأن ضرب الأرقام يخفي الحالات الحرجة. ⬅ حقل `AP` في بطاقة `3.10` و`LOCK360_TEMPLATES §5` + الفحص `A-FMEA-AP`.
- **Gary Klein — Pre-Mortem (`Performing a Project Premortem`, HBR 2007):** افترض أن المشروع فشل وابحث عن الأسباب قبل البدء. ⬅ `3.11` (موجود منذ الإصدارات الأولى) وبوابة `Pre-Mortem` كإشارة `L1` خفيفة.

## 2) هندسة مهارات الوكلاء

- **Agent Skills — المواصفة المفتوحة (`agentskills.io/specification`, 2025):** `SKILL.md` + `scripts/ references/ assets/`، **الكشف التدريجي** في 3 طبقات (كتالوج ≈ 100 توكن ⬅ تعليمات < 500 سطر ⬅ موارد عند الحاجة)، `description` هي الزناد، و*"قل للوكيل متى يحمّل كل ملف"*. ⬅ `SKILL.md` ≤ 115 سطراً بحقل `license` وقسم *"المراجع ومتى تحمّل كل واحد"* + اختبار `skill_size`.
- **OpenCode V2 — `docs/skills` و`docs/rules`:** المهارات العامة في `~/.config/opencode/skills/<id>/SKILL.md` (المعرّف = اسم المجلد)، والتعليمات العامة في `~/.config/opencode/AGENTS.md`؛ ملفات `opencode.json` و`cli.json` تكوين لا يُلمس. ⬅ خيار `--opencode` في المثبّتات.
- **Jesse Vincent — `obra/superpowers` (2025/2026):** مهارتا `verification-before-completion` (*القانون الحديدي*: لا ادعاء اكتمال بدون دليل تحقق طازج؛ الكلمات الحمراء `should / probably / Looks good`؛ جدول التبريرات) و`systematic-debugging` (جذر السبب قبل الإصلاح؛ فرضية واحدة؛ **3 إصلاحات فاشلة = مشكلة معمارية**؛ اختبار الانحدار أحمر-أخضر). ⬅ القانون الحديدي في `[0]`، شبكة الدبان `F-RATIONALIZE` / `F-FALSE-DONE`، قاعدة الـ 3 في عدسة البرمجة، ومبدأ أحمر-أخضر في `tests/eval_cases.json`.

## 3) التحقق والموديلات الصغيرة

- **Zhang et al. — `Small Language Models Need Strong Verifiers to Self-Correct Reasoning` (Findings of ACL 2024):** الموديلات ≤ 13B تتدهور عند التحقق الذاتي بالبرومبت فقط؛ المكسب يظهر مع مُحقِّق قوي أو مُدرَّب. ⬅ المُحقِّق الأساسي للموديل الضعيف = `lock360.py audit` لا الموديل نفسه.
- **Kang, Jeong & Cho — `T1: Tool-Integrated Verification for Test-Time Compute Scaling in Small Language Models` (ICLR 2026):** الموديل الصغير يفشل حتى في التحقق من حسابات بسيطة؛ دمج أداة خارجية ضروري لا مجرد مفيد. ⬅ فلسفة *"المحرك الحتمي هو المُحقِّق"*.
- **Dhuliawala et al. — `Chain-of-Verification Reduces Hallucination in Large Language Models` (Findings of ACL 2024):** مسودة ⬅ خطة أسئلة تحقق ⬅ إجابات **مستقلة** (`factored`) ⬅ نسخة نهائية. ⬅ تمريرة Pass-2 البديلة في `WEAK-MODEL-BOOSTER.md` عند غياب Python.
- **`When Does Verification Pay Off? A Closer Look at LLMs as Solution Verifiers` (arXiv 2025):** قِس ربح المُحقِّق لا دقته؛ المهام الهيكلية أسهل تحققاً من الاستدعاء؛ فضّل مُحقِّقاً يفكر بشكل مختلف عن الحلّال. ⬅ تبرير فصل الحلّال (LLM) عن المُحقِّق (كود حتمي).

## 4) ما أُخذ من حزم التقييم الداخلية

- **المسودة التقييمية السابقة (وكيل خارجي):** بنك الكلمات المفتاحية الموسّع، قائمة `Auto-Guard`، بطاقة `FMEA` بسطر `Tripwire`، تحذير الأنماط الموازية و`Tree Kill`. ⬅ مدمجة في الإصدار السابق مباشرة.
- **فرع `hardening/zero-gaps-max-pass`:** فكرة حدود الصدق، تصنيف بوابات `Trigger / Compliance / Boundary / Outcome`، سطح التهديد A–F، مسار `ANY-AI`. ⬅ حُوّلت في `v2.9` من نثر إلى فحوص حتمية وحالات اختبار وملفات مراجع مُعاد كتابتها.

---

> **ما لا نعتمد عليه:** مدونات تسويقية أو قوائم `awesome` كمرجع منهجي؛ تُذكر فقط لمراقبة اتجاهات المجتمع.
