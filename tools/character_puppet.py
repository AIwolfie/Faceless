#!/usr/bin/env python3
"""
character_puppet.py — Procedural 2D Character & Puppet Staging Engine.
Part of the Faceless Video Production Engine.

Renders expressive procedural 2D characters, stick figures, and vector puppets:
- Head, torso, segmented articulated limbs, and hands
- Configurable expressive face states: neutral, focused, shocked, error, happy, thinking
- Dynamic action poses: idle, point_left, point_right, explain, shock_recoil, inspect, error_glitch
- Customizable styles: Dark Cyber, Minimal Whiteboard, Blueprint Line, Accent Glow
- Fully alpha-composited into any video canvas (1080x1920 portrait or 1920x1080 landscape)
"""

from __future__ import annotations
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from typing import Tuple, Dict, Any, Optional

# Color Presets
THEMES = {
    "cyber_cyan": {
        "stroke": (70, 220, 255),
        "fill": (14, 20, 42),
        "glow": (30, 140, 220),
        "accent": (255, 205, 70),
        "eye": (70, 220, 255),
        "width": 6,
    },
    "cyber_glitch": {
        "stroke": (255, 45, 65),
        "fill": (35, 12, 22),
        "glow": (220, 30, 50),
        "accent": (255, 95, 30),
        "eye": (255, 45, 65),
        "width": 7,
    },
    "minimal_dark": {
        "stroke": (240, 245, 255),
        "fill": (20, 24, 38),
        "glow": (100, 140, 200),
        "accent": (70, 220, 255),
        "eye": (255, 255, 255),
        "width": 5,
    },
    "warm_handdrawn": {
        "stroke": (255, 225, 140),
        "fill": (30, 25, 20),
        "glow": (180, 130, 50),
        "accent": (255, 100, 50),
        "eye": (255, 235, 160),
        "width": 6,
    }
}

class CharacterPuppet:
    """Procedural 2D articulated character puppet."""
    def __init__(
        self,
        theme: str = "cyber_cyan",
        scale: float = 1.0,
        height_px: int = 650
    ):
        self.theme_name = theme
        self.cfg = THEMES.get(theme, THEMES["cyber_cyan"])
        self.scale = scale
        self.height_px = height_px

    def _draw_limb(
        self,
        draw: ImageDraw.ImageDraw,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        col: Tuple[int, int, int],
        width: int
    ):
        """Draws upper and lower limb segments with joint caps."""
        x0, y0 = p0
        x1, y1 = p1
        x2, y2 = p2
        # Upper limb
        draw.line([(x0, y0), (x1, y1)], fill=col, width=width)
        # Lower limb
        draw.line([(x1, y1), (x2, y2)], fill=col, width=width)
        # Joint cap
        r = width // 2 + 1
        draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=col)

    def render(
        self,
        canvas_size: Tuple[int, int],
        position: Tuple[int, int],
        pose: str = "idle",
        expression: str = "neutral",
        p_anim: float = 0.0,
        flip_x: bool = False
    ) -> Image.Image:
        """
        Renders the character onto a transparent RGBA image of canvas_size.
        position: (center_x, ground_y)
        """
        w, h = canvas_size
        cx, gy = position
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        col = self.cfg["stroke"]
        fill_col = self.cfg["fill"]
        eye_col = self.cfg["eye"]
        accent = self.cfg["accent"]
        l_w = max(2, int(self.cfg["width"] * self.scale))

        # Anatomy dimensions
        tot_h = self.height_px * self.scale
        head_r = int(tot_h * 0.14)
        torso_len = int(tot_h * 0.35)
        leg_len = int(tot_h * 0.40)
        arm_len = int(tot_h * 0.32)

        # Base skeletal points
        hips_y = gy - leg_len
        neck_y = hips_y - torso_len
        head_cy = neck_y - head_r

        # Breathing / idle bob
        bob_y = math.sin(p_anim * 2.0 * math.pi) * (4.0 * self.scale)
        neck_y += bob_y
        head_cy += bob_y

        # Torso spine
        draw.line([(cx, neck_y), (cx, hips_y)], fill=col, width=l_w + 2)

        # Pose Kinematics
        # Left & Right arm joints: (shoulder, elbow, hand)
        sh_l = (cx - int(24 * self.scale), neck_y + int(10 * self.scale))
        sh_r = (cx + int(24 * self.scale), neck_y + int(10 * self.scale))

        if pose == "point_right":
            # Right arm extended pointing up-right
            elb_r = (cx + int(arm_len * 0.55), neck_y - int(arm_len * 0.2))
            hand_r = (cx + int(arm_len * 1.1), neck_y - int(arm_len * 0.55))
            # Left arm on hip
            elb_l = (cx - int(arm_len * 0.5), neck_y + int(arm_len * 0.3))
            hand_l = (cx - int(15 * self.scale), hips_y)
        elif pose == "point_left":
            elb_l = (cx - int(arm_len * 0.55), neck_y - int(arm_len * 0.2))
            hand_l = (cx - int(arm_len * 1.1), neck_y - int(arm_len * 0.55))
            elb_r = (cx + int(arm_len * 0.5), neck_y + int(arm_len * 0.3))
            hand_r = (cx + int(15 * self.scale), hips_y)
        elif pose == "thinking":
            # Right hand touching chin
            elb_r = (cx + int(arm_len * 0.4), neck_y + int(arm_len * 0.25))
            hand_r = (cx + int(10 * self.scale), head_cy + int(head_r * 0.7))
            elb_l = (cx - int(arm_len * 0.45), neck_y + int(arm_len * 0.35))
            hand_l = (cx - int(10 * self.scale), hips_y)
        elif pose == "shock_recoil":
            # Both hands raised in shock
            elb_l = (cx - int(arm_len * 0.6), neck_y - int(arm_len * 0.3))
            hand_l = (cx - int(arm_len * 0.7), head_cy - int(head_r * 0.3))
            elb_r = (cx + int(arm_len * 0.6), neck_y - int(arm_len * 0.3))
            hand_r = (cx + int(arm_len * 0.7), head_cy - int(head_r * 0.3))
        elif pose == "explain":
            # Both hands gestural open outwards
            g_phase = math.sin(p_anim * 4.0 * math.pi) * (10.0 * self.scale)
            elb_l = (cx - int(arm_len * 0.5), neck_y + int(arm_len * 0.2))
            hand_l = (cx - int(arm_len * 0.95), neck_y - int(arm_len * 0.15) + g_phase)
            elb_r = (cx + int(arm_len * 0.5), neck_y + int(arm_len * 0.2))
            hand_r = (cx + int(arm_len * 0.95), neck_y - int(arm_len * 0.15) - g_phase)
        else:  # idle
            elb_l = (cx - int(arm_len * 0.3), neck_y + int(arm_len * 0.5))
            hand_l = (cx - int(arm_len * 0.2), neck_y + arm_len)
            elb_r = (cx + int(arm_len * 0.3), neck_y + int(arm_len * 0.5))
            hand_r = (cx + int(arm_len * 0.2), neck_y + arm_len)

        # Legs joints: (hip, knee, foot)
        hip_l = (cx - int(16 * self.scale), hips_y)
        hip_r = (cx + int(16 * self.scale), hips_y)
        knee_y = hips_y + int(leg_len * 0.5)
        foot_y = gy

        if pose == "shock_recoil":
            knee_l = (cx - int(38 * self.scale), knee_y)
            foot_l = (cx - int(55 * self.scale), foot_y)
            knee_r = (cx + int(38 * self.scale), knee_y)
            foot_r = (cx + int(55 * self.scale), foot_y)
        else:
            knee_l = (cx - int(20 * self.scale), knee_y)
            foot_l = (cx - int(24 * self.scale), foot_y)
            knee_r = (cx + int(20 * self.scale), knee_y)
            foot_r = (cx + int(24 * self.scale), foot_y)

        # Draw legs
        self._draw_limb(draw, hip_l, knee_l, foot_l, col, l_w)
        self._draw_limb(draw, hip_r, knee_r, foot_r, col, l_w)

        # Draw arms
        self._draw_limb(draw, sh_l, elb_l, hand_l, col, l_w)
        self._draw_limb(draw, sh_r, elb_r, hand_r, col, l_w)

        # Head (solid dark circle with glowing perimeter outline)
        draw.ellipse(
            [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
            fill=fill_col,
            outline=col,
            width=l_w
        )

        # Face Expression Details
        e_sz = max(2, int(6 * self.scale))
        eye_y = head_cy - int(head_r * 0.15)
        eye_spacing = int(head_r * 0.45)

        if expression == "error" or pose == "shock_recoil":
            # Crossed out or glowing exclamation eyes
            for side in (-1, 1):
                ex = cx + side * eye_spacing
                draw.line([(ex - e_sz, eye_y - e_sz), (ex + e_sz, eye_y + e_sz)], fill=accent, width=max(2, l_w // 2))
                draw.line([(ex - e_sz, eye_y + e_sz), (ex + e_sz, eye_y - e_sz)], fill=accent, width=max(2, l_w // 2))
            # Open O mouth
            draw.ellipse([cx - e_sz * 2, head_cy + int(head_r * 0.35), cx + e_sz * 2, head_cy + int(head_r * 0.65)], outline=col, width=2)
        elif expression == "thinking":
            # One eye squinted, one wide
            draw.ellipse([cx - eye_spacing - e_sz, eye_y - e_sz, cx - eye_spacing + e_sz, eye_y + e_sz], fill=eye_col)
            draw.line([(cx + eye_spacing - e_sz, eye_y), (cx + eye_spacing + e_sz, eye_y)], fill=eye_col, width=3)
            # Wavy mouth
            m_y = head_cy + int(head_r * 0.45)
            draw.line([(cx - int(head_r * 0.25), m_y), (cx + int(head_r * 0.25), m_y)], fill=col, width=2)
        elif expression == "focused":
            # Sharp visor / LED slit eyes
            draw.line([(cx - eye_spacing - e_sz, eye_y), (cx - eye_spacing + e_sz, eye_y)], fill=eye_col, width=3)
            draw.line([(cx + eye_spacing - e_sz, eye_y), (cx + eye_spacing + e_sz, eye_y)], fill=eye_col, width=3)
        else:  # neutral / default
            draw.ellipse([cx - eye_spacing - e_sz, eye_y - e_sz, cx - eye_spacing + e_sz, eye_y + e_sz], fill=eye_col)
            draw.ellipse([cx + eye_spacing - e_sz, eye_y - e_sz, cx + eye_spacing + e_sz, eye_y + e_sz], fill=eye_col)
            # Subtle smile arc
            m_y = head_cy + int(head_r * 0.45)
            draw.arc([cx - int(head_r * 0.3), m_y - int(head_r * 0.15), cx + int(head_r * 0.3), m_y + int(head_r * 0.15)], start=0, end=180, fill=col, width=2)

        return im

if __name__ == "__main__":
    puppet = CharacterPuppet(theme="cyber_cyan", scale=1.0)
    canvas = (1080, 1920)
    img = puppet.render(canvas, position=(540, 1400), pose="point_right", expression="focused")
    img.save("test_character_render.png")
    print(f"Character puppet test render saved (size: {img.size})")
