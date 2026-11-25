# 📡 دليل حزمة الغيست — النسخ المباشر بدون تثبيت (`gist/ — v3.1`)

> لو بتشتغل مباشرة على ChatGPT / Claude / Gemini / DeepSeek Web من غير ما تثبت المهارة على جهازك: ده مسارك السريع.

## 📁 ماذا داخل `gist/`؟

1. **[`01-CORE-PROMPT-360-v3.md`](./01-CORE-PROMPT-360-v3.md)** *(المصدر الرسمي الكامل `v3.1`)*: المنهج بـ `16` مرحلة، بوابة الصدق `[✅/⚠️/❓]`، ملف القارئ ثلاثي المحاور (`👤 القارئ` + `بالبلدي:`)، عقد الأسئلة `Q-Contract` (`HOLD / GO`)، الناقد الصريح `3.15`، والخلاصة المنظمة `3.16`. *(ملاحظة: [`01-CORE-PROMPT-360-v2.md`](./01-CORE-PROMPT-360-v2.md) محفوظ كـ Redirect Stub فقط للتوافق مع الروابط القديمة).*
2. **[`02-LENSES.md`](./02-LENSES.md)**: 7 عدسات تخصصية جاهزة للصق في قسم `[5]` (برمجة، قرارات حياتية، تفاوض، مال، دينية مشروطة، صحة، ميدان). *العدسة 5 معزولة ولا تُحمَّل إلا في الأسئلة الدينية الصريحة.*
3. **[`03-EXAMPLES.md`](./03-EXAMPLES.md)**: أمثلة عملية كاملة لكل ترس (`S / L / P`) + حوار جولتين `Q-Contract` + ترقية `/patch-360`.
4. **[`04-CHANGELOG.md`](./04-CHANGELOG.md)**: السجل التاريخي لكل إصدار (بما فيه توثيق `v3.1`).

---

## 🔗 روابط `raw` المثبّتة (`v3.1` لا تتغير)

- **النواة الكاملة (`v3.1`):** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/01-CORE-PROMPT-360-v3.md`
- **مكتبة العدسات:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/02-LENSES.md`
- **الأمثلة العملية:** `https://raw.githubusercontent.com/wewe00220033/CORE-PROMPT-360/v3.1/gist/03-EXAMPLES.md`
- **ملاحظة:** لثبات الأتمتة والمشاريع اعتمد وسم الإصدار (`/v3.1/`) أو رقم commit بدلاً من `/main/`.

---

## ⚡ كتل التفعيل السريعة
- **ترس `S` / `M` / `L` جاهزة للنسخ:** [`../prompts/QUICK-START.md`](../prompts/QUICK-START.md)
- **للموديلات الخفيفة:** الصق [`CORE-MINI v3.1`](./01-CORE-PROMPT-360-v3.md#L139) أو اتبع خطوات [`../prompts/WEAK-MODEL-BOOSTER.md`](../prompts/WEAK-MODEL-BOOSTER.md).
- **أمر الترقية السريع:** اكتب `/patch-360` + الثغرة التي واجهتك لتوليد إضافة في `[7] Extension Slots` وتحديث `04-CHANGELOG.md`.
