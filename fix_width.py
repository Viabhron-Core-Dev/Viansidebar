import glob
import re

for filename in glob.glob('app/src/main/java/**/*.kt', recursive=True):
    with open(filename, 'r') as f:
        content = f.read()
    
    if '320' in content:
        content = content.replace('320', '180')
        with open(filename, 'w') as f:
            f.write(content)

with open('app/src/main/java/com/example/PageCustomizeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('200f..maxScreenWidth', '100f..maxScreenWidth')
content = content.replace('maxScreenWidth - 200f', 'maxScreenWidth - 100f')

with open('app/src/main/java/com/example/PageCustomizeScreen.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('200f..maxScreenWidth', '100f..maxScreenWidth')
content = content.replace('maxScreenWidth - 200f', 'maxScreenWidth - 100f')

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'w') as f:
    f.write(content)
