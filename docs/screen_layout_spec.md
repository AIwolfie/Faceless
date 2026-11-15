# Antigravity Spec: Screen Utilization for Horizontal (16:9) and Vertical (9:16) YouTube Video
For Kenil, TechXKenil. 15 Nov 2026. Companion to docs/animation_sync_spec.md (animation, voice sync, sound).

## 0. Read this first
**Purpose.** Tell Antigravity exactly how to use the screen in the two formats you publish: long videos (horizontal, 1920x1080) and Shorts (vertical, 1080x1920): where content goes, where it must not go, how big text must be, and how each animated component changes between formats.
**About the numbers.** YouTube does not publish exact pixel margins for its Shorts overlay. Third-party tools measured them and disagree: on a 1080x1920 canvas, the bottom tray is quoted from about 300 px up to about 670 px, and the right button column from about 50 px up to about 190 px. I use a conservative composite and mark values [default]. Before trusting them, upload a private test of each format and look at it on a real phone (section 11).
**What I could not do.** I have not read the techXkenil/faceless repo (GitHub blocked automated access), so this spec is renderer-agnostic: it defines zones, templates, sizes and checks that any renderer can follow.

## 1. The two formats

| Feature | Long video | Short |
|---|---|---|
| **Canvas** | 1920x1080 (16:9), 30 fps | 1080x1920 (9:16), 30 fps |
| **Captions** | T2 sentence captions, small, bottom center | T1 word-highlight captions, large, lower middle |
| **Visible event at least every** | 2.5 s | 2.0 s |
| **Slide transitions** | Left / right | Up / down (feels like a swipe) |
| **Story plan** | Riya story, about 4 min | 30-60 s cutdowns (the 30 s hook, or one pattern per Short) |

### Three hard rules
1. **Recompose, never crop.** Do not take the 16:9 render and crop or scale it to 9:16, or the reverse.
2. **No letterboxing or blurred side bars** to fill the other format. Every format uses the full canvas with its own layout.
3. **One story, two layouts.** The same beat plan, the same voice timings and the same events drive both formats; only the layout template per beat changes (section 9).

## 2. Screen utilization principles
1. **Fill with purpose.** The main visual of a beat should take the dominant share of the key zone. Target 30-65 percent of key-zone pixels differing from the empty background [default]; below 20 percent is too empty, above 80 percent is cluttered.
2. **One focal point per beat, three levels of hierarchy by size:** hero (what to read first), supporting (the visual), small (labels, tags).
3. **Design for a phone.** A 16:9 video watched on a phone held upright uses only about a third of the screen height, so long-video text must still be legible when small (minimum sizes in section 5).
4. **Edges carry atmosphere, not information.** Background drift, glows and shapes may bleed to the edges; text, faces, logos, chips and tables may not.
5. **Compose for motion.** Leave room for where elements enter from and exit to, not only for their final positions.
6. **Same two motifs in both formats ("same AI, new words"):** the laptop and prompt box keep their roles in every layout.

## 3. Horizontal layout (1920x1080)
### 3.1 Zones
| Zone | Rect (x, y, w, h) | Rule |
|---|---|---|
| **Action-safe (key zone)** | 96, 54, 1728, 972 | All text, chips, tables, faces and logos inside |
| **Caption box (T2)** | 360, 850, 1200, 120 | Bottom center, 2 lines max |
| **Player controls** | bottom 110 px (y 970-1080) | No text; the YouTube progress bar and controls appear here when the viewer interacts |
| **Top-right** | 1760, 0, 160, 100 | No key content (cards icon) |
| **Bottom-right** | 1720, 960, 200, 120 | No key content (channel watermark, if enabled) |
| **Background** | full frame | Drift, gradients, decoration only |

### 3.2 Grid
12 columns, 6 rows, 24 px gutters inside the key zone: column width 122 px, row height 142 px. Snap panels and cards to the grid.

### 3.3 Layout templates (rects as x, y, w, h)
- **H1: Hero text** — Hero box 240, 300, 1440, 360
- **H2: Split 50/50** — Left 96, 150, 840, 680; right 984, 150, 840, 680; label strip 96, 54, 1728, 76
- **H3: Chat + callouts** — Chat window 96, 120, 1080, 700; callout column 1224, 120, 600, 700
- **H4: Story scene** — Full key zone. Character about x 200-560; laptop x 600-1300; calendar top-right area x 1450-1800, y 150-380; messy sheet x 96-420, y 600-820
- **H5: Wide diagram** — 96, 150, 1728, 680 (nodes left to right)
- **H6: Card row** — 4 cards, each 396 w, 48 gap, at y 250, h 510 (x 96, 540, 984, 1428)
- **H7: Template card** — Centered card 360, 100, 1200, 740
- **H8: End screen** — See 3.4
*Captions move up (but stay inside the key zone) if a template sits at the bottom.*

### 3.4 End-screen layout (last 5-20 s of the video)
YouTube end-screen elements are placed in Studio over the video. Keep these areas empty of content so nothing is covered, and set the Studio elements to match:
• Slot A (video): 96, 270, 800, 450
• Slot B (video or playlist): 1024, 270, 800, 450
• Subscribe circle: 860, 790, 200, 200
• Spoken outro and the red SUBSCRIBE card animation sit in the top strip (96, 54, 1728, 180) and animate in as the slots are revealed (empty frames outline in). The end-screen rules and timing can change; verify in Studio.

## 4. Vertical layout (1080x1920)
### 4.1 What the Shorts interface covers (conservative defaults)
• Top, about 180 px: search and menu icons.
• Right column, about 120-150 px: like, dislike, comment, share, remix.
• Bottom tray, about 420 px: channel name, Subscribe button, title and description. Some sources put it much higher (to about 576 px or more); keep CTAs and long text above y = 1344 when possible.
• Left, about 40-60 px: small edge margin.
**Key zone [default]:** x 120 to 960, y 180 to 1500, which is 840 x 1320. All text, faces, tables, chips and logos stay inside. The key zone is symmetric (120 px both sides) so layouts stay balanced.

### 4.2 Three bands
| Band | y range | Use |
|---|---|---|
| **A** | 180-560 | Headline or label (about 380 px) |
| **B** | 560-1280 | Main visual (about 720 px) |
| **C** | 1300-1500 | Captions (T1) and small callouts |
| **Reserved** | 1500-1920 | Nothing important |

Caption box (T1): 150, 1300, 780, 200. Background and decoration may use the full frame.

### 4.3 Layout templates
- **V1: Hero text** — Hero box 120, 520, 840, 600
- **V2: Stacked split** — Top panel 120, 190, 840, 510; VS chip 120, 700, 840, 60; bottom panel 120, 760, 840, 510
- **V3: Chat** — Chat card 120, 220, 840, 1000 (typed text and chips inside)
- **V4: Stacked cards** — 3 cards of 840 x 300 at y 240, 580, 920 (40 px gaps)
- **V5: Vertical diagram** — Nodes top to bottom inside 120, 220, 840, 1020
- **V6: Table as row cards** — Max 4 row cards of 840 x 220 at y 240-1200; drop the least important column (put it in the voice or a callout)
- **V7: Story scene** — Calendar widget in band A (y 200-420); messy sheet left, middle (x 120-420, y 520-820); laptop + character lower center in band B (x 200-880, y 700-1260)
- **V8: Template card** — Card 120, 200, 840, 1180; text wraps to about 28 characters per line at 44 px

### 4.4 Do not
• Place text in the right 120 px, the top 180 px, or the bottom 420 px.
• Center a caption under the like/comment column: captions stay centered in the key zone, never shifted right.
• Enter elements from the right edge (the button column sits there); enter from the bottom, top or left.

## 5. Typography and sizing (both formats)
| Item | Horizontal 1080p | Vertical 1080 wide |
|---|---|---|
| **Hero text (T3)** | 120-150 px, max about 24 chars per line | 110-140 px, max about 10-12 chars per line, 3 lines max |
| **Supporting heading** | 72-90 px | 72-84 px |
| **UI text (chat, table)** | 40-48 px | 48-54 px |
| **Captions** | T2: 44 px, 2 lines, about 38-42 chars per line | T1: 72-84 px, 2 lines of 2-4 words |
| **Smallest allowed (labels, tags)** | 36 px | 40 px |
| **Minimum stroke / line** | 4 px | 6 px |
| **Chip padding** | 20 px | 28 px |

Contrast: text to background at least 4.5:1. Captions use a pill background or a 6-8 px outline. Fonts and colors come from TechXKenil_Video_Rules.md; this doc sets only sizes and positions. Never shrink below the minimum to fit more text: split the beat or cut words instead.

## 6. Component adaptation matrix
| Component | Horizontal | Vertical |
|---|---|---|
| **HeroText (T3)** | One line or two, centered in H1 | Stack words on 2-3 lines, centered in V1 or band A |
| **Emphasis (T4)** | Scale pop 1.12, accent color, underline | Same, plus larger pop (1.15) so it reads small-screen |
| **Typewriter (T5)** | Inside chat window, left aligned | Same, line width 840, wrap earlier, larger font |
| **ChatUI (T7)** | Window about 1080 w with callout column | Full-width card (840 w), taller, chips overlay on the card |
| **Chips (E4)** | Row of chips (up to 7 in one row at 200 w) | Two rows or a vertical stack (4 + 3), or a 2-column grid |
| **TableBuild** | 3 columns, 4 rows | 2 columns or stacked row cards (V6) |
| **SplitScreen (E3)** | Side by side (H2) | Stacked top / bottom (V2) with a VS chip |
| **LineDraw** | Longer horizontal strokes | Shorter, thicker strokes (6 px minimum) |
| **BrandCard** | Centered, tagline below | Same, scaled so the tagline stays above y = 1500 |
| **Captions** | T2 bottom center | T1 band C |
| **Illustrative / Fictional tags** | Top-left of the key zone | Top-left of the key zone, below the 180 px top reserve |
| **Prompt Builder card** | Top-right, 7 slots in one row (about 520 x 90) | Top-left under the top reserve, 7 slots in two rows (about 400 x 150) |
| **Template card** | H7 | V8, taller, text wrapped |
| **Context-window box** | Wide box, items drop in from the left | Tall box, items drop in from the top |
| **Document pane (pattern 3)** | Left pane with email, right pane with the answer | Pane on top, answer below, key lines highlighted one by one |
| **Stepping stones (pattern 6)** | Left to right path | Top to bottom path |
| **Plan diagram (pattern 7)** | 3 boxes in a row | 3 boxes in a column |
| **Character scene** | H4 | V7 (recomposed, not cropped) |

## 7. Camera, motion and transitions per format
• Scene push-in (C1): at most 6 percent, zooming about the key-zone center (horizontal: 960, 540; vertical: 540, 840). Never about the frame corner.
• Punch-in (C2, up to 15 percent): applied to one element, not the whole scene, so text elsewhere stays inside the zone.
• Zoom-safe rule: every text element, at its largest scale during the scene, must still be inside the key zone (checked in section 11).
• Transitions: horizontal uses left/right slides and pushes; vertical uses up/down pushes. Match cuts (C4) work in both.
• Entrance origins: horizontal from left, bottom or center; vertical from bottom, top or center. Never from the right edge in vertical.
• Parallax: background layer moves at most 1-2 percent relative to foreground; foreground stays crisp.

## 8. Layout config and helpers
```yaml
formats:
  long:
    canvas: {w: 1920, h: 1080, fps: 30}
    key_zone: {x: 96, y: 54, w: 1728, h: 972}
    captions: {style: T2, box: {x: 360, y: 850, w: 1200, h: 120}, font_px: 44}
    reserved:
      - {name: player_controls, x: 0, y: 970, w: 1920, h: 110}
      - {name: top_right, x: 1760, y: 0, w: 160, h: 100}
      - {name: watermark, x: 1720, y: 960, w: 200, h: 120}
    grid: {cols: 12, rows: 6, gutter: 24}
    zoom_center: {x: 960, y: 540}
    max_event_gap_s: 2.5
  short:
    canvas: {w: 1080, h: 1920, fps: 30}
    key_zone: {x: 120, y: 180, w: 840, h: 1320}
    captions: {style: T1, box: {x: 150, y: 1300, w: 780, h: 200}, font_px: 78}
    reserved:
      - {name: top_ui, x: 0, y: 0, w: 1080, h: 180}
      - {name: right_column, x: 960, y: 0, w: 120, h: 1920}
      - {name: bottom_tray, x: 0, y: 1500, w: 1080, h: 420}
    bands: {A: [180, 560], B: [560, 1280], C: [1300, 1500]}
    zoom_center: {x: 540, y: 840}
    max_event_gap_s: 2.0
```

## 9. Beat-by-beat layout map for the Prompt Engineering video
| Beat | Long (horizontal) | Short (vertical) |
|---|---|---|
| **B1 Setup** | H4 desk scene, hero text over it | V7 desk scene, hero text in band A |
| **B2 Attempt** | Camera push into laptop, H3 chat | Push into laptop, V3 chat card |
| **B3 Failure** | H3, weak answer, pull back to Riya | V3, pull back to V7 |
| **B4 Turn** | H4, lightbulb above Riya, prompt box glows | V7, same |
| **B5 Fix** | H3, chips on the prompt | V3, chips on the card |
| **B6 Payoff** | Table build (3 cols), Riya sits up | V6 row cards, Riya in V7 lower center |
| **B7 Patterns** | 7 chips in one row (H6-like) + template card | 4 + 3 chips in two rows + template card |
| **B8 Open loop** | Chip 3 grows, fake bubble crossed out | Same, stacked layout |
| **Brand card** | Centered | Centered, tagline above y = 1500 |
| **Why (context window)** | H5, wide box, items drop in | V5, tall box, items drop from the top |
| **P1 Context + goal** | H3 chat + three chips | V3 chat + three chips |
| **P2 Audience** | H2 split (jargon vs plain) | V2 stacked split |
| **P3 Source only** | H2-style document pane + answer, NOT FOUND stamp | V2-style stacked panes, stamp over the answer |
| **P4 Example** | H6 example cards, then typed label | V4 stacked cards |
| **P5 Format** | Paragraph morphs into 5 bullets | Same, in one column |
| **P6 Steps** | H5 stepping stones left to right | V5 top to bottom |
| **P7 Critique** | H5 plan diagram, red callouts | V5 plan column, callouts below |
| **Mistakes** | H6 three cards | V4 three cards |
| **Template card** | H7 | V8 |
| **Recap + outro** | Chips recap, end-screen layout H8 | Chips recap, no end-screen slots (Shorts has none) |

## 10. Rules that apply to every scene
1. Choose the layout template from the table above (or a documented variant); do not hand-place elements outside templates.
2. Text inside the key zone at its maximum scale; nothing in reserved zones.
3. At least 30 percent coverage of the key zone by active content at the middle of each beat (the opening 0.5 s of a build may be emptier).
4. Minimum font sizes from section 5.
5. Captions never overlap the main visual; if they would, move the visual up inside its band, not the captions off-zone.
6. Same primary visual twice in a row is not allowed (see the animation spec); layout templates may repeat.

## 11. Automatic checks and real-device verification
### 11.1 Layout lint (from the scene graph, before rendering)
Run `lint_elements` for every beat in both formats. Pass: zero results. Also verify every text element's `min_font_px` meets section 5.

### 11.2 Coverage check (on rendered keyframes)
Render the mid-point frame of each beat twice: normally, and with only the background layer. Report beats below 0.20 or above 0.80 and fix them.

### 11.3 Overlay check
Build an overlay mask from the reserved rects and the key-zone boundary, composite it on the rendered keyframes for review, and report any text pixels inside reserved zones.

### 11.4 Real-device check (once per format, then again if YouTube's layout changes)
1. Upload a private or unlisted test of the long video and of a Short.
2. View on a phone upright, a phone in fullscreen landscape, and a desktop browser.
3. For the Short, check the right column, the bottom tray with the Subscribe button and the title, and the top icons; for the long video, tap the screen so the controls and progress bar appear, and check the end-screen slots.
4. Screenshot, then update `layout.yaml` (the reserved rects) if anything is covered. Record the date and phone model in the report.

## 12. Common failure modes
| Symptom | Likely cause | Fix |
|---|---|---|
| Captions hidden by the Subscribe button | Captions placed too low or shifted right | Keep captions in band C, centered, above y = 1500 |
| Vertical video looks empty | 16:9 layout shrunk into 9:16 | Use the V template and enlarge the main visual to the full key-zone width |
| Long video text unreadable on phone | Fonts below the minimum | Raise to at least 36 px; shorten the text |
| Text clipped during a push-in | Layout placed at the edge of the zone | Use max-scale lint; shrink the layout or reduce the push-in |
| Chips overflow in vertical | 7 chips in one row | Two rows (4 + 3) or a 2-column grid |
| Table unreadable in vertical | 3 columns at 840 px width | Use row cards (V6) |
| Double captions in long videos | Burned-in captions plus YouTube captions turned on | Keep burned-in T2; do not upload a same-language caption track unless it is needed |
| Dead edges on the long video | Content hugging the center only | Use the grid, widen the main visual to at least 8 of the 12 columns |

## 13. Deliverables and report
For each render (long and, when asked, short): the MP4, the `layout.yaml` used, the lint output, coverage numbers per beat, the list of layout templates used per beat, and a report of at most 10 lines: format, resolution, templates used, lint failures fixed, beats outside the coverage range, real-device check status (done or not done), and fallbacks.
