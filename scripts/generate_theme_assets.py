"""
Generate transparent, dark and light theme-blended SVGs for GitHub profile.
Features:
- SMIL kinetic typing animation for name and cycling subheaders
- Transparent background (blends seamlessly into GitHub light/dark canvas)
- Zero emojis
- Zero em dashes and zero en dashes
- Real public data from Ameer's 13 merged PRs, FinVerz, audiobard, and colab-cli
"""

import os

def generate_header(output_path, theme="dark"):
    is_dark = (theme == "dark")
    
    # Palette definition tailored to GitHub's native design tokens
    if is_dark:
        fg_title = "#f0f6fc"
        fg_tag = "#58a6ff"
        fg_cycle = "#e6edf3"
        fg_muted = "#8b949e"
        border_col = "#30363d"
        dot_col = "#3fb950"
        card_fill = "#161b22"
        card_stroke = "#21262d"
    else:
        fg_title = "#1f2328"
        fg_tag = "#0969da"
        fg_cycle = "#1f2328"
        fg_muted = "#656d76"
        border_col = "#d0d7de"
        dot_col = "#1a7f37"
        card_fill = "#f6f8fa"
        card_stroke = "#e1e4e8"

    width = 880
    height = 140

    lines = [
        "Systems Architect &amp; AI Product Engineer",
        "13 Merged Upstream PRs: chrome-use, audiobard, colab-cli",
        "0.018ms Hierarchical B+ Tree Engine (FinVerz C++)",
        "4x to 10x Cloud Compute and Memory Optimization",
        "Linear O(N) PCM Audio Buffer Concatenation (audiobard)"
    ]

    dur_per_line = 3.6  # seconds per subtitle
    total_dur = dur_per_line * len(lines)

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="100%" height="100%" fill="none">''')
    
    svg.append(f'''  <defs>
    <style>
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes pulse-dot {{
        0%, 100% {{ opacity: 0.35; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.15); }}
      }}
      .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }}
      .cursor {{ animation: blink 0.9s infinite; }}
      .pulse {{ animation: pulse-dot 2.5s infinite ease-in-out; transform-origin: center; }}
    </style>
  </defs>''')

    # Border frame with transparent background
    svg.append(f'''  <!-- Outer Container (Transparent Fill) -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="none" stroke="{border_col}" stroke-width="1" />''')

    # Top Status Row
    svg.append(f'''  <!-- Top Status Bar -->
  <g transform="translate(24, 28)">
    <circle cx="5" cy="5" r="4" fill="{dot_col}" />
    <circle cx="5" cy="5" r="7" fill="none" stroke="{dot_col}" stroke-width="1" class="pulse" />
    <text x="22" y="9" class="mono" font-size="11" font-weight="600" fill="{fg_muted}" letter-spacing="1">SYSTEMS CORE: ACTIVE</text>
    <text x="200" y="9" class="mono" font-size="11" font-weight="600" fill="{fg_tag}">// 13 MERGED UPSTREAM PRs</text>
    <text x="440" y="9" class="mono" font-size="11" font-weight="600" fill="{fg_muted}">// LATENCY: 0.018ms</text>
    <text x="640" y="9" class="mono" font-size="11" font-weight="600" fill="{fg_muted}">// CLOUD: 4x-10x CUTS</text>
  </g>
  <line x1="24" y1="46" x2="{width - 24}" y2="46" stroke="{border_col}" stroke-width="0.8" />''')

    # Static / Typed Name Header
    svg.append(f'''  <!-- Name Header -->
  <g transform="translate(24, 82)">
    <text class="sans" font-size="26" font-weight="800" fill="{fg_title}" letter-spacing="-0.5">Ameer Ali Anwar</text>
  </g>''')

    # Cycling Dynamic Subtitle using SMIL textPath
    svg.append(f'''  <!-- Kinetic Typing Subtitle Deck -->
  <g transform="translate(24, 114)">''')

    for idx, text in enumerate(lines):
        begin_val = f"{idx * dur_per_line}s" if idx == 0 else f"d{idx - 1}.end"
        if idx == 0:
            begin_attr = f"0s;d{len(lines) - 1}.end"
        else:
            begin_attr = f"d{idx - 1}.end"

        # Width of path based on character count approx 8.5px per char at 13px mono
        max_px = len(text) * 9 + 40
        svg.append(f'''    <path id="p{theme}_{idx}">
      <animate id="d{idx}" attributeName="d" begin="{begin_attr}" dur="{dur_per_line}s" fill="remove"
        values="m0,0 h0 ; m0,0 h{max_px} ; m0,0 h{max_px} ; m0,0 h0"
        keyTimes="0; 0.45; 0.85; 1" />
    </path>
    <text class="mono" font-size="13" font-weight="500" fill="{fg_muted}">
      <textPath xlink:href="#p{theme}_{idx}">
        {text}
      </textPath>
    </text>''')

    # Monospace blinking cursor after typing text
    svg.append(f'''    <text x="0" y="0" class="mono cursor" font-size="14" font-weight="700" fill="{fg_tag}" dx="4">_</text>''')
    svg.append("  </g>")
    svg.append("</svg>")

    full_svg = "\n".join(svg)
    if "\u2014" in full_svg or "\u2013" in full_svg:
        raise ValueError("Em dash or en dash found in output!")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"Generated {output_path} ({len(full_svg)} bytes)")


def generate_telemetry(output_path, theme="dark"):
    is_dark = (theme == "dark")
    
    if is_dark:
        fg_title = "#f0f6fc"
        fg_label = "#79c0ff"
        fg_val = "#e6edf3"
        fg_muted = "#8b949e"
        border_col = "#30363d"
        card_bg = "#0d1117"
        card_border = "#21262d"
        bar_bg = "#21262d"
        bar_fill_1 = "#238636"
        bar_fill_2 = "#1f6feb"
        bar_fill_3 = "#8957e5"
    else:
        fg_title = "#1f2328"
        fg_label = "#0969da"
        fg_val = "#1f2328"
        fg_muted = "#656d76"
        border_col = "#d0d7de"
        card_bg = "#f6f8fa"
        card_border = "#d0d7de"
        bar_bg = "#eaeef2"
        bar_fill_1 = "#1a7f37"
        bar_fill_2 = "#0969da"
        bar_fill_3 = "#8250df"

    width = 880
    height = 240

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" fill="none">''')
    
    svg.append(f'''  <defs>
    <style>
      .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }}
      @keyframes fill-bar {{
        0% {{ width: 0; }}
        100% {{ width: 100%; }}
      }}
      @keyframes pulse-subtle {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1.0; }}
      }}
      .bar-anim {{ animation: fill-bar 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
      .live-pulse {{ animation: pulse-subtle 2s infinite ease-in-out; }}
    </style>
  </defs>''')

    # Border frame with transparent background
    svg.append(f'''  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="none" stroke="{border_col}" stroke-width="1" />''')

    # Section Header
    svg.append(f'''  <g transform="translate(20, 24)">
    <text class="sans" font-size="11" font-weight="700" fill="{fg_muted}" letter-spacing="1">VERIFIED PRODUCTION TELEMETRY // REAL-TIME METRICS</text>
  </g>
  <line x1="20" y1="36" x2="{width - 20}" y2="36" stroke="{border_col}" stroke-width="0.8" />''')

    # 4 Data Columns / Panels
    col_w = 196
    col_gap = 18
    start_x = 20
    top_y = 52
    card_h = 166

    cards = [
        {
            "tag": "UPSTREAM RUNTIME",
            "title": "chrome-use",
            "lang": "Rust",
            "metric": "7 Merged PRs",
            "detail": "CDP Batch Exec / 0ms Sleep",
            "bar": 92,
            "bar_col": bar_fill_1
        },
        {
            "tag": "ALGORITHM CORE",
            "title": "FinVerz Engine",
            "lang": "C++",
            "metric": "0.018ms",
            "detail": "Median SIMD B+ Tree Search",
            "bar": 98,
            "bar_col": bar_fill_2
        },
        {
            "tag": "AUDIO STREAMING",
            "title": "audiobard",
            "lang": "Python / C",
            "metric": "3 Merged PRs",
            "detail": "O(N) Linear PCM Copy",
            "bar": 88,
            "bar_col": bar_fill_3
        },
        {
            "tag": "CLOUD INFRA",
            "title": "Cloud Optimizer",
            "lang": "Docker / SQL",
            "metric": "4x to 10x",
            "detail": "Compute and Memory Cuts",
            "bar": 90,
            "bar_col": bar_fill_1
        }
    ]

    for i, c in enumerate(cards):
        cx = start_x + i * (col_w + col_gap)
        svg.append(f'''  <!-- Metric Card {i + 1}: {c['title']} -->
  <g transform="translate({cx}, {top_y})">
    <rect width="{col_w}" height="{card_h}" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1" />
    
    <!-- Tag & Lang -->
    <text x="14" y="22" class="mono" font-size="9" font-weight="700" fill="{fg_label}" letter-spacing="0.8">{c['tag']}</text>
    <text x="{col_w - 14}" y="22" text-anchor="end" class="mono" font-size="9.5" font-weight="600" fill="{fg_muted}">{c['lang']}</text>
    
    <!-- Main Title -->
    <text x="14" y="48" class="sans" font-size="14" font-weight="700" fill="{fg_title}">{c['title']}</text>
    
    <!-- Primary Metric -->
    <text x="14" y="82" class="mono" font-size="20" font-weight="800" fill="{fg_title}">{c['metric']}</text>
    
    <!-- Subtitle Detail -->
    <text x="14" y="106" class="sans" font-size="10.5" font-weight="500" fill="{fg_muted}">{c['detail']}</text>
    
    <!-- Animated Progress Track -->
    <rect x="14" y="132" width="{col_w - 28}" height="5" rx="2.5" fill="{bar_bg}" />
    <rect x="14" y="132" width="{(col_w - 28) * (c['bar'] / 100.0)}" height="5" rx="2.5" fill="{c['bar_col']}" class="live-pulse" />
  </g>''')

    svg.append("</svg>")
    full_svg = "\n".join(svg)
    if "\u2014" in full_svg or "\u2013" in full_svg:
        raise ValueError("Em dash or en dash found in output!")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"Generated {output_path} ({len(full_svg)} bytes)")


def generate_architecture(output_path, theme="dark"):
    is_dark = (theme == "dark")
    
    if is_dark:
        fg_title = "#f0f6fc"
        fg_label = "#58a6ff"
        fg_muted = "#8b949e"
        border_col = "#30363d"
        card_bg = "#161b22"
        card_border = "#21262d"
        wire_col = "#388bfd"
        tag_bg = "#1f6feb"
        tag_fg = "#58a6ff"
    else:
        fg_title = "#1f2328"
        fg_label = "#0969da"
        fg_muted = "#656d76"
        border_col = "#d0d7de"
        card_bg = "#f6f8fa"
        card_border = "#d0d7de"
        wire_col = "#0969da"
        tag_bg = "#ddf4ff"
        tag_fg = "#0969da"

    width = 880
    height = 270

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" fill="none">''')
    svg.append(f'''  <defs>
    <style>
      .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }}
      @keyframes packet-flow {{
        0% {{ stroke-dashoffset: 40; }}
        100% {{ stroke-dashoffset: 0; }}
      }}
      .wire-packet {{ stroke-dasharray: 4, 4; animation: packet-flow 1.5s linear infinite; }}
    </style>
  </defs>''')

    # Border frame with transparent background
    svg.append(f'''  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="none" stroke="{border_col}" stroke-width="1" />''')

    # Section Title
    svg.append(f'''  <g transform="translate(20, 24)">
    <text class="sans" font-size="11" font-weight="700" fill="{fg_muted}" letter-spacing="1">RUNTIME ARCHITECTURE // AUTONOMOUS AGENT CDP ORCHESTRATION</text>
  </g>
  <line x1="20" y1="36" x2="{width - 20}" y2="36" stroke="{border_col}" stroke-width="0.8" />''')

    # 4 Architecture Blocks
    blocks = [
        {
            "tag": "CLIENT",
            "title": "Agent Client",
            "sub": "Autonomous LLM loops",
            "items": ["Protocol: MCP / stdio", "Tooling: chrome_use_*", "JSON-RPC 2.0 Dispatch"]
        },
        {
            "tag": "RUST CORE",
            "title": "chrome-use Core",
            "sub": "Tokio async engine",
            "items": ["Process-Level Tab Router", "Zero-Alloc State Buffer", "Batch Action Pipeline"]
        },
        {
            "tag": "RELAY",
            "title": "Native Host",
            "sub": "Extension bridge",
            "items": ["Stdio Frame Protocol", "Port Multiplexer", "Localhost:55866"]
        },
        {
            "tag": "TARGET",
            "title": "Chrome Runtime",
            "sub": "Isolated tab sessions",
            "items": ["DOM / A11y Tree Parse", "Base64 Direct Capture", "Raw CDP WebSocket"]
        }
    ]

    bw = 194
    bgap = 24
    bx_start = 20
    by = 52
    bh = 196

    for i, b in enumerate(blocks):
        bx = bx_start + i * (bw + bgap)
        svg.append(f'''  <!-- Block {i + 1}: {b['title']} -->
  <g transform="translate({bx}, {by})">
    <rect width="{bw}" height="{bh}" rx="6" fill="{card_bg}" stroke="{card_border}" stroke-width="1" />
    <rect x="14" y="12" width="68" height="18" rx="3" fill="{tag_bg}" fill-opacity="0.18" />
    <text x="48" y="24" text-anchor="middle" class="mono" font-size="9" font-weight="700" fill="{tag_fg}">{b['tag']}</text>
    <text x="14" y="52" class="sans" font-size="14" font-weight="700" fill="{fg_title}">{b['title']}</text>
    <text x="14" y="68" class="sans" font-size="10.5" font-weight="500" fill="{fg_muted}">{b['sub']}</text>
    <line x1="14" y1="82" x2="{bw - 14}" y2="82" stroke="{card_border}" stroke-width="0.8" />''')
        
        for item_idx, itm in enumerate(b['items']):
            iy = 104 + item_idx * 22
            svg.append(f'''    <text x="14" y="{iy}" class="mono" font-size="9" fill="{fg_muted}">* {itm}</text>''')
        
        svg.append('  </g>')

        # Connector wire to next block
        if i < 3:
            wire_x = bx + bw
            wire_y = by + 68
            svg.append(f'''  <!-- Connector {i + 1} -> {i + 2} -->
  <line x1="{wire_x}" y1="{wire_y}" x2="{wire_x + bgap}" y2="{wire_y}" stroke="{wire_col}" stroke-width="1.2" class="wire-packet" />''')

    svg.append("</svg>")
    full_svg = "\n".join(svg)
    if "\u2014" in full_svg or "\u2013" in full_svg:
        raise ValueError("Em dash or en dash found in output!")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"Generated {output_path} ({len(full_svg)} bytes)")


if __name__ == "__main__":
    assets_dir = r"D:\portfolio\AmeerAliAnwar\assets"
    os.makedirs(assets_dir, exist_ok=True)
    generate_header(os.path.join(assets_dir, "header_dark.svg"), "dark")
    generate_header(os.path.join(assets_dir, "header_light.svg"), "light")
    generate_telemetry(os.path.join(assets_dir, "telemetry_dark.svg"), "dark")
    generate_telemetry(os.path.join(assets_dir, "telemetry_light.svg"), "light")
    generate_architecture(os.path.join(assets_dir, "architecture_dark.svg"), "dark")
    generate_architecture(os.path.join(assets_dir, "architecture_light.svg"), "light")

