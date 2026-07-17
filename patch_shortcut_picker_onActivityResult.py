import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        com.example.LogKeeper.writeLog("ShortcutPicker", "onActivityResult req=$requestCode res=$resultCode data=$data")
        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            try {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Starting config intent: ${data.toUri(0)}")
                startActivityForResult(data, 101)
            } catch (e: Exception) {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        } else if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {
            // Android gives us back the shortcut itself
            @Suppress("DEPRECATION")
            var intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            val name = data.getStringExtra(Intent.EXTRA_SHORTCUT_NAME) ?: "Shortcut"
            
            val iconBitmap = data.getParcelableExtra<android.graphics.Bitmap>(Intent.EXTRA_SHORTCUT_ICON)
            
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
            }
            
            com.example.LogKeeper.writeLog("ShortcutPicker", "Got shortcut intent: ${intent.toUri(0)}, name: $name")
            if (intent != null) {
                val uri = intent.toUri(0)
                val encodedLabel = URLEncoder.encode(name, "UTF-8")
                val encodedUri = URLEncoder.encode(uri, "UTF-8")
                val id = if (iconPath.isNotEmpty()) {
                    "intent:$encodedLabel:$encodedUri:$iconPath"
                } else {
                    "intent:$encodedLabel:$encodedUri"
                }
                
                val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
                setResult(Activity.RESULT_OK, resultIntent)
                finish()
                return
            } else {
                finish()
            }
        } else {
            // Cancelled or failed
            finish()
        }
        
        if (resultCode != Activity.RESULT_OK) {
            finish()
        }
    }"""

replacement = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        com.example.LogKeeper.writeLog("ShortcutPicker", "onActivityResult req=$requestCode res=$resultCode data=$data")
        
        if (resultCode != Activity.RESULT_OK) {
            finish()
            return
        }
        
        if (requestCode == 100 && data != null) {
            try {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Starting config intent: ${data.toUri(0)}")
                startActivityForResult(data, 101)
                // Do not finish here! Wait for requestCode 101
            } catch (e: Exception) {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        } else if (requestCode == 101 && data != null) {
            // Android gives us back the shortcut itself
            @Suppress("DEPRECATION")
            var intent = data.getParcelableExtra<Intent>(Intent.EXTRA_SHORTCUT_INTENT)
            val name = data.getStringExtra(Intent.EXTRA_SHORTCUT_NAME) ?: "Shortcut"
            
            val iconBitmap = data.getParcelableExtra<android.graphics.Bitmap>(Intent.EXTRA_SHORTCUT_ICON)
            
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
            }
            
            com.example.LogKeeper.writeLog("ShortcutPicker", "Got shortcut intent: ${intent?.toUri(0)}, name: $name")
            if (intent != null) {
                val uri = intent.toUri(0)
                val encodedLabel = URLEncoder.encode(name, "UTF-8")
                val encodedUri = URLEncoder.encode(uri, "UTF-8")
                val id = if (iconPath.isNotEmpty()) {
                    "intent:$encodedLabel:$encodedUri:$iconPath"
                } else {
                    "intent:$encodedLabel:$encodedUri"
                }
                
                val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
                setResult(Activity.RESULT_OK, resultIntent)
                finish()
            } else {
                finish()
            }
        } else {
            finish()
        }
    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
