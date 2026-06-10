import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

mapping = {
    'dashboard': '../dashboard_copropietario/code.html',
    'payments': '../pagos_y_recibos/code.html',
    'event_available': '../espacios_y_gobernanza/code.html',
    'gavel': '../centro_de_votaciones_admin/code.html',
    'settings_applications': '../panel_de_administraci_n/code.html',
    'contact_support': '../asistente_ia_chat_de_copropiedad_1/code.html',
    'smart_toy': '../asistente_ia_chat_de_copropiedad_1/code.html',
    'description': '../gesti_n_de_documentos_admin/code.html',
    'settings': '../perfil_y_configuraci_n_1/code.html',
    'real_estate_agent': '../perfil_y_configuraci_n_1/code.html',
    'help': '../asistente_ia_chat_de_copropiedad_1/code.html'
}

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# Pattern to capture an anchor tag with href="#" and its inner span with data-icon
# It relies on the generic structure: <a ... href="#" ... > ... <span ... data-icon="XX" ...>
# Using a custom replacement logic to find indices and replace precisely

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Replace form action="#" with dashboard
    content = content.replace('action="#"', 'action="../dashboard_copropietario/code.html"')

    # 2. Iteratively find <a ...> blocks containing </a> and a span with data-icon
    # We will use regex to find all <a tags
    matches = list(re.finditer(r'<a\s+[^>]*?href=["\']?[^>]*?>', content))
    
    offset = 0
    for match in matches:
        start_idx = match.start() + offset
        end_idx = match.end() + offset
        
        # Look ahead from end_idx of <a to find </a>
        close_a_idx = content.find('</a>', end_idx)
        if close_a_idx != -1:
            inner_html = content[end_idx:close_a_idx]
            
            # Check for data-icon inside inner HTML
            icon_match = re.search(r'data-icon=["\']([^"\']+)["\']', inner_html)
            
            if icon_match:
                icon = icon_match.group(1)
                if icon in mapping:
                    target_url = mapping[icon]
                    # We need to replace href="#" or similar inside the <a ... tag
                    a_tag = content[start_idx:end_idx]
                    
                    new_a_tag = re.sub(r'href=["\'][^"\']*["\']', f'href="{target_url}"', a_tag)
                    if 'href=' not in new_a_tag:
                        # Fallback if no href exists
                        pass
                    else:
                        content = content[:start_idx] + new_a_tag + content[end_idx:]
                        offset += len(new_a_tag) - len(a_tag)
            elif "Cerrar Sesión" in inner_html or "Logout" in inner_html or "Log out" in inner_html:
                # Replace logout with login screen
                a_tag = content[start_idx:end_idx]
                new_a_tag = re.sub(r'href=["\'][^"\']*["\']', f'href="../inicio_de_sesi_n_actualizado_1/code.html"', a_tag)
                content = content[:start_idx] + new_a_tag + content[end_idx:]
                offset += len(new_a_tag) - len(a_tag)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

print("Batch update complete.")
