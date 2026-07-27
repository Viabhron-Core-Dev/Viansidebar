import re

with open("app/src/main/java/com/example/SettingsActivity.kt", "r") as f:
    content = f.read()

target = """                "screencap" -> ScreenCapSettingsScreen(
                    onBack = { currentRoute = "main" }
                )
            }"""

replacement = """                "screencap" -> ScreenCapSettingsScreen(
                    onBack = { currentRoute = "main" }
                )
                "permissions" -> WelcomeScreen(
                    onContinue = { currentRoute = "main" },
                    isFirstLaunch = false
                )
            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/SettingsActivity.kt", "w") as f:
    f.write(content)
