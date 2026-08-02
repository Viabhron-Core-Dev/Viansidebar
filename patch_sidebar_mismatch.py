with open("app/src/main/java/com/example/service/SidebarService.kt", "r") as f:
    content = f.read()

content = content.replace("p = NotificationPageView(this, { closeSidebar() }) { newHeight ->\n                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {\n                            sidebarView?.updatePageStyles(config, newHeight)\n                        }\n                    }", "p = NotificationPageView(this, { closeSidebar() }, { _ -> })")
content = content.replace("p = AppTrackerPageView(this, { closeSidebar() }) { newHeight ->\n                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {\n                            sidebarView?.updatePageStyles(config, newHeight)\n                        }\n                    }", "p = AppTrackerPageView(this, { closeSidebar() }, { _ -> })")

with open("app/src/main/java/com/example/service/SidebarService.kt", "w") as f:
    f.write(content)
