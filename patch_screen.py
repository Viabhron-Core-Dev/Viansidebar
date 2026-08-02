with open("app/src/main/java/com/example/HandleEditScreen.kt", "r") as f:
    content = f.read()

content = content.replace('listOf("triangle", "rectangle", "half_oval", "rounded_rect").forEach { s ->', 'listOf("triangle", "rectangle", "half_oval", "rounded_rect", "slanted_block").forEach { s ->')

with open("app/src/main/java/com/example/HandleEditScreen.kt", "w") as f:
    f.write(content)
