# Antigravity Spec: Voice-Synced Animation and Sound Design

30-second sample of "Prompt Engineering for Beginners: 7 Patterns That Actually Work". For Kenil, TechXKenil. 15 Nov 2026.

## 1. The problem and the rule

**Problem in current videos:** a still photo or screenshot sits on screen while the voice talks. Nothing changes, so the viewer's eyes have nothing to follow.

**Rule:** every visual must be *built, changed and removed over time, in step with the voice*. A scene is never an asset shown for N seconds. A scene is a set of animated elements whose state is a function of time.

**The pause test (use it on every scene):** pause on any frame, then on the frame 1 second later. If they look the same apart from background drift, the scene is static and fails.

### 1.1 Four levels of motion

| Level | What it is | Counts as a change? |
| --- | --- | --- |
| L0 Ambient | Background gradient drift, slow shapes | No (atmosphere only) |
| L1 Micro-motion | Push-in of 3-6 percent, float of 3-4 px, cursor blink | No (keeps frame alive) |
| L2 Sync event | New element enters, highlight, move, scale, counter, typing | **Yes** |
| L3 Structural | Cut, layout change, camera move, split-screen swap | **Yes** |

Requirements: an L2 or L3 change at least every **2.0 s** in this sample; no frame identical for more than **2.5 s**; an L3 change at least every 8 s.

### 1.2 Banned in this sample

- Any photo, stock image or screenshot as a layer. Chat windows, tables and cards are **built from components**, not pasted as pictures.
- Slideshow cross-fades between pictures.
- "Image + slow zoom" as the main visual.
- A whole block of text appearing at once when it could be built word by word.
- The logo as a still image: the TXK logo may be an asset, but it must animate (ring draws, logo scales in, tagline types).

### 1.3 Good vs bad (example)

- **Bad:** show a screenshot of a chat for 4 s with the voice reading it.
- **Good:** the chat window pops in, the cursor blinks, the prompt types as the voice says it, the message sends, typing dots appear, the answer appears, and "Generic" is stamped on it as the word is spoken.

## 2. Pipeline (one source of truth)

All visuals and all sound effects are generated from the **same event list**, so they cannot drift apart.

| Step | Output file | Notes |
| --- | --- | --- |
| 1 Script | script.json | Beats B1..B10 (section 6) |
| 2 Voice | voice.wav | Kokoro am_michael, speed 1.1 |
| 3 Word timestamps | words.json | [{word, start_s, end_s}] from the repo's method, else forced alignment |
| 4 Plan | plan.json | Events per beat, keyed to word indexes |
| 5 Resolve | events.json | Each event with absolute frame and target word start |
| 6 Render visuals | video_silent.mp4 | 1920x1080, 30 fps, every layer animated |
| 7 Render SFX | sfx.wav | From events.json, sample-accurate |
| 8 Bed | bed.wav | Optional soft ambient pad (procedural) |
| 9 Mix | mix.wav | Duck bed under voice, loudness to about -15 LUFS |
| 10 Mux | sample_30s.mp4 | Video + mix |
| 11 QA | qa_report.txt | Section 7 checks |

If Kokoro's output length differs from the estimates in section 6, **trust words.json**, not the estimated times.

## 3. Animation engine spec

### 3.1 Timing defaults

| Motion | Duration | Easing |
| --- | --- | --- |
| Pop-in (chip, bubble, card) | 180-250 ms | spring, overshoot about 8 percent |
| Slide or push transition | 300-400 ms | ease-out cubic |
| Hero text entrance | 250-350 ms | ease-out cubic + 4 percent scale settle |
| Highlight on a word | 120-180 ms | ease-out |
| Table rows | 80 ms stagger, 200 ms each | ease-out |
| Punch-in (C2) | 10-15 percent scale in 250 ms, hold, ease back | ease-in-out |
| Typing | 14-20 chars per second, matched to the spoken phrase end | linear |
| Exit | 200 ms | ease-in |

### 3.2 Easing and scheduling skeleton (Python, renderer-agnostic)

```python
import math
FPS = 30
LEAD_FRAMES = 2          # events land this many frames before the word

def ease_out_cubic(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def ease_in_out(x):
    x = min(max(x, 0.0), 1.0)
    return 3 * x * x - 2 * x * x * x

def spring(x):
    # 0..1 progress -> overshoots about 8 percent then settles at 1.0
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    return 1 - math.exp(-7 * x) * math.cos(9 * x)

def event_frame(word_start_s):
    return max(0, round(word_start_s * FPS) - LEAD_FRAMES)

class Tween:
    def __init__(self, start_frame, dur_frames, a, b, ease=ease_out_cubic):
        self.s, self.d, self.a, self.b, self.ease = start_frame, dur_frames, a, b, ease
    def value(self, frame):
        x = (frame - self.s) / max(1, self.d)
        return self.a + (self.b - self.a) * self.ease(x)
```

### 3.3 Components

- **HeroText (T3):** words slide up 24 px and fade in, stagger 60 ms per word, small scale settle. Exit: slide up and fade.
- **Emphasis (T4):** on the target word, scale 1.0 to 1.12 and back, color changes to the accent, underline sweeps left to right.
- **Typewriter (T5):** characters appear at a steady rate, cursor blinks at 2 Hz, finishes when the voice finishes the phrase.
- **ChatUI (T7):** window springs in; input box; send animation; typing-dots bubble; answer bubble builds line by line. Never a screenshot.
- **Chip (E4):** rounded label, springs in, can grow, glow or dim. Chips have a number and a short name.
- **TableBuild:** frame draws in, header fades in, rows stagger in, a highlighted row can pulse.
- **SplitScreen (E3):** two panels; one panel highlights while the other dims to 40 percent; slow camera push toward the highlighted side.
- **LineDraw:** a stroke drawn along a path (used for the cross-out), supersampled 2x.
- **BrandCard:** ring draws, logo scales in, tagline "AI • TECH • CODE" types or fades up letter by letter.
- **Captions (T2):** two-line sentence captions, small, bottom center, appear with the sentence; move up if a card sits at the bottom.
- **Illustrative tag:** small corner tag, visible the whole time a sample AI answer is on screen.

## 4. Voice sync spec

1. Generate voice.wav from the script, then words.json. Every word has start_s and end_s.
2. In plan.json, each event names a beat, a **word index** (0-based inside that beat's line), an action and an SFX id.
3. Resolve to a frame: `frame = round(word_start_s * 30) - 2`. Visuals land 0 to 3 frames early.
4. SFX are scheduled on the same frame as their visual.
5. If two events fall on the same frame, move the second by 3 frames.
6. Report count of estimated words if alignment fails.

## 5. Sound design spec

### 5.1 Levels
- Voice: Peaks about -3 dBFS before mix
- SFX: Peaks 12-20 dB under voice peak
- Bed: Soft ambient pad, ducked under voice (-30 dB under voice)
- Master: About -15 LUFS integrated, true peak -1.5 dB or lower

### 5.2 SFX Catalog
- SW: Soft whoosh, band-passed noise (250-350 ms, -18 dB)
- PP: Pop, short downward pitch sweep (90 ms, -16 dB)
- TK: Tick, tiny click (18 ms, -26 dB)
- SD: Send, soft swish + tick (120 ms, -20 dB)
- GL: Glitch zap, bit-crushed noise burst (180 ms, -16 dB) - exactly once at B3
- CH: Chime, two soft sine notes (250 ms, -20 dB)
- TH: Thump, low sine drop (120 ms, -20 dB)
- RS: Swell, rising filtered noise (500 ms, -22 dB)
- SC: Scratch, short filtered noise (200 ms, -22 dB)
- CP: Chip pop, short sine ping, pitch stepped (80 ms, -18 dB, pitches: 523, 587, 659, 698, 784, 880, 988 Hz)
- ST: Brand sting, soft chime + low swell (700 ms, -18 dB)

## 6. Beat-by-beat plan

Script:
- B1: "Same AI. Same task. Only the prompt changes."
- B2: "First, the prompt most beginners type: help me learn Python."
- B3: "The answer? Generic. Forgettable."
- B4: "Now: a beginner, thirty minutes a day, Excel automation, a four-week table."
- B5: "Clear plan. Real steps. Same AI."
- B6: "That's the difference between a bad prompt and a good one."
- B7: "In this video: seven patterns, each with a copy-paste template."
- B8: "And one of them stops AI from making things up."
- B9: "Let's start with why prompts matter."
- B10: Standard TXK card line from Video Rules (about 2.5 s)
