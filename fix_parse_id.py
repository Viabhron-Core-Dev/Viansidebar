import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# For Folder
old_folder_ret = 'return SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle)'
new_folder_ret = 'return SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle).apply { this.id = id }'
content = content.replace(old_folder_ret, new_folder_ret)

# For Link
old_link_ret = 'return SidebarItem.Link(uuid, obj.getString("url"), obj.getString("label"))'
new_link_ret = 'return SidebarItem.Link(uuid, obj.getString("url"), obj.getString("label")).apply { this.id = id }'
content = content.replace(old_link_ret, new_link_ret)

# For Spacer
old_spacer_ret = 'return SidebarItem.Spacer(uuid, height)'
new_spacer_ret = 'return SidebarItem.Spacer(uuid, height).apply { this.id = id }'
content = content.replace(old_spacer_ret, new_spacer_ret)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
