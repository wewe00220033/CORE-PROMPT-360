# 🔒 بروتوكول التقفيل الشامل 360° (`v3.1 — Adapter`)

> هذا الملف مسار استدعاء سريع (`/00-lock360-zero-gaps`) مرتبط بنفس القواعد الحتمية في [`../SKILL.md`](../SKILL.md).

## أوامر التنفيذ الفورية
*(على Windows استخدم `python -X utf8` بدلاً من `python3` لتفادي اختصار Store الوهمي).*

- **التوجيه الحتمي:** `python3 scripts/lock360.py route --text "<الطلب>"`
- **مراجعة ما بعد العمل (`Gear P`):** بوابات المتبقي والثغرات، التسليم ونوافذ الانتقال، الدليل الفعلي بعد آخر تعديل، وبوابة `Q-Contract`.
- **تدقيق المخرج قبل الإغلاق (`L2/L3`):** `python3 scripts/lock360.py audit --output <ردك> --gear <S|M|L> --request <الطلب>`
- **بوابة الجولات المتعددة:** `qa-ledger` و `qa-audit` (`HOLD / GO`).
- **بوابة النشر والإطلاق:** `deploy-gate --output <خطة_النشر>` (`DG-01..07`).

## المراجع المربوطة
- النواة الموحدة (`16` مرحلة): [`../gist/01-CORE-PROMPT-360-v3.md`](../gist/01-CORE-PROMPT-360-v3.md)
- العدسات التخصصية: [`../gist/02-LENSES.md`](../gist/02-LENSES.md) · الأمثلة: [`../gist/03-EXAMPLES.md`](../gist/03-EXAMPLES.md)
- القوالب و`Q-Contract`: [`../references/LOCK360_TEMPLATES.md`](../references/LOCK360_TEMPLATES.md) · اللهجات: [`../references/TONE_GLOSSARY.md`](../references/TONE_GLOSSARY.md)
- النشر والتراجع: [`../references/RELEASE_DEPLOY_ROLLBACK.md`](../references/RELEASE_DEPLOY_ROLLBACK.md)
- التكامل الاختياري مع المهارات المجاورة: `02-planning-system` · `egm-review` · `00-bolla-constitution` · `01-micro-tasker` · `00-architect-sre` · `00-evidence-inspector` · `00-reverse-engineer` · `everything-search`.
