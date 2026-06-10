import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

anchor_open_str = '<a href="../administracion_de_perfil/code.html"'
span_str = 'account_circle</span>\n</div>'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original = content
            
            # 1. FIX THE UNCLOSED ANCHOR TAG
            # My previous script (link_profiles.py) turned an opening <div class="flex..."> into <a href="...">
            # But the closing tag was left as </div> right after <span ...>account_circle</span>
            # We fix it by looking for the anchor and its matching span block, and replacing the </div> with </a>
            
            # Using regex to find the block
            # El bloque de interés suele ser siempre este:
            # <span class="material-symbols-outlined text-slate-900 text-3xl" data-icon="account_circle">account_circle</span>
            # </div>
            # Queremos cambiar ese </div> por </a>, pero SOLO si está dentro de una estructura que abrió con <a href="../administracion_de_perfil...
            
            # Es más seguro un reemplazo directo del pedazo estricto si existe la ancla arriba.
            if anchor_open_str in content:
                content = content.replace(
                    '<span class="material-symbols-outlined text-slate-900 text-3xl" data-icon="account_circle">account_circle</span>\n</div>',
                    '<span class="material-symbols-outlined text-slate-900 text-3xl" data-icon="account_circle">account_circle</span>\n</a>'
                )
            
            # 2. FIX THE INTERVAL FLICKERING IMAGE BUG
            # The JS was overwriting icon.src every 1000ms with a heavy base64 string without checking if it belonged.
            bad_js = '''                        if(icon.classList.contains('w-10')) {
                            icon.src = localStorage.getItem('userPicUrl');
                        }'''
                        
            good_js = '''                        if(icon.classList.contains('w-10')) {
                            let newSrc = localStorage.getItem('userPicUrl');
                            if (icon.src !== newSrc) {
                                icon.src = newSrc;
                            }
                        }'''
            
            if bad_js in content:
                content = content.replace(bad_js, good_js)
            
            # Extra safeguard for another common script block variance
            bad_js_2 = '''if(icon.classList.contains('w-10')) {
                        icon.src = localStorage.getItem('userPicUrl');
                    }'''
            good_js_2 = '''if(icon.classList.contains('w-10')) {
                        let newSrc = localStorage.getItem('userPicUrl');
                        if(icon.src !== newSrc) { icon.src = newSrc; }
                    }'''
            if bad_js_2 in content:
                content = content.replace(bad_js_2, good_js_2)
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Fixed core bugs in: {f}")
