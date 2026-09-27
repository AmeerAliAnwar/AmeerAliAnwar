"""
Generate an animated 3D Isometric Cyberdeck and Systems Matrix SVG.
A developer-centric isometric visualization of Tokio agent runtimes,
hierarchical B+ tree memory structures, and contribution activity.
Zero em dashes or en dashes.
"""

import math
import os

def create_isometric_svg(output_path):
    width = 960
    height = 520
    
    # Isometric projection constants
    # angle 30 degrees: cos(30) = 0.866025, sin(30) = 0.5
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    
    # Origin in 2D canvas for isometric (0,0,0)
    ox = 480
    oy = 230
    scale = 32  # grid step size

    def iso(x, y, z=0):
        """Convert 3D grid coords to 2D canvas coords."""
        px = ox + (x - y) * cos30 * scale
        py = oy + (x + y) * sin30 * scale - z
        return round(px, 1), round(py, 1)

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    
    # Defs: gradients, filters, patterns
    svg_parts.append("""  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#07090e" />
      <stop offset="50%" stop-color="#0b0f17" />
      <stop offset="100%" stop-color="#05070a" />
    </linearGradient>

    <!-- Scanline pattern -->
    <pattern id="scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="100" y2="0" stroke="#000000" stroke-width="1.2" stroke-opacity="0.3" />
    </pattern>

    <!-- Glow Filter -->
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="glow-amber" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Linear Gradients for 3D Faces -->
    <linearGradient id="pillar-tokio-top" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f5ff" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="pillar-tokio-left" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0369a1" />
      <stop offset="100%" stop-color="#082f49" />
    </linearGradient>
    <linearGradient id="pillar-tokio-right" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0ea5e9" />
      <stop offset="100%" stop-color="#075985" />
    </linearGradient>

    <linearGradient id="pillar-btree-top" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>
    <linearGradient id="pillar-btree-left" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#047857" />
      <stop offset="100%" stop-color="#064e3b" />
    </linearGradient>
    <linearGradient id="pillar-btree-right" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#065f46" />
    </linearGradient>

    <linearGradient id="pillar-cost-top" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>
    <linearGradient id="pillar-cost-left" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#b45309" />
      <stop offset="100%" stop-color="#78350f" />
    </linearGradient>
    <linearGradient id="pillar-cost-right" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d97706" />
      <stop offset="100%" stop-color="#92400e" />
    </linearGradient>
  </defs>""")

    # Styles and Keyframe Animations
    svg_parts.append("""  <style>
    .mono { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }
    .hud-title { font-size: 13px; font-weight: 700; fill: #00f5ff; letter-spacing: 1.5px; }
    .hud-sub { font-size: 10px; font-weight: 600; fill: #64748b; letter-spacing: 1px; }
    .hud-val { font-size: 11px; font-weight: 700; fill: #f1f5f9; }
    .node-label { font-size: 9.5px; font-weight: 700; fill: #e2e8f0; }
    .node-metric { font-size: 8.5px; font-weight: 600; fill: #38bdf8; }
    .grid-line { stroke: #1e293b; stroke-width: 0.7; stroke-opacity: 0.7; fill: none; }
    .grid-axis { stroke: #334155; stroke-width: 1.2; stroke-dasharray: 4, 3; fill: none; }
    
    /* Animations */
    @keyframes pulse-cyan {
      0%, 100% { opacity: 0.35; }
      50% { opacity: 0.95; }
    }
    @keyframes pulse-amber {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1.0; }
    }
    @keyframes blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    @keyframes packet-flow-1 {
      0% { stroke-dashoffset: 200; }
      100% { stroke-dashoffset: 0; }
    }
    @keyframes packet-flow-2 {
      0% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: -200; }
    }
    @keyframes rover-patrol {
      0% { transform: translate(0px, 0px); }
      25% { transform: translate(75px, 43px); }
      50% { transform: translate(150px, 0px); }
      75% { transform: translate(75px, -43px); }
      100% { transform: translate(0px, 0px); }
    }
    @keyframes scan-radar {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .pulse-glow { animation: pulse-cyan 3s infinite ease-in-out; }
    .pulse-glow-amber { animation: pulse-amber 2.5s infinite ease-in-out; }
    .cursor-blink { animation: blink 1s infinite steps(1); }
    .bus-packet-1 { stroke-dasharray: 8, 16; animation: packet-flow-1 4s linear infinite; }
    .bus-packet-2 { stroke-dasharray: 10, 20; animation: packet-flow-2 3.5s linear infinite; }
    .agent-rover { animation: rover-patrol 12s infinite ease-in-out; }
  </style>""")

    # Background frame
    svg_parts.append(f"""  <!-- Viewport Frame -->
  <rect width="{width}" height="{height}" rx="10" fill="url(#bg-grad)" stroke="#1e2638" stroke-width="1.2" />
  <rect width="{width}" height="{height}" rx="10" fill="url(#scanlines)" pointer-events="none" />""")

    # HUD Header Bar
    svg_parts.append("""  <!-- HUD Top Deck -->
  <g transform="translate(24, 28)">
    <!-- Status LED -->
    <circle cx="6" cy="6" r="4.5" fill="#10b981" />
    <circle cx="6" cy="6" r="7" fill="none" stroke="#10b981" stroke-width="1" class="pulse-glow" />
    <text x="22" y="10" class="mono hud-title">AMEER ALI ANWAR // AUTONOMOUS SYSTEMS MATRIX</text>
    <text x="22" y="24" class="mono hud-sub">CORE ENGINE: TOKIO RUNTIME (CDP) + SIMD B+ TREE (0.018ms) + CLOUD COST OPTIMIZATION (4x-10x)</text>

    <!-- Right HUD telemetry stats -->
    <g transform="translate(620, -4)">
      <rect x="0" y="0" width="130" height="34" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1" />
      <text x="10" y="14" class="mono hud-sub">LATENCY TARGET</text>
      <text x="10" y="28" class="mono hud-val" fill="#00f5ff">0.018 ms</text>

      <rect x="140" y="0" width="146" height="34" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1" />
      <text x="10" y="14" class="mono hud-sub" transform="translate(140, 0)">CDP BATCH</text>
      <text x="10" y="28" class="mono hud-val" fill="#10b981" transform="translate(140, 0)">10,000 evt/s</text>
    </g>
  </g>
  
  <line x1="24" y1="68" x2="936" y2="68" stroke="#1e293b" stroke-width="1" />""")

    # Draw 3D Isometric Grid Floor
    # Grid coordinates range: x from -5 to 5, y from -4 to 4
    svg_parts.append("  <!-- 3D Isometric Floor Grid -->")
    svg_parts.append('  <g class="grid-layer">')
    
    # Grid lines along X
    for y in range(-4, 5):
      p1x, p1y = iso(-5, y, 0)
      p2x, p2y = iso(5, y, 0)
      svg_parts.append(f'    <line x1="{p1x}" y1="{p1y}" x2="{p2x}" y2="{p2y}" class="grid-line" />')
      
    # Grid lines along Y
    for x in range(-5, 6):
      p1x, p1y = iso(x, -4, 0)
      p2x, p2y = iso(x, 4, 0)
      svg_parts.append(f'    <line x1="{p1x}" y1="{p1y}" x2="{p2x}" y2="{p2y}" class="grid-line" />')

    # Accent coordinate axes
    ax1_x, ax1_y = iso(-5, 0, 0)
    ax2_x, ax2_y = iso(5, 0, 0)
    ay1_x, ay1_y = iso(0, -4, 0)
    ay2_x, ay2_y = iso(0, 4, 0)
    svg_parts.append(f'    <line x1="{ax1_x}" y1="{ax1_y}" x2="{ax2_x}" y2="{ax2_y}" class="grid-axis" />')
    svg_parts.append(f'    <line x1="{ay1_x}" y1="{ay1_y}" x2="{ay2_x}" y2="{ay2_y}" class="grid-axis" />')
    svg_parts.append('  </g>')

    # Helper function to generate an isometric 3D prism / pillar
    def draw_iso_prism(x, y, w, d, h, top_style, left_style, right_style, stroke="#00f5ff", stroke_w=0.8):
        """
        Draw a 3D isometric pillar at grid (x, y) with width w, depth d, height h.
        h is in canvas pixels.
        """
        # Ground corners
        g0 = iso(x, y, 0)
        g1 = iso(x + w, y, 0)
        g2 = iso(x + w, y + d, 0)
        g3 = iso(x, y + d, 0)

        # Top corners (elevated by h)
        t0 = iso(x, y, h)
        t1 = iso(x + w, y, h)
        t2 = iso(x + w, y + d, h)
        t3 = iso(x, y + d, h)

        res = []
        # Left face: (g3, g2, t2, t3) - depending on angle, left face is (x, y+d) to (x+w, y+d)
        res.append(f'    <!-- Isometric Prism at ({x}, {y}) -->')
        res.append(f'    <polygon points="{g3[0]},{g3[1]} {g2[0]},{g2[1]} {t2[0]},{t2[1]} {t3[0]},{t3[1]}" fill="{left_style}" stroke="{stroke}" stroke-width="{stroke_w}" />')
        # Right face: (g1, g2, t2, t1)
        res.append(f'    <polygon points="{g1[0]},{g1[1]} {g2[0]},{g2[1]} {t2[0]},{t2[1]} {t1[0]},{t1[1]}" fill="{right_style}" stroke="{stroke}" stroke-width="{stroke_w}" />')
        # Top face: (t0, t1, t2, t3)
        res.append(f'    <polygon points="{t0[0]},{t0[1]} {t1[0]},{t1[1]} {t2[0]},{t2[1]} {t3[0]},{t3[1]}" fill="{top_style}" stroke="{stroke}" stroke-width="{stroke_w}" />')
        return "\n".join(res)

    # 3D Data Buses / Circuit Channels on floor
    svg_parts.append("""  <!-- High-Speed Data Buses -->
  <g class="buses">""")
    # Bus 1: Central Obelisk (0,0) to B+ Tree Node (-3.5, 1)
    b1_start = iso(0.5, 0.5, 0)
    b1_mid = iso(-1.5, 0.5, 0)
    b1_end = iso(-2.5, 1.5, 0)
    svg_parts.append(f'    <path d="M {b1_start[0]} {b1_start[1]} L {b1_mid[0]} {b1_mid[1]} L {b1_end[0]} {b1_end[1]}" stroke="#00f5ff" stroke-width="2" fill="none" stroke-opacity="0.4" />')
    svg_parts.append(f'    <path d="M {b1_start[0]} {b1_start[1]} L {b1_mid[0]} {b1_mid[1]} L {b1_end[0]} {b1_end[1]}" stroke="#00f5ff" stroke-width="2.5" fill="none" class="bus-packet-1" />')

    # Bus 2: Central Obelisk (0,0) to Cloud Cost Node (3, -1.5)
    b2_start = iso(0.5, 0.5, 0)
    b2_mid = iso(2.0, 0.5, 0)
    b2_end = iso(2.5, -1.0, 0)
    svg_parts.append(f'    <path d="M {b2_start[0]} {b2_start[1]} L {b2_mid[0]} {b2_mid[1]} L {b2_end[0]} {b2_end[1]}" stroke="#f59e0b" stroke-width="2" fill="none" stroke-opacity="0.4" />')
    svg_parts.append(f'    <path d="M {b2_start[0]} {b2_start[1]} L {b2_mid[0]} {b2_mid[1]} L {b2_end[0]} {b2_end[1]}" stroke="#f59e0b" stroke-width="2.5" fill="none" class="bus-packet-2" />')

    # Bus 3: Tokio Core to Agent Client Rover Station (0.5, 2.5)
    b3_start = iso(0.5, 0.5, 0)
    b3_end = iso(0.5, 2.5, 0)
    svg_parts.append(f'    <path d="M {b3_start[0]} {b3_start[1]} L {b3_end[0]} {b3_end[1]}" stroke="#10b981" stroke-width="2" fill="none" stroke-opacity="0.5" />')
    svg_parts.append(f'    <path d="M {b3_start[0]} {b3_start[1]} L {b3_end[0]} {b3_end[1]}" stroke="#10b981" stroke-width="2.5" fill="none" class="bus-packet-1" />')
    svg_parts.append("  </g>")

    # Background Contribution Pillars (Simulation of 3D commit blocks on the grid)
    svg_parts.append("  <!-- 3D Contribution Landscape -->")
    contributions = [
        (-4, -3, 0.6, 0.6, 18, "#0e4429", "#082b1a", "#0c3b24", "#22c55e"),
        (-3, -3, 0.6, 0.6, 32, "#006d32", "#004721", "#005a2a", "#22c55e"),
        (-2, -3, 0.6, 0.6, 45, "#26a641", "#196c2e", "#218838", "#39d353"),
        (-1, -3, 0.6, 0.6, 25, "#006d32", "#004721", "#005a2a", "#22c55e"),
        (1, -3, 0.6, 0.6, 12, "#0e4429", "#082b1a", "#0c3b24", "#22c55e"),
        (2, -3, 0.6, 0.6, 38, "#26a641", "#196c2e", "#218838", "#39d353"),
        (3, -3, 0.6, 0.6, 52, "#39d353", "#238636", "#2ea44f", "#39d353"),
        
        (-4, -1, 0.6, 0.6, 30, "#006d32", "#004721", "#005a2a", "#22c55e"),
        (-3, -1, 0.6, 0.6, 40, "#26a641", "#196c2e", "#218838", "#39d353"),
        (3, -2, 0.6, 0.6, 28, "#006d32", "#004721", "#005a2a", "#22c55e"),
        (4, -2, 0.6, 0.6, 48, "#39d353", "#238636", "#2ea44f", "#39d353"),
    ]
    for c in contributions:
        svg_parts.append(draw_iso_prism(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], 0.5))

    # NODE 1 (LEFT): Hierarchical B+ Tree Memory Engine (0.018ms)
    svg_parts.append("  <!-- Node 1: Hierarchical B+ Tree -->")
    # Base Tier
    svg_parts.append(draw_iso_prism(-3.5, 0.5, 1.4, 1.4, 20, "url(#pillar-btree-top)", "url(#pillar-btree-left)", "url(#pillar-btree-right)", "#10b981", 1.0))
    # Mid Tier
    svg_parts.append(draw_iso_prism(-3.3, 0.7, 1.0, 1.0, 42, "url(#pillar-btree-top)", "url(#pillar-btree-left)", "url(#pillar-btree-right)", "#34d399", 1.0))
    # Top Tier / Apex
    svg_parts.append(draw_iso_prism(-3.1, 0.9, 0.6, 0.6, 64, "#34d399", "#059669", "#10b981", "#6ee7b7", 1.2))
    
    # Label for Node 1
    lbl1_pos = iso(-2.8, 1.2, 78)
    svg_parts.append(f"""  <g transform="translate({lbl1_pos[0]}, {lbl1_pos[1]})">
    <rect x="-85" y="-28" width="170" height="28" rx="4" fill="#0b1319" stroke="#10b981" stroke-width="1" />
    <text x="0" y="-15" text-anchor="middle" class="mono node-label" fill="#34d399">B+ TREE MEMORY ENGINE</text>
    <text x="0" y="-4" text-anchor="middle" class="mono node-metric" fill="#6ee7b7">0.018ms Median Latency</text>
  </g>""")

    # NODE 2 (RIGHT): Cloud Cost & Infra Compression Engine (4x - 10x)
    svg_parts.append("  <!-- Node 2: Cloud Infrastructure Compression -->")
    svg_parts.append(draw_iso_prism(2.2, -1.8, 1.3, 1.3, 35, "url(#pillar-cost-top)", "url(#pillar-cost-left)", "url(#pillar-cost-right)", "#f59e0b", 1.0))
    svg_parts.append(draw_iso_prism(2.35, -1.65, 1.0, 1.0, 58, "#fbbf24", "#b45309", "#d97706", "#fde68a", 1.2))
    
    # Label for Node 2
    lbl2_pos = iso(2.8, -1.2, 72)
    svg_parts.append(f"""  <g transform="translate({lbl2_pos[0]}, {lbl2_pos[1]})">
    <rect x="-80" y="-28" width="160" height="28" rx="4" fill="#181308" stroke="#f59e0b" stroke-width="1" />
    <text x="0" y="-15" text-anchor="middle" class="mono node-label" fill="#fbbf24">CLOUD COST OPTIMIZER</text>
    <text x="0" y="-4" text-anchor="middle" class="mono node-metric" fill="#fcd34d">4x to 10x Footprint Reduction</text>
  </g>""")

    # CENTRAL MASTER OBELISK: Tokio Async Daemon & CDP Multiplexer (chrome-use)
    svg_parts.append("  <!-- Central Master Node: Tokio CDP Daemon -->")
    # Base pedestal
    svg_parts.append(draw_iso_prism(-0.6, -0.6, 1.8, 1.8, 16, "#0f172a", "#061325", "#0a1f3d", "#00f5ff", 0.8))
    # Main Tower Column
    svg_parts.append(draw_iso_prism(-0.4, -0.4, 1.4, 1.4, 90, "url(#pillar-tokio-top)", "url(#pillar-tokio-left)", "url(#pillar-tokio-right)", "#00f5ff", 1.2))
    # Top Core Emitter
    svg_parts.append(draw_iso_prism(-0.2, -0.2, 1.0, 1.0, 115, "#38bdf8", "#0369a1", "#0284c7", "#e0f2fe", 1.4))

    # Holographic Ring above Central Obelisk
    ring_pos = iso(0.3, 0.3, 130)
    svg_parts.append(f"""  <!-- Holographic Core Rings -->
  <g transform="translate({ring_pos[0]}, {ring_pos[1]})">
    <ellipse cx="0" cy="0" rx="38" ry="19" fill="none" stroke="#00f5ff" stroke-width="1.4" stroke-dasharray="8 4" class="pulse-glow" />
    <ellipse cx="0" cy="0" rx="22" ry="11" fill="none" stroke="#38bdf8" stroke-width="1.8" />
    <circle cx="0" cy="0" r="4" fill="#ffffff" filter="url(#glow-cyan)" />
    
    <!-- Radar scanner beam -->
    <line x1="0" y1="0" x2="36" y2="-10" stroke="#00f5ff" stroke-width="1.5" stroke-linecap="round" opacity="0.8" />
  </g>""")

    # Central Node Label
    lbl0_pos = iso(0.3, 0.3, 150)
    svg_parts.append(f"""  <g transform="translate({lbl0_pos[0]}, {lbl0_pos[1]})">
    <rect x="-95" y="-32" width="190" height="32" rx="4" fill="#04121d" stroke="#00f5ff" stroke-width="1.4" filter="url(#glow-cyan)" />
    <text x="0" y="-18" text-anchor="middle" class="mono node-label" fill="#ffffff" font-size="10.5px">TOKIO CDP DAEMON</text>
    <text x="0" y="-6" text-anchor="middle" class="mono node-metric" fill="#38bdf8">chrome-use Core Host // PR #342</text>
  </g>""")

    # ANIMATED AUTONOMOUS ROVER / CYBER-AGENT
    # Roaming along the 3D isometric tracks
    # We place it inside an animated group
    rover_base = iso(0, 2.2, 0)
    svg_parts.append(f"""  <!-- Autonomous Agent Harvester (The 3D Cyber-Rover) -->
  <g class="agent-rover" transform="translate(0, 0)">
    <!-- Rover Body in Isometric Projection -->
    <g transform="translate({rover_base[0]}, {rover_base[1]})">
      <!-- Shadow -->
      <ellipse cx="0" cy="4" rx="20" ry="10" fill="#000000" fill-opacity="0.6" />
      
      <!-- Rover Chassis -->
      <polygon points="-16,-6 0,-14 16,-6 0,2" fill="#0284c7" stroke="#38bdf8" stroke-width="1.2" />
      <polygon points="-16,-6 0,2 0,10 -16,2" fill="#0369a1" stroke="#38bdf8" stroke-width="1" />
      <polygon points="16,-6 0,2 0,10 16,2" fill="#0ea5e9" stroke="#38bdf8" stroke-width="1" />
      
      <!-- Cockpit / Sensor Eye -->
      <polygon points="-8,-9 0,-13 8,-9 0,-5" fill="#ffffff" filter="url(#glow-cyan)" />
      
      <!-- Scanning Laser Cone -->
      <polygon points="0,-10 -35,-35 35,-35" fill="none" stroke="#00f5ff" stroke-width="0.8" stroke-dasharray="3, 3" opacity="0.6" />
      
      <!-- Agent Status Badge -->
      <rect x="-42" y="-46" width="84" height="15" rx="3" fill="#021422" stroke="#00f5ff" stroke-width="0.8" />
      <text x="0" y="-36" text-anchor="middle" class="mono" font-size="7.5px" font-weight="700" fill="#00f5ff">AGENT: HARVESTING</text>
    </g>
  </g>""")

    # Bottom Terminal Deck & Status Telemetry
    svg_parts.append("""  <!-- HUD Bottom Deck -->
  <line x1="24" y1="460" x2="936" y2="460" stroke="#1e293b" stroke-width="1" />
  
  <g transform="translate(24, 488)">
    <!-- Terminal Prompt -->
    <text x="0" y="0" class="mono hud-sub" fill="#38bdf8">runtime@engine</text>
    <text x="96" y="0" class="mono hud-sub" fill="#64748b">:</text>
    <text x="104" y="0" class="mono hud-sub" fill="#a855f7">~/production</text>
    <text x="180" y="0" class="mono hud-sub" fill="#64748b">$</text>
    <text x="194" y="0" class="mono hud-val" fill="#f8fafc">tokio-agent --inspect-matrix --verify-all</text>
    <rect x="490" y="-10" width="8" height="14" fill="#00f5ff" class="cursor-blink" />

    <!-- Right System Health Indicators -->
    <g transform="translate(680, 0)">
      <text x="0" y="0" class="mono hud-sub" fill="#94a3b8">ALLOC_PRESSURE: <tspan fill="#10b981">NORMAL</tspan></text>
      <text x="145" y="0" class="mono hud-sub" fill="#94a3b8">SIMD_WIDTH: <tspan fill="#00f5ff">AVX-512</tspan></text>
    </g>
  </g>""")

    svg_parts.append("</svg>")
    
    full_svg = "\n".join(svg_parts)
    
    # Safety Check: Zero em dashes or en dashes
    if "\u2014" in full_svg or "\u2013" in full_svg:
        raise ValueError("Em dash or en dash found in SVG output!")
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"Generated 3D Isometric Matrix SVG at {output_path} ({len(full_svg)} bytes)")

if __name__ == "__main__":
    out = os.path.join(r"D:\portfolio\AmeerAliAnwar\assets", "cyber_matrix_3d.svg")
    create_isometric_svg(out)
