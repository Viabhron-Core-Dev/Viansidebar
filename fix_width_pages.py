import re

with open('app/src/main/java/com/example/service/SidebarView.kt', 'r') as f:
    content = f.read()

content = content.replace('"calculator", "compass", "notification", "scheduler", "reader" -> 180', '"calculator", "compass", "notification", "scheduler", "reader" -> 320')

with open('app/src/main/java/com/example/service/SidebarView.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/utils/PageManager.kt', 'r') as f:
    content = f.read()
content = content.replace('width = 180', 'width = 320')
with open('app/src/main/java/com/example/utils/PageManager.kt', 'w') as f:
    f.write(content)
