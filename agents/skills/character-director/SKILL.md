---
name: character-director
description: Autonomous character direction and puppet staging skill for the Faceless Video Engine. Directs procedural characters, stickmen, and vector puppets across 9:16 Shorts and 16:9 explainers. Staging, motivated gestures, emotional expressions, and voice-action synchronization.
---

# 🎭 Character Director Skill

Autonomous staging, kinematic posing, and performance direction for animated characters, stick figures, and vector puppets within the Faceless Video Production Engine.

---

## 1. When to Use
- Adding an animated presenter, mascot, or explainer figure to technical videos.
- Converting dry abstract concepts into story-driven character narratives (e.g. AI robot undergoing glitch meltdown, developer debugging code, researcher discovering an anomaly).
- Staging character emotional reactions: shock, confusion, triumph, deep thinking, or pointing to on-screen cards and charts.
- Generating procedural character animation via `tools/character_puppet.py`.

---

## 2. Core Directing Principles

### 1. The Lead Visual Rule (Action Before Speech)
A character action must precede or instantly snap to the spoken word:
- When the voice says *"There is a glitch..."*, the character's eye state switches to `error` and body to `shock_recoil` **0.15s before or on the exact beat**.
- Never linger on a completed gesture after the spoken point has passed.

### 2. The 3-Second Visual Dwell Gate
No character may remain static for more than **3.0 seconds**:
- Idle breathing bob (`p_anim` sinusoidal harmonic drift) keeps limbs alive during speech.
- Alternate between broad gestures (`explain`, `point_right`) and micro-actions (head tilt, blink, hand rest).

### 3. Spatial Staging & Safe Margin Blocking
- **Shorts (9:16 Portrait - 1080×1920)**:
  - Character grounded at $y = 1400\text{px} - 1500\text{px}$.
  - Clearance above the subtitle container ($y = 1560\text{px}$).
  - Top boundary clear for HUD headers and prompt cards ($y < 700\text{px}$).
- **Long Video (16:9 Landscape - 1920×1080)**:
  - Left Stage ($x = 350\text{px}, y = 920\text{px}$) or Right Stage ($x = 1570\text{px}, y = 920\text{px}$).
  - Center stage reserved for architectural diagrams, code windows, and data charts.
  - Grounded strictly above the horizontal caption boundary ($y \le 915\text{px}$).

---

## 3. Poses & Kinematic Vocabulary

| Pose | Kinematic Description | Best Story Context |
|---|---|---|
| `idle` | Arms resting at sides, subtle harmonic breathing drift | Scene opening, listening, passive transitions |
| `explain` | Both arms open outward, dynamic hand oscillation | Explaining complex concepts, introducing facts |
| `point_right` | Right arm extended upward-right towards graphics | Highlighting an on-screen chart, metric, or code window |
| `point_left` | Left arm extended upward-left towards graphics | Directing viewer focus to a left-stage diagram |
| `thinking` | Right hand resting on chin, asymmetric head tilt | Posing a mystery, analyzing a paradox, introducing a bug |
| `shock_recoil` | Both hands raised beside head, legs spread wide, torso recoiled | Meltdown, crash, critical exception, sudden surprise |

---

## 4. Facial Expression Matrix

| Expression | Features | Spoken Emotion |
|---|---|---|
| `neutral` | Standard circular pupil LEDs, calm mouth line | Default narration, balanced delivery |
| `focused` | Horizontal slit visor eyes, sharp focus line | Reading code, analyzing vectors, deep logic |
| `thinking` | Asymmetric eyebrow squint, wavy mouth arc | Puzzlement, calculating, skepticism |
| `error` | Crossed-out glowing amber/crimson eyes, open O mouth | System failure, glitch token, crashed program |
| `happy` | Arched eyes, upward smile arc | Breakthrough, optimization success, subscription call |

---

## 5. Technical Integration with `character_puppet.py`

```python
from tools.character_puppet import CharacterPuppet

# 1. Initialize character puppet with theme
puppet = CharacterPuppet(theme="cyber_cyan", scale=1.0, height_px=650)

# 2. Render onto canvas at specified ground position
frame = puppet.render(
    canvas_size=(1080, 1920),
    position=(540, 1420),
    pose="explain",
    expression="focused",
    p_anim=t_sc / dur_sc
)

# 3. Alpha-composite onto scene background
canvas.alpha_composite(frame)
```
