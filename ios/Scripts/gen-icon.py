#!/usr/bin/env python3
"""Generate a minimal 180x180 app icon PNG (solid blue with 'M' letter)."""
import struct, zlib, sys

WIDTH, HEIGHT = 180, 180
R, G, B = 74, 144, 226  # warm blue

def chunk(ctype, data):
    c = ctype + data
    return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

def letter_M(w, h):
    """Return a 1-channel mask (0=transparent, 255=opaque) for the letter M."""
    mask = bytearray(h * w)
    cx, cy = w // 2, h // 2
    left, top = cx - 40, cy - 40
    right, bottom = cx + 40, cy + 40
    for y in range(h):
        for x in range(w):
            if left <= x < right and top <= y < bottom:
                rel_x = x - left
                rel_y = y - top
                # Simplified 'M': two vertical bars + center V
                bar_w = 10
                if rel_x < bar_w or rel_x >= 80 - bar_w:
                    mask[y * w + x] = 255
                elif rel_x < 20 and rel_y >= rel_x * 2:
                    mask[y * w + x] = 255
                elif rel_x >= 60 and rel_y >= (80 - rel_x) * 2:
                    mask[y * w + x] = 255
    return bytes(mask)

raw_data = b''
mask = letter_M(WIDTH, HEIGHT)
for y in range(HEIGHT):
    raw_data += b'\x00'  # filter byte
    for x in range(WIDTH):
        idx = y * WIDTH + x
        if mask[idx]:
            raw_data += bytes([R, G, B])
        else:
            raw_data += bytes([R, G, B])

out = b'\x89PNG\r\n\x1a\n'
out += chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, 8, 2, 0, 0, 0))
out += chunk(b'IDAT', zlib.compress(raw_data))
out += chunk(b'IEND', b'')

path = sys.argv[1] if len(sys.argv) > 1 else 'AppIcon.png'
with open(path, 'wb') as f:
    f.write(out)
print(f'Icon generated: {path} ({WIDTH}x{HEIGHT})')