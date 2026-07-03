import re

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    content = content.replace('}.take(4)', '}')

    with open(filename, 'w') as f:
        f.write(content)

process_file('app/src/main/java/com/example/service/AppsPageView.kt')
process_file('app/src/main/java/com/example/service/SidebarEditOverlayView.kt')
process_file('app/src/main/java/com/example/service/FolderStyleDialog.kt')

print("Fixed take(4)")
