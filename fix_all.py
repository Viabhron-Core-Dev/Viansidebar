import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# 1. Remove the appended receiver code at the end
end_idx = content.find("private val iconUpdateReceiver = object : android.content.BroadcastReceiver()")
if end_idx != -1:
    content = content[:end_idx].rstrip() + "\n}\n"

# 2. Add UPDATE_SIDEBAR_ICONS to the existing receiver and handle it
target_receiver = """    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            loadWidgets()
        }
    }"""
    
replacement_receiver = """    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "com.example.UPDATE_SIDEBAR_ICONS") {
                val itemId = intent.getStringExtra("item_id")
                if (itemId != null) {
                    val manager = SidebarAppsManager(context!!)
                    manager.iconCache.remove("custom_$itemId")
                    manager.iconCache.remove(itemId)
                }
            }
            loadWidgets()
        }
    }"""
content = content.replace(target_receiver, replacement_receiver)

target_filter = """        filter.addAction("UPDATE_GRID")"""
replacement_filter = """        filter.addAction("UPDATE_GRID")
        filter.addAction("com.example.UPDATE_SIDEBAR_ICONS")"""
content = content.replace(target_filter, replacement_filter)


# 3. Replace SettingsShortcutHandler with inline intent logic
target_settings = """                                } else if (parsed is SidebarItem.SettingsShortcut) {
                                    try {
                                        SettingsShortcutHandler.handleSettingsShortcut(context, parsed.action)
                                    } catch (e: Exception) {}
                                }"""

replacement_settings = """                                } else if (parsed is SidebarItem.SettingsShortcut) {
                                    val settingsIntent = when (parsed.action) {
                                        "wifi" -> Intent(android.provider.Settings.ACTION_WIFI_SETTINGS)
                                        "bluetooth" -> Intent(android.provider.Settings.ACTION_BLUETOOTH_SETTINGS)
                                        "display" -> Intent(android.provider.Settings.ACTION_DISPLAY_SETTINGS)
                                        "sound" -> Intent(android.provider.Settings.ACTION_SOUND_SETTINGS)
                                        "location" -> Intent(android.provider.Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                                        "apps" -> Intent(android.provider.Settings.ACTION_APPLICATION_SETTINGS)
                                        "security" -> Intent(android.provider.Settings.ACTION_SECURITY_SETTINGS)
                                        "battery" -> Intent(android.provider.Settings.ACTION_BATTERY_SAVER_SETTINGS)
                                        "date" -> Intent(android.provider.Settings.ACTION_DATE_SETTINGS)
                                        else -> Intent(android.provider.Settings.ACTION_SETTINGS)
                                    }
                                    settingsIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                    try { context.startActivity(settingsIntent) } catch (e: Exception) {}
                                }"""

content = content.replace(target_settings, replacement_settings)

# There are two instances of target_settings (grid and folder popup). Replace both.
# But wait, the second one might use `popupWindow?.dismiss()`? No, it just dismisses popupWindow below it.
# Let's replace the one in folder popup explicitly.
target_settings_popup = """                    } else if (parsed is SidebarItem.SettingsShortcut) {
                        try {
                            SettingsShortcutHandler.handleSettingsShortcut(context, parsed.action)
                        } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    }"""

replacement_settings_popup = """                    } else if (parsed is SidebarItem.SettingsShortcut) {
                        val settingsIntent = when (parsed.action) {
                            "wifi" -> Intent(android.provider.Settings.ACTION_WIFI_SETTINGS)
                            "bluetooth" -> Intent(android.provider.Settings.ACTION_BLUETOOTH_SETTINGS)
                            "display" -> Intent(android.provider.Settings.ACTION_DISPLAY_SETTINGS)
                            "sound" -> Intent(android.provider.Settings.ACTION_SOUND_SETTINGS)
                            "location" -> Intent(android.provider.Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                            "apps" -> Intent(android.provider.Settings.ACTION_APPLICATION_SETTINGS)
                            "security" -> Intent(android.provider.Settings.ACTION_SECURITY_SETTINGS)
                            "battery" -> Intent(android.provider.Settings.ACTION_BATTERY_SAVER_SETTINGS)
                            "date" -> Intent(android.provider.Settings.ACTION_DATE_SETTINGS)
                            else -> Intent(android.provider.Settings.ACTION_SETTINGS)
                        }
                        settingsIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        try { context.startActivity(settingsIntent) } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    }"""

content = content.replace(target_settings_popup, replacement_settings_popup)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)

