#!/usr/bin/env python3
"""Generate a polished 180x180 app icon: gradient bg + white game controller."""
import struct, zlib, math, sys

W, H = 180, 180

# ── helpers ──────────────────────────────────────────────────────────

def chunk(ctype, data):
    c = ctype + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp_c(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))

# anti-aliased shape drawing via signed-distance field

def sd_circle(px, py, cx, cy, r):
    return math.hypot(px - cx, py - cy) - r

def sd_rounded_box(px, py, cx, cy, w, h, r):
    dx, dy = abs(px - cx) - w / 2 + r, abs(py - cy) - h / 2 + r
    return min(max(dx, dy), 0.0) + math.hypot(max(dx, 0.0), max(dy, 0.0)) - r

def sd_cross(px, py, cx, cy, arm, thick):
    """Center cross for d-pad."""
    dx, dy = abs(px - cx), abs(py - cy)
    # vertical arm
    dv = max(dx - thick / 2, 0.0) if dy <= arm / 2 else math.hypot(dx - thick / 2, dy - arm / 2)
    dv = min(dv, math.hypot(dx + thick / 2, dy - arm / 2))
    # horizontal arm
    dh = max(dy - thick / 2, 0.0) if dx <= arm / 2 else math.hypot(dx - arm / 2, dy - thick / 2)
    dh = min(dh, math.hypot(dx - arm / 2, dy + thick / 2))
    return min(dv, dh)

def alpha(px, py, sd):
    """Smooth edge: 1 inside, 0 outside, sub-pixel ramp."""
    # sample 5x5 sub-pixels for better AA
    s = 0.0
    for dy in (-0.4, -0.2, 0.0, 0.2, 0.4):
        for dx in (-0.4, -0.2, 0.0, 0.2, 0.4):
            d = sd(px + dx, py + dy)
            s += max(0.0, min(1.0, 0.5 - d))
    return s / 25.0

# ── build pixel buffer ───────────────────────────────────────────────

# 1. background gradient (top-left  →  bottom-right)
bg_a = (30, 27, 75)    # #1E1B4B  deep indigo
bg_b = (124, 58, 237)  # #7C3AED  violet

buf = bytearray(W * H * 3)  # RGB
for y in range(H):
    for x in range(W):
        t = (x / W + y / H) / 2  # diagonal blend
        r, g, b = lerp_c(bg_a, bg_b, t)
        buf[(y * W + x) * 3:(y * W + x) * 3 + 3] = (r, g, b)

# 2. game controller (white silhouette with slight transparency gradient)
cx, cy = W // 2, H // 2

def overlay_shape(px, py, intensity, r, g, b):
    if intensity <= 0:
        return
    i = (py * W + px) * 3
    a = intensity
    buf[i]   = lerp(buf[i],   r, a)
    buf[i+1] = lerp(buf[i+1], g, a)
    buf[i+2] = lerp(buf[i+2], b, a)

for py in range(H):
    for px in range(W):
        # main body: rounded rect
        a1 = alpha(px, py, lambda x, y: sd_rounded_box(x, y, cx, cy + 6, 96, 30, 14))
        if a1 > 0:
            overlay_shape(px, py, a1, 255, 255, 255)

        # left grip
        a2 = alpha(px, py, lambda x, y: sd_circle(x, y, cx - 38, cy + 18, 26))
        if a2 > 0:
            overlay_shape(px, py, a2, 255, 255, 255)

        # right grip
        a3 = alpha(px, py, lambda x, y: sd_circle(x, y, cx + 38, cy + 18, 26))
        if a3 > 0:
            overlay_shape(px, py, a3, 255, 255, 255)

        # left joystick
        a4 = alpha(px, py, lambda x, y: sd_circle(x, y, cx - 20, cy + 2, 10))
        if a4 > 0:
            overlay_shape(px, py, a4, 200, 200, 220)

        # joystick inner ring
        a5 = alpha(px, py, lambda x, y: sd_circle(x, y, cx - 20, cy + 2, 6))
        if a5 > 0:
            overlay_shape(px, py, a5, 60, 55, 120)

        # right joystick
        a6 = alpha(px, py, lambda x, y: sd_circle(x, y, cx + 20, cy + 2, 10))
        if a6 > 0:
            overlay_shape(px, py, a6, 200, 200, 220)

        # right joystick inner ring
        a7 = alpha(px, py, lambda x, y: sd_circle(x, y, cx + 20, cy + 2, 6))
        if a7 > 0:
            overlay_shape(px, py, a7, 60, 55, 120)

        # d-pad cross
        a8 = alpha(px, py, lambda x, y: sd_cross(x, y, cx - 44, cy - 4, 16, 5.0))
        if a8 > 0:
            overlay_shape(px, py, a8, 200, 200, 220)

        # action buttons: A B X Y as small circles
        for i, (bpx, bpy) in enumerate([(cx + 44, cy - 14), (cx + 44, cy + 6),
                                          (cx + 34, cy - 4), (cx + 54, cy - 4)]):
            a9 = alpha(px, py, lambda x, y, _cx=bpx, _cy=bpy: sd_circle(x, y, _cx, _cy, 4.5))
            if a9 > 0:
                colors = [(255, 80, 80), (80, 200, 80), (80, 120, 255), (255, 200, 80)]
                r, g, b = colors[i]
                overlay_shape(px, py, a9 * 0.85, r, g, b)

        # home button
        a10 = alpha(px, py, lambda x, y: sd_circle(x, y, cx, cy - 12, 4))
        if a10 > 0:
            overlay_shape(px, py, a10, 255, 255, 255)

# ── encode PNG ────────────────────────────────────────────────────────

raw = bytearray()
for y in range(H):
    raw.append(0)  # filter byte
    raw.extend(buf[y * W * 3:(y + 1) * W * 3])

out = b'\x89PNG\r\n\x1a\n'
out += chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
out += chunk(b'IDAT', zlib.compress(bytes(raw)))
out += chunk(b'IEND', b'')

path = sys.argv[1] if len(sys.argv) > 1 else 'AppIcon.png'
with open(path, 'wb') as f:
    f.write(out)
print(f'Icon generated: {path} ({W}x{H})')