from PIL import Image, ImageDraw, ImageFont

S = 2  # render at 2x for crispness
W, H = 1440, 770
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)

SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
def f(path, size): return ImageFont.truetype(path, size * S)

ORANGE, ORANGE_BG = "#e8a33d", "#fff4e5"
GREEN, GREEN_BG = "#3cc35a", "#ffffff"
RED, RED_BG = "#e5484d", "#fff0f0"
GRN_T, GRN_BG = "#2e9e4a", "#effbf1"
PURPLE_BG, PURPLE = "#f1f0fd", "#d9d6f2"
GREY, GREY_BG = "#c8ccd2", "#f5f6f7"
TEXT, MUTED = "#222222", "#8a8f98"

def box(x0, y0, x1, y1, fill, outline, r=10, w=1.5):
    d.rounded_rectangle([x0*S, y0*S, x1*S, y1*S], r*S, fill=fill, outline=outline, width=int(w*S))

def text_c(cx, cy, lines, color=TEXT, size=13):
    """lines: list of list of (text, font_path) runs, centred."""
    lh = size * 1.45
    y = cy - lh * len(lines) / 2
    for runs in lines:
        widths = [d.textlength(t, font=f(p, size)) for t, p in runs]
        x = cx * S - sum(widths) / 2
        for (t, p), wd in zip(runs, widths):
            d.text((x, (y + lh / 2) * S), t, font=f(p, size), fill=color, anchor="lm")
            x += wd
        y += lh

def arrow(x0, x1, y):
    d.line([x0*S, y*S, x1*S, y*S], fill="#333333", width=int(1.3*S))
    tip = x1; back = 8 if x1 > x0 else -8
    d.polygon([(tip*S, y*S), ((tip-back)*S, (y-4)*S), ((tip-back)*S, (y+4)*S)], fill="#333333")

# Title
d.text((32*S, 40*S), "Same App, Different Mechanics: What Caching and Fragments Change",
       font=f(SANS, 22), fill=TEXT, anchor="lm")

# Side panels
box(25, 77, 415, 715, ORANGE_BG, ORANGE, 12, 2)
box(1025, 77, 1415, 715, GREEN_BG, GREEN, 12, 2)
d.text((40*S, 100*S), "Before  |  No caching, no fragment", font=f(BOLD, 17), fill="#c05e12", anchor="lm")
d.text((1040*S, 100*S), "After  |  @st.cache_data + @st.fragment", font=f(BOLD, 17), fill=GRN_T, anchor="lm")

def side(x0, x1, y0, y1, fill, outline, lines, color=TEXT, size=13):
    box(x0, y0, x1, y1, fill, outline)
    text_c((x0 + x1) / 2, (y0 + y1) / 2, lines, color, size)

# Before column
side(45, 396, 119, 173, RED_BG, RED, [[("CSV read #1: ", BOLD), ("load_filtered()", MONO), (" calls", BOLD)],
                                      [("load_events()", MONO), (", which reads the CSV", BOLD)]], RED, 12)
side(45, 396, 180, 233, RED_BG, RED, [[("CSV read #2: ", BOLD), ("load_mau()", MONO), (" calls", BOLD)],
                                      [("load_events()", MONO), (" again, rereads the CSV", BOLD)]], RED, 12)
side(45, 396, 250, 337, PURPLE_BG, PURPLE, [[("No ", SANS), ("@st.fragment", MONO), (": changing a filter", SANS)],
                                            [("reruns the whole script, top to", SANS)],
                                            [("bottom, including every data load.", SANS)]])
side(77, 363, 346, 381, RED_BG, RED, [[("Every filter click: full rerun", BOLD)]], RED, 13)
side(45, 396, 425, 507, PURPLE_BG, PURPLE, [[("No ", SANS), ("@st.cache_data", MONO), (": the chart and the", SANS)],
                                            [("table each read the CSV, so every", SANS)],
                                            [("run reads it twice (2x per run).", SANS)]])
side(77, 363, 520, 556, RED_BG, RED, [[("Refresh is slow again: ~0.4s", BOLD)]], RED, 13)
side(45, 396, 617, 680, "white", GREY, [[("First run ~2.2s (2 CSV reads)", SANS)],
                                        [("Avg rerun ~0.4s (2 CSV reads again)", SANS)]])

# After column
side(1045, 1396, 119, 173, GRN_BG, GREEN, [[("CSV read #1: ", BOLD), ("load_filtered()", MONO), (" calls", BOLD)],
                                           [("load_events()", MONO), (", reads CSV, caches it", BOLD)]], GRN_T, 12)
side(1045, 1396, 180, 233, GRN_BG, GREEN, [[("No CSV read: ", BOLD), ("load_mau()", MONO), (" calls", BOLD)],
                                           [("load_events()", MONO), (", gets the cached copy", BOLD)]], GRN_T, 12)
side(1045, 1396, 250, 337, PURPLE_BG, PURPLE, [[("@st.fragment", MONO), (": changing a filter", SANS)],
                                               [("reruns only the Input and Data", SANS)],
                                               [("section, not the whole page.", SANS)]])
side(1077, 1363, 346, 381, GRN_BG, GREEN, [[("Filter click: fragment-only rerun", BOLD)]], GRN_T, 13)
side(1045, 1396, 425, 507, PURPLE_BG, PURPLE, [[("@st.cache_data", MONO), (": the first call reads", SANS)],
                                               [("the CSV once; the second call and", SANS)],
                                               [("later runs reuse the cached copy.", SANS)]])
side(1077, 1363, 520, 556, GRN_BG, GREEN, [[("Fragment rerun from cache: ~0.05s", BOLD)]], GRN_T, 13)
side(1045, 1396, 617, 680, "white", GREY, [[("First run ~0.3s (1 CSV read)", SANS)],
                                           [("Avg rerun ~0.05s (0 reads, ~8x faster)", SANS)]])

# Mock app
box(450, 89, 991, 699, "white", "#b9bec6", 12, 1.5)
side(457, 984, 97, 133, GREY_BG, GREY, [[("localhost:8601   User activity dashboard", SANS)]], TEXT, 12)
d.text((468*S, 156*S), "User activity dashboard", font=f(BOLD, 19), fill=TEXT, anchor="lm")
d.text((468*S, 179*S), "Same UI in both versions: only the code behind it changes.", font=f(SANS, 12), fill=MUTED, anchor="lm")
side(468, 619, 193, 230, "white", GREY, [[("Reset cache", SANS)]])
d.text((468*S, 249*S), "Input", font=f(BOLD, 14), fill=TEXT, anchor="lm")
side(468, 712, 261, 298, GREY_BG, GREY, [[("Region: AMER  v", SANS)]], TEXT, 12)
side(728, 971, 261, 298, GREY_BG, GREY, [[("Channel: web  v", SANS)]], TEXT, 12)
d.text((468*S, 323*S), "Data", font=f(BOLD, 14), fill=TEXT, anchor="lm")
for i, (lab, val) in enumerate([("Events", "21,212"), ("Revenue", "$5,301,681"), ("Avg revenue per event", "$249.94")]):
    x0 = 468 + i * 172
    side(x0, x0 + 160, 336, 393, GREY_BG, GREY, [[(lab, SANS)], [(val, SANS)]], TEXT, 12)

# Wide bar chart: 12 monthly bars, square tops, small gaps
heights = [46, 52, 49, 55, 50, 58, 53, 60, 51, 57, 54, 59]
base, x, bw, gap = 490, 472, 39, 2.5
d.line([468*S, base*S, 972*S, base*S], fill="#c8ccd2", width=S)
for h in heights:
    d.rectangle([x*S, (base - h * 1.25)*S, (x + bw)*S, base*S], fill="#83c9ff")
    x += bw + gap

# Table
cols = [("EVENT_DATE", 112), ("USER_ID", 103), ("REGION", 88), ("CHANNEL", 96), ("REVENUE", 103)]
rows = [["EVENT_DATE", "USER_ID", "REGION", "CHANNEL", "REVENUE"],
        ["2026-08-28", "user_1991", "AMER", "web", "107"],
        ["2026-02-03", "user_1927", "AMER", "web", "212"]]
for r, row in enumerate(rows):
    x = 468
    y0 = 498 + r * 35
    for (_, wd), cell in zip(cols, row):
        side(x, x + wd - 3, y0, y0 + 32, GREY_BG if r == 0 else "white", GREY, [[(cell, SANS)]], TEXT, 13)
        x += wd
d.text((468*S, 622*S), "Run timing", font=f(BOLD, 14), fill=TEXT, anchor="lm")
for i, lab in enumerate(["First run", "Avg rerun", "Rerun speedup"]):
    x0 = 468 + i * 172
    side(x0, x0 + 160, 636, 687, GREY_BG, GREY, [[(lab, SANS)], [("...", SANS)]], TEXT, 12)

# Arrows: widgets, data, timing
for y in (276, 460, 648):
    arrow(448, 398, y)
    arrow(993, 1043, y)

d.text((32*S, 742*S), "Local timings from the guide's Compare the Results step (After first run measured right after "
       "Reset cache); your numbers will vary.", font=f(SANS, 12), fill="#555555", anchor="lm")

img = img.resize((W, H), Image.LANCZOS)
for p in ["/Users/cnantasenamat/Documents/Coco/speed-up-streamlit-apps-with-caching-and-fragments/assets/before-after-caching.png",
          "/Users/cnantasenamat/Documents/Coco/sfguide-speed-up-streamlit-apps-with-caching-and-fragments/assets/before-after-caching.png"]:
    import os
    if os.path.isdir(os.path.dirname(p)):
        img.save(p)
        print("saved", p)
img.save("/tmp/hero_preview.png")
