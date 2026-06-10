import glob

ROLE_SCRIPT = """
<!-- Ocultamiento dinámico de pantallas administrativas -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const role = localStorage.getItem('userRole') || 'COPROPIETARIO';
        if (role !== 'ADMIN') {
            const linksToHide = [
                'centro_de_votaciones_admin',
                'panel_de_administraci_n',
                'cargue_de_archivos'
            ];
            document.querySelectorAll('aside nav a').forEach(link => {
                const href = link.getAttribute('onclick') || link.getAttribute('href') || '';
                if (linksToHide.some(frag => href.includes(frag))) {
                    link.style.display = 'none';
                }
            });
        }
    });
</script>
</body>
"""

def inject():
    html_files = glob.glob('*/code.html')
    count = 0
    for file in html_files:
        # No tiene sentido inyectar en la página de login
        if "inicio_de_sesi_n" in file:
            continue 
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Ocultamiento dinámico de pantallas administrativas' in content:
            continue # ya fue inyectado
            
        if '</body>' in content:
            new_content = content.replace('</body>', ROLE_SCRIPT)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Inyectado en: {file}")
            
    print(f"Listo. Securización inyectada en {count} pantallas.")

if __name__ == '__main__':
    inject()
