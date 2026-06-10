import os
import re

base_dir = r"c:/Users/Andres Alvarado/Downloads/stitch_propiedad_transparente_gesti_n"

active_classes = "text-slate-900 dark:text-white font-bold border-r-4 border-slate-900 dark:border-white bg-white/50 dark:bg-slate-800/50"
inactive_classes = "text-slate-500 dark:text-slate-400 font-medium hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-200/50 dark:hover:bg-slate-800"

html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and 'inicio_de_sesi_n' not in root:
            html_files.append(os.path.join(root, f))

for filepath in html_files:
    folder_name = os.path.basename(os.path.dirname(filepath))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Reset all links in <nav> to inactive_classes
    # Find all <a class="..." blocks inside <nav> and replace the class string.
    # To be safe, we'll just replace the active_classes with inactive_classes globally in the navigation area
    
    # We can do this by regexing the <nav> block
    nav_match = re.search(r'<nav class="flex-1 space-y-1">(.*?)</nav>', content, re.DOTALL)
    if not nav_match:
        continue
        
    nav_content = nav_match.group(1)
    
    # Replace any active classes back to inactive
    nav_content = nav_content.replace(active_classes, inactive_classes)
    
    # 2. Find the link that corresponds to the current folder and make it active
    target_href = f"href=\"../{folder_name}/code.html\""
    
    # We find the <a> tag that contains this href, and replace its inactive_classes with active_classes
    # A simple regex to find the start of the <a> tag until the target_href
    def replace_active(match):
        a_tag = match.group(0)
        return a_tag.replace(inactive_classes, active_classes)

    # Use regex to find the full <a> tag that points to the current active page
    route_pattern = r'<a class="[^"]*" href="\.\./' + re.escape(folder_name) + r'/code\.html">'
    nav_content = re.sub(route_pattern, replace_active, nav_content)
    
    # Now replace the <nav> block back into content
    new_content = content[:nav_match.start(1)] + nav_content + content[nav_match.end(1):]
    
    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated active link for {folder_name}")
    else:
        print(f"No changes for {folder_name}")
