---
name: motion-director
description: Master motion graphics and animation skill for the Faceless Video Engine. Directs kinetic typography, spring-eased card reveals, beat-synced visual pacing, continuous camera drift (anti-freeze), diagram animation, and deliver-and-verify QA workflows.
---

# ⚡ Motion Director Skill

The core motion graphics, kinetic animation, and visual rhythm intelligence for the Faceless Video Production Engine.

---

## 1. When to Use
- Designing on-screen motion graphics: card entrances, kinetic text, stat counter tickers, vector diagrams, and split screens.
- Synchronizing motion graphics to Kokoro ONNX speech beats and sound effects.
- Preventing video freezes and passing automated zero-static-hold QA audits.
- Implementing easing mathematics, camera push-in, and spatial composition.

---

## 2. Core Motion Rules & Disciplines

### 1. The Deliver-and-Verify Loop
Never render blindly. Every motion plan must be inspected via:
1. **Frame Probing**: Mathematical state evaluation at specific timestamps ($t = 0.1\text{s}$, $t = 0.5\times\text{duration}$, $t = 0.95\times\text{duration}$).
2. **Contact Sheet Verification**: 6-panel summary sheet capturing every scene's peak visual state.
3. **Automated Stream QA**: Decoding check (0 errors), broadcast loudness (-16.5 to -12.5 LUFS), and freeze detection (<4s content holds).

### 2. Kinetic Typography Standards
- **Split Granularity**:
  - *By line*: Elegant, editorial, chapter headers.
  - *By word*: High-energy taglines, active karaoke subtitles, punchy punchlines.
  - *By character*: Reserve for terminal typewriter effects or single high-impact words.
- **Reveal Mechanics**:
  - Masked Baseline Rise: Clip container with upward $110\% \to 0\%$ slide.
  - Word Bounce: Active word illuminates in Electric Yellow `(255, 205, 70)` with a $1.06\times$ scale pop.
  - Typewriter Cursor: Smooth character reveal matching narration duration with blinking cursor block `█`.

### 3. Continuous Camera Push-In (Anti-Freeze Mandate)
Every scene must apply continuous camera motion before subtitles and watermarks are composited:
$$\text{scale} = 1.0 + \text{amount} \cdot p_{\text{scene}}$$
$$\text{drift}_x = \text{drift\_amp} \cdot \sin(scene\_idx \cdot 1.7)$$
$$\text{drift}_y = \text{drift\_amp} \cdot \cos(scene\_idx \cdot 1.3)$$
This guarantees every pixel moves continuously and passes zero-static-hold QA gates.

### 4. Easing Curves & Spring Physics
Never use flat linear motion for UI elements:
```python
def ease_out_back(x: float) -> float:
    """Tactile pop with subtle overshoot for cards and badges."""
    c1 = 1.70158
    c3 = c1 + 1.0
    t = max(0.0, min(1.0, x))
    return 1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2)

def ease_out_quad(x: float) -> float:
    """Smooth, fluid deceleration for numbers, bars, and pans."""
    t = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - t) * (1.0 - t)

def smooth_float(t: float, freq: float = 1.5, amp: float = 4.0) -> float:
    """Organic idle floating micro-motion."""
    return amp * math.sin(2.0 * math.pi * freq * t)
```

---

## 3. Motion Density Budgeting
To preserve viewer retention and eliminate cognitive overload:
- **Maximum Active Focal Points**: Exactly **ONE** primary visual event at any given instant.
- **Card Cascades**: Stagger sequential cards by **0.20s – 0.35s**. Never pop multiple cards simultaneously.
- **Clearance Margins**: Keep content layer strictly above $y = 915\text{px}$ on 16:9 ($80\text{px}$ safe clearance from subtitles) and above $y = 1500\text{px}$ on 9:16 Shorts.
