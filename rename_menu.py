import os

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

old_text = ">Espacios y Gobernanza<"
new_text = ">Zonas comunes<"

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if old_text in content:
        new_content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Modificado {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios {os.path.basename(os.path.dirname(filepath))}")

print("Completado.")
