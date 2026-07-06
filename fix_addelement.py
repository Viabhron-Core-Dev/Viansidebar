import re

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'r') as f:
    content = f.read()

# ActionType
old_enum = """enum class ActionType {
    APP, SHORTCUT, FOLDER, LINK, EMPTY_ITEM, INTENT,
    SYSTEM, VOLUME, MEDIA, BRIGHTNESS, SCREEN_TIMEOUT, SCREEN_ORIENTATION, WIDGET, SETTINGS_SHORTCUT_HEADER, QUICK_TILES_HEADER,
    SPECIFIC_SYSTEM_ACTION, SPECIFIC_SETTINGS_SHORTCUT, SPECIFIC_QUICK_TILE
}"""

new_enum = """enum class ActionType {
    APP, SHORTCUT, FOLDER, LINK, EMPTY_ITEM, INTENT,
    SYSTEM, VOLUME, MEDIA, BRIGHTNESS, SCREEN_TIMEOUT, SCREEN_ORIENTATION, WIDGET, SETTINGS_SHORTCUT_HEADER, QUICK_TILES_HEADER, SCREEN_CAPTURE,
    SPECIFIC_SYSTEM_ACTION, SPECIFIC_SETTINGS_SHORTCUT, SPECIFIC_QUICK_TILE
}"""

content = content.replace(old_enum, new_enum)

# Mode
old_mode = """    enum class Mode {
        MAIN, SYSTEM_ACTIONS, VOLUME_ACTIONS, MEDIA_ACTIONS, DISPLAY_ACTIONS, SETTINGS_SHORTCUTS, QUICK_TILES
    }"""

new_mode = """    enum class Mode {
        MAIN, SYSTEM_ACTIONS, VOLUME_ACTIONS, MEDIA_ACTIONS, DISPLAY_ACTIONS, SETTINGS_SHORTCUTS, QUICK_TILES, SCREEN_CAPTURE_ACTIONS
    }"""

content = content.replace(old_mode, new_mode)

# Mode.MAIN items
old_main = """            items.add(AddElementItem.Action(android.R.drawable.ic_menu_preferences, "Android Settings Shortcut", "(${ALL_SETTINGS_SHORTCUTS.size})", ActionType.SETTINGS_SHORTCUT_HEADER))
            items.add(AddElementItem.Action(android.R.drawable.ic_menu_info_details, "System", "(${ALL_SYSTEM_ACTIONS.size})", ActionType.SYSTEM))
            items.add(AddElementItem.Action(android.R.drawable.ic_lock_silent_mode_off, "Volume", "(${ALL_VOLUME_ACTIONS.size})", ActionType.VOLUME))"""

new_main = """            items.add(AddElementItem.Action(android.R.drawable.ic_menu_preferences, "Android Settings Shortcut", "(${ALL_SETTINGS_SHORTCUTS.size})", ActionType.SETTINGS_SHORTCUT_HEADER))
            items.add(AddElementItem.Action(android.R.drawable.ic_menu_info_details, "System", "(${ALL_SYSTEM_ACTIONS.size})", ActionType.SYSTEM))
            items.add(AddElementItem.Action(android.R.drawable.ic_menu_camera, "Screen Capture", "(${ALL_SCREEN_CAPTURE_ACTIONS.size})", ActionType.SCREEN_CAPTURE))
            items.add(AddElementItem.Action(android.R.drawable.ic_lock_silent_mode_off, "Volume", "(${ALL_VOLUME_ACTIONS.size})", ActionType.VOLUME))"""

content = content.replace(old_main, new_main)

# loading loop
old_loop = """        } else if (currentMode == Mode.SYSTEM_ACTIONS) {
            items.add(AddElementItem.Header("System actions"))
            for (action in ALL_SYSTEM_ACTIONS) {
                items.add(AddElementItem.Action(action.iconResId, action.label, "", ActionType.SPECIFIC_SYSTEM_ACTION, action.id))
            }"""

new_loop = """        } else if (currentMode == Mode.SYSTEM_ACTIONS) {
            items.add(AddElementItem.Header("System actions"))
            for (action in ALL_SYSTEM_ACTIONS) {
                items.add(AddElementItem.Action(action.iconResId, action.label, "", ActionType.SPECIFIC_SYSTEM_ACTION, action.id))
            }
        } else if (currentMode == Mode.SCREEN_CAPTURE_ACTIONS) {
            items.add(AddElementItem.Header("Screen capture actions"))
            for (action in ALL_SCREEN_CAPTURE_ACTIONS) {
                items.add(AddElementItem.Action(action.iconResId, action.label, "", ActionType.SPECIFIC_SYSTEM_ACTION, action.id))
            }"""

content = content.replace(old_loop, new_loop)

# Action handler
old_handler = """            ActionType.SYSTEM -> {
                currentMode = Mode.SYSTEM_ACTIONS
                loadData()
                updateHeaderTitle("System")
            }"""

new_handler = """            ActionType.SYSTEM -> {
                currentMode = Mode.SYSTEM_ACTIONS
                loadData()
                updateHeaderTitle("System")
            }
            ActionType.SCREEN_CAPTURE -> {
                currentMode = Mode.SCREEN_CAPTURE_ACTIONS
                loadData()
                updateHeaderTitle("Screen Capture")
            }"""

content = content.replace(old_handler, new_handler)

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'w') as f:
    f.write(content)
