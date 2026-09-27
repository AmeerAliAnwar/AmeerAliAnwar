import random
import os

width = 880
height = 160
cell_size = 11
gap = 3
cols = 52
rows = 7
start_x = 24
start_y = 30

colors = ['#161b22', '#161b22', '#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']

svg_cells = []
for c in range(cols):
    for r in range(rows):
        x = start_x + c * (cell_size + gap)
        y = start_y + r * (cell_size + gap)
        weight = [0.85, 0.05, 0.04, 0.03, 0.015, 0.01, 0.005] if c < 38 else [0.25, 0.15, 0.15, 0.2, 0.1, 0.08, 0.07]
        color = random.choices(colors, weights=weight)[0]
        svg_cells.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" />')

cells_str = "\n  ".join(svg_cells)

snake_head_x = start_x + 42 * (cell_size + gap)
snake_head_y = start_y + 3 * (cell_size + gap)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="snake-head" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#3b82f6" />
    </linearGradient>
  </defs>
  <style>
    .grid-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .title {{ font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; letter-spacing: 0.5px; }}
    .legend-text {{ font-family: ui-monospace, SFMono-Regular, monospace; font-size: 10px; fill: #6e7681; }}
    @keyframes crawl {{
      0% {{ transform: translate(0px, 0px); }}
      25% {{ transform: translate(-120px, 28px); }}
      50% {{ transform: translate(-280px, -14px); }}
      75% {{ transform: translate(-180px, -28px); }}
      100% {{ transform: translate(0px, 0px); }}
    }}
    .snake-body {{ animation: crawl 10s infinite ease-in-out; }}
  </style>

  <rect width="{width}" height="{height}" class="grid-bg" />
  <text x="24" y="20" class="title">CONTRIBUTION ACTIVITY // SNAKE GAME ENGINE</text>

  <!-- Legend -->
  <g transform="translate(680, 10)">
    <text x="0" y="10" class="legend-text">Less</text>
    <rect x="32" y="1" width="10" height="10" rx="2" fill="#161b22" />
    <rect x="46" y="1" width="10" height="10" rx="2" fill="#0e4429" />
    <rect x="60" y="1" width="10" height="10" rx="2" fill="#006d32" />
    <rect x="74" y="1" width="10" height="10" rx="2" fill="#26a641" />
    <rect x="88" y="1" width="10" height="10" rx="2" fill="#39d353" />
    <text x="104" y="10" class="legend-text">More</text>
  </g>

  <g id="cells">
  {cells_str}
  </g>

  <!-- Animated Retro Snake -->
  <g class="snake-body">
    <rect x="{snake_head_x - 3 * (cell_size + gap)}" y="{snake_head_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="#38bdf8" fill-opacity="0.3" />
    <rect x="{snake_head_x - 2 * (cell_size + gap)}" y="{snake_head_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="#38bdf8" fill-opacity="0.5" />
    <rect x="{snake_head_x - 1 * (cell_size + gap)}" y="{snake_head_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="#38bdf8" fill-opacity="0.8" />
    <rect x="{snake_head_x}" y="{snake_head_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="url(#snake-head)" />
    <circle cx="{snake_head_x + 8}" cy="{snake_head_y + 3}" r="1.2" fill="#ffffff" />
    <circle cx="{snake_head_x + 8}" cy="{snake_head_y + 8}" r="1.2" fill="#ffffff" />
  </g>
</svg>'''

os.makedirs(r'D:\portfolio\AmeerAliAnwar\assets', exist_ok=True)
with open(r'D:\portfolio\AmeerAliAnwar\assets\github-snake-dark.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
with open(r'D:\portfolio\AmeerAliAnwar\assets\github-snake.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print("Generated assets/github-snake-dark.svg and assets/github-snake.svg")
