import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """            val intent = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
                data.getParcelableExtra(Intent.EXTRA_SHORTCUT_INTENT, Intent::class.java)
            } else {
                @Suppress("DEPRECATION")
                data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            }"""

replacement = """            @Suppress("DEPRECATION")
            var intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            if (intent == null) {
                // Some apps might return the intent directly as the data
                intent = data
            }"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
