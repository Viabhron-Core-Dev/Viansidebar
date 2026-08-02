with open("app/src/main/java/com/example/service/PageWindowService.kt", "r") as f:
    content = f.read()

content = content.replace("val window = PageWindowManager(this, pageType)", "val window = PageWindowManager(this, pageType) { windows.remove(pageType) }")

with open("app/src/main/java/com/example/service/PageWindowService.kt", "w") as f:
    f.write(content)
