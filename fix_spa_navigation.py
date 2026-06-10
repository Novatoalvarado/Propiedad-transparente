import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# Vamos a transformar los enlaces estáticos en transiciones suaves JS para evitar
# que el navegador muestre rutas del disco duro (tooltip de URLs) y enmascarar el parpadeo 
# agresivo de los saltos entre archivos HTML puros con una animación Fade-In sutil.

style_injection = """
<style>
    /* UX Transitions para navegación estática sin React/Next */
    @keyframes smoothLoad { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    body { animation: smoothLoad 0.25s ease-out forwards; }
</style>
"""

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            
            # Inyectar transition style en caso de no existir
            if "smoothLoad" not in content:
                content = content.replace("</head>", style_injection + "\n</head>")
            
            # Reemplazar href por navigations JS en la barra lateral (nav)
            # Para cada elemento con href dentro de tag <nav ...> o <a class="... text-slate-500 ...">
            # Es más sencillo buscar 'href="../' y transformarlo a onclick para los tag <a>
            # pero necesitamos conservar `class="... pointer-cursor"`
            def anchor_replacer(match):
                # match.group(0) es todo el tag <a>
                # match.group(1) es la parte antes del href
                # match.group(2) es el target url
                # match.group(3) es la parte despues
                pre = match.group(1)
                url = match.group(2)
                post = match.group(3)
                
                # Agregamos cursor pointer por si acaso y cambiamos la via de accion
                if "cursor-pointer" not in pre and "cursor-pointer" not in post:
                    pre = pre + ' cursor-pointer '
                    
                return f'{pre} onclick="window.location.href=\'{url}\'"{post}'

            # Este regex localiza un tag <a ... href="URL" ...>
            # Buscamos de manera segura
            content = re.sub(r'(<a\s+[^>]*?)href="([^"]+)"([^>]*>)', anchor_replacer, content)

            if content != original:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Applied smooth SPA UX to: {f}")
