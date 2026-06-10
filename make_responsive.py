import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

js_script = """<!-- Menú Deslizante JS -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('toggle-menu-btn')) return;

        const sidebar = document.querySelector('aside');
        const header = document.querySelector('header');
        const main = document.querySelector('main');
        
        if (sidebar && header && main) {
            // Eliminar clases conflictivas estáticas si las hay y asegurar base
            sidebar.classList.add('transform', 'transition-transform', 'duration-300', 'z-[60]');
            header.classList.add('transition-all', 'duration-300');
            main.classList.add('transition-all', 'duration-300');

            const menuBtnContainer = document.createElement('div');
            menuBtnContainer.innerHTML = '<button id="toggle-menu-btn" class="flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-800 rounded-full p-2 mr-2 lg:mr-4"><span class="material-symbols-outlined text-slate-800 dark:text-white">menu</span></button>';
            const menuBtn = menuBtnContainer.firstChild;
            header.insertBefore(menuBtn, header.firstChild);

            // Capa oscura para dispositivos móviles
            const overlay = document.createElement('div');
            overlay.className = 'fixed inset-0 bg-black/50 z-50 hidden transition-opacity duration-300 opacity-0 lg:hidden';
            document.body.appendChild(overlay);
            
            let isSidebarOpen = window.innerWidth >= 1024; // breakpoint lg Tailwind

            function updateMenuUI() {
                if (window.innerWidth >= 1024) { // Pantallas grandes (escritorio)
                    overlay.classList.add('hidden');
                    overlay.classList.remove('opacity-100');
                    if (isSidebarOpen) {
                        sidebar.classList.remove('-translate-x-full');
                        sidebar.classList.add('lg:translate-x-0');
                        header.style.width = 'calc(100% - 16rem)';
                        main.style.marginLeft = '16rem';
                    } else {
                        sidebar.classList.add('-translate-x-full');
                        sidebar.classList.remove('lg:translate-x-0');
                        header.style.width = '100%';
                        main.style.marginLeft = '0';
                    }
                } else { // Pantallas móviles e iPad vertical
                    header.style.width = '100%';
                    main.style.marginLeft = '0';
                    if (isSidebarOpen) {
                        sidebar.classList.remove('-translate-x-full');
                        overlay.classList.remove('hidden');
                        setTimeout(() => overlay.classList.add('opacity-100'), 10);
                    } else {
                        sidebar.classList.add('-translate-x-full');
                        overlay.classList.remove('opacity-100');
                        setTimeout(() => overlay.classList.add('hidden'), 300);
                    }
                }
            }

            menuBtn.onclick = () => {
                isSidebarOpen = !isSidebarOpen;
                updateMenuUI();
            };

            overlay.onclick = () => {
                isSidebarOpen = false;
                updateMenuUI();
            };

            // Escuchar redimensionamiento dinámico
            window.addEventListener('resize', () => {
                let wasDesktop = window.innerWidth >= 1024;
                // Pequeño hack para resetear estado al pasar de mobile a desktop o viceversa
                if(wasDesktop && sidebar.classList.contains('-translate-x-full') && header.style.width == '100%') {
                    // Mantener decisiones del usuario
                } else {
                    isSidebarOpen = window.innerWidth >= 1024;
                    updateMenuUI();
                }
            });

            // Botón X en el propio sidebar para celular
            const closeBtnContainer = document.createElement('div');
            closeBtnContainer.innerHTML = '<button class="absolute top-4 right-4 lg:hidden flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-800 rounded-full p-1"><span class="material-symbols-outlined text-slate-800 dark:text-white">close</span></button>';
            const closeBtn = closeBtnContainer.firstChild;
            closeBtn.onclick = () => {
                isSidebarOpen = false;
                updateMenuUI();
            };
            sidebar.appendChild(closeBtn);
            
            // Inicialización visual forzada
            updateMenuUI();
        }
    });
</script>"""

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Ajustar el <aside> para default responsivo oculto
    # Buscar el inicio de <aside class="...">
    content = re.sub(r'<aside class="[^"]*"', r'<aside class="h-screen w-64 fixed left-0 top-0 bg-slate-50 dark:bg-slate-900 flex flex-col py-6 px-4 z-[60] transform -translate-x-full lg:translate-x-0 transition-transform duration-300"', content, count=1)

    # 2. Ajustar el <header> para default width responsivo
    content = re.sub(r'<header class="[^"]*"', r'<header class="fixed top-0 right-0 w-full lg:w-[calc(100%-16rem)] h-16 z-40 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md flex justify-between items-center px-4 lg:px-8 border-b border-slate-100 dark:border-slate-800 transition-all duration-300"', content, count=1)

    # 3. Ocultar la barra de búsqueda en moviles
    content = re.sub(r'<div class="flex items-center gap-4 bg-surface-container-low px-4 py-2 rounded-full w-96([^"]*)"', r'<div class="hidden md:flex items-center gap-4 bg-surface-container-low px-4 py-2 rounded-full w-80 lg:w-96\1"', content)

    # 4. Ajustar el <main> para márgenes dinámicos
    # Puede que tenga "ml-64" o similar
    content = re.sub(r'<main class="([^"]*)"', lambda m: '<main class="' + m.group(1).replace('ml-64', '').replace('px-8', '') + ' lg:ml-64 px-4 md:px-8 transition-all duration-300 w-full overflow-x-hidden"', content, count=1)

    # 5. Reemplazar completamente la sección de Javascript del Menu
    content = re.sub(r'<!-- Menú Deslizante JS -->.*?</body>', js_script + '\n</body>', content, flags=re.DOTALL)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Hecho responsivo: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios: {os.path.basename(os.path.dirname(filepath))}")
