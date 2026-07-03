import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

bad_pattern = r'\} else if \(item is SidebarItem\.Folder\) \{\s*icon\.setImageDrawable\(null\).*?\} else if \(item is SidebarItem\.Link\) \{\s*\} else if \(item is SidebarItem\.Link\) \{'

good_replacement = """} else if (item is SidebarItem.Folder) {
                    showFolderPopup(itemView, item)
                } else if (item is SidebarItem.Link) {"""

content = re.sub(bad_pattern, good_replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

print("Fixed the bug in AppsPageView.")
