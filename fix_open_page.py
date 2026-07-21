import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace("fun openSidebarPage(type: String) {", "fun openSidebarPage(handleId: String, type: String) {")
content = content.replace('showSidebar("sidebar")', 'showSidebar(handleId)')

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/service/TriggerHandleView.kt", "r") as f:
    content = f.read()

content = content.replace(
    'FloatingReaderService.instance?.openSidebarPage(pageType)',
    'FloatingReaderService.instance?.openSidebarPage(handleId, pageType)'
)

with open("app/src/main/java/com/example/service/TriggerHandleView.kt", "w") as f:
    f.write(content)
