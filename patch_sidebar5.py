with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("pageWindows[pageType]?.getCurrentHeightPx()", "pageWindows[pageType]?.height")

content = content.replace("pwaWindows.remove(id)", "pwaWindows.remove(id.toIntOrNull() ?: 0)")
content = content.replace("pwaWindows.remove(id: String)", "pwaWindows.remove(id: Int)")
content = content.replace("removePwaWindow(pwa.id)", "removePwaWindow(pwa.id.toIntOrNull() ?: 0)")
content = content.replace("removePwaWindow(pageType)", "removePwaWindow(pageType.toIntOrNull() ?: 0)")
content = content.replace("removePwaWindow(id: String)", "removePwaWindow(id: Int)")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("mediaPlayerView?.getCurrentHeightPx()", "mediaPlayerView?.height")

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content2)
