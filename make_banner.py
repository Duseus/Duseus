# -*- coding: utf-8 -*-
"""生成 Duseus GitHub 主页封面 banner.png（GitHub 深色风格）"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 480  # 10:3 比例，适配 GitHub 主页宽度
BG = (13, 17, 23)        # #0d1117 GitHub dark
BLUE = (88, 166, 255)    # #58a6ff
BLUE_DIM = (31, 111, 235)
GRAY = (139, 148, 158)
WHITE = (230, 237, 243)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ---- 背景装饰：右侧大圆弧光晕 ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(glow)
# 几个同心圆弧，营造深色科技感
for i, r in enumerate([620, 520, 420, 320, 220]):
    alpha = 18 + i * 10
    gdraw.ellipse([W - 320 - r, H // 2 - r, W - 320 + r, H // 2 + r],
                  outline=(88, 166, 255, alpha), width=3)
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img)

# 左下角散点（星点）
import random
random.seed(42)
for _ in range(60):
    x = random.randint(20, W // 2)
    y = random.randint(H - 200, H - 20)
    r = random.choice([1, 1, 2])
    c = random.choice([(88, 166, 255), (139, 148, 158), (48, 54, 61)])
    draw.ellipse([x, y, x + r, y + r], fill=c)

# ---- 字体 ----
def find_font(names, sizes):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc",  # 微软雅黑 Bold
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\seguisb.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

font_path = find_font(None, None)

f_main = ImageFont.truetype(font_path, 96)
f_sub = ImageFont.truetype(font_path, 34)
f_small = ImageFont.truetype(font_path, 26)

# ---- 主标题 ----
title = "Hi, I'm Duseus"
# 手动居中
bbox = draw.textbbox((0, 0), title, font=f_main)
tw = bbox[2] - bbox[0]
tx = (W - tw) // 2
ty = 120
draw.text((tx, ty), title, font=f_main, fill=WHITE)

# 下划光条（标题下方渐变条用纯色分段模拟）
bar_y = ty + 130
for i in range(60):
    alpha_ratio = 1 - abs(i - 30) / 30
    c = tuple(int(BLUE[k] * alpha_ratio) for k in range(3))
    draw.rectangle([tx + tw // 2 - 150 + i * 5, bar_y, tx + tw // 2 - 145 + i * 5, bar_y + 6], fill=c)

# ---- 副标题 ----
sub = "自动化折腾党  ×  AI Agent 学习者"
bbox = draw.textbbox((0, 0), sub, font=f_sub)
sw = bbox[2] - bbox[0]
draw.text(((W - sw) // 2, bar_y + 40), sub, font=f_sub, fill=BLUE)

# ---- 底部小字 ----
small = "Talk is cheap. Show me the code."
bbox = draw.textbbox((0, 0), small, font=f_small)
ssw = bbox[2] - bbox[0]
draw.text(((W - ssw) // 2, bar_y + 110), small, font=f_small, fill=GRAY)

# ---- 左上角小徽标 ----
draw.rounded_rectangle([40, 36, 76, 72], radius=10, outline=BLUE_DIM, width=3)
draw.ellipse([50, 46, 66, 62], fill=BLUE)

img.save(os.path.join(os.path.dirname(__file__), "assets", "banner.png"))
print("saved:", os.path.join(os.path.dirname(__file__), "assets", "banner.png"))
