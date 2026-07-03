with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

content = content.replace('override val id =', 'override var id =')
content = content.replace('abstract val id:', 'abstract var id:')

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
