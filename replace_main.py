import os
import re

target_file = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n/cargue_de_archivos/code.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

new_main = """<!-- Main Content Canvas -->
<main class="ml-64 pt-24 pb-12 px-8 min-h-screen bg-surface">
    <!-- Welcome Header -->
    <div class="mb-10">
        <h1 class="text-4xl font-extrabold text-primary tracking-tight mb-2">Cargue de Archivos</h1>
        <p class="text-on-surface-variant max-w-lg">Sube documentos de gestión, reportes contables (Excel/CSV) o facturas. Los datos impactarán automáticamente al sistema localmente para visualización.</p>
    </div>

    <!-- Drag & Drop Uploader -->
    <div class="bg-surface-container-lowest p-8 md:p-12 rounded-2xl shadow-sm border border-outline-variant/30 max-w-4xl mx-auto mt-10">
        <div id="drop-zone" class="w-full border-2 border-dashed border-primary-fixed-dim/80 hover:border-primary-container bg-surface-container-low/30 hover:bg-surface-container-low transition-all duration-300 rounded-xl p-12 text-center cursor-pointer flex flex-col items-center justify-center gap-4">
            <div class="w-20 h-20 bg-primary-container rounded-full flex items-center justify-center shadow-lg mb-2">
                <span class="material-symbols-outlined text-white text-4xl">cloud_upload</span>
            </div>
            <h3 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Selecciona o arrastra tu archivo aquí</h3>
            <p class="text-sm font-medium text-on-surface-variant">Formatos soportados: Excel (.xlsx, .csv), PDF, Imágenes (JPEG, PNG)</p>
            
            <input type="file" id="file-input" class="hidden" accept=".xlsx,.csv,.pdf,.jpg,.jpeg,.png">
            <button onclick="document.getElementById('file-input').click()" class="mt-4 bg-primary text-on-primary px-8 py-3 rounded-full font-bold hover:opacity-90 transition-all shadow-md active:scale-95">
                Explorar Archivos
            </button>
        </div>

        <!-- Uploading Status (Initially Hidden) -->
        <div id="upload-status" class="hidden mt-8">
            <div class="flex items-center gap-4 mb-2">
                <span class="material-symbols-outlined text-primary animate-spin">sync</span>
                <span class="font-bold text-slate-900 dark:text-white" id="file-name-display">Procesando archivo...</span>
            </div>
            <div class="w-full bg-surface-container h-2.5 rounded-full overflow-hidden relative">
                <div id="progress-bar" class="bg-primary h-full rounded-full w-0 transition-all duration-700 ease-out"></div>
            </div>
            <p class="text-xs text-on-surface-variant mt-2 text-right" id="progress-text">0% Completado</p>
        </div>

        <!-- Success Message (Initially Hidden) -->
        <div id="success-message" class="hidden mt-8 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 p-6 rounded-xl flex flex-col sm:flex-row items-start gap-4">
            <span class="material-symbols-outlined text-green-600 dark:text-green-400 text-3xl">check_circle</span>
            <div>
                <h4 class="text-lg font-bold text-slate-900 dark:text-white tracking-tight">¡Archivo procesado con éxito!</h4>
                <p class="text-sm text-on-surface-variant mt-1">Se han actualizado los registros contables. El balance en pantalla cambiará a <strong class="text-green-700 dark:text-green-300">$437,450.00 MXN</strong> y la métrica de solvencia se ha optimizado al <strong class="text-green-700 dark:text-green-300">98.5%</strong>.</p>
                <button onclick="verCambios()" class="mt-4 text-sm font-bold text-primary hover:underline flex items-center gap-1 group">
                    Ver el impacto en el Dashboard <span class="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                </button>
            </div>
        </div>
    </div>
</main>

<script>
    // Script de Interacción de Subida de Archivos
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');
    const successMsg = document.getElementById('success-message');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const fileNameDisplay = document.getElementById('file-name-display');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-primary-container', 'bg-surface-container-low', 'scale-[1.01]');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-primary-container', 'bg-surface-container-low', 'scale-[1.01]');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-primary-container', 'bg-surface-container-low', 'scale-[1.01]');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        dropZone.classList.add('hidden');
        uploadStatus.classList.remove('hidden');
        fileNameDisplay.innerText = "Sincronizando " + file.name + "...";

        // Simulación de subida fluida
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.floor(Math.random() * 25) + 5;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                
                setTimeout(() => {
                    uploadStatus.classList.add('hidden');
                    successMsg.classList.remove('hidden');
                    
                    // ALMACENAR DATOS GLOBALES
                    localStorage.setItem('archivoCargado', 'true');
                    localStorage.setItem('nuevoBalance', '$437,450.00'); // Balance simulado post-excel
                    localStorage.setItem('nuevaSolvencia', '98.5%'); // Solvencia simulada
                }, 600);
            }
            progressBar.style.width = progress + '%';
            progressText.innerText = progress + '% Completado';
        }, 350);
    }

    function verCambios() {
        window.location.href = '../dashboard_copropietario/code.html';
    }
</script>
"""

# Replace anything from <!-- Main Content Canvas --> up to <!-- Menú Deslizante JS -->
content = re.sub(r'<!-- Main Content Canvas -->.*?<!-- Menú Deslizante JS -->', new_main + '\n<!-- Menú Deslizante JS -->', content, flags=re.DOTALL)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)
