with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("removePwaWindow(pwa.id)", "removePwaWindow(pwa.id.toInt())")
content = content.replace("removePwaWindow(id: String)", "removePwaWindow(id: Int)")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)
