import re
with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_folder_class = """    data class Folder(
        val uuid: String,
        val name: String,
        val colorHex: String,
        val items: List<String>,
        val folderStyle: Int = 0
    ) : SidebarItem() {
        override var id = "folder:$uuid"
        override val label = name
    }"""

new_folder_class = """    data class Folder(
        val uuid: String,
        val name: String,
        val colorHex: String,
        val items: List<String>,
        val folderStyle: Int = 0,
        override var id: String = "folder:$uuid"
    ) : SidebarItem() {
        override val label = name
    }"""
content = content.replace(old_folder_class, new_folder_class)

old_parse1 = """return SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle).apply { this.id = id }"""
new_parse1 = """return SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle, id)"""
content = content.replace(old_parse1, new_parse1)

old_parse2 = """result.add(SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle).apply { this.id = id })"""
new_parse2 = """result.add(SidebarItem.Folder(uuid, obj.getString("name"), obj.getString("colorHex"), itemsList, folderStyle, id))"""
content = content.replace(old_parse2, new_parse2)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
