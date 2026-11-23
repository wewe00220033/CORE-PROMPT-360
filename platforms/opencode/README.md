# 🟣 OpenCode — Lock360 `v2.4` عبر `AGENTS.md`

> **الاصطلاح (مؤكد من توثيق OpenCode):** OpenCode يقرأ `AGENTS.md` من جذر المشروع وكل مجلد أعلى حتى الـ home، بالإضافة إلى الملف العام `~/.config/opencode/AGENTS.md`. وفي أي مجلد بلا `AGENTS.md` يقرأ `CLAUDE.md` كبديل. التوثيق: `https://opencode.ai/docs/rules/`

## الخطوات

1. استنسخ المستودع في مكان ثابت:
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
```
2. الصق محتوى [`AGENTS.md.snippet`](./AGENTS.md.snippet) في:
   - `~/.config/opencode/AGENTS.md` ⬅ ليعمل في كل المشاريع، **أو**
   - `AGENTS.md` في جذر مشروع واحد ⬅ ليعمل في هذا المشروع فقط.
3. *(اختياري)* بدل اللصق، أضف الملف نفسه إلى `instructions` في `opencode.jsonc`:
```jsonc
{
  "instructions": ["~/CORE-PROMPT-360/platforms/opencode/AGENTS.md.snippet"]
}
```

## ملاحظات

- الـ snippet يشير إلى `~/CORE-PROMPT-360/SKILL.md`؛ لو استنسخت في مسار آخر عدّل السطر الأول فقط.
- OpenCode يكتشف تغيّر `AGENTS.md` أثناء الجلسة ويحدّث التعليمات قبل الطلب التالي (مؤكد من التوثيق).
- النواة الكاملة لقراءتها مباشرة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.4/gist/01-CORE-PROMPT-360-v2.md`
