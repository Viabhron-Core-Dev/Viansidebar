import re

with open("app/src/main/java/com/example/WelcomeScreen.kt", "r") as f:
    content = f.read()

content = content.replace('Text("Continue to Settings", style = MaterialTheme.typography.titleMedium)', 'Text(if (isFirstLaunch) "Continue to Settings" else "Back", style = MaterialTheme.typography.titleMedium)')

with open("app/src/main/java/com/example/WelcomeScreen.kt", "w") as f:
    f.write(content)
