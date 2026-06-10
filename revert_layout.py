import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original = content
            
            # Quitar el wrapper de clases estrictas y el viejo (Cualquier div flex flex-col h-full despues de main)
            # Primero buscamos el div de apertura. 
            # Los hemos estado inyectando despues del tag <main ...>
            
            # Buscar el div de apertura:
            pattern_open = r'<div id="layout-center-wrapper"[^>]*>\n?'
            content = re.sub(pattern_open, '', content)
            
            # Buscar el cierre que inyectamos antes del </main>: 
            # Inyectamos: </div>\n</main>
            # Vamos a buscar </div>\n</main> o </div>\s*</main>
            pattern_close = r'</div>\s*</main>'
            content = re.sub(pattern_close, '</main>', content)
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Reverted layout wrapper in: {f}")
