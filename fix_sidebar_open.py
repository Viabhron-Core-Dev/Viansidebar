import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

replacement = """
        }
        sidebarView?.goToPage(sidebarDefaultIndex)
        sidebarView?.attach()
    }
"""

content = content.replace('}\n        sidebarView?.attach()\n    }', replacement.strip() + '\n')

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)

print("Fixed FloatingReaderService showSidebar.")
