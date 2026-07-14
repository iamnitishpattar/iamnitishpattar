import urllib.request
import re
import sys

# Included potential names just in case
icons = "py,js,html,css,react,nextjs,fastapi,flask,nodejs,mongodb,mysql,git,github,docker,vscode,aws,scikit,pandas,opencv,numpy,matplotlib"
url = f'https://skillicons.dev/icons?i={icons}&perline=30'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        svg_data = response.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching icons: {e}")
    sys.exit(1)

# Extract the inner contents (all the <g> tags)
inner_content_match = re.search(r'<svg.*?>([\s\S]*)</svg>', svg_data)
if not inner_content_match:
    print("Could not find inner content")
    sys.exit(1)
    
inner_content = inner_content_match.group(1)

# Find all individual icon groups
icon_blocks = re.findall(r'<g transform="translate\(\d+,\s*0\)">(.*?)</g>', inner_content, re.DOTALL)

# Filter out the 'undefined' ones
valid_icons = []
for block in icon_blocks:
    if "undefined" not in block:
        valid_icons.append(block)

if not valid_icons:
    print("No valid icons found")
    sys.exit(1)

# Rebuild the inner content without gaps
rebuilt_content = ""
current_x = 0
for icon in valid_icons:
    rebuilt_content += f'\n<g transform="translate({current_x}, 0)">{icon}</g>'
    current_x += 300

# Total width is the x position of the next item (which would be placed there) minus the 44px gap
total_width = current_x - 44

viewport_width = 3500
viewport_height = 256

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
        {rebuilt_content}
    </g>
    <g class="carousel" transform="translate({total_width + 44}, 0)">
        {rebuilt_content}
    </g>
</svg>'''

with open('tech-carousel.svg', 'w', encoding='utf-8') as f:
    f.write(animated_svg)
print('Created tech-carousel.svg with gaps removed')
