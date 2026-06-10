import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# Diccionario de nombres a reemplazar en el menú
names_mapping = {
    '>Dashboard<': '>Dashboard Copropietario<',
    '>Finances<': '>Pagos y Recibos<',
    '>Bookings<': '>Espacios y Gobernanza<',
    '>Governance<': '>Centro Votaciones<',
    '>Admin Tools<': '>Panel Administrador<',
    '>Support<': '>Asistente y Chat<'
}

js_snippet = """
<!-- Menú Deslizante JS -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Evitamos doble inyección si el script se corre más de una vez
        if (document.getElementById('toggle-menu-btn')) return;

        const sidebar = document.querySelector('aside');
        const header = document.querySelector('header');
        const main = document.querySelector('main');
        
        if (sidebar && header && main) {
            // Añadir clases de transición
            sidebar.classList.add('transition-transform', 'duration-300', 'z-[60]');
            header.classList.add('transition-all', 'duration-300');
            main.classList.add('transition-all', 'duration-300');

            // Crear el botón de hamburguesa
            const menuBtnContainer = document.createElement('div');
            menuBtnContainer.innerHTML = '<button id="toggle-menu-btn" class="flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-800 rounded-full p-2 mr-2"><span class="material-symbols-outlined text-slate-800 dark:text-white">menu</span></button>';
            const menuBtn = menuBtnContainer.firstChild;
            
            let isClosed = false;
            
            // Lógica de toggle
            menuBtn.onclick = () => {
                isClosed = !isClosed;
                if (isClosed) {
                    sidebar.classList.add('-translate-x-full');
                    header.style.width = '100%';
                    main.style.marginLeft = '0';
                } else {
                    sidebar.classList.remove('-translate-x-full');
                    header.style.width = 'calc(100% - 16rem)';
                    main.style.marginLeft = '16rem'; // 64 padding * 4px = 256px = 16rem
                }
            };
            
            // Insertar botón en el header
            header.insertBefore(menuBtn, header.firstChild);
            
            // Crear botón de cerrar (X) que sólo se muestra en pantallas pequeñas, dentro del aside
            const closeBtnContainer = document.createElement('div');
            closeBtnContainer.innerHTML = '<button class="absolute top-4 right-4 md:hidden flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-800 rounded-full p-1"><span class="material-symbols-outlined text-slate-800 dark:text-white">close</span></button>';
            const closeBtn = closeBtnContainer.firstChild;
            closeBtn.onclick = () => menuBtn.click();
            sidebar.appendChild(closeBtn);
        }
    });
</script>
</body>
"""

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Reemplazar los textos del menú
    for old_text, new_text in names_mapping.items():
        content = content.replace(old_text, new_text)

    # 2. Inyectar el script de JS antes del </body>
    if '<!-- Menú Deslizante JS -->' not in content:
        content = content.replace('</body>', js_snippet)

    # Solo escribir si hubo cambios
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Modificado {filepath}")
    else:
        print(f"Sin cambios {filepath}")

print("Proceso completado.")
