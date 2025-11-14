

import os
os.chdir(r'C:\Users\patty\OfficeAgents_new\OfficeAgents')
print(f"Working directory: {os.getcwd()}")
from datetime import datetime

def run_notebook_with_env(env_name, notebook_path, execute=True):
    """
    Run a Jupyter notebook with a specific conda environment
    
    Args:
        env_name: Name of conda environment (e.g., 'lerobo')
        notebook_path: Full path to notebook
        execute: If True, execute and save. If False, open in browser
    """
    
    # Change to notebook directory
    notebook_dir = os.path.dirname(notebook_path)
    notebook_file = os.path.basename(notebook_path)
    import subprocess
impo
    if execute:
        # Execute notebook without opening UI
        print(f"Executing {notebook_file} with {env_name} environment...")
        
        output_file = notebook_path.replace('.ipynb', f'_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.ipynb')
        
        result = subprocess.run([
            'conda', 'run', '-n', env_name,
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--ExecutePreprocessor.timeout=600',  # Jupyter timeout (10 minutes)
            '--output', output_file,
            notebook_path
       ], shell=True, capture_output=True, text=True, timeout=660)  # subprocess timeout (11 minutes)
        
        if result.returncode == 0:
            print(f"✅ Success! Output saved to: {output_file}")
        else:
            print(f"❌ Error: {result.stderr}")
            
    else:
        # Open notebook in browser
        print(f"Opening {notebook_file} with {env_name} environment...")
        
        subprocess.Popen([
            'conda', 'run', '-n', env_name,
            'jupyter', 'notebook',
            notebook_path
        ], shell=True, cwd=notebook_dir)
        
        print("✅ Jupyter Notebook opened in browser")