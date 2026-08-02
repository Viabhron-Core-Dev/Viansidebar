with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("pageWindows[pageType]?.getCurrentHeightPx()", "pageWindows[pageType]?.height")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("mediaPlayerView?.getCurrentHeightPx()", "mediaPlayerView?.height")

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content2)
