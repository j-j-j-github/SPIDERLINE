import os
import re

dir_path = "/Users/jeevaljollyjacob/Desktop/SPIDERLINE/PROJECT"
files = [f for f in os.listdir(dir_path) if f.endswith(".html")]

hamburger_html = """
                <input type="checkbox" id="menu-toggle" class="menu-toggle-checkbox">
                <label for="menu-toggle" class="hamburger-icon">
                    <span></span>
                    <span></span>
                    <span></span>
                </label>
"""

for f in files:
    if f == "index.html": continue
    filepath = os.path.join(dir_path, f)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    
    if "hamburger-icon" not in content and "<nav class=\"navbar\">" in content:
        # We need to insert hamburger_html right after <nav class="navbar">
        content = re.sub(r'(<nav class="navbar">\s*)', r'\1' + hamburger_html + '\n', content, count=1)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Updated {f}")

