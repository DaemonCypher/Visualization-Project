#!/usr/bin/env python3
import os
import cv2
import numpy as np
import base64

def extract_ranges(blank_mask):
    """
    Given a 1D boolean array blank_mask (True=blank),
    return list of (start, end) intervals where blank_mask is False.
    """
    regions = []
    in_region = False
    for i, is_blank in enumerate(blank_mask):
        if not is_blank and not in_region:
            start = i
            in_region = True
        elif is_blank and in_region:
            regions.append((start, i))
            in_region = False
    if in_region:
        regions.append((start, len(blank_mask)))
    return regions

def split_png_to_svgs(png_path):
    """
    Split one PNG (with transparency) into SVG files in the same folder.
    Returns list of generated SVG filenames.
    """
    # Load with alpha channel
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    if img is None or img.shape[2] < 4:
        print(f"[!] Skipping {png_path}: not a 4-channel PNG")
        return []
    h, w, _ = img.shape

    # Extract alpha channel
    alpha = img[:, :, 3]
    # Build blank masks
    blank_rows = np.all(alpha == 0, axis=1)  # shape (h,)
    blank_cols = np.all(alpha == 0, axis=0)  # shape (w,)

    # Compute non-blank spans
    y_spans = extract_ranges(blank_rows)
    x_spans = extract_ranges(blank_cols)

    base, _ = os.path.splitext(png_path)
    out_svgs = []
    count = 1

    for (y0, y1) in y_spans:
        for (x0, x1) in x_spans:
            crop = img[y0:y1, x0:x1]
            if crop.size == 0:
                continue

            # Encode crop as PNG
            success, buf = cv2.imencode('.png', crop)
            if not success:
                continue
            b64 = base64.b64encode(buf.tobytes()).decode('ascii')

            # Create SVG wrapper
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{x1-x0}" height="{y1-y0}">\n'
                f'  <image href="data:image/png;base64,{b64}" '
                f'x="0" y="0" width="{x1-x0}" height="{y1-y0}" />\n'
                f'</svg>'
            )

            svg_name = f"{base}_{count}.svg"
            with open(svg_name, 'w', encoding='utf-8') as f:
                f.write(svg)
            print(f"✔ Wrote {svg_name}")
            out_svgs.append(svg_name)
            count += 1

    if not out_svgs:
        print(f"[!] No opaque regions found in {png_path}")
    return out_svgs

def main():
    png_files = sorted(f for f in os.listdir('.') if f.lower().endswith('.png'))
    if not png_files:
        print("No PNG files found in current directory.")
        return

    for png in png_files:
        print(f"\nProcessing '{png}' …")
        split_png_to_svgs(png)

if __name__ == "__main__":
    main()
