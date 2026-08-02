with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("AppTrackerPageView(this, { standaloneSidebarView?.close() }) { newHeight ->\n                standaloneSidebarView?.updatePageStyles(config, newHeight)\n            }", "AppTrackerPageView(this, { standaloneSidebarView?.close() }, { _ -> })")
content = content.replace("\"notifications\" -> NotificationPageView(this, { standaloneSidebarView?.close() }) { newHeight ->\n                standaloneSidebarView?.updatePageStyles(config, newHeight)\n            }", "\"notifications\" -> NotificationPageView(this, { standaloneSidebarView?.close() }, { _ -> })")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)
