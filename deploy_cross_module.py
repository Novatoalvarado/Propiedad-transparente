import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# 1. ACTUALIZAR ESPACIOS Y GOBERNANZA (Zonas Comunes)
zonas_file = os.path.join(base_dir, "espacios_y_gobernanza", "code.html")
if os.path.exists(zonas_file):
    with open(zonas_file, 'r', encoding='utf-8') as f:
        zonas_content = f.read()

    # Botones
    zonas_content = re.sub(r"onclick=\"alert\('¡Éxito!.*?'\)\"", 'onclick="confirmarReserva()"', zonas_content)
    zonas_content = re.sub(r"onclick=\"alert\('Abriendo.*?'\)\"", 'onclick="verReglamentoBtn()"', zonas_content)

    # Dia header
    zonas_content = zonas_content.replace('<h4 class="font-bold text-sm">Reserva seleccionada: 3 de Junio</h4>', '<h4 class="font-bold text-sm">Reserva seleccionada: <span id="reserva-dia">ningún día</span> de Junio</h4>')

    # JavaScript exclusivo de zonas comunes
    zonas_js = """
<!-- Zonas Comunes Logic -->
<script>
    function confirmarReserva() {
        const dia = document.getElementById('reserva-dia').innerText;
        if(dia === 'ningún día') return alert('Por favor selecciona un día en el calendario primero.');
        
        localStorage.setItem('reservaSocial', 'true');
        localStorage.setItem('notifsLeidas', 'false'); // reset notificaciones
        
        if(typeof renderDynamicState === 'function') renderDynamicState();
        
        const notifDropdown = document.getElementById('notif-dropdown');
        if(notifDropdown) {
            notifDropdown.classList.remove('hidden', 'scale-95', 'opacity-0');
            notifDropdown.classList.add('scale-100', 'opacity-100');
        }
    }

    function verReglamentoBtn() {
        if(localStorage.getItem('archivoReglamento') === 'true') {
            const wind = window.open('about:blank', '_blank');
            wind.document.write('<div style="font-family:sans-serif; text-align:center; padding-top: 50px;"><h2>Reglamento_Zonas_Comunes.pdf simulado</h2><p>Viendo el archivo que el administrador subió en el módulo de Cargue de Archivos.</p></div>');
        } else {
            alert('El archivo "Reglamento" no ha sido cargado. Pídele al administrador que lo suba a través de la sección "Cargue de Archivos".');
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.aspect-square.bg-surface-container-lowest').forEach(cell => {
            cell.addEventListener('click', function() {
                // Desplazar seleccionado anterior
                document.querySelectorAll('.aspect-square.bg-primary').forEach(el => {
                    if(el !== this) {
                        el.classList.remove('bg-primary', 'text-white', 'ring-4', 'ring-primary/20');
                        el.classList.add('bg-surface-container-lowest');
                    }
                });

                // Toggle click actual
                this.classList.toggle('bg-surface-container-lowest');
                this.classList.toggle('bg-primary');
                this.classList.toggle('text-white');
                this.classList.toggle('ring-4');
                this.classList.toggle('ring-primary/20');
                
                const isSelected = this.classList.contains('bg-primary');
                document.getElementById('reserva-dia').innerText = isSelected ? this.innerText.trim().split('\\n')[0] : 'ningún día';
            });
        });
    });
</script>
"""
    if "<!-- Zonas Comunes Logic -->" not in zonas_content:
        zonas_content = zonas_content.replace('</body>', zonas_js + '\n</body>')

    with open(zonas_file, 'w', encoding='utf-8') as f:
        f.write(zonas_content)

# 2. ACTUALIZAR CARGUE DE ARCHIVOS
cargue_file = os.path.join(base_dir, "cargue_de_archivos", "code.html")
if os.path.exists(cargue_file):
    with open(cargue_file, 'r', encoding='utf-8') as f:
        cargue_content = f.read()

    target = "localStorage.setItem('archivoCargado', 'true');"
    replacement = "localStorage.setItem('archivoCargado', 'true');\n                    localStorage.setItem('archivoReglamento', file.name.toLowerCase().includes('reglamento') ? 'true' : 'false');"
    cargue_content = cargue_content.replace(target, replacement)

    with open(cargue_file, 'w', encoding='utf-8') as f:
        f.write(cargue_content)

# 3. ACTUALIZAR GLOBAL JS PARA TODAS LAS PAGINAS (Render Dinámico de Notificaciones)
html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

global_js = """
<!-- Arquitectura Global JS -->
<script>
    function renderDynamicState() {
        const notifsContainer = document.querySelector('#notif-dropdown .max-h-80');
        const redDot = document.querySelector('#notif-btn .bg-error');
        const countBadge = document.querySelector('#notif-dropdown .bg-primary.text-on-primary');
        const markReadBtn = document.getElementById('mark-read-btn');
        
        if(localStorage.getItem('reservaSocial') === 'true' && localStorage.getItem('notifsLeidas') !== 'true') {
             if(notifsContainer) {
                 notifsContainer.innerHTML = `
                    <a href="../pagos_y_recibos/code.html" class="block p-4 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer group">
                        <div class="flex gap-3">
                            <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                                <span class="material-symbols-outlined text-blue-600 dark:text-blue-400 text-sm">calendar_month</span>
                            </div>
                            <div>
                                <p class="text-xs font-bold text-slate-900 dark:text-white mb-0.5">Reserva Emitida Exitosamente</p>
                                <p class="text-xs text-slate-500">Tu reserva del Salón Social generó un recargo por concepto de limpieza y aforo.</p>
                                <p class="text-[10px] text-primary mt-1 font-bold">Ver factura pendiente en Pagos</p>
                            </div>
                        </div>
                    </a>
                 `;
             }
             if(redDot) redDot.classList.remove('hidden');
             if(countBadge) {
                 countBadge.classList.remove('hidden');
                 countBadge.innerText = "1 Nueva";
             }
             if(markReadBtn) {
                 const foot = markReadBtn.closest('div');
                 if(foot) foot.classList.remove('hidden');
             }
        }
    }
    document.addEventListener('DOMContentLoaded', renderDynamicState);
</script>
"""

# 4. AÑADIR LÓGICA DE TABLA DE PAGOS Y RECIBOS EN SU ARCHIVO
finanzas_js = """
<!-- Pagos y Recibos Logic -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        if(localStorage.getItem('reservaSocial') === 'true') {
            const tbody = document.querySelector('tbody');
            if(tbody) {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group";
                tr.innerHTML = `
                    <td class="py-4 pl-8"><div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center group-hover:bg-white dark:group-hover:bg-slate-700 transition-colors"><span class="material-symbols-outlined text-primary text-lg" data-icon="chair">chair</span></div><div><p class="text-sm font-bold text-slate-900 dark:text-white">Alquiler Salón Social</p><p class="text-[10px] text-slate-500 font-medium">Concepto Aforo C</p></div></div></td>
                    <td class="py-4 text-sm font-semibold text-slate-700 dark:text-slate-300">03 Jun 2024</td>
                    <td class="py-4"><p class="text-sm font-bold text-slate-900 dark:text-white">$45,000.00 <span class="text-[10px] text-slate-500 font-normal">COP</span></p></td>
                    <td class="py-4"><span class="px-3 py-1 rounded-full bg-error-container text-on-error-container text-[10px] font-bold tracking-wider inline-flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-error animate-pulse"></span>PENDIENTE</span></td>
                    <td class="py-4 pr-8 text-right"><button class="px-4 py-2 bg-primary text-white text-xs font-bold rounded-lg hover:opacity-90 transition-opacity">Pagar ahora</button></td>
                `;
                tbody.insertBefore(tr, tbody.firstChild);
            }
        }
    });
</script>
"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "<!-- Arquitectura Global JS -->" not in content:
        content = content.replace("</body>", global_js + "\n</body>")
        
    if "pagos_y_recibos" in filepath and "<!-- Pagos y Recibos Logic -->" not in content:
        content = content.replace("</body>", finanzas_js + "\n</body>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Integración arquitectónica dinámica implementada exitosamente en todos los módulos.")
