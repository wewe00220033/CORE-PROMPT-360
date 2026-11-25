# 🧩 `platforms/` — تثبيت Lock360 `v3.1` على كل منصة

> **الغرض:** نفس القاعدة ذات الأسطر الأربعة (`L1 Auto-Guard` + `L2 / L3`) معبّأة بصيغة كل أداة، بمسارات محمولة `~/...` وروابط `raw` مثبّتة على `v3.1`. النواة نفسها لا تتغير: المصدر الوحيد هو [`../gist/01-CORE-PROMPT-360-v3.md`](../gist/01-CORE-PROMPT-360-v3.md).

## 📍 اختر منصتك

- **Antigravity** ← [`antigravity/README.md`](./antigravity/README.md) — تثبيت كـ Skill عبر `scripts/install.ps1` / `install.sh` + الأسطر الأربعة في `GEMINI.md` تلقائياً. المسار: `~/.gemini/config/skills/00-lock360-zero-gaps/`.
- **OpenCode** ← [`opencode/README.md`](./opencode/README.md) + [`opencode/AGENTS.md.snippet`](./opencode/AGENTS.md.snippet) — آلياً بـ `--opencode` / `-OpenCode` (المهارة في `~/.config/opencode/skills/` + الكتلة في `~/.config/opencode/AGENTS.md`) أو يدوياً باللصق.
- **Claude Code** ← [`claude-code/README.md`](./claude-code/README.md) + [`claude-code/CLAUDE.md.snippet`](./claude-code/CLAUDE.md.snippet) — يُلصق في `CLAUDE.md` (المشروع أو `~/.claude/CLAUDE.md`)؛ والمهارات في `~/.claude/skills/` (OpenCode يقرأها أيضاً كتوافق).
- **Codex CLI** ← نفس [`opencode/AGENTS.md.snippet`](./opencode/AGENTS.md.snippet) يُلصق في `AGENTS.md` بجذر المشروع أو `~/.codex/AGENTS.md`؛ والمهارات بمسار `.agents/skills/` (مقروء من OpenCode أيضاً).
- **Cursor** ← [`cursor/README.md`](./cursor/README.md) + [`cursor/lock360.mdc`](./cursor/lock360.mdc) — قاعدة مشروع في `.cursor/rules/`.
- **Windsurf** ← الصق [`opencode/AGENTS.md.snippet`](./opencode/AGENTS.md.snippet) في `.windsurf/rules/lock360.md` (قاعدة مشروع) أو في القواعد العامة من الإعدادات؛ ⚠️ [مستنتج] أسماء المسارات قد تتغير بين الإصدارات.
- **ChatGPT (ويب)** ← [`chatgpt/custom-instructions.md`](./chatgpt/custom-instructions.md) — كتلتا Custom Instructions.
- **أي AI آخر (Gemini Web / DeepSeek / Kimi / Mistral / ...)** ← [`generic/ANY-AI.md`](./generic/ANY-AI.md) + [`../prompts/WEAK-MODEL-BOOSTER.md`](../prompts/WEAK-MODEL-BOOSTER.md) للموديلات الضعيفة + كتل النسخ الجاهزة في [`../prompts/QUICK-START.md`](../prompts/QUICK-START.md).

## 🧭 القاعدة المشتركة (ما تعنيه الأسطر الأربعة)

1. **المصدر الموحد:** أين توجد المهارة والنواة والـ workflow على هذا الجهاز.
2. **`L1 Auto-Guard` ⬅ ترس `P`:** بعد أي عمل غير تافه راجع 4 بوابات (المتبقي والحدود · أمان التسليم والتزامن · الدليل بعد آخر تعديل · الاستيضاح بدل التخمين).
3. **`L2 / L3` ⬅ أتراس `S / M / L`:** عند الكلمات المفتاحية (`قفّل 360`، `بالضبة والمفتاح`، `1600°/10000°`، `/lock360`) حمّل النواة ونفّذ الترس المناسب، ومرّر المخرج على `scripts/lock360.py audit` قبل الإغلاق.
4. **`RTL-Safe`:** بلا جداول `| col |` في الشات — قوائم وكروت رأسية فقط.

> المنصات التي تقرأ الروابط مباشرة تستطيع الاكتفاء برابط النواة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/01-CORE-PROMPT-360-v3.md`
