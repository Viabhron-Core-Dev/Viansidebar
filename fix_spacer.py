with open('app/src/main/java/com/example/WelcomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('        Spacer(modifier = Modifier.height(32.dp))\n\n        PermissionItem(\n            title = "Accessibility Access"', '        Spacer(modifier = Modifier.height(12.dp))\n\n        PermissionItem(\n            title = "Accessibility Access"')
content = content.replace('        )\n        Spacer(modifier = Modifier.height(12.dp))\n        \n        Button(', '        )\n        Spacer(modifier = Modifier.height(32.dp))\n        \n        Button(')

with open('app/src/main/java/com/example/WelcomeScreen.kt', 'w') as f:
    f.write(content)

print("Fixed Spacers.")
