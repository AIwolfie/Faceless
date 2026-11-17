#!/usr/bin/env python3
"""
universal_branding.py — Canonical Universal Intro & Outro Renderer.
Replicates the exact, battle-tested intro & outro choreography from stop_paying_for_ai_local_llms:
- Procedural concentric tech glow rings with spring easing
- Official channel logo integrated directly inside the ring and outro
- Smooth harmonic micro-motion floating (smooth_float)
- Channel badge & brand typography hierarchy
- Dynamic red-to-green subscribe button conversion
- Smooth OS cursor Bezier trajectory glide, tactile compression pulse, and expanding gold shockwave ripple
- Full resolution responsiveness: 1080p horizontal (1920x1080), 4K UHD (3840x2160), and 9:16 vertical Shorts (1080x1920).
"""

import os
import math
from typing import Tuple, Optional, Callable
from PIL import Image, ImageDraw, ImageFont

# Brand Palette (Tech standard)
C_WHITE = (255, 255, 255)
C_CYAN = (70, 220, 255)
C_PURPLE = (140, 75, 255)
C_RING_OUTER = (30, 16, 70)
C_RING_INNER = (16, 12, 38)
C_SUB_RED = (255, 30, 50)
C_SUB_GREEN = (35, 195, 110)
C_YELLOW = (255, 205, 70)

_DEFAULT_FONTS = {}
def _get_font(size: int) -> ImageFont.ImageFont:
    if size not in _DEFAULT_FONTS:
        # Search candidate font locations
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidates = [
            os.path.join(repo_root, "fonts", "InterDisplay-Bold.otf"),
            os.path.join(repo_root, "fonts", "Inter-Bold.ttf"),
            r"C:\Windows\Fonts\Arialbd.ttf",
            r"C:\Windows\Fonts\Segoeui.ttf"
        ]
        for c in candidates:
            if os.path.exists(c):
                try:
                    _DEFAULT_FONTS[size] = ImageFont.truetype(c, size)
                    break
                except Exception:
                    pass
        if size not in _DEFAULT_FONTS:
            _DEFAULT_FONTS[size] = ImageFont.load_default()
    return _DEFAULT_FONTS[size]

_ACTIVE_LOGO: Optional[Image.Image] = None
def find_active_logo() -> Optional[Image.Image]:
    """Resolves channel logo from private space or media directory."""
    global _ACTIVE_LOGO
    if _ACTIVE_LOGO is not None:
        return _ACTIVE_LOGO
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(repo_root, "Kenil", "assets", "txk_logo.png"),
        os.path.join(repo_root, "Kenil", "assets", "TXK AI Tech Code Logo.png"),
        os.path.join(repo_root, "media", "logo.png"),
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                _ACTIVE_LOGO = Image.open(c).convert("RGBA")
                return _ACTIVE_LOGO
            except Exception:
                pass
    return None

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def ease_out_quart(x: float) -> float:
    x = clamp(x)
    return 1.0 - math.pow(1.0 - x, 4)

def ease_in_out(x: float) -> float:
    x = clamp(x)
    return x * x * (3.0 - 2.0 * x)

def smooth_float(t: float, freq: float = 1.6, amp: float = 4.0, phase: float = 0.0) -> float:
    return amp * math.sin(t * freq * 2.0 * math.pi + phase)

def bezier_point(p0: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float], t: float) -> Tuple[float, float]:
    t = clamp(t)
    u = 1.0 - t
    x = u * u * p0[0] + 2.0 * u * t * p1[0] + t * t * p2[0]
    y = u * u * p0[1] + 2.0 * u * t * p1[1] + t * t * p2[1]
    return (x, y)

def draw_cursor(
    dr: ImageDraw.ImageDraw,
    pos: Tuple[float, float],
    click_p: float = 0.0,
    color: Tuple[int, int, int] = (255, 255, 255),
    ripple: Tuple[int, int, int] = C_YELLOW,
    scale: float = 1.0
):
    """Draws an authentic dark-mode OS cursor with dynamic click ripple."""
    x, y = pos
    s = scale
    poly = [
        (x, y),
        (x, y + int(36 * s)),
        (x + int(10 * s), y + int(28 * s)),
        (x + int(18 * s), y + int(44 * s)),
        (x + int(24 * s), y + int(41 * s)),
        (x + int(16 * s), y + int(25 * s)),
        (x + int(29 * s), y + int(25 * s))
    ]
    dr.polygon(poly, fill=color, outline=(0, 0, 0), width=max(1, int(2 * s)))

    if 0.0 < click_p < 1.0:
        r = int((14 + 55 * click_p) * s)
        dr.ellipse([x - r, y - r, x + r, y + r], outline=ripple, width=max(2, int(4 * s)))


def draw_universal_intro(
    dr: ImageDraw.ImageDraw,
    w: int,
    h: int,
    t_sc: float,
    channel_name: str = "TechChannel",
    badge: str = "TC",
    tagline: str = "AI • TECH • CODE",
    is_vertical: Optional[bool] = None,
    font_func: Optional[Callable[[int], ImageFont.ImageFont]] = None,
    im: Optional[Image.Image] = None,
    logo_img: Optional[Image.Image] = None
):
    """
    Renders the universal Intro card with concentric tech rings and official logo.
    Works for 1920x1080 (horizontal), 4K UHD, and 1080x1920 (Shorts).
    """
    f = font_func or _get_font
    if is_vertical is None:
        is_vertical = (h > w)

    if logo_img is None:
        logo_img = find_active_logo()

    cx = w // 2
    if not is_vertical:
        # Horizontal (1920x1080 standard)
        sc = w / 1920.0
        cy_ring = int(320 * sc)
        r_base = int(140 * sc)
        name_y = int(570 * sc)
        tag_y = int(675 * sc)
        badge_sz = int(84 * sc)
        name_sz = int(130 * sc)
        tag_sz = int(46 * sc)
    else:
        # Vertical (1080x1920 Shorts standard)
        sc = w / 1080.0
        cy_ring = int(700 * sc)
        r_base = int(160 * sc)
        name_y = cy_ring + r_base + int(90 * sc)
        tag_y = cy_ring + r_base + int(175 * sc)
        badge_sz = int(92 * sc)
        name_sz = int(100 * sc)
        tag_sz = int(36 * sc)

    s = ease_out_quart(t_sc / 0.6)
    r = int(r_base * s)
    flt = smooth_float(t_sc, freq=1.6, amp=4.0 * sc)

    # Concentric Tech Glow Rings
    r_outer = r + int(10 * sc)
    dr.ellipse([cx - r_outer, cy_ring - r_outer, cx + r_outer, cy_ring + r_outer],
               fill=C_RING_OUTER, outline=C_CYAN, width=max(1, int(3 * sc)))
    dr.ellipse([cx - r, cy_ring - r, cx + r, cy_ring + r], fill=C_PURPLE)
    r_inner = max(1, r - int(22 * sc))
    dr.ellipse([cx - r_inner, cy_ring - r_inner, cx + r_inner, cy_ring + r_inner], fill=C_RING_INNER)

    # Official Logo or Badge in center of ring
    if logo_img is not None and im is not None and s > 0.35:
        logo_sz = int(r_inner * 1.95)
        if logo_sz > 10:
            res_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
            lx = cx - logo_sz // 2
            ly = cy_ring - logo_sz // 2 + int(flt)
            im.paste(res_logo, (lx, ly), res_logo)
    elif s > 0.6:
        # Fallback procedural badge text
        dr.text((cx, cy_ring + int(flt)), badge, fill=C_WHITE, font=f(int(badge_sz * s)), anchor="mm")

    if s > 0.5:
        # Channel Name
        dr.text((cx, name_y), channel_name, fill=C_WHITE, font=f(name_sz), anchor="mm")
        # Tagline
        dr.text((cx, tag_y), tagline, fill=C_CYAN, font=f(tag_sz), anchor="mm")


def draw_universal_outro(
    dr: ImageDraw.ImageDraw,
    w: int,
    h: int,
    t_sc: float,
    channel_name: str = "TechChannel",
    tagline: str = "AI • TECH • CODE",
    click_time: float = 3.8,
    is_vertical: Optional[bool] = None,
    comment_prompt: Optional[str] = None,
    font_func: Optional[Callable[[int], ImageFont.ImageFont]] = None,
    im: Optional[Image.Image] = None,
    logo_img: Optional[Image.Image] = None
):
    """
    Renders the universal Outro conversion card with official logo and subscribe button.
    Works for 1920x1080 (horizontal), 4K UHD, and 1080x1920 (Shorts).
    """
    f = font_func or _get_font
    if is_vertical is None:
        is_vertical = (h > w)

    if logo_img is None:
        logo_img = find_active_logo()

    cx = w // 2
    flt = smooth_float(t_sc, freq=1.5, amp=3.5)

    if not is_vertical:
        # Horizontal (1920x1080 standard)
        sc = w / 1920.0
        logo_sz = int(140 * sc)
        logo_y = int(170 * sc)
        name_y = int(320 * sc)
        tag_y = int(410 * sc)
        btn_y = int(620 * sc)
        btn_w, btn_h = int(740 * sc), int(160 * sc)
        name_sz = int(130 * sc)
        tag_sz = int(44 * sc)
        btn_font_sz = int(84 * sc)
        prompt_y = int(765 * sc)
        prompt_sz = int(32 * sc)

        cur_start = (int(1650 * sc), int(950 * sc))
        cur_mid = (int(1350 * sc), int(650 * sc))
        cur_target = (cx + int(30 * sc), btn_y + int(10 * sc))
        cur_exit_mid = (cx + int(200 * sc), btn_y + int(150 * sc))
        cur_end = (int(1600 * sc), int(950 * sc))
    else:
        # Vertical (1080x1920 Shorts standard)
        sc = w / 1080.0
        logo_sz = int(220 * sc)
        logo_y = int(440 * sc)
        name_y = int(630 * sc)
        tag_y = int(715 * sc)
        btn_y = int(920 * sc)
        btn_w, btn_h = int(600 * sc), int(144 * sc)
        name_sz = int(98 * sc)
        tag_sz = int(36 * sc)
        btn_font_sz = int(66 * sc)
        prompt_y = int(1140 * sc)
        prompt_sz = int(28 * sc)

        cur_start = (int(920 * sc), int(1500 * sc))
        cur_mid = (int(760 * sc), int(1100 * sc))
        cur_target = (cx + int(25 * sc), btn_y + int(10 * sc))
        cur_exit_mid = (cx + int(160 * sc), btn_y + int(180 * sc))
        cur_end = (int(900 * sc), int(1450 * sc))

    # 1. Official Logo
    if logo_img is not None and im is not None:
        res_outro_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
        olx = cx - logo_sz // 2
        oly = logo_y - logo_sz // 2 + int(flt * sc)
        im.paste(res_outro_logo, (olx, oly), res_outro_logo)

    # 2. Channel Name & Tagline
    dr.text((cx, name_y), channel_name, fill=C_WHITE, font=f(name_sz), anchor="mm")
    dr.text((cx, tag_y), tagline, fill=C_CYAN, font=f(tag_sz), anchor="mm")

    # 3. Dynamic Subscribe Button: Red -> Green transition
    is_subscribed = (t_sc >= (click_time + 0.2))

    # Scale compression bounce on click
    if (click_time - 0.1) <= t_sc <= (click_time + 0.3):
        press_s = 0.94 + 0.06 * math.sin((t_sc - (click_time - 0.1)) / 0.4 * math.pi)
    else:
        press_s = 1.0 + (0.015 * math.sin(t_sc * 6.0) if is_subscribed else 0.0)

    cur_w = int(btn_w * press_s)
    cur_h = int(btn_h * press_s)
    cur_box = [cx - cur_w // 2, btn_y - cur_h // 2, cx + cur_w // 2, btn_y + cur_h // 2]

    btn_color = C_SUB_GREEN if is_subscribed else C_SUB_RED
    btn_text = "✓ SUBSCRIBED!" if is_subscribed else "SUBSCRIBE"

    dr.rounded_rectangle(cur_box, radius=cur_h // 2, fill=btn_color)
    dr.text((cx, btn_y), btn_text, fill=C_WHITE, font=f(btn_font_sz), anchor="mm")

    # Expanding gold ripple ring on click
    if is_subscribed:
        rip_p = clamp((t_sc - click_time) / 0.8)
        if rip_p < 1.0:
            rip_r = int((btn_w * 0.45 + rip_p * 180) * sc)
            dr.ellipse([cx - rip_r, btn_y - rip_r, cx + rip_r, btn_y + rip_r],
                       outline=C_YELLOW, width=max(2, int(4 * sc)))

    # 4. Animated Cursor Glide & Click
    glide_start = max(0.5, click_time - 2.8)
    if glide_start <= t_sc <= click_time:
        p_cursor = ease_in_out((t_sc - glide_start) / (click_time - glide_start))
        pos = bezier_point(cur_start, cur_mid, cur_target, p_cursor)
        draw_cursor(dr, pos, click_p=0.0, scale=sc)
    elif click_time < t_sc <= (click_time + 0.6):
        click_p = (t_sc - click_time) / 0.6
        pos = cur_target
        draw_cursor(dr, pos, click_p=click_p, ripple=C_YELLOW, scale=sc)
    elif (click_time + 0.6) < t_sc <= (click_time + 3.0):
        p_exit = ease_out_quart((t_sc - (click_time + 0.6)) / 2.4)
        pos = bezier_point(cur_target, cur_exit_mid, cur_end, p_exit)
        draw_cursor(dr, pos, click_p=0.0, scale=sc)

    # 5. Prompt / Comment callout
    if comment_prompt:
        dr.text((cx, prompt_y + int(flt * sc)), comment_prompt, fill=C_YELLOW, font=f(prompt_sz), anchor="mm")
