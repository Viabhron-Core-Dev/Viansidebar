import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """            @Suppress("DEPRECATION")
            var intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            if (intent == null) {
                // Some apps might return the intent directly as the data
                intent = data
            }
            val name = data.getStringExtra(Intent.EXTRA_SHORTCUT_NAME) ?: "Shortcut"
            
            android.util.Log.d("ShortcutPicker", "Got shortcut intent: $intent, name: $name")
            if (intent != null) {"""

replacement = """            @Suppress("DEPRECATION")
            var intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            val name = data.getStringExtra(Intent.EXTRA_SHORTCUT_NAME) ?: "Shortcut"
            
            if (intent == null) {
                // Some apps might return the intent directly as the data
                intent = Intent(data).apply {
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON)
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE)
                    removeExtra(Intent.EXTRA_SHORTCUT_NAME)
                }
            }
            
            com.example.LogKeeper.writeLog("ShortcutPicker", "Got shortcut intent: ${intent.toUri(0)}, name: $name")
            if (intent != null) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
