with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "r") as f:
    content = f.read()

content = content.replace("(context as? FloatingReaderService)?.removePwaWindow(pwa.id)", "(context as? SidebarService)?.removePwaWindow(pwa.id)")

with open("app/src/main/java/com/example/service/PwaWindowManager.kt", "w") as f:
    f.write(content)
