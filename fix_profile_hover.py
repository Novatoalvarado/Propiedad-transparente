import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# Bug 1: Unclosed DIV that breaks layout and swallows tags
malformed_div = """<!-- Oculto para evitar parse errors --> <div class="hidden" onclick="alert('Sistema conectado:\\nTodos tus datos y metadatos han sido validados e inyectados en la Base de Datos Relacional y guardados en tu historial de operaciones NoSQL.')" class="bg-primary-container text-white px-8 py-3 rounded-full font-bold text-sm hover:opacity-90 hover:-translate-y-0.5 transition-all shadow-xl hover:shadow-primary/40 flex items-center gap-2">
                        <span class="material-symbols-outlined text-[18px]">verified_user</span> Confirmar y Guardar Perfil
                    </button>"""

# Bug 2: group class on the entire left panel
panel_broken = 'relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow'
panel_fixed = 'relative overflow-hidden shadow-sm hover:shadow-md transition-shadow'

# Bug 3: add group class to the avatar container so hover only works there
avatar_broken = 'w-32 h-32 mx-auto rounded-full bg-surface-container border-4 border-white dark:border-slate-800 shadow-xl overflow-hidden relative cursor-pointer ring-4 ring-primary-container/10"'
avatar_fixed = 'w-32 h-32 mx-auto rounded-full bg-surface-container border-4 border-white dark:border-slate-800 shadow-xl overflow-hidden relative cursor-pointer ring-4 ring-primary-container/10 group"'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original = content
            
            # Remove malformed div
            if malformed_div in content:
                content = content.replace(malformed_div, '')
            
            # Fix left panel group class
            if panel_broken in content and avatar_broken in content:
                content = content.replace(panel_broken, panel_fixed)
                content = content.replace(avatar_broken, avatar_fixed)
                
            if content != original:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed profile bugs in: {f}")
