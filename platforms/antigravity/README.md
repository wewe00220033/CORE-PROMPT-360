# 🟢 Antigravity — تثبيت Lock360 `v2.9` كـ Skill

> Antigravity هو البيئة الأصلية للحزمة: `SKILL.md` في جذر المستودع هو المحوّل (`Adapter`) الذي يحدد متى يعمل كل ترس. الدليل الكامل في [`../../README.md`](../../README.md).

## 1) أمر واحد (المستحسن) — Skill + Workflow + قاعدة `GEMINI.md`

**Windows (PowerShell):**
```powershell
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git "$HOME\CORE-PROMPT-360"
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -All
```

**macOS / Linux:**
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
bash ~/CORE-PROMPT-360/scripts/install.sh --all
```

ماذا يفعل المثبّت ([`install.ps1`](../../scripts/install.ps1) / [`install.sh`](../../scripts/install.sh)):
- ينسخ المهارة إلى `~/.gemini/config/skills/00-lock360-zero-gaps/` (مع نسخة احتياطية `.backup_lock360_*` لو كانت موجودة).
- ينسخ `workflows/00-lock360-zero-gaps.md` إلى `~/.gemini/config/workflows/` لتفعيل `/lock360`.
- يضيف الأسطر الأربعة أدناه داخل `~/.gemini/GEMINI.md` بين وسمي `LOCK360_START/END` فقط (يحفظ `.bak` ولا يلمس أي قاعدة أخرى).
- الإلغاء الآمن: `-Uninstall` / `--uninstall` يزيل الكتلة والمجلدات ويحتفظ بنسخة احتياطية.

## 2) يدوياً — الأسطر الأربعة في `~/.gemini/GEMINI.md`

لو ثبّت المهارة بالاستنساخ المباشر (`git clone` إلى مجلد المهارات) بدون المثبّت، الصق هذه الكتلة في `~/.gemini/GEMINI.md`:

```markdown
<!-- LOCK360_START -->
## 🔒 بروتوكول التقفيل الشامل 360° (Lock360 v2.9)

- **المصدر الموحد:** `00-lock360-zero-gaps` (`~/.gemini/config/skills/00-lock360-zero-gaps/SKILL.md` · `gist/01-CORE-PROMPT-360-v2.md` · `workflows/00-lock360-zero-gaps.md`).
- **`L1 Auto-Guard` (`P` تلقائياً بعد الأعمال غير التافهة):** راجع المتبقي/الحدود، أمان التسليم والتزامن، الدليل القاطع بعد آخر تعديل، واسأل المستخدم عن أي غموض بدل التخمين.
- **`L2 / L3`:** عند طلب قفّل 360 / بالضبة والمفتاح / 1600°-10000° / `/lock360` حمّل المهارة ونفّذ الترس المناسب (`S / M / L`)، مع الالتزام بقاعدة `RTL-Safe` (بلا جداول `| col |` في الشات).
<!-- LOCK360_END -->
```

## 3) التحقق

- اكتب في الشات: `قفّل 360 على: [موضوع تجريبي]` ⬅ يجب أن يبدأ الرد من `3.1` بترس مُعلن.
- بعد تعديل متعدد الملفات ⬅ يجب أن يظهر فحص `P` ذو البوابات الأربع تلقائياً.

> رابط النواة المثبّت: `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.9/gist/01-CORE-PROMPT-360-v2.md`
