with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# We want to replace the part that starts SidebarService with SettingsActivity for non-first launches
old_block = """        if (!firstLaunch && Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
            val svcIntent = Intent(this@MainActivity, com.example.service.SidebarService::class.java).apply {
                putExtra("OPEN_FROM_LAUNCHER", true)
            }
            androidx.core.content.ContextCompat.startForegroundService(this, svcIntent)
            finish()
            return
        }"""

new_block = """        if (!firstLaunch && Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
            val settingsIntent = Intent(this@MainActivity, SettingsActivity::class.java)
            startActivity(settingsIntent)
            finish()
            return
        }"""

content = content.replace(old_block, new_block)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
