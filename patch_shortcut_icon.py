import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """            if (intent == null) {
                // Some apps might return the intent directly as the data
                intent = Intent(data).apply {
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON)
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE)
                    removeExtra(Intent.EXTRA_SHORTCUT_NAME)
                }
            }"""

replacement = """            val iconBitmap = data.getParcelableExtra<android.graphics.Bitmap>(Intent.EXTRA_SHORTCUT_ICON)
            
            if (intent == null) {
                // Some apps might return the intent directly as the data
                intent = Intent(data).apply {
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON)
                    removeExtra(Intent.EXTRA_SHORTCUT_ICON_RESOURCE)
                    removeExtra(Intent.EXTRA_SHORTCUT_NAME)
                }
            }
            
            // Save the icon to a file if it exists
            var iconPath = ""
            if (iconBitmap != null) {
                try {
                    val file = java.io.File(filesDir, "shortcut_icon_${System.currentTimeMillis()}.png")
                    java.io.FileOutputStream(file).use { out ->
                        iconBitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, out)
                    }
                    iconPath = file.absolutePath
                } catch(e: Exception) {}
            }"""

target2 = """                val id = "intent:$encodedLabel:$encodedUri\""""
replacement2 = """                val id = if (iconPath.isNotEmpty()) {
                    "intent:$encodedLabel:$encodedUri:$iconPath"
                } else {
                    "intent:$encodedLabel:$encodedUri"
                }"""

content = content.replace(target, replacement)
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
