#!/usr/bin/env python3
import os
import cv2
import numpy as np
import base64

def crop_to_alpha_bounds(img):
    """
    Crop transparent borders (alpha=0) from a 4-channel image.
    Returns the cropped image and (x0, y0) offset.
    """
    if img.shape[2] < 4:
        raise ValueError("Image must have alpha channel")

    alpha = img[:, :, 3]
    coords = cv2.findNonZero((alpha > 0).astype(np.uint8))
    if coords is None:
        return None, (0, 0)

    x, y, w, h = cv2.boundingRect(coords)
    cropped = img[y:y+h, x:x+w]
    return cropped, (x, y)

def convert_png_to_svg(png_path):
    """
    Convert a PNG to a single SVG file with white margin removed.
    """
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    if img is None or img.shape[2] < 4:
        print(f"[!] Skipping {png_path}: not a 4-channel PNG")
        return None

    cropped, _ = crop_to_alpha_bounds(img)
    if cropped is None or cropped.size == 0:
        print(f"[!] No visible content in {png_path}")
        return None

    # Encode cropped image to base64
    success, buf = cv2.imencode('.png', cropped)
    if not success:
        print(f"[!] Encoding failed for {png_path}")
        return None

    b64 = base64.b64encode(buf.tobytes()).decode('ascii')
    h, w = cropped.shape[:2]

    # Generate SVG
    svg_content = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">\n'
        f'  <image href="data:image/png;base64,{b64}" '
        f'x="0" y="0" width="{w}" height="{h}" />\n'
        f'</svg>'
    )

    svg_path = os.path.splitext(png_path)[0] + ".svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✔ Wrote {svg_path}")
    return svg_path

def main():
    png_files = sorted(f for f in os.listdir('.') if f.lower().endswith('.png'))
    if not png_files:
        print("No PNG files found in current directory.")
        return

    for png in png_files:
        print(f"\nProcessing '{png}' …")
        convert_png_to_svg(png)

if __name__ == "__main__":
    main()
