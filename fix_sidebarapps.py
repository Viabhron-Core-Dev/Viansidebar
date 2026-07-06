import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_sys = """val ALL_SYSTEM_ACTIONS = listOf(
    SidebarItem.SystemAction("back", "Back", android.R.drawable.ic_menu_revert),
    SidebarItem.SystemAction("home", "Home", android.R.drawable.ic_menu_compass),
    SidebarItem.SystemAction("lock_screen", "Lock screen", android.R.drawable.ic_lock_power_off),
    SidebarItem.SystemAction("notifications", "Notifications", android.R.drawable.ic_menu_info_details),
    SidebarItem.SystemAction("quick_settings", "Quick settings", android.R.drawable.ic_menu_manage),
    SidebarItem.SystemAction("recents", "Recents", android.R.drawable.ic_menu_recent_history),
    SidebarItem.SystemAction("screenshot", "Screenshot", android.R.drawable.ic_menu_camera),
    SidebarItem.SystemAction("screen_record", "Screen Record", android.R.drawable.ic_media_play),
    SidebarItem.SystemAction("splitscreen", "Splitscreen", android.R.drawable.ic_menu_gallery),
    SidebarItem.SystemAction("log_keeper", "Log Keeper", android.R.drawable.ic_menu_agenda),
    SidebarItem.SystemAction("ebook_reader", "eBook Reader", com.example.R.drawable.ic_library_books),
    SidebarItem.SystemAction("settings", "Settings", android.R.drawable.ic_menu_preferences)
)"""

new_sys = """val ALL_SYSTEM_ACTIONS = listOf(
    SidebarItem.SystemAction("back", "Back", android.R.drawable.ic_menu_revert),
    SidebarItem.SystemAction("home", "Home", android.R.drawable.ic_menu_compass),
    SidebarItem.SystemAction("lock_screen", "Lock screen", android.R.drawable.ic_lock_power_off),
    SidebarItem.SystemAction("notifications", "Notifications", android.R.drawable.ic_menu_info_details),
    SidebarItem.SystemAction("quick_settings", "Quick settings", android.R.drawable.ic_menu_manage),
    SidebarItem.SystemAction("recents", "Recents", android.R.drawable.ic_menu_recent_history),
    SidebarItem.SystemAction("splitscreen", "Splitscreen", android.R.drawable.ic_menu_gallery),
    SidebarItem.SystemAction("log_keeper", "Log Keeper", android.R.drawable.ic_menu_agenda),
    SidebarItem.SystemAction("ebook_reader", "eBook Reader", com.example.R.drawable.ic_library_books),
    SidebarItem.SystemAction("settings", "Settings", android.R.drawable.ic_menu_preferences)
)

val ALL_SCREEN_CAPTURE_ACTIONS = listOf(
    SidebarItem.SystemAction("screenshot", "Screenshot", android.R.drawable.ic_menu_camera),
    SidebarItem.SystemAction("screen_record", "Screen Record", android.R.drawable.ic_media_play)
)"""

content = content.replace(old_sys, new_sys)

old_get_act = """        return ALL_SYSTEM_ACTIONS.find { it.action == id }
            ?: ALL_VOLUME_ACTIONS.find { it.action == id }
            ?: ALL_MEDIA_ACTIONS.find { it.action == id }
            ?: ALL_DISPLAY_ACTIONS.find { it.action == id }
            ?: ALL_SETTINGS_SHORTCUTS.find { it.id == id }
            ?: ALL_QUICK_TILES.find { it.id == id }"""

new_get_act = """        return ALL_SYSTEM_ACTIONS.find { it.action == id }
            ?: ALL_VOLUME_ACTIONS.find { it.action == id }
            ?: ALL_MEDIA_ACTIONS.find { it.action == id }
            ?: ALL_DISPLAY_ACTIONS.find { it.action == id }
            ?: ALL_SETTINGS_SHORTCUTS.find { it.id == id }
            ?: ALL_QUICK_TILES.find { it.id == id }
            ?: ALL_SCREEN_CAPTURE_ACTIONS.find { it.action == id }"""

content = content.replace(old_get_act, new_get_act)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
