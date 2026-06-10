import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# The original button HTML string that we want to replace
original_btn_pattern = r'<button class="relative text-slate-400 hover:text-slate-600 transition-all">(\s*)<span class="material-symbols-outlined" data-icon="notifications">notifications</span>(\s*)<span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full border-2 border-white"></span>(\s*)</button>'

replacement_dropdown = """<div class="relative" id="notifications-wrapper">
<button id="notif-btn" class="relative text-slate-400 hover:text-slate-600 transition-all focus:outline-none focus:ring-2 focus:ring-primary/20 rounded-full p-1">
<span class="material-symbols-outlined" data-icon="notifications">notifications</span>
<span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full border-2 border-white"></span>
</button>

<!-- Dropdown Flotante -->
<div id="notif-dropdown" class="absolute right-0 top-full mt-3 w-80 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl shadow-xl hidden z-[70] overflow-hidden origin-top-right transition-all transform scale-95 opacity-0">
    <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center bg-slate-50 dark:bg-slate-800/50">
        <h3 class="font-bold text-slate-900 dark:text-white text-sm">Notificaciones</h3>
        <span class="bg-primary text-on-primary text-[10px] font-bold px-2 py-0.5 rounded-full">3 Nuevas</span>
    </div>
    <div class="max-h-80 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800">
        <!-- Notif 1 -->
        <a href="../centro_de_votaciones_admin/code.html" class="block p-4 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer group">
            <div class="flex gap-3">
                <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-blue-600 dark:text-blue-400 text-sm">how_to_vote</span>
                </div>
                <div>
                    <p class="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Nueva Encuesta: Zonas Comunes</p>
                    <p class="text-xs text-slate-500">Participa en la votación sobre paneles solares.</p>
                    <p class="text-[10px] text-slate-400 mt-1 font-medium">Hace 2 horas</p>
                </div>
            </div>
        </a>
        <!-- Notif 2 -->
        <div class="block p-4 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer group">
            <div class="flex gap-3">
                <div class="w-8 h-8 rounded-full bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-yellow-600 dark:text-yellow-400 text-sm">campaign</span>
                </div>
                <div>
                    <p class="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Aviso de Mantenimiento</p>
                    <p class="text-xs text-slate-500">Limpieza de cisternas programada para este sábado a las 9:00 AM.</p>
                    <p class="text-[10px] text-slate-400 mt-1 font-medium">Hoy a las 10:15</p>
                </div>
            </div>
        </div>
        <!-- Notif 3 -->
        <a href="../pagos_y_recibos/code.html" class="block p-4 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer group">
            <div class="flex gap-3">
                <div class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-green-600 dark:text-green-400 text-sm">receipt_long</span>
                </div>
                <div>
                    <p class="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Pago Exitoso</p>
                    <p class="text-xs text-slate-500">Tu recibo por la cuota de mantenimiento de Mayo está disponible.</p>
                    <p class="text-[10px] text-slate-400 mt-1 font-medium">Hace 3 días</p>
                </div>
            </div>
        </a>
    </div>
    <div class="p-3 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-center">
        <button class="text-xs font-bold text-primary hover:underline">Marcar todas como leídas</button>
    </div>
</div>
</div>"""

js_script = """
<!-- Notificaciones JS -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const notifBtn = document.getElementById('notif-btn');
        const notifDropdown = document.getElementById('notif-dropdown');
        const notifWrapper = document.getElementById('notifications-wrapper');

        if (notifBtn && notifDropdown && notifWrapper) {
            notifBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent closing immediately
                const isHidden = notifDropdown.classList.contains('hidden');
                
                if (isHidden) {
                    notifDropdown.classList.remove('hidden');
                    // Small delay to allow CSS display:block to apply before animating opacity
                    setTimeout(() => {
                        notifDropdown.classList.remove('scale-95', 'opacity-0');
                        notifDropdown.classList.add('scale-100', 'opacity-100');
                    }, 10);
                } else {
                    notifDropdown.classList.remove('scale-100', 'opacity-100');
                    notifDropdown.classList.add('scale-95', 'opacity-0');
                    setTimeout(() => {
                        notifDropdown.classList.add('hidden');
                    }, 150); // Matches transition duration
                }
            });

            // Close when clicking outside
            document.addEventListener('click', (e) => {
                if (!notifWrapper.contains(e.target) && !notifDropdown.classList.contains('hidden')) {
                    notifDropdown.classList.remove('scale-100', 'opacity-100');
                    notifDropdown.classList.add('scale-95', 'opacity-0');
                    setTimeout(() => {
                        notifDropdown.classList.add('hidden');
                    }, 150);
                }
            });
        }
    });
</script>
"""

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Prevenir doble inyección asegurándonos de que ya no esté el dropdown insertado
    if 'id="notif-dropdown"' not in content:
        # Reemplazar botón original
        content = re.sub(original_btn_pattern, replacement_dropdown, content)
        
        # Inyectar Javascript justo antes de </body>
        content = re.sub(r'</body>', js_script + '\n</body>', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Notificaciones agregadas a: {os.path.basename(os.path.dirname(filepath))}")
    else:
        print(f"Sin cambios o ya instalado: {os.path.basename(os.path.dirname(filepath))}")
