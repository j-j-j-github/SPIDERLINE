import glob

favicon_link = '<link rel="icon" type="image/png" href="media/herofavicon.png">'

for filename in glob.glob('*.html'):
    with open(filename, 'r') as f:
        content = f.read()
    
    if 'herofavicon.png' not in content:
        if '</head>' in content:
            new_content = content.replace('</head>', f'    {favicon_link}\n</head>')
            with open(filename, 'w') as f:
                f.write(new_content)
                print(f"Added favicon to {filename}")

