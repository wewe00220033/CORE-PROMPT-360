<div dir="rtl">

# 🔒 CORE-PROMPT-360 — بروتوكول التقفيل الشامل 360° بالضبة والمفتاح (`v2.3`)

> **مستودع جاهز كـ Skill محمولة + نواة برومبت عالمية** لنقل منهجية `Lock360 v2.3` إلى **أي جهاز** (Windows / macOS / Linux) وأي أداة ذكاء اصطناعي (Antigravity / OpenCode / Claude / Gemini / ChatGPT / DeepSeek).
> *(ملاحظة: هذا الدليل خاص بالتثبيت والنشر على الأجهزة عبر Git؛ لاستخدام البرومبت بالنسخ اليدوي المباشر اقرأ [`gist/00-README.md`](./gist/00-README.md)).*

---

## 🌟 إيه اللي جوه الحزمة؟

- **`SKILL.md` (`00-lock360-zero-gaps`):** المحوّل القياسي للأتراس ومستويات التشغيل (`L1/L2/L3 ↔ P/S/M/L`) — يشتغل فوراً بمجرد وجود المجلد في مسار المهارات.
- **`gist/`:** النواة المحمولة المكتفية بذاتها ([`01-CORE-PROMPT-360-v2.md`](./gist/01-CORE-PROMPT-360-v2.md)) بـ `14` مرحلة + بوابة الصدق المضادة للمجاملة `[✅/⚠️/❓]` + `Explicit Non-Goals` + فيزياء الواقع والميكانيكا + نوع الباب + `Kill Switch / Pre-Mortem` + `8` أسئلة تصيّد سريعة + [`02-LENSES.md`](./gist/02-LENSES.md) (7 عدسات تخصصية) + [`03-EXAMPLES.md`](./gist/03-EXAMPLES.md) + [`04-CHANGELOG.md`](./gist/04-CHANGELOG.md).
- **`references/`:** مراجع `L3` التقنية ([`DOMAIN_MATRICES.md`](./references/DOMAIN_MATRICES.md)، [`ADVERSARIAL_CHECKLIST_360.md`](./references/ADVERSARIAL_CHECKLIST_360.md)، [`LOCK360_TEMPLATES.md`](./references/LOCK360_TEMPLATES.md)).
- **`workflows/00-lock360-zero-gaps.md`:** سير عمل `/lock360`.
- **`scripts/`:** مثبّت آمن لـ Windows ([`install.ps1`](./scripts/install.ps1)) وmacOS/Linux ([`install.sh`](./scripts/install.sh)) مع النسخ الاحتياطي وإلغاء التثبيت.

---

## 🚀 طرق التثبيت والاستخدام على أي جهاز

### 1️⃣ التثبيت المباشر كـ Skill في Antigravity (أمر واحد — يعمل فوراً)

> مهم: نحدّد اسم المجلد `00-lock360-zero-gaps` صراحةً عشان يطابق `name` داخل `SKILL.md`:

</div>

**Windows (PowerShell):**
```powershell
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git "$env:USERPROFILE\.gemini\config\skills\00-lock360-zero-gaps"
```

**macOS / Linux:**
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/.gemini/config/skills/00-lock360-zero-gaps
```

*(للتحديث لاحقاً على نفس الجهاز — Windows: `git -C "$env:USERPROFILE\.gemini\config\skills\00-lock360-zero-gaps" pull` · macOS/Linux: `git -C ~/.gemini/config/skills/00-lock360-zero-gaps pull`).*

> *ملاحظة: اختر **طريقة 1** أو **طريقة 2** فقط على الجهاز الواحد لتفادي نسختين لنفس المهارة.*

<div dir="rtl">

---

### 2️⃣ التثبيت الكامل مع `/lock360` والقاعدة العالمية المختصرة (`GEMINI.md`)

لو عايز تثبّت الـ Skill + الوورك فلو + الـ 4 أسطر الدائمة في `GEMINI.md` بشكل آمن (يحفظ نسخة احتياطية `.bak` ومش بيلمس أي قواعد تانية ليك):

</div>

**Windows (PowerShell):**
```powershell
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git "$HOME\CORE-PROMPT-360"
powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -All
```
*(لإلغاء التثبيت بأمان لاحقاً: `powershell -ExecutionPolicy Bypass -File "$HOME\CORE-PROMPT-360\scripts\install.ps1" -Uninstall`)*

**macOS / Linux:**
```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git ~/CORE-PROMPT-360
bash ~/CORE-PROMPT-360/scripts/install.sh --all
```
*(لإلغاء التثبيت لاحقاً: `bash ~/CORE-PROMPT-360/scripts/install.sh --uninstall`)*

<div dir="rtl">

---

### 3️⃣ التثبيت داخل مشروع واحد فقط (`.agents/skills/`)

</div>

```bash
git clone https://github.com/wewe00220033/CORE-PROMPT-360.git .agents/skills/00-lock360-zero-gaps
```

<div dir="rtl">

---

### 4️⃣ الاستخدام المباشر في ChatGPT / Claude / DeepSeek / Gemini Web

انسخ محتوى [`gist/01-CORE-PROMPT-360-v2.md`](./gist/01-CORE-PROMPT-360-v2.md) أو وجّه أي ذكاء اصطناعي لرابط `raw` المثبّت على الإصدار `v2.3`:

</div>

- **Core Prompt (`v2.3`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.3/gist/01-CORE-PROMPT-360-v2.md`
- **Plugin Lenses:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.3/gist/02-LENSES.md`
- **Examples (`P/S/M/L`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.3/gist/03-EXAMPLES.md`
- **Prompt Guide:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v2.3/gist/00-README.md`

<div dir="rtl">

---

## 🎚️ ملخص التفعيل والأتراس السريع

- **`🔍 P` (`L1 Auto-Guard`):** بوابة فحص ما بعد المهام غير التافهة (المتبقي والثغرات · أمان التسليم والتزامن · الدليل بعد آخر تعديل · بوابة الاستيضاح).
- **`⚡ S`:** قرار يومي قابل للرجوع (<= 450 كلمة تقريباً).
- **`🔧 M`:** مشروع أو خطة متوسطة (`L2 Full Lock360`).
- **`🏰 L` (`1600° / 10000°`):** نظام حرج أو قرار مصيري (الـ 14 مرحلة كاملة + العدسات + المراجع التقنية).

</div>
