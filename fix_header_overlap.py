import os

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# Vamos a buscar cualquier contenedor principal que use mt-16 lg:mt-0 
# (el cual empuja el contenido hacia arriba sobre el header fijo en escritorio)
# y lo reemplazaremos por pt-20 para dar un padding interior consistente en todas las resoluciones.

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original = content
            
            # Reemplazar la clase problemática si existe
            content = content.replace('mt-16 lg:mt-0', 'pt-20')
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed header overlap padding in: {f}")
