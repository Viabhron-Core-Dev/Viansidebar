import re

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'r') as f:
    content = f.read()

# Remove 'var pages' and 'var defaultIndex' from their current location
content = content.replace("    // Pages\n    var pages by remember { mutableStateOf(PageManager.getPages(prefs)) }\n    var defaultIndex by remember { mutableStateOf(PageManager.getDefaultPageIndex(prefs)) }\n", "")

# Insert them before the if (customisingPage != null) block
insert_point = "    if (customisingPage != null) {"
new_insert = """    // Pages
    var pages by remember { mutableStateOf(PageManager.getPages(prefs)) }
    var defaultIndex by remember { mutableStateOf(PageManager.getDefaultPageIndex(prefs)) }
    
    if (customisingPage != null) {"""
content = content.replace(insert_point, new_insert)

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'w') as f:
    f.write(content)
