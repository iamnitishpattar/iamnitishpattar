import urllib.request
import re
import sys

icons = "py,js,html,css,react,nextjs,fastapi,flask,nodejs,mongodb,mysql,git,github,docker,vscode,aws,scikit,pandas,opencv,numpy,matplotlib"
url = f'https://skillicons.dev/icons?i={icons}&perline=30'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        svg_data = response.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching icons: {e}")
    sys.exit(1)

match = re.search(r'width="(\d+)"', svg_data)
if match:
    width = int(match.group(1))
    
    # Extract the inner contents
    inner_content_match = re.search(r'<svg.*?>([\s\S]*)</svg>', svg_data)
    if not inner_content_match:
        print("Could not find inner content")
        sys.exit(1)
        
    inner_content = inner_content_match.group(1)
    
    # Create the animated SVG. We duplicate the content to make the scrolling seamless.
    # The first set scrolls from 0 to -width, and the second set follows right behind it.
    animated_svg = f'''<svg width="100%" height="80" viewBox="0 0 {width} 80" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .carousel {{
            animation: scroll 25s linear infinite;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-{width}px); }}
        }}
    </style>
    <g class="carousel">
        {inner_content}
    </g>
    <g class="carousel" transform="translate({width}, 0)">
        {inner_content}
    </g>
</svg>'''
    
    with open('tech-carousel.svg', 'w', encoding='utf-8') as f:
        f.write(animated_svg)
    print('Created tech-carousel.svg')
else:
    print('Could not find width')
