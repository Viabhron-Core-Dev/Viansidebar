import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

# in onCreate, change rebuildSidebarPages(handleId) to rebuildSidebarPages("sidebar")
# Let's find exactly that line inside onCreate
lines = content.split('\n')
for i, line in enumerate(lines):
    if "rebuildSidebarPages(handleId)" in line and i < 400: # it's around 299
        lines[i] = line.replace("rebuildSidebarPages(handleId)", 'rebuildSidebarPages("sidebar")')

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write('\n'.join(lines))
