import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

# 1. FIX PROFILE PAGE BUGS & ADD FUNCTIONALITY
profile_file = os.path.join(base_dir, "administracion_de_perfil", "code.html")
if os.path.exists(profile_file):
    with open(profile_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Eliminar scripts estáticos que podrían estar causando el error visual o de "titileo"
    # como replace de innerText en renderDynamicState() que heredé del dashboard
    content = re.sub(
        r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*if\(localStorage\.getItem\(\'archivoCargado\'\).*?</script>',
        '', content, flags=re.DOTALL
    )

    # Reemplazar inputs estáticos y agregar ID's, remover animaciones locas que generen flicker
    content = content.replace(
        '<input type="text" value="Carlos Rodriguez" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">',
        '<input id="input-name" type="text" value="Carlos Rodriguez" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border-none focus:ring-2 focus:ring-primary-container text-sm font-bold text-slate-900 dark:text-white outline-none">'
    )
    content = content.replace(
        '<input type="email" value="carlos.rod@stitch.com" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">',
        '<input id="input-email" type="email" value="carlos.rod@stitch.com" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border-none focus:ring-2 focus:ring-primary-container text-sm font-bold text-slate-900 dark:text-white outline-none">'
    )
    content = content.replace(
        '<input type="tel" value="+57 320 445 9931" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">',
        '<input id="input-phone" type="tel" value="+57 320 445 9931" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border-none focus:ring-2 focus:ring-primary-container text-sm font-bold text-slate-900 dark:text-white outline-none">'
    )

    # Identificar la imagen para subir y el botón de confirmar
    content = content.replace(
        '<div class="absolute inset-0 bg-slate-900/60 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 backdrop-blur-[2px]">',
        '<div id="trigger-upload" class="absolute inset-0 bg-slate-900/60 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 backdrop-blur-[2px] cursor-pointer">'
    )
    content = content.replace('<img src="https://ui-avatars.com', '<img id="profile-pic-img" src="https://ui-avatars.com')
    content = content.replace('<h3 class="mt-6 font-extrabold text-slate-900 dark:text-white text-xl">Carlos', '<h3 id="display-name" class="mt-6 font-extrabold text-slate-900 dark:text-white text-xl">Carlos')
    content = content.replace('<button onclick="alert(\'Sistema', '<button id="btn-save-profile" class="bg-primary-container text-white px-8 py-3 rounded-full font-bold text-sm hover:opacity-90 transition-all shadow-xl hover:shadow-primary/40 flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">verified_user</span> Confirmar y Guardar Perfil</button>\n<input type="file" id="pic-upload" accept="image/*" class="hidden">\n<!-- Oculto para evitar parse errors --> <div class="hidden" onclick="alert(\'Sistema')

    # Inyectar script funcional de perfil antes del fin del body
    profile_script = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const nameInput = document.getElementById('input-name');
            const phoneInput = document.getElementById('input-phone');
            const emailInput = document.getElementById('input-email');
            const saveBtn = document.getElementById('btn-save-profile');
            const profilePicUrl = document.getElementById('profile-pic-img');
            const picUploader = document.getElementById('pic-upload');
            const triggerUpload = document.getElementById('trigger-upload');
            const bigName = document.getElementById('display-name');

            if(localStorage.getItem('userName') && nameInput) {
                nameInput.value = localStorage.getItem('userName');
                if(bigName) bigName.innerText = localStorage.getItem('userName');
            }
            if(localStorage.getItem('userPhone') && phoneInput) phoneInput.value = localStorage.getItem('userPhone');
            if(localStorage.getItem('userEmail') && emailInput) emailInput.value = localStorage.getItem('userEmail');
            if(localStorage.getItem('userPicUrl') && profilePicUrl) profilePicUrl.src = localStorage.getItem('userPicUrl');

            if(triggerUpload && picUploader) {
                triggerUpload.addEventListener('click', () => picUploader.click());
                picUploader.addEventListener('change', (e) => {
                    const file = e.target.files[0];
                    if(file) {
                        const reader = new FileReader();
                        reader.onload = (ev) => {
                            if(profilePicUrl) profilePicUrl.src = ev.target.result;
                            localStorage.setItem('userPicUrl', ev.target.result);
                        }
                        reader.readAsDataURL(file);
                    }
                });
            }

            if(saveBtn) {
                saveBtn.addEventListener('click', () => {
                    if(nameInput) localStorage.setItem('userName', nameInput.value);
                    if(phoneInput) localStorage.setItem('userPhone', phoneInput.value);
                    if(emailInput) localStorage.setItem('userEmail', emailInput.value);
                    if(bigName && nameInput) bigName.innerText = nameInput.value;
                    
                    // Actualizar el header de arriba instantaneamente si está en esta misma pantalla
                    document.querySelectorAll('.font-semibold.text-slate-900').forEach(el => {
                        el.innerText = localStorage.getItem('userName');
                    });
                    
                    // Disparar pequeño check de exito en pantalla (simulado rápido)
                    const tempAlert = document.createElement('div');
                    tempAlert.className = 'fixed bottom-10 inset-x-0 mx-auto w-max bg-green-600 text-white px-6 py-3 rounded-full font-bold shadow-2xl z-[100] transform transition-transform animate-bounce';
                    tempAlert.innerText = '¡Cambios Guardados!';
                    document.body.appendChild(tempAlert);
                    setTimeout(() => tempAlert.remove(), 3000);
                });
            }
        });
    </script>
    """
    content = content.replace("</body>", profile_script + "\n</body>")
    
    with open(profile_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("1. Perfil arreglado.")


# 2. FIX LAYOUT CENTERING GLOBALMENTE
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                htmltext = file.read()
                
            # Verificar si ya centramos para evitar envolver dos veces
            if 'id="layout-center-wrapper"' in htmltext:
                continue

            # Buscar la apertura del main, usualmente: <main class="...">
            match = re.search(r'<main[^>]*>', htmltext)
            if match:
                main_tag = match.group(0)
                
                # Si es asistent chat u otro que requiera altura, pasamos h-full
                inner_wrap = '<div id="layout-center-wrapper" class="w-full max-w-7xl mx-auto flex flex-col h-full">'
                
                # Reemplazar la etiqueta main original inyectando el wrapper adentro
                new_html = htmltext.replace(main_tag, main_tag + '\n' + inner_wrap)
                
                # Buscar el ultimo </main> para cerrarlo
                new_html = re.sub(r'</main>', '</div>\n</main>', new_html, count=1)
                
                if new_html != htmltext:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_html)

print("2. Interfaces centradas localmente.")
