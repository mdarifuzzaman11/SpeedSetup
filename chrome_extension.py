# chrome_extension.py

import os

def create_manifest_json(project_path, project_name):
    manifest_content = f"""{{
    "manifest_version": 2,
    "name": "{project_name}",
    "version": "1.0",
    "description": "Description here",
    "browser_action": {{
        "default_popup": "popup.html",
        "default_icon": "icon.png"
    }},
    "permissions": []
    }}"""

    manifest_path = os.path.join(project_path, 'manifest.json')
    with open(manifest_path, 'w') as file:
        file.write(manifest_content)

def setup(project_name, open_editor):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    project_path = os.path.join(desktop_path, project_name)

    # Ensure the project directory exists
    os.makedirs(project_path, exist_ok=True)
    
    # Set up the rest of the Chrome extension files
    create_manifest_json(project_path, project_name)
    # Create other necessary files for the extension
    open(os.path.join(project_path, 'popup.html'), 'w').close()
    open(os.path.join(project_path, 'popup.js'), 'w').close()
    open(os.path.join(project_path, 'background.js'), 'w').close()
    open(os.path.join(project_path, 'styles.css'), 'w').close()

    print(f"Chrome extension project '{project_name}' created successfully at {project_path}.")

    if open_editor:
        import subprocess
        subprocess.run(["code", project_path])
