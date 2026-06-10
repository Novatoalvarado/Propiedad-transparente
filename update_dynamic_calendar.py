import os
import re

file_path = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n/espacios_y_gobernanza/code.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Añadir el ID al selector de mes
content = re.sub(
    r'<input type="month"(.*?)>',
    r'<input id="month-selector" type="month"\1>',
    content
)

# 2. Reemplazar los días harcodeados con el contenedor dinámico
# Buscamos desde <!-- Mock Calendar Cells hasta el cierre del último dic de dia (11)
start_idx = content.find('<!-- Mock Calendar Cells')
if start_idx != -1:
    end_idx = content.find('</div>\n<div class="mt-8 p-6 rounded-xl bg-surface-container-low border border-outline-variant/10">')
    
    if end_idx != -1:
        # Extraemos lo que vamos a reemplazar
        content = content[:start_idx] + '<!-- Dynamic Calendar Cells Container -->\n<div id="calendar-days-wrapper" class="contents"></div>\n' + content[end_idx:]

# 3. Remover la logica de inicializacion vieja y reemplazar por la nueva que rinde dinamico
# Delete the old DOMContentLoaded for calendar
old_js_start = content.find("document.querySelectorAll('.aspect-square.bg-surface-container-lowest').forEach(cell => {")
# No problem, it's easier to just Regex replace the entire old DOMContentLoaded listener block if we can,
# But let's just append our render logic, the old block won't find elements anyway because they are built later,
# wait, the old block runs on DOMContentLoaded BEFORE renderCalendar... Oh wait, if it finds nothing, it does nothing.
# Let's remove the block using regex.
block_to_delete_regex = r"document\.querySelectorAll\('\.aspect-square\.bg-surface-container-lowest'\)\.forEach\(cell => \{.*?\}\);\n\s*\}\);\n"
content = re.sub(block_to_delete_regex, "", content, flags=re.DOTALL)

# Add the new dynamic logic
new_js = """
    function renderCalendar(year, month) {
        const wrapper = document.getElementById('calendar-days-wrapper');
        if(!wrapper) return;
        
        const endOfMonth = new Date(year, month, 0).getDate();
        let startDayOfWeek = new Date(year, month - 1, 1).getDay();
        if (startDayOfWeek === 0) startDayOfWeek = 7; // Lunes = 1
        
        let html = '';
        for(let i=1; i<startDayOfWeek; i++) {
            html += '<div class="aspect-square bg-surface p-2 text-xs font-medium text-outline-variant opacity-50"></div>';
        }
        
        for(let i=1; i<=endOfMonth; i++) {
            html += `<div class="aspect-square bg-surface-container-lowest p-2 text-xs font-bold hover:bg-primary-container/5 cursor-pointer flex flex-col justify-between transition-colors break-words text-center items-center">
                         <span>${i}</span>
                     </div>`;
        }
        wrapper.innerHTML = html;
        
        // Re-attach listeners to dynamically generated DOM
        document.querySelectorAll('.aspect-square.bg-surface-container-lowest').forEach(cell => {
            cell.addEventListener('click', function() {
                // Desplazar..
                document.querySelectorAll('.aspect-square.bg-primary-container').forEach(el => {
                    if(el !== this) {
                        el.classList.remove('bg-primary-container', 'text-white', 'ring-4', 'ring-primary-container/20');
                        el.classList.add('bg-surface-container-lowest', 'hover:bg-primary-container/5');
                    }
                });

                this.classList.toggle('bg-surface-container-lowest');
                this.classList.toggle('hover:bg-primary-container/5');
                this.classList.toggle('bg-primary-container');
                this.classList.toggle('text-white');
                this.classList.toggle('ring-4');
                this.classList.toggle('ring-primary-container/20');
                
                const isSelected = this.classList.contains('bg-primary-container');
                document.getElementById('reserva-dia').innerText = isSelected ? this.querySelector('span').innerText : 'ningún día';
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        const monthSelector = document.getElementById('month-selector');
        if(monthSelector) {
            monthSelector.addEventListener('change', (e) => {
                const val = e.target.value.split('-');
                if(val.length === 2) {
                    renderCalendar(parseInt(val[0]), parseInt(val[1]));
                }
            });
            const initVal = monthSelector.value.split('-');
            if(initVal.length === 2) renderCalendar(parseInt(initVal[0]), parseInt(initVal[1]));
        }
    });
"""
content = content.replace('</script>\n\n<!-- Arquitectura Global', new_js + '</script>\n\n<!-- Arquitectura Global')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Calendario dinámico implementado.')
