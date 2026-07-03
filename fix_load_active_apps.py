import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# For Folder
old_folder_add = 'result.add(SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle))'
new_folder_add = 'result.add(SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle).apply { this.id = id })'
content = content.replace(old_folder_add, new_folder_add)

# For Link
old_link_add = 'result.add(SidebarItem.Link(uuid, obj.getString("url"), obj.getString("label")))'
new_link_add = 'result.add(SidebarItem.Link(uuid, obj.getString("url"), obj.getString("label")).apply { this.id = id })'
content = content.replace(old_link_add, new_link_add)

# For Spacer
old_spacer_add = 'result.add(SidebarItem.Spacer(uuid, obj.getInt("heightDp")))'
new_spacer_add = 'result.add(SidebarItem.Spacer(uuid, obj.getInt("heightDp")).apply { this.id = id })'
content = content.replace(old_spacer_add, new_spacer_add)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
