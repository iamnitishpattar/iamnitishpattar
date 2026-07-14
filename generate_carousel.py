import urllib.request
import re
import sys

# Removed invalid icons (scikit, pandas, numpy, matplotlib) that were causing gaps and undefined behavior
icons = "py,js,html,css,react,nextjs,fastapi,flask,nodejs,mongodb,mysql,git,github,docker,vscode,aws,opencv"
url = f'https://skillicons.dev/icons?i={icons}&perline=30'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        svg_data = response.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching icons: {e}")
    sys.exit(1)

# Extract the viewBox from the ROOT svg tag
root_svg_match = re.search(r'<svg[^>]*viewBox="0 0 (\d+) (\d+)"', svg_data)
if root_svg_match:
    total_width = int(root_svg_match.group(1))
    total_height = int(root_svg_match.group(2))
    
    # Extract the inner contents securely without breaking nested tags
    inner_content_match = re.search(r'<svg.*?>([\s\S]*)</svg>', svg_data)
    if not inner_content_match:
        print("Could not find inner content")
        sys.exit(1)
        
    inner_content = inner_content_match.group(1)
    
    # The viewport width controls how small the icons are.
    viewport_width = 3500
    viewport_height = total_height
    
    # Create the animated SVG. We duplicate the content to make the scrolling seamless.
    animated_svg = f'''<svg width="100%" viewBox="0 0 {viewport_width} {viewport_height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .carousel {{
            animation: scroll 25s linear infinite;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-{total_width}px); }}
        }}
    </style>
    <g class="carousel">
        {inner_content}
    </g>
    <g class="carousel" transform="translate({total_width + 44}, 0)">
        {inner_content}
    </g>
</svg>'''
    
    with open('tech-carousel-v2.svg', 'w', encoding='utf-8') as f:
        f.write(animated_svg)
    print('Created tech-carousel-v2.svg perfectly')
else:
    print('Could not find root viewBox')
