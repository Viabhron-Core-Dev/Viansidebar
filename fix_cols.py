import re
import glob

for filename in glob.glob('app/src/main/java/**/*.kt', recursive=True):
    with open(filename, 'r') as f:
        content = f.read()
    
    if 'sidebar_columns' in content:
        content = content.replace('prefs.getInt("sidebar_columns", 4)', 'prefs.getInt("sidebar_columns", 3)')
        with open(filename, 'w') as f:
            f.write(content)

