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

    # Buscamos la clase en <main> y removemos `w-full` y `overflow-x-hidden`.
    # Esto soluciona que el margen empuje la pantalla a un ancho del 120% y oculte cosas.
    def fix_main(match):
        classes = match.group(1)
        classes = classes.replace('w-full', '').replace('overflow-x-hidden', '')
        # Remove extra spaces
        classes = ' '.join(classes.split())
        return f'<main class="{classes}">'

    content = re.sub(r'<main class="([^"]*)">', fix_main, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Main class fix aplicado en: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios: {os.path.basename(os.path.dirname(filepath))}")
