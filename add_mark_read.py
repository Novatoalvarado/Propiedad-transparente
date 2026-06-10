import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

# The additional JS code to append inside the DOMContentLoaded of the notifications script
js_injection = """
            // Lógica para Marcar todo como leído
            const markReadBtn = document.getElementById('mark-read-btn');
            const notifsContainer = document.querySelector('#notif-dropdown .max-h-80');
            const redDot = document.querySelector('#notif-btn .bg-error');
            const countBadge = document.querySelector('#notif-dropdown .bg-primary.text-on-primary');

            function clearNotifs() {
                if(notifsContainer) {
                    notifsContainer.innerHTML = '<div class="p-8 text-center text-slate-500 flex flex-col items-center"><span class="material-symbols-outlined text-4xl mb-2 opacity-30">check_circle</span><p class="text-sm font-medium">Estás al día</p><p class="text-xs mt-1">No hay notificaciones nuevas</p></div>';
                }
                if(redDot) redDot.classList.add('hidden');
                if(countBadge) countBadge.classList.add('hidden');
                if(markReadBtn) markReadBtn.closest('div').classList.add('hidden'); // hides the footer action
            }

            // Check if already read across pages using localStorage
            if(localStorage.getItem('notifsLeidas') === 'true') {
                clearNotifs();
            }

            if(markReadBtn) {
                markReadBtn.addEventListener('click', (e) => {
                    e.stopPropagation(); // no cerrar el panel
                    localStorage.setItem('notifsLeidas', 'true');
                    clearNotifs();
                });
            }
"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Add id="mark-read-btn" to the button if not present
    content = re.sub(r'<button class="text-xs font-bold text-primary hover:underline">Marcar todas como leídas</button>', 
                     r'<button id="mark-read-btn" class="text-xs font-bold text-primary hover:underline">Marcar todas como leídas</button>', 
                     content)

    # 2. Inject the JS logic inside the existing Notificaciones JS block, right after event listener declarations
    # Look for "         if (notifBtn && notifDropdown && notifWrapper) {" block
    if "const markReadBtn = document.getElementById('mark-read-btn');" not in content:
        insert_marker = "if (notifBtn && notifDropdown && notifWrapper) {"
        content = content.replace(insert_marker, insert_marker + js_injection)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Lógica de 'Marcar como leído' agregada a: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios o ya aplicado: {os.path.basename(os.path.dirname(filepath))}")
