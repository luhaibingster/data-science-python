import re

with open('c:\\Users\\hlu\\Downloads\\preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

def increment_font_size(match):
    num = int(match.group(1))
    return f'font-size: {num + 1}px'

content = re.sub(r'font-size:\s*(\d+)px', increment_font_size, content)

with open('c:\\Users\\hlu\\Downloads\\preview.html', 'w', encoding='utf-8') as f:
    f.write(content)