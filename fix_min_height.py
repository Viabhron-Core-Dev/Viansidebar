import re

with open('app/src/main/java/com/example/service/SidebarView.kt', 'r') as f:
    content = f.read()

content = content.replace('targetHeight = Math.max((150 * density), targetHeight)', 'targetHeight = Math.max((80 * density), targetHeight)')

with open('app/src/main/java/com/example/service/SidebarView.kt', 'w') as f:
    f.write(content)

