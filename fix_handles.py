import re

# Edit HandlesListSettingsScreen.kt
with open('app/src/main/java/com/example/HandlesListSettingsScreen.kt', 'r') as f:
    content = f.read()

old_list = """    val handles = listOf(
        "sidebar" to "Sidebar Handle",
        "reader" to "Reader Handle"
    )"""

new_list = """    val handles = listOf(
        "sidebar" to "Sidebar Handle"
    )"""

content = content.replace(old_list, new_list)

with open('app/src/main/java/com/example/HandlesListSettingsScreen.kt', 'w') as f:
    f.write(content)

# Edit SettingsActivity.kt
with open('app/src/main/java/com/example/SettingsActivity.kt', 'r') as f:
    content = f.read()

old_state = '    var readerHandleEnabled by remember { mutableStateOf(prefs.getBoolean("reader_handle_enabled", false)) }'
content = content.replace(old_state, '')

old_ui = """                Divider()
                ListItem(
                    headlineContent = { Text("Reader Floating Handle") },
                    supportingContent = { Text("Show a dedicated handle to quickly open the reader") },
                    trailingContent = {
                        Switch(
                            checked = readerHandleEnabled,
                            onCheckedChange = { 
                                readerHandleEnabled = it
                                prefs.edit().putBoolean("reader_handle_enabled", it).apply()
                            }
                        )
                    }
                )"""
content = content.replace(old_ui, '')

with open('app/src/main/java/com/example/SettingsActivity.kt', 'w') as f:
    f.write(content)
