import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# 1. Add data class QuickTile
old_class_marker = """    data class SettingsShortcut("""
new_class_marker = """    data class QuickTile(
        val action: String,
        override val label: String,
        val iconResId: Int
    ) : SidebarItem() {
        override var id = "quicktile:$action"
    }
    
    data class SettingsShortcut("""
content = content.replace(old_class_marker, new_class_marker)

# 2. Add ALL_QUICK_TILES
old_list_marker = """val ALL_SYSTEM_ACTIONS = listOf("""
new_list_marker = """val ALL_QUICK_TILES = listOf(
    SidebarItem.QuickTile("torch", "Torch", android.R.drawable.ic_menu_camera),
    SidebarItem.QuickTile("wifi", "Wi-Fi", android.R.drawable.ic_menu_search),
    SidebarItem.QuickTile("bluetooth", "Bluetooth", android.R.drawable.ic_menu_share),
    SidebarItem.QuickTile("airplane", "Airplane Mode", android.R.drawable.ic_dialog_alert),
    SidebarItem.QuickTile("dnd", "Do Not Disturb", android.R.drawable.ic_lock_silent_mode_off),
    SidebarItem.QuickTile("location", "Location", android.R.drawable.ic_menu_mylocation),
    SidebarItem.QuickTile("nfc", "NFC", android.R.drawable.ic_menu_sort_by_size),
    SidebarItem.QuickTile("data", "Mobile Data", android.R.drawable.ic_menu_sort_alphabetically)
)

val ALL_SYSTEM_ACTIONS = listOf("""
content = content.replace(old_list_marker, new_list_marker)

# 3. Add to loadIcon and getLabel
old_load_icon = """            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }"""
new_load_icon = """            val qTile = ALL_QUICK_TILES.find { it.action == action }
            if (qTile != null) {
                return getDrawableBitmap(context.resources.getDrawable(qTile.iconResId, context.theme))
            }
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }"""
content = content.replace(old_load_icon, new_load_icon)

old_get_label = """                val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }"""
new_get_label = """                val qTile = ALL_QUICK_TILES.find { it.action == action }
                if (qTile != null) return qTile.label
                val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }"""
content = content.replace(old_get_label, new_get_label)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
