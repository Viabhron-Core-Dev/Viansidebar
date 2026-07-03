import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace('The adapter calls currentFolderPopup?.dismiss()\n                        onCloseSidebar() which closes the sidebar.', 'The adapter calls onCloseSidebar() which closes the sidebar.')
content = content.replace('Wait, currentFolderPopup?.dismiss()\n                        onCloseSidebar() is fine.', 'Wait, onCloseSidebar() is fine.')

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

print("Fixed comments.")
