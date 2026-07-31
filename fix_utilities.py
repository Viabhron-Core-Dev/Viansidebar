import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Add auto_scroll to ALL_UTILITIES_ACTIONS
    content = re.sub(r'val ALL_UTILITIES_ACTIONS = listOf\(\n', 'val ALL_UTILITIES_ACTIONS = listOf(\n    SidebarItem.SystemAction("auto_scroll", "Auto Scroll", android.R.drawable.ic_menu_sort_by_size),\n', content)

    with open(path, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/service/SidebarAppsManager.kt')
