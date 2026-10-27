# CCS (Implementation of UPS under NPS) Rules, 2025 — Detailed Hinglish File Series

Ye folder aapke UPS study-file project ka source hai. Har batch ek **self-contained detailed HTML file**
(voiced narration + synced subtitles ke saath) ke roop me banta hai.

| Batch | Content | Rules | Status |
|---|---|---|---|
| **01** | Preamble + Chapter I — short title, application, 32 definitions | 1–3 | **Ready (doc)**; audio pending voice selection |
| 02 | Chapter II — enrolment, emoluments, contributions, delayed deposit, investment, Rule 10 option, switch | 4–11 | Queued |
| 03 | Chapter III — superannuation, VR, FR 56, resignation, absorption, invalidation, disablement, death | 12–19 | Queued |
| 04 | Chapter IV — compulsory retirement, dismissal/removal, pending proceedings, spouse debarment | 20–23 | Queued |
| 05 | Chapter V–VI — retirement list, no-demand certificate, claim, deputation, oversight, interpretation, relax, repeal + Forms 1, 2, Format 1 | 24–33 + Forms | Queued |

## Har file me kya hota hai (template = aapke screenshot jaisa)

* Top status strip: `MODULE 0x/05` · source chip · voice chip · verified date + batch counter
* Progress bar (scroll ke saath bharta hai)
* Crumb pill (`G.S.R. 599(E) · 02.09.2025 · …`)
* H1 + lede
* **4 idea-cards** row (blue / green / teal / purple) — screenshot ki tarah
* Clause rows: left label chip + tag (Farz · Shart · Ghadi · Natija · Paribhasha · Apwad · Vivek), right me
  Gazette limb (mono box) + Hinglish explanation
* **Har explanation ke baad** real-life example ya step-wise numerical (`Step 1 / Step 2 / = calculation / Answer`)
* Amber **TRAP** bar (screenshot ke "CLASSIC UPSC TRAP" jaisa)
* Green **Naya / Missing-info** boxes — rules me na hone wali, par zaroori non-obsolete baatein, source ke naam ke saath
* Voice + subtitle strip

## Narration + subtitles

* `dist/narration/BATCH_01/clip_01.txt … clip_10.txt` — exact TTS text (pronunciation-fixed: `G.S.R.` → `G S R`, `₹` → `rupees`, rule numbers expanded)
* `dist/BATCH_01.srt` — sidecar subtitles, **clip ke asli audio duration** se calculate hui timings (proportional cue split inside each clip)
* `dist/BATCH_01_player.html` — screenshot-jaisa player: cards + narration + karaoke subtitle highlight
* `dist/BATCH_01_timing.json` — machine-readable cue table

Pipeline:

```bash
python3 build/build.py doc        # detailed HTML
python3 build/build.py narration  # TTS text + script
# ... voice layer clip_XX.mp3 yahan rakhta hai ...
python3 build/build.py audio      # mp3 duration -> SRT + timing.json + player
```

## Sources (verified 27 Oct 2026)

1. **G.S.R. 599(E) dated 02.09.2025** — Gazette of India, Extraordinary, Part II, Sec. 3(i), No. 555 —
   CCS (Implementation of UPS under NPS) Rules, 2025. Rule text is quoted verbatim (including printed quirks
   `shall means`, `it’s receipt`, `wedged`, `fifty- four thousand`).
2. **UPS Notification F. No. FX-1/3/2024-PR dated 24.01.2025** (DFS, Ministry of Finance).
3. **PFRDA (Operationalisation of UPS under NPS) Regulations, 2025** — 19.03.2025; amended by PFRDA gazette
   notification No. PFRDA-16/07/0001/2025-SUP-CG dated 23.12.2025 (published 27.12.2025).
4. **DoPPW O.M. No. 57/01/2025-P&PW(B)/UPS/10498 dated 18.06.2025** — retirement + death gratuity to UPS subscribers.
5. **Option cut-off extension chain** — 30.06.2025 → 30.09.2025 (DFS, 23.06.2025 / 01.07.2025) → **30.11.2025**
   (PFRDA circular dated 06.10.2025).
6. **Railway Services (Implementation of UPS under NPS) Rules, 2026** — G.S.R. 827(E) dated 16.09.2026
   (Gazette 21.09.2026) — Rule 2(a) ke Railway servants ke liye alag rulebook.
7. **CBDT O.M. dated 02.07.2025** — income-tax provisions (80CCD(1), (1B), (2), (3), (4); 10(12A), 10(12B)) UPS par mutatis mutandis.
8. DoPPW/PIB releases: switch facility (15.09.2025), voluntary retirement pro-rata (16.09.2025).

## Honest limitations

* Rule wording Gazette MD transcript se hai; **Gazette/India Code PDF se shabd-ba-shabd cross-check baaki hai** —
  exam answer me official PDF se confirm karein.
* PFRDA Amendment Regulations (27.12.2025) ka **text** padha nahi gaya; sirf existence aur date verified hai.
* Scheme ke numbers (50%, ₹10,000, 60%, 1/10th, 8.5%) PFRDA page/UPS notification se hain, **in Rules se nahi** —
  har jagah source label kiya gaya hai.
