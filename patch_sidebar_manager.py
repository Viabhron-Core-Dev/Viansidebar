with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """            is SidebarItem.Link -> android.R.drawable.ic_menu_set_as"""
replacement = """            is SidebarItem.Link -> android.R.drawable.ic_menu_set_as
            is SidebarItem.Folder -> android.R.drawable.ic_menu_agenda"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
