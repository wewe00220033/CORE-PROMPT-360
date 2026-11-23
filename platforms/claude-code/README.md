# 🟠 Claude Code — Lock360 `v2.4` عبر `CLAUDE.md`

> **الاصطلاح (مؤكد من توثيق Claude Code):** يقرأ `./CLAUDE.md` أو `./.claude/CLAUDE.md` للمشروع، و`~/.claude/CLAUDE.md` لكل المشاريع، و`CLAUDE.local.md` للتفضيلات الشخصية غير المرفوعة. ويدعم استيراد ملفات بصيغة `@path`. كما يقرأ `AGENTS.md` مباشرةً عندما لا يوجد `CLAUDE.md` في المسار. التوثيق: `https://code.claude.com/docs/en/memory`

## الخطوات

1. استنسخ المستودع:
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
```
2. اختر طريقة واحدة:
   - **لصق:** انسخ محتوى [`CLAUDE.md.snippet`](./CLAUDE.md.snippet) إلى `~/.claude/CLAUDE.md` (عام) أو `CLAUDE.md` في جذر المشروع.
   - **استيراد:** أضف سطراً واحداً في `CLAUDE.md`:
```markdown
@~/CORE-PROMPT-360/platforms/claude-code/CLAUDE.md.snippet
```
   *(الاستيراد من خارج مجلد العمل يطلب موافقة مرة واحدة لكل مشروع — مؤكد من التوثيق).*

3. تحقق بـ `/context all` وتأكد أن الملف ظاهر تحت **Memory files**.

## ملاحظات

- لو مشروعك يستخدم `AGENTS.md` أصلاً، يكفي لصق نفس الـ snippet هناك؛ Claude Code يقرأه عند غياب `CLAUDE.md`.
- النواة الكاملة: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.4/gist/01-CORE-PROMPT-360-v2.md`
