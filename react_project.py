# react_project.py

import os
import subprocess

def setup(project_name, open_editor):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    project_path = os.path.join(desktop_path, project_name)

    # Ensure the project directory exists
    os.makedirs(project_path, exist_ok=True)

    # Create React app
    subprocess.run(["npx", "create-react-app", project_name], cwd=desktop_path)
    print(f"React.js project '{project_name}' created successfully at {project_path}.")

    if open_editor:
        # Open in VS Code
        subprocess.run(["code", project_path])

        # Start the React app using VS Code terminal
        vscode_terminal_command = f'''
        -c "cd {project_path} && npm start"
        '''
        subprocess.run(["osascript", "-e", f'tell app "Visual Studio Code" to activate {vscode_terminal_command}'])
        subprocess.run(["npm", "install"])  # Ensure dependencies are installed
        subprocess.run(["npm", "start"])