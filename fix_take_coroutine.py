import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace('for (it in item.items.take(4)) {', 'for (it in item.items.take(9)) {')

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

content = content.replace('for (it in item.items.take(4)) {', 'for (it in item.items.take(9)) {')

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)

print("Fixed take(4) to take(9) in coroutines.")
