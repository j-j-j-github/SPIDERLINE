import re

# Update styles.css
with open('styles.css', 'r') as f:
    css = f.read()

N = 7
duration = N * 5

# Generate CSS for N slides
css_lines = []
css_lines.append(f"        /* Pure CSS Slider */")
css_lines.append(f"        .css-slider-container {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}")
css_lines.append(f"        .css-slider-container input {{ display: none; }}")
css_lines.append(f"        .css-slides {{ position: absolute; width: 100%; height: 100%; }}")
css_lines.append(f"        .css-slide {{ position: absolute; width: 100%; height: 100%; background-size: cover; background-position: center; background-repeat: no-repeat; opacity: 0; z-index: 1; transition: opacity 0.5s ease-in-out; }}")
css_lines.append(f"        .video-slide iframe {{ width: 100%; height: 100%; object-fit: cover; pointer-events: auto; }}")

for i in range(1, N+1):
    css_lines.append(f"        .css-slider-container.autoplay .css-slide.s{i} {{ animation: cssFade{i} {duration}s infinite; }}")

for i in range(1, N+1):
    # Calculate percentages
    # Each slide is active for 1/N of the time.
    # We need a small fade out transition.
    # Example for 7: 100/7 = 14.28%
    step = 100.0 / N
    start_active = (i-1) * step
    end_active = start_active + step - 1
    fade_out = end_active + 1
    
    # We must wrap around for the first slide
    if i == 1:
        css_lines.append(f"        @keyframes cssFade1 {{ 0%, {end_active:.1f}% {{ opacity: 1; z-index: 2; }} {fade_out:.1f}%, {(100-step+1):.1f}% {{ opacity: 0; z-index: 1; }} 100% {{ opacity: 1; z-index: 2; }} }}")
    else:
        css_lines.append(f"        @keyframes cssFade{i} {{ 0%, {(start_active-1):.1f}% {{ opacity: 0; z-index: 1; }} {start_active:.1f}%, {end_active:.1f}% {{ opacity: 1; z-index: 2; }} {fade_out:.1f}%, 100% {{ opacity: 0; z-index: 1; }} }}")

css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .css-slides .s{i}" for i in range(1, N+1)]) + " { opacity: 1; z-index: 3; animation: none; }")
css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .css-slides .css-slide" for i in range(1, N+1)]) + " { animation: none; }")

css_lines.append(f"        .css-controls {{ position: absolute; top: 50%; transform: translateY(-50%); width: 100%; display: flex; justify-content: space-between; padding: 0 40px; z-index: 0; opacity: 0; pointer-events: none; }}")
css_lines.append(f"        .css-controls label {{ pointer-events: auto; }}")

for i in range(1, N+1):
    css_lines.append(f"        .css-slider-container.autoplay .css-controls.c{i} {{ animation: cssCtrl{i} {duration}s infinite; }}")

for i in range(1, N+1):
    step = 100.0 / N
    start_active = (i-1) * step
    end_active = start_active + step - 1
    fade_out = end_active + 1
    if i == 1:
        css_lines.append(f"        @keyframes cssCtrl1 {{ 0%, {end_active:.1f}% {{ z-index: 20; opacity: 1; }} {fade_out:.1f}%, 100% {{ z-index: 0; opacity: 0; }} }}")
    else:
        css_lines.append(f"        @keyframes cssCtrl{i} {{ 0%, {(start_active-1):.1f}% {{ z-index: 0; opacity: 0; }} {start_active:.1f}%, {end_active:.1f}% {{ z-index: 20; opacity: 1; }} {fade_out:.1f}%, 100% {{ z-index: 0; opacity: 0; }} }}")

css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .c{i}" for i in range(1, N+1)]) + " { z-index: 20; opacity: 1; animation: none; }")
css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .css-controls" for i in range(1, N+1)]) + " { animation: none; }")

css_lines.append(f"        .css-dots {{ position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; z-index: 20; }}")
css_lines.append(f"        .css-dots label {{ width: 10px; height: 10px; background-color: rgba(255,255,255,0.4); border-radius: 50%; cursor: pointer; transition: var(--transition); }}")

for i in range(1, N+1):
    css_lines.append(f"        .css-slider-container.autoplay .css-dots label.d{i} {{ animation: cssDot{i} {duration}s infinite; }}")

for i in range(1, N+1):
    step = 100.0 / N
    start_active = (i-1) * step
    end_active = start_active + step - 1
    fade_out = end_active + 1
    if i == 1:
        css_lines.append(f"        @keyframes cssDot1 {{ 0%, {end_active:.1f}% {{ background: var(--primary-red); transform: scale(1.2); }} {fade_out:.1f}%, 100% {{ background: rgba(255,255,255,0.4); transform: scale(1); }} }}")
    else:
        css_lines.append(f"        @keyframes cssDot{i} {{ 0%, {(start_active-1):.1f}% {{ background: rgba(255,255,255,0.4); transform: scale(1); }} {start_active:.1f}%, {end_active:.1f}% {{ background: var(--primary-red); transform: scale(1.2); }} {fade_out:.1f}%, 100% {{ background: rgba(255,255,255,0.4); transform: scale(1); }} }}")

css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .css-dots .d{i}" for i in range(1, N+1)]) + " { background: var(--primary-red); transform: scale(1.2); animation: none; }")
css_lines.append(f"        " + ", ".join([f"input#s{i}:checked ~ .css-dots label" for i in range(1, N+1)]) + " { animation: none; }")

new_css = "\n".join(css_lines)

# Replace the block in styles.css
start_marker = "/* Pure CSS Slider */"
end_marker = "/* --- HAMBURGER BASE STYLES --- */"

if start_marker in css and end_marker in css:
    before = css.split(start_marker)[0]
    after = css.split(end_marker)[1]
    with open('styles.css', 'w') as f:
        f.write(before + new_css + "\n\n        " + end_marker + after)

# Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# We need to replace the contents of <div class="css-slider-container autoplay">
# Let's extract the outer parts
start_html = html.split('<div class="css-slider-container autoplay">')[0] + '<div class="css-slider-container autoplay">\n'
end_html = '        <div class="hero-overlay"></div>\n' + html.split('<div class="hero-overlay"></div>')[1]

html_lines = []
for i in range(1, N+1):
    html_lines.append(f'            <input type="radio" name="slider" id="s{i}" {"checked" if i==1 else ""}>')

html_lines.append('            <div class="css-slides">')
html_lines.append('                <div class="css-slide s1 bg-image-86284b"></div>')
html_lines.append('                <div class="css-slide s2 bg-image-3c4152"></div>')
html_lines.append('                <div class="css-slide s3 bg-image-66ae2b"></div>')
html_lines.append('                <div class="css-slide s4 bg-image-e206a8"></div>')

videos = [
    '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/SDTZ9I2JzIc?si=mFayKpRNAfXvlSml&autoplay=1&mute=1&loop=1&playlist=SDTZ9I2JzIc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
    '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/1XdWK_v2uns?si=iwOu2o85fQRkiVRV&autoplay=1&mute=1&loop=1&playlist=1XdWK_v2uns" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
    '<iframe width="100%" height="100%" src="https://www.youtube.com/embed/8a4N2nSN32o?si=DwrfodMtL6CKb-Xm&autoplay=1&mute=1&loop=1&playlist=8a4N2nSN32o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
]

for i in range(5, N+1):
    html_lines.append(f'                <div class="css-slide s{i} video-slide">{videos[i-5]}</div>')

html_lines.append('            </div>')

for i in range(1, N+1):
    prev_s = N if i == 1 else i - 1
    next_s = 1 if i == N else i + 1
    html_lines.append(f'            <div class="css-controls c{i}">')
    html_lines.append(f'                <label for="s{prev_s}" class="arrow prev-arrow"><i class="fas fa-chevron-left"></i></label>')
    html_lines.append(f'                <label for="s{next_s}" class="arrow next-arrow"><i class="fas fa-chevron-right"></i></label>')
    html_lines.append(f'            </div>')

html_lines.append('            <div class="css-dots">')
for i in range(1, N+1):
    html_lines.append(f'                <label for="s{i}" class="d{i}"></label>')
html_lines.append('            </div>\n        </div>\n')

with open('index.html', 'w') as f:
    f.write(start_html + "\n".join(html_lines) + end_html)

