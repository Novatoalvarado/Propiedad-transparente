import os
import re

file_path = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n/espacios_y_gobernanza/code.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Expandir calendario y cambiar selector Semana/Mes por dropdowns de Mes/Año
content = re.sub(
    r'<section class="col-span-12 lg:col-span-8 space-y-6">',
    r'<section class="col-span-12 space-y-6">',
    content
)

old_calendar_header = """<div class="flex bg-surface-container rounded-lg p-1">
<button class="px-4 py-1.5 bg-white shadow-sm rounded-md text-xs font-bold">Semana</button>
<button class="px-4 py-1.5 text-xs font-medium text-on-surface-variant">Mes</button>
</div>"""
new_calendar_header = """<div class="flex gap-2">
<select class="border-none bg-surface-container rounded-lg text-xs font-bold px-4 py-2 hover:bg-surface-container-high transition-colors focus:ring-0 cursor-pointer text-slate-900 outline-none">
    <option>Enero</option>
    <option>Febrero</option>
    <option>Marzo</option>
    <option>Abril</option>
    <option>Mayo</option>
    <option selected>Junio</option>
    <option>Julio</option>
    <option>Agosto</option>
    <option>Septiembre</option>
    <option>Octubre</option>
    <option>Noviembre</option>
    <option>Diciembre</option>
</select>
<select class="border-none bg-surface-container rounded-lg text-xs font-bold px-4 py-2 hover:bg-surface-container-high transition-colors focus:ring-0 cursor-pointer text-slate-900 outline-none">
    <option>2023</option>
    <option selected>2024</option>
    <option>2025</option>
</select>
</div>"""
content = content.replace(old_calendar_header, new_calendar_header)

# 2. Eliminar "Centro de Votaciones" y "Transparencia Total"
# Utilizaremos una REGEX muy precisa o borrado de strings literales identificados
# Buscaremos desde <!-- 2. Centro de Votaciones (Participation Lists) --> hasta el fin del section
delete_pattern = r'<!-- 2\. Centro de Votaciones \(Participation Lists\) -->.*?</section>'
content = re.sub(delete_pattern, '', content, flags=re.DOTALL)

# 3. Interaccion de las estrellas
# Buscamos <div class="flex gap-1 mb-6"> y lo cambiamos a <div class="flex gap-1 mb-6 rating-container">
content = content.replace('<div class="flex gap-1 mb-6">', '<div class="flex gap-1 mb-6 rating-container justify-center">')

# Y añadimos JS de calificacion justo antes de </body>
rating_js = """
<!-- Interacción Estrellas JS -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.rating-container').forEach(container => {
            const stars = container.querySelectorAll('.material-symbols-outlined');
            stars.forEach((star, index) => {
                star.classList.add('cursor-pointer', 'transition-all', 'hover:scale-125');
                star.onclick = () => {
                    stars.forEach((s, i) => {
                        if (i <= index) {
                            s.classList.add('text-tertiary-fixed');
                            s.classList.remove('text-outline-variant', 'group-hover:text-white/20');
                            s.style.fontVariationSettings = "'FILL' 1";
                        } else {
                            s.classList.remove('text-tertiary-fixed');
                            s.classList.add('text-outline-variant', 'group-hover:text-white/20');
                            s.style.fontVariationSettings = "'FILL' 0";
                        }
                    });
                };
            });
        });
    });
</script>
"""
if "<!-- Interacción Estrellas JS -->" not in content:
    content = content.replace('</body>', rating_js + '\n</body>')

# 4. Modificar el boton Flotante "Necesitas Ayuda" con WhatsApp
old_help_widget = """<!-- Selection Modal (Floating Placeholder) -->
<div class="fixed bottom-8 right-8 z-50 pointer-events-none">
<div class="pointer-events-auto bg-white p-4 rounded-xl shadow-[0_10px_40px_rgba(0,0,0,0.15)] flex items-center gap-4 border border-outline-variant/30 animate-bounce">
<div class="w-12 h-12 bg-primary-container rounded-lg flex items-center justify-center">
<span class="material-symbols-outlined text-white" data-icon="chat">chat</span>
</div>
<div>
<p class="text-sm font-bold">¿Necesitas ayuda?</p>
<p class="text-xs text-on-surface-variant">Consulta las normas de convivencia.</p>
</div>
</div>
</div>"""

# Como puede haber un espaciado algo diferente, usaré RegEx
widget_regex = r'<!-- Selection Modal \(Floating Placeholder\) -->\s*<div class="fixed bottom-8 right-8 z-50 pointer-events-none">.*?</div>\s*</div>'
new_help_widget = """<!-- Ayuda Whatsapp -->
<div class="fixed bottom-8 right-8 z-50 pointer-events-none">
<a href="https://wa.me/3201234567" target="_blank" class="pointer-events-auto bg-white dark:bg-slate-900 p-4 rounded-xl shadow-2xl flex items-center gap-4 border border-outline-variant/30 animate-bounce hover:scale-105 hover:shadow-primary/30 transition-all cursor-pointer no-underline">
<div class="w-12 h-12 bg-[#25D366] rounded-lg flex items-center justify-center shadow-lg">
<span class="material-symbols-outlined text-white" data-icon="chat">chat</span>
</div>
<div class="pr-2">
<p class="text-sm font-bold text-slate-900 dark:text-white">¿Necesitas ayuda?</p>
<p class="text-xs text-slate-500">Comunícate con administración.</p>
</div>
</a>
</div>"""

content = re.sub(widget_regex, new_help_widget, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Modificaciones en Zonas Comunes realizadas con éxito.")
