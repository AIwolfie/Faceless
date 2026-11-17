# Motion Graphics & Visual Standards

Universal animation constraints for the Faceless Video Production Engine. All generated videos (Shorts and Long Form) must adhere strictly to these rules.

---

## 1. Frame-Accurate Rational Pacing
- **FPS Locking**:
  - Shorts: Strictly **30.0 FPS** or **60.0 FPS** ($\Delta t = 33.33\text{ms}$ or $16.67\text{ms}$).
  - Long Form: Strictly **24.0**, **30.0**, or **60.0 FPS**.
- Frame indices evaluate strictly as $t = \text{frame\_index} / \text{FPS}$. Never accumulate floating-point time increments ($t += dt$).

---

## 2. Zero-Freeze Quality Assurance
- **Static Hold Threshold**: Any scene whose principal content area remains static for $\ge 4.0\text{ seconds}$ on Shorts or $\ge 9.0\text{ seconds}$ on Long Form fails the automated QA gate (`tools/qa.py`).
- **Required Movement Vectors**:
  - Continuous camera push-in ($\ge 0.035$ zoom progression).
  - Floating ambient micro-drift (`smooth_float` harmonic sine oscillation).
  - Breathing idle motion for characters and vector puppets.

---

## 3. Kinetic Subtitle Safety Zones
- **Shorts (9:16 - 1080×1920)**:
  - Subtitle pill container centered at $y = 1560\text{px}$.
  - Strictly 3–5 words per chunk.
  - Active spoken word illuminates in Electric Yellow `(255, 205, 70)` with a subtle $1.06\times$ scale bounce.
  - Content graphics must maintain an $80\text{px}$ clearance buffer ($y \le 1480\text{px}$).
- **Long Form (16:9 - 1920×1080 / 3840×2160)**:
  - Subtitles centered at $y = 1010\text{px}$ (1080p) or $y = 2020\text{px}$ (4K).
  - Content graphics must never exceed $y = 915\text{px}$ (1080p) or $y = 1830\text{px}$ (4K).

---

## 4. Brand Consistency vs. Story World
- **The Anchor**: ONLY the **Intro Card** and **Outro Card** are fixed and standardized across all channel videos for conversion and recognition.
- **Story-Driven Freedom**: All body scenes must be dynamically tailored to the specific topic (color themes, background environments, card geometry, character styling). Never force every video into the exact same background or color palette.

---

## 5. Verification Protocol Before Final Delivery
1. Generate 6-panel contact sheet capturing all key scene states.
2. Probe audio mix to ensure integrated loudness lands in **$-16.5\text{ LUFS}$ to $-12.5\text{ LUFS}$** with true peak $\le -0.5\text{ dBFS}$.
3. Verify video stream with `python tools/qa.py <video.mp4> <short|long>` with exit code 0.
