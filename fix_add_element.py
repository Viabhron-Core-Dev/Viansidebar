import re

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'r') as f:
    content = f.read()

# 1. Update Mode Enum
old_mode = """    enum class Mode {
        MAIN, SYSTEM_ACTIONS, VOLUME_ACTIONS, MEDIA_ACTIONS, DISPLAY_ACTIONS, SETTINGS_SHORTCUTS
    }"""
new_mode = """    enum class Mode {
        MAIN, SYSTEM_ACTIONS, VOLUME_ACTIONS, MEDIA_ACTIONS, DISPLAY_ACTIONS, SETTINGS_SHORTCUTS, QUICK_TILES
    }"""
content = content.replace(old_mode, new_mode)

# 2. Add QUICK_TILES ActionType
old_action_type = """    SYSTEM, VOLUME, MEDIA, BRIGHTNESS, SCREEN_TIMEOUT, SCREEN_ORIENTATION, WIDGET, SETTINGS_SHORTCUT_HEADER,
    SPECIFIC_SYSTEM_ACTION, SPECIFIC_SETTINGS_SHORTCUT"""
new_action_type = """    SYSTEM, VOLUME, MEDIA, BRIGHTNESS, SCREEN_TIMEOUT, SCREEN_ORIENTATION, WIDGET, SETTINGS_SHORTCUT_HEADER, QUICK_TILES_HEADER,
    SPECIFIC_SYSTEM_ACTION, SPECIFIC_SETTINGS_SHORTCUT, SPECIFIC_QUICK_TILE"""
content = content.replace(old_action_type, new_action_type)

# 3. Add Quick Tiles row in MAIN mode
old_android_actions = """            // Android actions
            items.add(AddElementItem.Header("Android actions"))"""
new_android_actions = """            // Android actions
            items.add(AddElementItem.Header("Android actions"))
            items.add(AddElementItem.Action(android.R.drawable.ic_menu_preferences, "System Quick Tiles", "(${ALL_QUICK_TILES.size})", ActionType.QUICK_TILES_HEADER))"""
content = content.replace(old_android_actions, new_android_actions)

# 4. Add items in QUICK_TILES mode
old_mode_if = """        } else if (currentMode == Mode.SETTINGS_SHORTCUTS) {"""
new_mode_if = """        } else if (currentMode == Mode.QUICK_TILES) {
            items.add(AddElementItem.Header("Quick Tiles"))
            for (action in ALL_QUICK_TILES) {
                items.add(AddElementItem.Action(action.iconResId, action.label, "", ActionType.SPECIFIC_QUICK_TILE, action.id))
            }
        } else if (currentMode == Mode.SETTINGS_SHORTCUTS) {"""
content = content.replace(old_mode_if, new_mode_if)

# 5. Handle clicks for QUICK_TILES_HEADER and SPECIFIC_QUICK_TILE
old_click = """            ActionType.SYSTEM -> {
                currentMode = Mode.SYSTEM_ACTIONS
                loadData()
                updateHeaderTitle("System")
            }"""
new_click = """            ActionType.QUICK_TILES_HEADER -> {
                currentMode = Mode.QUICK_TILES
                loadData()
                updateHeaderTitle("Quick Tiles")
            }
            ActionType.SPECIFIC_QUICK_TILE -> {
                addSidebarItem(item.id)
                close()
            }
            ActionType.SYSTEM -> {
                currentMode = Mode.SYSTEM_ACTIONS
                loadData()
                updateHeaderTitle("System")
            }"""
content = content.replace(old_click, new_click)

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'w') as f:
    f.write(content)
