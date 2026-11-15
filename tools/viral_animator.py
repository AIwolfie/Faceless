#!/usr/bin/env python3
"""
viral_animator.py — High-Retention Motion Graphics & UI Component Library.
Replicates the visual archetypes from viral tech explainers:
- 3D Perspective Grid with vanishing horizon & dual-color ambient spotlights
- Frosted white card with warm Gaussian-blurred ambient glow
- Genuine GitHub Repository Card with neon border, Octocat SVG, stars & forks
- macOS Dark Terminal Window with 3 control dots & live typing
- Model Switching / Session Limit Failover with animated arrow & slam sticker
- 2D Illustrated Comic Character with stippled texture & reactive poses
- Strikethrough pricing / anti-pattern comparison cards
- Top Dot-Dash Progress Tracker (• • • — • • •)
- High-contrast containerized kinetic pill captions
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Universal Colors
C_WHITE = (255, 255, 255)
C_BLACK = (10, 12, 18)
C_CYAN = (64, 215, 255)
C_PURPLE = (155, 110, 255)
C_YELLOW = (255, 205, 70)
C_ORANGE = (255, 120, 40)
C_GREEN = (50, 215, 120)
C_RED = (255, 60, 80)
C_MUTED = (140, 155, 185)

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def draw_star(draw, cx: int, cy: int, r_outer: int = 12, r_inner: int = 5, fill=(255, 215, 60)):
    """Draws a clean 5-pointed star polygon."""
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)

def draw_fork_icon(draw, cx: int, cy: int, size: int = 14, color=C_MUTED):
    """Draws a clean vector git fork icon."""
    r = 3
    # Bottom circle
    draw.ellipse([cx - r, cy + size//2 - r, cx + r, cy + size//2 + r], fill=color)
    # Top left circle
    draw.ellipse([cx - size//2 - r, cy - size//2 - r, cx - size//2 + r, cy - size//2 + r], fill=color)
    # Top right circle
    draw.ellipse([cx + size//2 - r, cy - size//2 - r, cx + size//2 + r, cy - size//2 + r], fill=color)
    # Stem
    draw.line([(cx, cy + size//2), (cx, cy)], fill=color, width=2)
    # Left branch
    draw.line([(cx, cy), (cx - size//2, cy - size//2)], fill=color, width=2)
    # Right branch
    draw.line([(cx, cy), (cx + size//2, cy - size//2)], fill=color, width=2)

def draw_octocat(draw, cx: int, cy: int, r: int = 18, bg_color=(255, 255, 255), fg_color=(16, 18, 28)):
    """Draws GitHub Octocat icon with ears and silhouette."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg_color)
    # Ears
    ear_w = int(r * 0.35)
    ear_h = int(r * 0.45)
    draw.polygon([(cx - int(r*0.65), cy - int(r*0.1)), (cx - int(r*0.3), cy - int(r*0.85)), (cx - int(r*0.1), cy - int(r*0.4))], fill=fg_color)
    draw.polygon([(cx + int(r*0.65), cy - int(r*0.1)), (cx + int(r*0.3), cy - int(r*0.85)), (cx + int(r*0.1), cy - int(r*0.4))], fill=fg_color)
    # Face & head
    draw.ellipse([cx - int(r*0.65), cy - int(r*0.5), cx + int(r*0.65), cy + int(r*0.75)], fill=fg_color)


_FONT_CACHE = {}
def get_font(size: int, bold: bool = True):
    key = (size, bold)
    if key not in _FONT_CACHE:
        candidates = [
            os.path.join(REPO_ROOT, "fonts", "Inter-Bold.ttf"),
            r"C:\Windows\Fonts\Arialbd.ttf",
            r"C:\Windows\Fonts\Segoeui.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    _FONT_CACHE[key] = ImageFont.truetype(c, size)
                    break
                except: pass
        if key not in _FONT_CACHE:
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]

# -------------------------------------------------------------
# 1. 3D PERSPECTIVE FLOOR GRID WITH AMBIENT LIGHTING
# -------------------------------------------------------------
def render_3d_perspective_grid(width: int, height: int, t: float, horizon_ratio: float = 0.35) -> Image.Image:
    """Renders a 3D perspective floor grid with glowing horizon, depth lines, and dual ambient spotlights."""
    img = Image.new("RGB", (width, height), (8, 10, 20))
    draw = ImageDraw.Draw(img)
    hy = int(height * horizon_ratio)
    cx = width // 2

    # Top warm amber ambient glow
    top_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(top_glow)
    gdraw.ellipse([cx - int(width * 0.4), hy - int(height * 0.25), cx + int(width * 0.4), hy + int(height * 0.35)], fill=(120, 60, 20, 75))
    top_glow = top_glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(Image.alpha_composite(Image.new("RGBA", (width, height), (0,0,0,0)), top_glow).convert("RGB"), (0,0))

    # Bottom blue ambient glow
    bot_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(bot_glow)
    bdraw.ellipse([cx - int(width * 0.35), height - int(height * 0.3), cx + int(width * 0.35), height + int(height * 0.1)], fill=(30, 45, 110, 85))
    bot_glow = bot_glow.filter(ImageFilter.GaussianBlur(90))
    img.paste(Image.alpha_composite(Image.new("RGBA", (width, height), (0,0,0,0)), bot_glow).convert("RGB"), (0,0))
    draw = ImageDraw.Draw(img)

    # Perspective vertical fan lines
    num_fans = 18
    for i in range(-num_fans, num_fans + 1):
        bx = cx + int(i * (width / (num_fans * 0.75)))
        draw.line([(cx, hy), (bx, height)], fill=(28, 38, 68), width=1)

    # Horizontal grid lines with quadratic depth perspective
    num_horiz = 14
    for j in range(1, num_horiz + 1):
        prog = (j / num_horiz) ** 2.3
        y = hy + int((height - hy) * prog)
        alpha = int(25 + 50 * prog)
        draw.line([(0, y), (width, y)], fill=(alpha, alpha + 10, alpha + 35), width=1)

    # Upper sky lines
    for k in range(1, 6):
        y = int(hy * (k / 6.0))
        draw.line([(0, y), (width, y)], fill=(15, 18, 32), width=1)

    # Moving dust stars/particles
    for p in range(30):
        px = int((p * 97 + t * 40) % width)
        py = int((p * 67 + t * 20) % height)
        draw.ellipse([px-1, py-1, px+1, py+1], fill=(140, 180, 255))

    return img

# -------------------------------------------------------------
# 2. FROSTED WHITE CARD WITH WARM GAUSSIAN AMBIENT SHADOW
# -------------------------------------------------------------
def render_frosted_card(draw_target, bbox, title, tag="• Open source", squircle_color=C_ORANGE, has_waveform=True, star=True):
    """Renders the clean floating frosted card from Video 1 with soft diffused ambient glow."""
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0

    # Ambient drop shadow via blurred underlay
    shadow = Image.new("RGBA", (w + 120, h + 120), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([60, 60, 60 + w, 60 + h], radius=28, fill=(255, 120, 50, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(32))
    draw_target.paste(shadow, (x0 - 60, y0 - 60), shadow)

    # Card body
    card_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_im)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=(255, 255, 255, 248), outline=(255, 255, 255, 255), width=2)

    # Squircle App Icon
    icon_pad = 28
    icon_size = 72
    cdraw.rounded_rectangle([icon_pad, icon_pad, icon_pad + icon_size, icon_pad + icon_size], radius=18, fill=squircle_color)
    # Audio bars inside icon
    for bi, bh in enumerate([18, 32, 22, 12]):
        bx = icon_pad + 18 + bi * 11
        cdraw.rounded_rectangle([bx, icon_pad + (icon_size - bh)//2, bx + 5, icon_pad + (icon_size + bh)//2], radius=2, fill=C_WHITE)

    # Title & Tag
    cdraw.text((icon_pad + icon_size + 20, icon_pad + 8), title, fill=(18, 20, 25), font=get_font(26))
    # Green tag pill
    cdraw.rounded_rectangle([icon_pad + icon_size + 20, icon_pad + 44, icon_pad + icon_size + 160, icon_pad + 72], radius=14, fill=(235, 248, 240))
    cdraw.text((icon_pad + icon_size + 28, icon_pad + 48), tag, fill=(35, 160, 80), font=get_font(13))

    # Star badge in top-right
    if star:
        draw_star(cdraw, w - 45, icon_pad + 25, r_outer=14, r_inner=6, fill=(255, 195, 45))

    # Inset Waveform Container
    if has_waveform:
        in_y0 = icon_pad + icon_size + 24
        in_y1 = h - 22
        cdraw.rounded_rectangle([20, in_y0, w - 20, in_y1], radius=16, fill=(248, 245, 240))
        # Orange audio waveform bars
        wf_bars = [12, 18, 28, 44, 32, 16, 24, 38, 48, 30, 18, 26, 40, 22, 14, 28, 42, 35, 20, 12]
        bar_w = 6
        gap = 11
        start_bx = (w - len(wf_bars) * gap) // 2
        for idx, bh in enumerate(wf_bars):
            bx = start_bx + idx * gap
            by_mid = (in_y0 + in_y1) // 2
            cdraw.rounded_rectangle([bx, by_mid - bh//2, bx + bar_w, by_mid + bh//2], radius=3, fill=(245, 90, 45))

    draw_target.paste(card_im, (x0, y0), card_im)

# -------------------------------------------------------------
# 2B. TOP DOT-DASH PROGRESS TRACKER (FROM VIDEO 1)
# -------------------------------------------------------------
def render_dots_progress_tracker(draw_target, cx: int, cy: int, total_dots: int = 7, active_index: int = 0):
    """
    Renders the minimal progress tracker: • • • — • • •
    The active item expands into a rounded horizontal dash, inactive are dots.
    """
    draw = ImageDraw.Draw(draw_target)
    dot_r = 5
    dash_w = 32
    gap = 20
    # Calculate total width
    total_w = (total_dots - 1) * gap + dash_w
    start_x = cx - total_w // 2

    cur_x = start_x
    for i in range(total_dots):
        if i == active_index:
            draw.rounded_rectangle([cur_x, cy - dot_r, cur_x + dash_w, cy + dot_r], radius=dot_r, fill=(40, 45, 60))
            cur_x += dash_w + gap
        else:
            draw.ellipse([cur_x, cy - dot_r, cur_x + dot_r * 2, cy + dot_r], fill=(185, 190, 205))
            cur_x += dot_r * 2 + gap

# -------------------------------------------------------------
# 2C. STRIKETHROUGH PRICING / COMPARISON HERO CARD
# -------------------------------------------------------------
def render_strikethrough_card(draw_target, bbox, title: str, strike_text: str, new_text: str, tag: str = "100% FREE", squircle_color=C_ORANGE):
    """
    Renders comparison card with high-impact red strikethrough over expensive competitor/cost.
    """
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0

    # Ambient drop shadow
    shadow = Image.new("RGBA", (w + 100, h + 100), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([50, 50, 50 + w, 50 + h], radius=28, fill=(255, 120, 50, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    draw_target.paste(shadow, (x0 - 50, y0 - 50), shadow)

    card_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_im)
    cdraw.rounded_rectangle([0, 0, w, h], radius=26, fill=(255, 255, 255, 250), outline=(255, 255, 255, 255), width=2)

    # App icon
    pad = 28
    icon_s = 64
    cdraw.rounded_rectangle([pad, pad, pad + icon_s, pad + icon_s], radius=16, fill=squircle_color)
    draw_star(cdraw, pad + icon_s // 2, pad + icon_s // 2, r_outer=18, r_inner=8, fill=C_WHITE)

    # Title
    cdraw.text((pad + icon_s + 20, pad + 6), title, fill=(20, 22, 28), font=get_font(28))
    # Green tag pill
    cdraw.rounded_rectangle([pad + icon_s + 20, pad + 44, pad + icon_s + 180, pad + 72], radius=14, fill=(235, 248, 240))
    cdraw.text((pad + icon_s + 32, pad + 48), f"• {tag}", fill=(35, 160, 80), font=get_font(14))

    # Old text with RED strikethrough
    old_font = get_font(32)
    old_y = pad + icon_s + 36
    tb = cdraw.textbbox((pad, old_y), strike_text, font=old_font)
    cdraw.text((pad, old_y), strike_text, fill=(160, 165, 175), font=old_font)
    strike_mid = (tb[1] + tb[3]) // 2
    cdraw.line([(tb[0] - 6, strike_mid + 4), (tb[2] + 8, strike_mid - 4)], fill=C_RED, width=4)

    # New replacement text
    new_font = get_font(42)
    new_y = old_y + 44
    cdraw.text((pad, new_y), new_text, fill=(35, 180, 85), font=new_font)

    draw_target.paste(card_im, (x0, y0), card_im)

# -------------------------------------------------------------
# 3. GENUINE GITHUB REPOSITORY CARD (FROM VIDEO 2)
# -------------------------------------------------------------
def render_github_repo_card(draw_target, bbox, author, repo_name, description, stars="41.4k", forks="5.6k", badge_num="#1"):
    """Renders the authentic dark-mode GitHub repo card with glowing neon border and stats."""
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0

    # Ambient border glow
    glow = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=24, outline=(255, 140, 40, 120), width=4)
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    draw_target.paste(glow, (x0 - 20, y0 - 20), glow)

    # Card body
    card_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_im)
    cdraw.rounded_rectangle([0, 0, w, h], radius=22, fill=(16, 18, 28, 250), outline=(255, 160, 50), width=2)

    # GitHub Octocat Header
    draw_octocat(cdraw, 42, 42, r=18, bg_color=(255, 255, 255), fg_color=(16, 18, 28))
    cdraw.text((72, 34), "GitHub repo", fill=C_MUTED, font=get_font(18))

    # Badge #1 in top-right
    cdraw.rounded_rectangle([w - 75, 20, w - 24, 62], radius=10, fill=(255, 150, 30))
    cdraw.text((w - 50, 41), badge_num, fill=C_BLACK, font=get_font(24), anchor="mm")

    # Author avatar + handle
    cdraw.ellipse([24, 82, 60, 118], fill=(60, 70, 95))
    cdraw.text((72, 92), f"{author} /", fill=C_MUTED, font=get_font(20))

    # Big Bold Repo Name
    cdraw.text((24, 130), repo_name, fill=C_WHITE, font=get_font(42))

    # Description
    cdraw.text((24, 186), description, fill=C_MUTED, font=get_font(18))

    # Stars, Forks, MIT badge
    stat_y = h - 35
    draw_star(cdraw, 34, stat_y + 10, r_outer=10, r_inner=4, fill=(255, 215, 60))
    cdraw.text((50, stat_y), stars, fill=C_WHITE, font=get_font(19))

    draw_fork_icon(cdraw, 130, stat_y + 10, size=14, color=C_MUTED)
    cdraw.text((146, stat_y), forks, fill=C_MUTED, font=get_font(19))

    cdraw.text((220, stat_y), "• MIT • Open source", fill=C_GREEN, font=get_font(18))

    draw_target.paste(card_im, (x0, y0), card_im)

# -------------------------------------------------------------
# 4. MACOS DARK TERMINAL WINDOW
# -------------------------------------------------------------
def render_terminal_window(draw_target, bbox, command="claude", prompt="~ $", banner_text="Welcome to Claude Code!", output_line="> build my app"):
    """Renders the authentic dark terminal window with 3 window controls and typing prompt."""
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0

    term_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(term_im)
    tdraw.rounded_rectangle([0, 0, w, h], radius=18, fill=(18, 16, 24, 250), outline=(50, 45, 65), width=2)

    # Window Controls (Red, Yellow, Green dots)
    tdraw.ellipse([20, 18, 34, 32], fill=(255, 95, 85))
    tdraw.ellipse([42, 18, 56, 32], fill=(255, 190, 45))
    tdraw.ellipse([64, 18, 78, 32], fill=(40, 205, 65))
    tdraw.text((100, 18), "terminal", fill=(120, 115, 135), font=get_font(15))

    # Terminal Prompt
    tdraw.text((24, 58), prompt, fill=C_GREEN, font=get_font(20))
    tdraw.text((68, 58), command, fill=C_WHITE, font=get_font(20))

    # Boxed Banner
    tdraw.rounded_rectangle([24, 95, w - 24, 145], radius=10, fill=(28, 22, 32), outline=(90, 50, 60), width=1)
    # Sunburst icon simple
    tdraw.text((45, 120), "✹", fill=(235, 120, 95), font=get_font(22), anchor="mm")
    tdraw.text((68, 110), banner_text, fill=(235, 130, 110), font=get_font(18))

    # Output line with white block cursor
    tdraw.text((24, 165), output_line, fill=C_MUTED, font=get_font(20))
    tb = tdraw.textbbox((24, 165), output_line, font=get_font(20))
    cur_x = tb[2] + 4
    tdraw.rectangle([cur_x, 167, cur_x + 10, 187], fill=C_WHITE)

    draw_target.paste(term_im, (x0, y0), term_im)

# -------------------------------------------------------------
# 5. 3D ANGLED SLAM STICKER / STAMP BADGE
# -------------------------------------------------------------
def render_slam_sticker(cx: int, cy: int, text: str, bg_color=C_RED, text_color=C_WHITE, angle: float = -9.0, font_size: int = 24):
    """Generates a 3D angled stamp badge with high-contrast border and rotated transform."""
    font = get_font(font_size)
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    tb = dummy.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 26, 12
    bw, bh = tw + pad_x * 2, th + pad_y * 2

    im = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(im)
    idraw.rounded_rectangle([10, 10, bw + 10, bh + 10], radius=14, fill=bg_color, outline=(255, 255, 255, 220), width=2)
    idraw.text((bw // 2 + 10, bh // 2 + 10), text, fill=text_color, font=font, anchor="mm")

    rotated = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    rx = int(cx - rotated.width // 2)
    ry = int(cy - rotated.height // 2)
    return rotated, rx, ry

# -------------------------------------------------------------
# 6. MODEL SWITCHING & FAILOVER VISUALIZER
# -------------------------------------------------------------
def render_model_switch_failover(draw_target, top_y: int, cx: int = None, fill_pct: float = 1.0, is_limit_reached: bool = True):
    """Renders the exact Model 1 -> Model 2 failover sequence from Video 2."""
    if cx is None:
        cx = draw_target.width // 2

    # Model 1 Card
    m1_color = C_RED if is_limit_reached else C_GREEN
    card1 = Image.new("RGBA", (840, 100), (0, 0, 0, 0))
    c1draw = ImageDraw.Draw(card1)
    c1draw.rounded_rectangle([0, 0, 840, 100], radius=20, fill=(18, 16, 26), outline=(90, 45, 55) if is_limit_reached else (35, 75, 55), width=2)
    c1draw.ellipse([35, 38, 59, 62], fill=m1_color)
    c1draw.text((80, 36), "MODEL 1", fill=C_MUTED if is_limit_reached else C_WHITE, font=get_font(28))
    draw_target.paste(card1, (cx - 420, top_y), card1)

    # Session limit bar
    bar_y = top_y + 115
    b_im = Image.new("RGBA", (840, 50), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(b_im)
    bdraw.text((0, 0), "SESSION LIMIT", fill=C_MUTED, font=get_font(16))
    bdraw.text((840, 0), f"{int(fill_pct*100)}%", fill=C_RED if is_limit_reached else C_ORANGE, font=get_font(16), anchor="ra")
    bdraw.rounded_rectangle([0, 24, 840, 46], radius=10, fill=(28, 22, 32))
    fill_w = int(840 * clamp(fill_pct))
    if fill_w > 0:
        bdraw.rounded_rectangle([0, 24, fill_w, 46], radius=10, fill=C_RED if is_limit_reached else C_ORANGE)
    draw_target.paste(b_im, (cx - 420, bar_y), b_im)

    # 3D Angled "LIMIT REACHED" Sticker
    if is_limit_reached:
        st_im, sx, sy = render_slam_sticker(cx + 180, top_y + 40, "LIMIT REACHED", C_RED, C_BLACK, angle=-9, font_size=26)
        draw_target.paste(st_im, (sx, sy), st_im)

    # Downward Animated Yellow Arrow
    arrow_y0 = bar_y + 65
    arrow_y1 = arrow_y0 + 90
    adraw = ImageDraw.Draw(draw_target)
    adraw.line([(cx, arrow_y0), (cx, arrow_y1 - 18)], fill=C_YELLOW, width=6)
    adraw.polygon([(cx, arrow_y1), (cx - 18, arrow_y1 - 22), (cx + 18, arrow_y1 - 22)], fill=C_YELLOW)

    # Model 2 Card with Auto Switch Pill
    m2_y = arrow_y1 + 25
    card2 = Image.new("RGBA", (840, 100), (0, 0, 0, 0))
    c2draw = ImageDraw.Draw(card2)
    c2draw.rounded_rectangle([0, 0, 840, 100], radius=20, fill=(18, 16, 26), outline=C_GREEN, width=2)
    c2draw.ellipse([35, 38, 59, 62], fill=C_GREEN)
    c2draw.text((80, 36), "MODEL 2", fill=C_WHITE, font=get_font(28))
    draw_target.paste(card2, (cx - 420, m2_y), card2)

    # Green AUTO SWITCH Pill
    as_im = Image.new("RGBA", (220, 50), (0, 0, 0, 0))
    asdraw = ImageDraw.Draw(as_im)
    asdraw.rounded_rectangle([0, 0, 220, 50], radius=14, fill=C_GREEN)
    asdraw.text((110, 25), "AUTO SWITCH", fill=C_BLACK, font=get_font(18), anchor="mm")
    draw_target.paste(as_im, (cx - 110, m2_y + 115), as_im)

# -------------------------------------------------------------
# 7. 2D ILLUSTRATED COMIC CHARACTER RIG (FROM VIDEO 1)
# -------------------------------------------------------------
def render_comic_character(draw_target, cx: int, cy: int, pose="shrug", mouth="smile"):
    """
    Renders the exact comic-style illustrated character:
    - Red stippled baseball cap
    - Curled black side hair
    - Detailed knitted sweater with cuff stripes & chest clover emblem
    - Expressive mouth, blushes & articulated arms
    """
    char_im = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(char_im)
    x, y = 300, 280

    # 1. Knit Sweater (Stippled grey texture)
    cdraw.rounded_rectangle([x - 140, y + 40, x + 140, y + 260], radius=28, fill=(240, 240, 242), outline=(20, 20, 25), width=3)
    # Stippled dots inside sweater
    for di in range(40):
        dx = x - 120 + (di * 17) % 240
        dy = y + 55 + (di * 23) % 190
        cdraw.ellipse([dx, dy, dx + 2, dy + 2], fill=(160, 165, 175))
    # Bottom ribbing
    cdraw.line([(x - 140, y + 235), (x + 140, y + 235)], fill=(20, 20, 25), width=2)
    for r in range(x - 130, x + 130, 12):
        cdraw.line([(r, y + 235), (r, y + 260)], fill=(120, 125, 135), width=1)
    # Red flower chest emblem
    cdraw.ellipse([x + 45, y + 90, x + 57, y + 102], fill=(230, 50, 40))
    cdraw.ellipse([x + 35, y + 90, x + 47, y + 102], fill=(230, 50, 40))
    cdraw.ellipse([x + 40, y + 83, x + 52, y + 95], fill=(230, 50, 40))
    cdraw.ellipse([x + 40, y + 97, x + 52, y + 109], fill=(230, 50, 40))

    # 2. Neck & Stitched Collar
    cdraw.rectangle([x - 30, y + 5, x + 30, y + 50], fill=(255, 230, 215), outline=(20, 20, 25), width=3)
    cdraw.arc([x - 45, y + 30, x + 45, y + 65], 0, 180, fill=(20, 20, 25), width=3)

    # 3. Head & Face
    cdraw.ellipse([x - 85, y - 110, x + 85, y + 35], fill=(255, 230, 215), outline=(20, 20, 25), width=3)
    # Cute ears
    cdraw.ellipse([x - 110, y - 50, x - 75, y], fill=(255, 230, 215), outline=(20, 20, 25), width=3)
    cdraw.ellipse([x + 75, y - 50, x + 110, y], fill=(255, 230, 215), outline=(20, 20, 25), width=3)
    # Curled black hair on sides
    for hx, hy in [(x - 85, y - 70), (x - 80, y - 85), (x + 80, y - 70), (x + 75, y - 85)]:
        cdraw.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=(20, 20, 25))

    # 4. Red Baseball Cap with Stippled Pattern
    cdraw.chord([x - 90, y - 150, x + 90, y - 30], 180, 360, fill=(235, 75, 50), outline=(20, 20, 25), width=3)
    # Stipple pattern on cap
    for ci in range(25):
        cxp = x - 70 + (ci * 13) % 140
        cyp = y - 130 + (ci * 11) % 70
        cdraw.ellipse([cxp, cyp, cxp + 1, cyp + 1], fill=(180, 45, 30))
    # Visor
    cdraw.rounded_rectangle([x - 105, y - 70, x + 75, y - 48], radius=8, fill=(215, 60, 40), outline=(20, 20, 25), width=3)
    cdraw.ellipse([x - 6, y - 152, x + 6, y - 140], fill=(20, 20, 25)) # top button

    # 5. Facial Features
    # Eyebrows
    cdraw.arc([x - 50, y - 55, x - 20, y - 35], 200, 340, fill=(20, 20, 25), width=3)
    cdraw.arc([x + 20, y - 55, x + 50, y - 35], 200, 340, fill=(20, 20, 25), width=3)
    # Eyes (clear dots)
    cdraw.ellipse([x - 42, y - 30, x - 28, y - 16], fill=(20, 20, 25))
    cdraw.ellipse([x + 28, y - 30, x + 42, y - 16], fill=(20, 20, 25))
    # Nose line
    cdraw.arc([x - 10, y - 18, x + 10, y], 0, 180, fill=(20, 20, 25), width=2)
    # Pink cheek blush dots
    cdraw.ellipse([x - 55, y - 12, x - 45, y - 2], fill=(255, 170, 170))
    cdraw.ellipse([x + 45, y - 12, x + 55, y - 2], fill=(255, 170, 170))
    # Mouth
    if mouth == "smile":
        cdraw.chord([x - 30, y + 8, x + 30, y + 36], 0, 180, fill=(180, 40, 45), outline=(20, 20, 25), width=2)
        cdraw.chord([x - 18, y + 20, x + 18, y + 36], 0, 180, fill=(245, 120, 130)) # tongue
    else:
        cdraw.line([(x - 20, y + 18), (x + 20, y + 18)], fill=(20, 20, 25), width=3)

    # 6. Arms and Gestures with Striped Cuffs
    if pose == "shrug":
        # Left arm extending left
        cdraw.line([(x - 130, y + 70), (x - 220, y + 150), (x - 260, y + 160)], fill=(240, 240, 242), width=26)
        cdraw.line([(x - 130, y + 70), (x - 220, y + 150), (x - 260, y + 160)], fill=(20, 20, 25), width=3)
        # Cuff stripes
        cdraw.rectangle([x - 250, y + 146, x - 235, y + 172], fill=(235, 75, 50), outline=(20, 20, 25))
        # Hand with articulated fingers
        cdraw.ellipse([x - 280, y + 150, x - 255, y + 175], fill=(255, 230, 215), outline=(20, 20, 25), width=2)
        # Right arm extending right
        cdraw.line([(x + 130, y + 70), (x + 220, y + 150), (x + 260, y + 160)], fill=(240, 240, 242), width=26)
        cdraw.rectangle([x + 235, y + 146, x + 250, y + 172], fill=(235, 75, 50), outline=(20, 20, 25))
        cdraw.ellipse([x + 255, y + 150, x + 280, y + 175], fill=(255, 230, 215), outline=(20, 20, 25), width=2)

    draw_target.paste(char_im, (cx - 300, cy - 280), char_im)

# -------------------------------------------------------------
# 8. HIGH-CONTRAST KINETIC PILL CAPTIONS
# -------------------------------------------------------------
def render_kinetic_pill_caption(draw_target, text_chunk: str, active_word: str, cx: int, cy: int, pill_bg=(35, 45, 140)):
    """Renders the containerized high-contrast pill subtitle from Video 2."""
    font = get_font(28)
    words = text_chunk.split()
    spacings = []
    tot_w = 0
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for wi, w in enumerate(words):
        w_str = w.upper() + (" " if wi < len(words) - 1 else "")
        tb = dummy.textbbox((0, 0), w_str, font=font)
        ww = tb[2] - tb[0]
        spacings.append((w_str, ww, w.upper() == active_word.upper()))
        tot_w += ww

    pill_w = max(320, tot_w + 50)
    pill_h = 60
    pill_x0 = cx - pill_w // 2
    pill_y0 = cy - pill_h // 2

    # Draw pill container
    p_im = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(p_im)
    pdraw.rounded_rectangle([0, 0, pill_w, pill_h], radius=14, fill=(pill_bg[0], pill_bg[1], pill_bg[2], 250))
    draw_target.paste(p_im, (pill_x0, pill_y0), p_im)

    # Render words
    draw = ImageDraw.Draw(draw_target)
    cur_x = cx - tot_w // 2
    for w_str, ww, is_active in spacings:
        col = C_YELLOW if is_active else C_WHITE
        draw.text((cur_x, cy), w_str, fill=col, font=font, anchor="lm")
        cur_x += ww
