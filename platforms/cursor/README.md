# 🔵 Cursor — Lock360 `v2.7` كقاعدة مشروع (`.mdc`)

> **الاصطلاح (مؤكد من توثيق Cursor):** قواعد المشروع تعيش في `.cursor/rules/` بامتداد `.mdc` إلزامياً (ملف `.md` عادي يُتجاهل). الـ frontmatter يتحكم في التفعيل: `alwaysApply: false` + `description` ⬅ الوكيل يقرر التفعيل حسب الوصف (`Apply Intelligently`)؛ أو `globs` ⬅ تفعيل عند فتح ملفات مطابقة. كما يدعم Cursor ملف `AGENTS.md` عادي في الجذر كبديل بسيط. التوثيق: `https://cursor.com/docs/context/rules`

## الخطوات

1. انسخ [`lock360.mdc`](./lock360.mdc) إلى مشروعك:
```bash
mkdir -p .cursor/rules
cp ~/CORE-PROMPT-360/platforms/cursor/lock360.mdc .cursor/rules/lock360.mdc
```
2. الملف مضبوط على `alwaysApply: false` مع `description` ⬅ يُفعَّل عندما يرى الوكيل أن الطلب يخص التقفيل الشامل، أو يدوياً بكتابة `@lock360` في الشات.
3. *(اختياري)* لتفعيله دائماً غيّر `alwaysApply` إلى `true`؛ ولتفعيله على ملفات بعينها أضف `globs:` (مثلاً `src/**`).

## بديل أبسط

الصق محتوى [`../opencode/AGENTS.md.snippet`](../opencode/AGENTS.md.snippet) في `AGENTS.md` بجذر المشروع — Cursor يقرأه بدون frontmatter.

> النواة الكاملة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.7/gist/01-CORE-PROMPT-360-v2.md`
