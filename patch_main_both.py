with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_block = """        if (!firstLaunch && Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
            val settingsIntent = Intent(this@MainActivity, SettingsActivity::class.java)
            startActivity(settingsIntent)
            finish()
            return
        }"""

new_block = """        if (!firstLaunch && Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
            val svcIntent = Intent(this@MainActivity, com.example.service.SidebarService::class.java).apply {
                putExtra("OPEN_FROM_LAUNCHER", true)
            }
            androidx.core.content.ContextCompat.startForegroundService(this, svcIntent)
            val settingsIntent = Intent(this@MainActivity, SettingsActivity::class.java)
            startActivity(settingsIntent)
            finish()
            return
        }"""

content = content.replace(old_block, new_block)

# Also start it after WelcomeScreen
old_welcome = """                            prefs.edit().putBoolean("first_launch", false).apply()
                            val settingsIntent = Intent(this@MainActivity, SettingsActivity::class.java)
                            startActivity(settingsIntent)
                            finish()"""

new_welcome = """                            prefs.edit().putBoolean("first_launch", false).apply()
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this@MainActivity)) {
                                val svcIntent = Intent(this@MainActivity, com.example.service.SidebarService::class.java)
                                androidx.core.content.ContextCompat.startForegroundService(this@MainActivity, svcIntent)
                            }
                            val settingsIntent = Intent(this@MainActivity, SettingsActivity::class.java)
                            startActivity(settingsIntent)
                            finish()"""
content = content.replace(old_welcome, new_welcome)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
