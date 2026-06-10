import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"
dashboard_path = os.path.join(base_dir, "dashboard_copropietario", "code.html")

# Read the source of truth
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard_html = f.head = f.read()

# EXTRACT COMPONENTS FROM DASHBOARD
# 1. Configs and styles inside <head>
head_match = re.search(r'(<script src="https://cdn.tailwindcss.com.*?</style>)', dashboard_html, re.DOTALL)
if not head_match:
    print("Could not find head config in dashboard.")
    exit(1)
head_config = head_match.group(1)

# 2. Body class
body_match = re.search(r'<body class="([^"]+)">', dashboard_html)
body_class = body_match.group(1) if body_match else "bg-surface text-on-surface"

# 3. Sidebar NavBar
sidebar_match = re.search(r'(<!-- SideNavBar \(Shared Component\) -->.*?</aside>)', dashboard_html, re.DOTALL)
# It's possible some don't have the exact comment, so we fallback to finding the <aside>
if not sidebar_match:
    sidebar_match = re.search(r'(<aside.*?</aside>)', dashboard_html, re.DOTALL)
sidebar_html = sidebar_match.group(1)

# 4. Top NavBar
header_match = re.search(r'(<!-- TopNavBar \(Shared Component\) -->.*?</header>)', dashboard_html, re.DOTALL)
if not header_match:
    header_match = re.search(r'(<header.*?</header>)', dashboard_html, re.DOTALL)
header_html = header_match.group(1)


# Iterate over all html files
html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    if filepath == dashboard_path or 'inicio_de_sesi_n' in filepath:
        continue # Skip the template itself and login pages
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Replace head configs
    # We find what's between <meta name="viewport"...> and </head> or similar.
    # A safe way is to replace everything from <script src="https://cdn.tailwindcss.com to </style>
    content = re.sub(r'<script src="https://cdn\.tailwindcss\.com.*?</style>', head_config, content, flags=re.DOTALL)
    
    # 2. Update body class
    content = re.sub(r'<body class="[^"]*">', f'<body class="{body_class}">', content)
    
    # 3. Replace Sidebar
    content = re.sub(r'(<!-- SideNavBar \(Shared Component\) -->.*?</aside>|<aside.*?</aside>)', sidebar_html, content, flags=re.DOTALL)

    # 4. Replace Header
    content = re.sub(r'(<!-- TopNavBar \(Shared Component\) -->.*?</header>|<header.*?</header>)', header_html, content, flags=re.DOTALL)

    # Note: JavaScript sliding menu is at the bottom, before </body>. It should remain untouched.

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Sincronizado {filepath}")
    else:
        print(f"Sin cambios {filepath}")

print("Sincronización de tema y estructura completada.")
