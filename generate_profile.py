import os
from io import BytesIO
import requests
from PIL import Image, ImageEnhance, ImageOps

# Set Pink Theme Colors
PINK = "#ff69b4"  # Hot Pink for ASCII text
CYAN = "#58a6ff"
BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
WHITE = "#c9d1d9"
USERNAME = "paramjyot2004"


def generate_ascii_terminal_svg():
    image_path = "profile.jpg"

    if os.path.exists(image_path):
        img = Image.open(image_path).convert("L")
    else:
        url = f"https://github.com/{USERNAME}.png"
        try:
            res = requests.get(url)
            img = Image.open(BytesIO(res.content)).convert("L")
        except Exception:
            img = Image.new("L", (38, 26), color=128)

    # Enhance contrast so facial features & glasses pop out
    img = ImageOps.autocontrast(img, cutoff=2)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)

    # Resize with aspect ratio correction
    target_width = 38
    aspect_ratio = img.height / img.width
    target_height = int(target_width * aspect_ratio * 0.52)
    target_height = min(max(target_height, 20), 25)

    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # ASCII character spectrum
    chars = [
        " ",
        ".",
        "'",
        "`",
        "^",
        '"',
        ",",
        ":",
        ";",
        "I",
        "l",
        "!",
        "i",
        ">",
        "<",
        "~",
        "+",
        "_",
        "-",
        "?",
        "]",
        "[",
        "}",
        "{",
        "1",
        ")",
        "(",
        "|",
        "\\",
        "/",
        "t",
        "f",
        "j",
        "r",
        "x",
        "n",
        "u",
        "v",
        "c",
        "z",
        "X",
        "Y",
        "U",
        "J",
        "C",
        "L",
        "Q",
        "0",
        "O",
        "Z",
        "m",
        "w",
        "q",
        "p",
        "d",
        "b",
        "k",
        "h",
        "a",
        "o",
        "*",
        "#",
        "M",
        "W",
        "&",
        "%",
        "B",
        "@",
        "$",
    ]

    ascii_rows = []
    for y in range(target_height):
        row_str = ""
        for x in range(target_width):
            pixel = img.getpixel((x, y))
            char_idx = int((pixel / 255) * (len(chars) - 1))
            char = chars[char_idx]

            if char == "<":
                char = "&lt;"
            elif char == ">":
                char = "&gt;"
            elif char == "&":
                char = "&amp;"
            elif char == '"':
                char = "&quot;"
            elif char == "'":
                char = "&#39;"

            row_str += char
        ascii_rows.append(row_str)

    # Generate rows for SVG
    svg_rows = []
    start_y = 52
    line_height = 12.5

    for i, row in enumerate(ascii_rows):
        y_pos = start_y + (i * line_height)
        delay = round(i * 0.05, 2)
        row_html = f"""
        <text x="20" y="{y_pos}" class="ascii-text" opacity="0">
            {row}
            <animate attributeName="opacity" values="0;1" dur="0.1s" begin="{delay}s" fill="freeze" />
        </text>
        """
        svg_rows.append(row_html)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 390" width="100%" height="100%">
  <style>
    .bg {{ fill: {BG_COLOR}; rx: 10px; }}
    .header {{ fill: #161b22; rx: 10px 10px 0 0; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .term-title {{ font-family: monospace; font-size: 11px; fill: #8b949e; text-anchor: middle; }}
    .ascii-text {{ font-family: 'Courier New', Courier, monospace; font-size: 10.5px; fill: {PINK}; font-weight: bold; xml:space: preserve; }}
    .prompt {{ font-family: monospace; font-size: 12px; fill: {CYAN}; }}
    .cursor {{ fill: {WHITE}; }}
  </style>
  <rect width="400" height="390" class="bg" stroke="{BORDER_COLOR}" stroke-width="1"/>
  <rect width="400" height="30" class="header"/>
  <circle cx="20" cy="15" r="5" class="dot-red"/>
  <circle cx="35" cy="15" r="5" class="dot-yellow"/>
  <circle cx="50" cy="15" r="5" class="dot-green"/>
  <text x="200" y="19" class="term-title">bash - {USERNAME}@profile</text>
  
  <g>{''.join(svg_rows)}</g>

  <g transform="translate(20, 370)">
    <text class="prompt">$ whoami</text>
    <rect x="75" y="-10" width="8" height="12" class="cursor">
      <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>"""

    with open("terminal-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)