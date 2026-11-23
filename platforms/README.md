# 🧩 `platforms/` — تثبيت Lock360 `v2.5` على كل منصة

> **الغرض:** نفس القاعدة ذات الأسطر الأربعة (`L1 Auto-Guard` + `L2 / L3`) معبّأة بصيغة كل أداة، بمسارات محمولة `~/...` وروابط `raw` مثبّتة على `v2.5`. النواة نفسها لا تتغير: المصدر الوحيد هو [`../gist/01-CORE-PROMPT-360-v2.md`](../gist/01-CORE-PROMPT-360-v2.md).

## 📍 اختر منصتك

- **Antigravity** ← [`antigravity/README.md`](./antigravity/README.md) — تثبيت كـ Skill عبر `scripts/install.ps1` / `install.sh` + الأسطر الأربعة في `GEMINI.md` تلقائياً.
- **OpenCode** ← [`opencode/README.md`](./opencode/README.md) + [`opencode/AGENTS.md.snippet`](./opencode/AGENTS.md.snippet) — يُلصق في `AGENTS.md` (جذر المشروع أو `~/.config/opencode/AGENTS.md`).
- **Claude Code** ← [`claude-code/README.md`](./claude-code/README.md) + [`claude-code/CLAUDE.md.snippet`](./claude-code/CLAUDE.md.snippet) — يُلصق في `CLAUDE.md` (المشروع أو `~/.claude/CLAUDE.md`).
- **Cursor** ← [`cursor/README.md`](./cursor/README.md) + [`cursor/lock360.mdc`](./cursor/lock360.mdc) — قاعدة مشروع في `.cursor/rules/`.
- **ChatGPT (ويب)** ← [`chatgpt/custom-instructions.md`](./chatgpt/custom-instructions.md) — كتلتا Custom Instructions.
- **أي AI آخر (Gemini Web / DeepSeek / ...)** ← كتل النسخ الجاهزة في [`../prompts/QUICK-START.md`](../prompts/QUICK-START.md).

## 🧭 القاعدة المشتركة (ما تعنيه الأسطر الأربعة)

1. **المصدر الموحد:** أين توجد المهارة والنواة والـ workflow على هذا الجهاز.
2. **`L1 Auto-Guard` ⬅ ترس `P`:** بعد أي عمل غير تافه راجع 4 بوابات (المتبقي والحدود · أمان التسليم والتزامن · الدليل بعد آخر تعديل · الاستيضاح بدل التخمين).
3. **`L2 / L3` ⬅ أتراس `S / M / L`:** عند الكلمات المفتاحية (`قفّل 360`، `بالضبة والمفتاح`، `1600°/10000°`، `/lock360`) حمّل النواة ونفّذ الترس المناسب.
4. **`RTL-Safe`:** بلا جداول `| col |` في الشات — قوائم وكروت رأسية فقط.

> المنصات التي تقرأ الروابط مباشرة تستطيع الاكتفاء برابط النواة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.5/gist/01-CORE-PROMPT-360-v2.md`
