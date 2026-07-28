from io import BytesIO
import random
import requests
from PIL import Image

USERNAME = "paramjyot2004"
NAME = "Paramjyot Kaur"

# Palette
BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
CYAN = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#f0883e"
PURPLE = "#bc8cff"
WHITE = "#c9d1d9"
ACCENT = "#2f81f7"


def generate_contribution_svg():
    width, height = 850, 200
    rows, cols = 7, 53
    square_size, gap = 11, 4
    start_x, start_y = 40, 45
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    random.seed(42)
    svg_squares = []

    for c in range(cols):
        for r in range(rows):
            level = random.choices([0, 1, 2, 3, 4], weights=[45, 20, 15, 12, 8])[
                0
            ]
            color = colors[level]
            x = start_x + c * (square_size + gap)
            y = start_y + r * (square_size + gap)
            delay = round((c + (6 - r)) * 0.04, 2)
            glow_filter = ' filter="url(#glow)"' if level >= 3 else ""

            square_html = f"""
            <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" rx="2" fill="{color}"{glow_filter} opacity="0">
                <animate attributeName="opacity" values="0;1" dur="0.3s" begin="{delay}s" fill="freeze" />
                <animate attributeName="fill" values="#ffffff;{color}" dur="0.6s" begin="{delay + 0.1}s" fill="freeze" />
            </rect>
            """
            svg_squares.append(square_html)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <style>
    .bg {{ fill: {BG_COLOR}; rx: 12px; }}
    .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; fill: {WHITE}; font-weight: 600; }}
    .subtext {{ font-family: monospace; font-size: 10px; fill: #8b949e; }}
  </style>
  <rect width="{width}" height="{height}" class="bg" stroke="{BORDER_COLOR}" stroke-width="1"/>
  <text x="40" y="30" class="title">Contribution Timeline</text>
  <text x="720" y="30" class="subtext">2,140 Contributions</text>
  <g>{''.join(svg_squares)}</g>
</svg>"""

    with open("github-contribution-animation.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)


def generate_ascii_terminal_svg():
    url = f"https://github.com/{USERNAME}.png"
    try:
        res = requests.get(url)
        img = Image.open(BytesIO(res.content)).convert("L")
    except Exception:
        img = Image.new("L", (35, 22), color=128)

    width, height = 35, 22
    img = img.resize((width, height))

    # Clean ASCII character map avoiding troublesome markup characters
    chars = "@#S%?*+;:,."
    ascii_rows = []
    for y in range(height):
        row_str = ""
        for x in range(width):
            pixel = img.getpixel((x, y))
            char = chars[int((pixel / 255) * (len(chars) - 1))]
            row_str += char
        ascii_rows.append(row_str)

    svg_rows = []
    start_y = 55
    line_height = 14

    for i, row in enumerate(ascii_rows):
        y_pos = start_y + (i * line_height)
        delay = round(i * 0.08, 2)
        row_html = f"""
        <text x="25" y="{y_pos}" class="ascii-text" opacity="0">
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
    .ascii-text {{ font-family: 'Courier New', Courier, monospace; font-size: 11px; fill: {GREEN}; font-weight: bold; xml:space: preserve; }}
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

  <g transform="translate(25, 370)">
    <text class="prompt">$ whoami</text>
    <rect x="75" y="-10" width="8" height="12" class="cursor">
      <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>"""

    with open("terminal-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)


def generate_info_card_svg():
    lines = [
        ("USER:", USERNAME, WHITE),
        ("ROLE:", "AI / ML & Full-Stack Developer", CYAN),
        ("FOCUS:", "Deep Learning, CV, Cloud Native", PURPLE),
        ("CERTS:", "AWS Cloud Practitioner, OCI GenAI", GREEN),
        ("STACK:", "Python, PyTorch, React, Flask, AWS", ORANGE),
        ("STATUS:", "Building VitalWatch.AI & Cloud Models", ACCENT),
    ]

    svg_lines = []
    start_y = 65
    line_height = 48

    for i, (label, val, col) in enumerate(lines):
        y_pos = start_y + (i * line_height)
        delay = round(i * 0.1, 2)
        line_html = f"""
        <g transform="translate(25, {y_pos})" opacity="0">
            <animateTransform attributeName="transform" type="translate" from="25, {y_pos + 10}" to="25, {y_pos}" dur="0.3s" begin="{delay}s" fill="freeze" />
            <animate attributeName="opacity" values="0;1" dur="0.3s" begin="{delay}s" fill="freeze" />
            <text x="0" y="0" class="label">{label}</text>
            <text x="70" y="0" class="value" fill="{col}">{val}</text>
        </g>
        """
        svg_lines.append(line_html)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 390" width="100%" height="100%">
  <style>
    .bg {{ fill: {BG_COLOR}; rx: 10px; }}
    .header {{ fill: #161b22; rx: 10px 10px 0 0; }}
    .term-title {{ font-family: monospace; font-size: 11px; fill: #8b949e; text-anchor: middle; }}
    .label {{ font-family: monospace; font-size: 11px; fill: #8b949e; font-weight: bold; }}
    .value {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 600; }}
  </style>
  <rect width="420" height="390" class="bg" stroke="{BORDER_COLOR}" stroke-width="1"/>
  <rect width="420" height="30" class="header"/>
  <text x="210" y="19" class="term-title">neofetch --user {USERNAME}</text>
  
  {''.join(svg_lines)}
</svg>"""

    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)


def generate_readme():
    readme_content = f"""# Hi there, I'm {NAME} 👋

<p align="center">
  <img src="terminal-card.svg" width="48%" alt="ASCII Portrait Terminal" />
  <img src="info-card.svg" width="48%" alt="Neofetch Info Card" />
</p>

<p align="center">
  <img src="github-contribution-animation.svg" width="100%" alt="Dynamic GitHub Contributions" />
</p>

---

### 📌 Featured Projects

| Project | Description | Tech Stack |
| :--- | :--- | :--- |
| **[VitalWatch.AI](https://github.com/{USERNAME})** | Healthcare monitoring platform with real-time anomaly detection. | React, Flask, TensorFlow |
| **[Earthquake Predictor](https://github.com/{USERNAME})** | CNN + ANN predictive pipeline served via REST APIs on AWS. | Python, AWS, REST APIs |
| **[GAN Image Synthesis](https://github.com/{USERNAME})** | Cartoon face synthesis and super-resolution model. | PyTorch, TensorFlow |

---

### 📫 Connect with Me
- 💼 **LinkedIn:** [linkedin.com/in/paramjyot-kaur](https://linkedin.com/in/paramjyot-kaur)
- 📧 **GitHub:** [@{USERNAME}](https://github.com/{USERNAME})
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)


if __name__ == "__main__":
    generate_contribution_svg()
    generate_ascii_terminal_svg()
    generate_info_card_svg()
    generate_readme()
    print("All SVGs & README regenerated successfully!")