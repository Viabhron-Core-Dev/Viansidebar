import sys
import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """                    p = AppsPageView(this, config, appsManager, serviceScope,
                        onHeightChanged = { newHeight ->"""

replacement = """                    p = AppsPageView(this, config, appsManager, serviceScope,
                        onCloseSidebar = { closeSidebar() },
                        onHeightChanged = { newHeight ->"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
