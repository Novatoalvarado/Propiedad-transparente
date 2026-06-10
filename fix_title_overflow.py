import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix the title overflowing the container (causing it to peek out when sidebar is hidden)
    # 1. Update <aside> to have overflow-x-hidden and overflow-y-auto
    content = re.sub(r'<aside class="([^"]*)"', lambda m: '<aside class="' + m.group(1).replace('overflow-x-hidden', '').replace('overflow-y-auto', '') + ' overflow-x-hidden overflow-y-auto"', content, count=1)
    
    # 2. Update <h2> to have text-lg (instead of text-xl) and truncate
    content = re.sub(r'<h2 class="(.*?)text-xl(.*?)">PropiedadTransparente</h2>', r'<h2 class="\1text-lg truncate\2">PropiedadTransparente</h2>', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fix overflow en: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios: {os.path.basename(os.path.dirname(filepath))}")
