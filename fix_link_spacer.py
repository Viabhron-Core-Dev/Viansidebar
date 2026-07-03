import re
with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_link_class = """    data class Link(
        val uuid: String,
        val url: String,
        override val label: String
    ) : SidebarItem() {
        override var id = "link:$uuid"
    }"""
new_link_class = """    data class Link(
        val uuid: String,
        val url: String,
        override val label: String,
        override var id: String = "link:$uuid"
    ) : SidebarItem()"""
content = content.replace(old_link_class, new_link_class)

old_spacer_class = """    data class Spacer(
        val uuid: String,
        val heightDp: Int
    ) : SidebarItem() {
        override var id = "spacer:$uuid"
        override val label = "Spacer"
    }"""
new_spacer_class = """    data class Spacer(
        val uuid: String,
        val heightDp: Int,
        override var id: String = "spacer:$uuid"
    ) : SidebarItem() {
        override val label = "Spacer"
    }"""
content = content.replace(old_spacer_class, new_spacer_class)

# fix apply calls
content = content.replace("SidebarItem.Link(uuid, obj.getString(\"url\"), obj.getString(\"label\")).apply { this.id = id }", "SidebarItem.Link(uuid, obj.getString(\"url\"), obj.getString(\"label\"), id)")
content = content.replace("SidebarItem.Spacer(uuid, height).apply { this.id = id }", "SidebarItem.Spacer(uuid, height, id)")
content = content.replace("SidebarItem.Spacer(uuid, obj.getInt(\"heightDp\")).apply { this.id = id }", "SidebarItem.Spacer(uuid, obj.getInt(\"heightDp\"), id)")

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
