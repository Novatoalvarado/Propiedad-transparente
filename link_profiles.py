import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

pattern = re.compile(
    r'<div class="flex items-center gap-3 pl-4 border-l border-slate-100 dark:border-slate-800">(.*?)</div>\s*</div>\s*</header>', 
    re.DOTALL
)

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            file_path = os.path.join(root, f)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            def replacer(match):
                inner = match.group(1)
                # Ensure we capture up to the end of the profile div but leave header closures intact
                return f'<a href="../administracion_de_perfil/code.html" class="flex items-center gap-3 pl-4 border-l border-slate-100 dark:border-slate-800 hover:opacity-60 transition-opacity cursor-pointer text-inherit no-underline">{inner}</div>\n</div>\n</header>'
            
            new_content = pattern.sub(replacer, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated: {file_path}")

print("Proceso de enlace completado.")
