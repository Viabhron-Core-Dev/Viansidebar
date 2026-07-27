import re

with open("app/src/main/java/com/example/WelcomeScreen.kt", "r") as f:
    content = f.read()

content = content.replace("fun WelcomeScreen(onContinue: () -> Unit) {", "fun WelcomeScreen(onContinue: () -> Unit, isFirstLaunch: Boolean = true) {")
content = content.replace('text = "Welcome to LiteReader",', 'text = if (isFirstLaunch) "Welcome to LiteReader" else "Permissions Manager",')

with open("app/src/main/java/com/example/WelcomeScreen.kt", "w") as f:
    f.write(content)
