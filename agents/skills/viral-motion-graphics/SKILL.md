---
name: viral-motion-graphics
description: Production-grade motion graphics and animation blueprints for high-retention tech explainer videos (Shorts and Long-form). Codifies the exact animation techniques, card designs, 3D perspective grids, real developer UI components, illustrated character rigs, angled slam stickers, and procedural sound design learned from viral motion graphics benchmarks. Use whenever creating animated explainer videos, kinetic tech cards, or replicating premium motion design.
---

# Viral Motion Graphics & Kinetic Tech Animation Skill

This skill provides production blueprints and design standards for high-retention tech explainer videos, replicating the premium animation quality seen in modern developer documentaries and viral technical Shorts.

---

## 1. Core Visual Archetypes

### Archetype A: The Developer 3D Grid & UI System (Video Benchmark 1)
- **Background:** Deep obsidian/midnight canvas (`#080C18` to `#16122E`) with a 3D perspective floor grid vanishing at the horizon (`perspective: 1000px`), dual ambient spotlights (warm amber/orange at top, electric cyan/purple at bottom), and floating dust particles.
- **Hero Cards:** Real developer interfaces:
  - **macOS Terminal Window:** Dark window with authentic red/yellow/green control buttons, `terminal` title bar, command line prompt (`~ $ claude`), boxed tool banner, and live typed command with blinking block cursor.
  - **GitHub Repository Card:** Container with neon orange/cyan border glow, Octocat SVG icon, author avatar image, repo name in bold white, description, star/fork counts (`★ 41.4k  ⑂ 5.6k`), and MIT badge.
  - **Auto Model Switching & Session Failover:**
    1. Active model card (`MODEL 1`) with green status dot.
    2. Session limit progress bar filling dynamically from 0% &rarr; 65% (amber) &rarr; 100% (red).
    3. 3D angled red sticker (`LIMIT REACHED`) rotated -9° slamming down with bounce physics and procedural `slam` audio thud.
    4. Downward animated yellow arrow pointing to `MODEL 2` with green `"AUTO SWITCH"` pill.
  - **Large Metric Callouts:** Enormous bold numbers with quartic count-up easing (e.g. `7.4 BILLION TOKENS`, `330+ PROVIDERS`).
  - **Summary Checklist Card:** Floating card with green checkmark circles snapping into place with double-bell chime audio.

---

### Archetype B: The Clean Frosted Card & Illustrated Character System (Video Benchmark 2)
- **Background:** Warm cream/off-white matte canvas (`#F7F4EE`) with a subtle micro-dot grid.
- **Top Header:** Dot-dash progress indicator (`• • • — • • •`) tracking listicle tips (#1 to #9).
- **Hero Cards:**
  - Floating white frosted card with rounded corners (`border-radius: 24px`) and warm red/orange ambient drop shadow (`box-shadow: 0 24px 60px rgba(255, 100, 50, 0.22)`).
  - Competitor or price with bold red strikethrough line (e.g. `$5,000+` <s>struck through</s>, `ElevenLabs` <s>struck through</s>, `Notion` <s>struck through</s>).
  - Inset squircle app icons, yellow star badges, and green `✓ Free` / `• Open source` pill tags.
  - Dynamic in-card visuals: lively audio waveform bars of varying heights, video player preview rows, ascending bar charts, or document preview lines.
- **2D Illustrated Vector Character:**
  - Comic-style stippled texture character anchored in the lower frame.
  - Red/orange baseball cap with stippled dot pattern.
  - Textured knitted sweater with cuff stripes and chest emblem.
  - Expressive facial rig: responsive mouth shapes (open tongue smile, neutral, frown), eyebrow shifts, and blinking.
  - Articulated arms/hands with distinct reactive poses:
    - Hands clasped / attentive
    - Shrugging / palms open
    - Pointing up with index finger
    - Pointing out towards the card

---

## 2. Universal Design Elements

### 1. 3D Angled Slam Stickers / Stamp Badges
- **Visual:** Rounded pill or rectangle rotated between -8° and -12°.
- **Border & Shadow:** 2–3px high-contrast border and soft drop shadow.
- **Motion:** Spring scale bounce ($1.35\times \rightarrow 0.95\times \rightarrow 1.0\times$) synchronized with the procedural `slam` audio thud.
- **Common Tags:** `"LIMIT REACHED"`, `"FREE OF COST"`, `"STOP HALLUCINATIONS"`, `"RULE LOCKED"`, `"10X RESULTS"`.

### 2. Containerized Kinetic Pill Subtitles
- **Placement:** Centered in Band C (`y = 1340–1480` on 9:16 Shorts, `y = 1980–2060` on 4K 16:9 Long).
- **Surface:** High-contrast pill container (`#101630` or vibrant blue `#3B3EE8`) with 2px accent outline.
- **Karaoke Highlight:** Inactive words in crisp white; active spoken word illuminated in Electric Yellow (`#FFCD46`) or Lime Green (`#5AEB96`).

### 3. Scene Transition Dynamics
- **Whip Swipe:** 140–180ms directional camera swipe / whip-pan accompanied by procedural `whip` air swipe.
- **Staggered Card Enqueue:** Secondary cards enter 6–10 frames after the hero container with slight spring overshoot.

---

## 3. Procedural Audio Synchronization

Every motion event must be synchronized within 0 to 3 frames of audio triggers:
- `whoosh`: Major chapter wipe and intro/outro card reveals (350ms).
- `whip`: Rapid card slide or tip transition (140ms).
- `slam`: 3D angled sticker impact and limit alerts (220ms low-frequency thud).
- `switch`: Auto-switching, status changes, and dot progress step (80ms digital chirp).
- `pop`: Card reveals, pill tags, and chip entrances (120ms).
- `tick`: List item staggered reveals and metric counts (40ms tactile click).
- `clack`: Terminal command and prompt character typing (50ms mechanical key tap).
- `chime`: Verified output, green checkmarks, and subscribe conversion (500ms double-bell chime).
- **Mastering Target:** Broadcast audio mastered to **-14.0 to -16.0 LUFS** with safe true peak $\le -1.0\text{ dBFS}$.

---

## 4. Multi-Platform Recomposition Rules

- **Shorts (9:16, 1080×1920):**
  - **Band A (y=180–560):** Top progress dots, category pill, tip numbers.
  - **Band B (y=560–1300):** Main hero cards, terminal windows, vector character.
  - **Band C (y=1300–1500):** Containerized kinetic pill subtitles.
  - **Reserved Zones:** Top 180px, bottom 420px (YouTube tray & subscribe), right 120px (action buttons).
- **Long Video (16:9, 1920×1080 or 3840×2160):**
  - Recompose into dual-panel side-by-side containers (e.g. Left = Anti-Pattern / Input, Right = Senior Specification / Verified Output).
  - Subtitles placed at bottom center with $>80\text{px}$ clearance from all content cards.
