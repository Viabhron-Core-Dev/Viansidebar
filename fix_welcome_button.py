with open('app/src/main/java/com/example/WelcomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('Button(\n        Button(', 'Button(')

with open('app/src/main/java/com/example/WelcomeScreen.kt', 'w') as f:
    f.write(content)

print("Fixed WelcomeScreen.kt")
