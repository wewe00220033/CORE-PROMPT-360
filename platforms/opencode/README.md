# 🟣 OpenCode — Lock360 `v3.1` كـ Skill + `AGENTS.md`

> **الاصطلاح (مؤكد من توثيق OpenCode V2):** المهارات العامة تُكتشف تلقائياً من `~/.config/opencode/skills/<id>/SKILL.md` (المعرّف = اسم المجلد)، والتعليمات العامة من `~/.config/opencode/AGENTS.md` ثم ملفات `AGENTS.md` في المشروع. وفي أي مجلد بلا `AGENTS.md` يقرأ `CLAUDE.md` كبديل. التوثيق: `https://opencode.ai/docs/skills` · `https://opencode.ai/docs/rules`

## الطريقة الآلية (الموصى بها)

1. استنسخ المستودع في مكان ثابت:
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
```
2. ثبّت المهارة + الكتلة في `AGENTS.md` (يمكن دمجها مع `--all` لتثبيت Antigravity في نفس الأمر):

**macOS / Linux:**
```bash
bash ~/CORE-PROMPT-360/scripts/install.sh --opencode
# إلغاء التثبيت (نسخة احتياطية ثم إزالة المجلد والكتلة فقط):
bash ~/CORE-PROMPT-360/scripts/install.sh --uninstall --opencode
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -OpenCode
# إلغاء التثبيت:
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -Uninstall -OpenCode
```

- المثبّت ينسخ حمولة المهارة (`SKILL.md` · `README.md` · `gist/` · `references/` · `prompts/` · `tests/` · `scripts/lock360.py`) إلى `~/.config/opencode/skills/00-lock360-zero-gaps/` (يحترم `XDG_CONFIG_HOME` إن ضُبط؛ أو مرّر `--opencode-root DIR` / `-OpenCodeRoot DIR`).
- يحدّث **فقط** كتلة `<!-- LOCK360_START --> ... <!-- LOCK360_END -->` في `~/.config/opencode/AGENTS.md` ويحفظ `.bak` ويحافظ على كل سطورك الأخرى.
- **لا يلمس أبداً** `opencode.json` / `opencode.jsonc` / `cli.json`؛ المهارة تُكتشف من المسار بلا إضافة في `skills[]`. والتغييرات تُحمَّل حياً دون إعادة تشغيل.
- ⚠️ **أسبقية المشروع:** لو مشروعك فيه `.opencode/skills/00-lock360-zero-gaps/` فهي تغلب النسخة العامة (المعرّف نفسه) — لا تثبّت الاثنتين إلا عمداً.

## الطريقة اليدوية

1. الصق محتوى [`AGENTS.md.snippet`](./AGENTS.md.snippet) في `~/.config/opencode/AGENTS.md` (كل المشاريع) **أو** في `AGENTS.md` بجذر مشروع واحد.
2. انسخ المستودع (أو `SKILL.md` + `gist/` + `references/` + `prompts/` + `tests/` + `scripts/lock360.py`) إلى `~/.config/opencode/skills/00-lock360-zero-gaps/`.
3. *(اختياري)* بدل اللصق، أضف الملف إلى `instructions` في `opencode.jsonc` بنفسك:
```jsonc
{
  "instructions": ["~/CORE-PROMPT-360/platforms/opencode/AGENTS.md.snippet"]
}
```

## ملاحظات

- داخل OpenCode: `@00-lock360-zero-gaps` يحمّل المهارة صراحة، و`python3 ~/.config/opencode/skills/00-lock360-zero-gaps/scripts/lock360.py audit --output <رد> --gear <X>` يفحص أي مخرج قبل الإغلاق *(وعلى Windows استخدم `python -X utf8`)*.
- النواة الكاملة لقراءتها مباشرة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/01-CORE-PROMPT-360-v3.md`
