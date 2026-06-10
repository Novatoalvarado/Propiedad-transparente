import os

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# Vamos a buscar el <div id="layout-center-wrapper" ...> y reemplazar sus clases
# para asegurar que siempre haya márgenes visuales explícitos con porcentajes
# de forma que cualquier pantalla se vea perfectamente encuadrada con independencia del monitor.

old_wrapper = 'id="layout-center-wrapper" class="w-full max-w-7xl mx-auto flex flex-col h-full"'
new_wrapper = 'id="layout-center-wrapper" class="w-[94%] xl:w-[90%] max-w-[1440px] mx-auto flex flex-col h-full"'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            if old_wrapper in content:
                new_content = content.replace(old_wrapper, new_wrapper)
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Mejorado layout en: {f}")
            elif new_wrapper not in content:
                print(f"[!] Wrapper no encontrado en {f}")
