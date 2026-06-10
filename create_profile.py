import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"
reference_file = os.path.join(base_dir, "dashboard_copropietario", "code.html")
target_folder = os.path.join(base_dir, "administracion_de_perfil")
target_file = os.path.join(target_folder, "code.html")

# Create folder if not exists
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

with open(reference_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar el bloque original de <main>...</main>
# Para no fallar por saltos de línea, usamos re.DOTALL
match = re.search(r'<main.*?</main>', content, re.DOTALL)

if match:
    original_main = match.group(0)
    
    new_main_content = """<main class="flex-1 lg:ml-64 lg:w-[calc(100%-16rem)] p-4 lg:p-8 ml-0 transition-all duration-300">
    <div class="max-w-5xl mx-auto space-y-8 mt-16 lg:mt-0">
        
        <!-- Header -->
        <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
                <h2 class="text-3xl font-extrabold text-primary tracking-tight">Mi Perfil Integrado</h2>
                <p class="text-on-surface-variant mt-2 text-sm">Administra tu información personal, opciones de seguridad y preferencias del ecosistema Stitch.</p>
            </div>
            <!-- Quick Alert for Auth Method -->
            <div class="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 px-4 py-2.5 rounded-lg border border-green-200 dark:border-green-800/30 flex items-center gap-2 text-xs font-bold tracking-wide">
                <span class="material-symbols-outlined text-[16px]">verified</span> AUTENTICACIÓN VERIFICADA
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-8">
            <!-- Left Panel (Photo & Oauth) -->
            <div class="col-span-1 md:col-span-4 space-y-6">
                <!-- Avatar Layout -->
                <div class="bg-surface-container-lowest p-8 rounded-3xl border border-outline-variant/10 text-center relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
                    <div class="w-32 h-32 mx-auto rounded-full bg-surface-container border-4 border-white dark:border-slate-800 shadow-xl overflow-hidden relative cursor-pointer ring-4 ring-primary-container/10">
                        <img src="https://ui-avatars.com/api/?name=Carlos+Rodriguez&background=00174b&color=fff&size=200" alt="Profile" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-slate-900/60 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 backdrop-blur-[2px]">
                            <span class="material-symbols-outlined text-white mb-1 animate-bounce">upload</span>
                            <span class="text-[10px] uppercase font-bold text-white tracking-widest">Cambiar</span>
                        </div>
                    </div>
                    <h3 class="mt-6 font-extrabold text-slate-900 dark:text-white text-xl">Carlos Rodríguez</h3>
                    <div class="mt-2 inline-block px-3 py-1 bg-primary-container/10 text-primary-container rounded-full text-xs font-bold tracking-widest uppercase">Copropietario</div>
                    
                    <div class="mt-8 pt-8 border-t border-outline-variant/20 space-y-4 text-left">
                        <div class="flex items-center gap-4 text-sm">
                            <div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0">
                                <span class="material-symbols-outlined text-slate-500 text-[18px]">domain</span>
                            </div>
                            <div>
                                <p class="font-bold text-slate-900 dark:text-slate-100">Apto 402</p>
                                <p class="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Torre Vista Central</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-4 text-sm">
                            <div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0">
                                <span class="material-symbols-outlined text-slate-500 text-[18px]">shield_person</span>
                            </div>
                            <div>
                                <p class="font-bold text-slate-900 dark:text-slate-100">Acceso Estándar</p>
                                <p class="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Permisos del Sistema</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Conexiones OAuth Tablas de la BD -->
                <div class="bg-surface-container-lowest p-6 rounded-3xl border border-outline-variant/10 space-y-4 shadow-sm">
                    <h4 class="font-bold text-xs tracking-widest text-on-surface-variant uppercase mb-6 flex items-center gap-2"><span class="material-symbols-outlined text-[16px]">api</span> Cuentas API Vinculadas</h4>
                    
                    <button class="w-full flex items-center justify-between py-3 px-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 cursor-default">
                        <div class="flex items-center gap-3">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" alt="Google" class="w-5 h-5">
                            <span class="text-sm font-bold text-slate-700 dark:text-slate-200">Google Workspace</span>
                        </div>
                        <span class="material-symbols-outlined text-green-500 text-[18px]">check_circle</span>
                    </button>
                    
                    <button class="w-full flex items-center justify-between py-3 px-4 rounded-xl border-2 border-dashed border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors group">
                        <div class="flex items-center gap-3 opacity-60 group-hover:opacity-100 transition-opacity">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg" alt="MS" class="w-5 h-5">
                            <span class="text-sm font-bold text-slate-600 dark:text-slate-300">Conectar Microsoft</span>
                        </div>
                        <span class="material-symbols-outlined text-slate-400 group-hover:text-primary transition-colors text-[18px]">add</span>
                    </button>
                </div>
            </div>

            <!-- Right Panel (Forms - Coincidiendo con BD Relacional) -->
            <div class="col-span-1 md:col-span-8 space-y-6">
                
                <!-- Personal Info -->
                <div class="bg-surface-container-lowest p-8 rounded-3xl border border-outline-variant/10 shadow-sm relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1 h-full bg-primary-container"></div>
                    <h3 class="text-lg font-bold mb-8 flex items-center gap-2"><span class="material-symbols-outlined text-primary-container">person</span> Datos Oficiales del Usuario</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-8">
                        <div class="space-y-2">
                            <label class="text-[10px] font-bold text-primary-container uppercase tracking-widest pl-1">Nombre Completo</label>
                            <input type="text" value="Carlos Rodriguez" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-bold text-primary-container uppercase tracking-widest pl-1">Documento de Identidad (ID)</label>
                            <div class="relative">
                                <input type="text" value="1.144.598.665" class="w-full bg-slate-100 dark:bg-slate-900/50 text-slate-500 px-4 py-3.5 rounded-xl border-none text-sm font-bold focus:outline-none" readonly>
                                <span class="material-symbols-outlined absolute right-4 top-3.5 text-slate-400 text-[18px]">lock</span>
                            </div>
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-bold text-primary-container uppercase tracking-widest pl-1">Correo Electrónico (Login)</label>
                            <input type="email" value="carlos.rod@stitch.com" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-bold text-primary-container uppercase tracking-widest pl-1">Teléfono / WhatsApp Móvil</label>
                            <input type="tel" value="+57 320 445 9931" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                        </div>
                        <div class="space-y-2 sm:col-span-2">
                            <label class="text-[10px] font-bold text-primary-container uppercase tracking-widest pl-1">Contacto de Emergencia</label>
                            <input type="text" placeholder="Ej: Maria Rodriguez - +57 300 000 0000" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-primary-container focus:ring-4 focus:ring-primary-container/10 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                        </div>
                    </div>
                </div>

                <!-- Security Info -->
                <div class="bg-surface-container-lowest p-8 rounded-3xl border border-outline-variant/10 shadow-sm relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1 h-full bg-slate-300 dark:bg-slate-700"></div>
                    <h3 class="text-lg font-bold mb-8 flex items-center gap-2"><span class="material-symbols-outlined text-slate-700 dark:text-slate-300">key</span> Control de Acceso (Contraseña)</h3>
                    
                    <div class="bg-blue-50 dark:bg-blue-900/10 rounded-xl p-4 mb-8 flex items-start gap-3 border border-blue-100 dark:border-blue-900/30">
                        <span class="material-symbols-outlined text-blue-600 dark:text-blue-400 mt-0.5">info</span>
                        <div>
                            <h4 class="text-sm font-bold text-blue-900 dark:text-blue-300">Inicio de Sesión Alternativo</h4>
                            <p class="text-xs text-blue-700 dark:text-blue-400 mt-1">Has activado tu login híbrido vía Google OAuth. Si deseas ingresar utilizando correo + contraseña de forma clásica, asegúrate de renovar tu llave aquí abajo.</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 gap-8">
                        <div class="space-y-2 max-w-sm">
                            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-1">Contraseña Actual</label>
                            <input type="password" placeholder="••••••••••••" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-slate-400 focus:ring-4 focus:ring-slate-200 dark:focus:ring-slate-700 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-6 border-t border-slate-100 dark:border-slate-800">
                            <div class="space-y-2">
                                <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-1">Crear Nueva Contraseña</label>
                                <input type="password" placeholder="Mínimo 8 caracteres" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-slate-400 focus:ring-4 focus:ring-slate-200 dark:focus:ring-slate-700 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                            </div>
                            <div class="space-y-2">
                                <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest pl-1">Verificar Nueva Contraseña</label>
                                <input type="password" placeholder="Confirmación idéntica" class="w-full bg-surface-container px-4 py-3.5 rounded-xl border border-transparent focus:border-slate-400 focus:ring-4 focus:ring-slate-200 dark:focus:ring-slate-700 text-sm font-bold text-slate-900 dark:text-white transition-all outline-none">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-end gap-4 pt-6">
                    <button class="px-6 py-3 rounded-full font-bold text-sm text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">Descartar</button>
                    <button onclick="alert('Sistema conectado:\\nTodos tus datos y metadatos han sido validados e inyectados en la Base de Datos Relacional y guardados en tu historial de operaciones NoSQL.')" class="bg-primary-container text-white px-8 py-3 rounded-full font-bold text-sm hover:opacity-90 hover:-translate-y-0.5 transition-all shadow-xl hover:shadow-primary/40 flex items-center gap-2">
                        <span class="material-symbols-outlined text-[18px]">verified_user</span> Confirmar y Guardar Perfil
                    </button>
                </div>

            </div>
        </div>
    </div>
</main>"""

    new_content = content.replace(original_main, new_main_content)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Página de perfil creada éxitosamente en {target_file}")
else:
    print("No se encontró la etiqueta main en el archivo base.")
