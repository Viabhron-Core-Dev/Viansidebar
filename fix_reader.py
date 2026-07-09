import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

widget_handling = """                "notifications" -> {
                    var p: NotificationPageView? = null
                    p = NotificationPageView(this, onCloseSidebar = { closeSidebar() }) { newHeight ->
                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }
                "widget" -> {
                    var p: WidgetPageView? = null
                    p = WidgetPageView(this, config.id) { newHeight ->
                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }"""

content = content.replace("""                "notifications" -> {
                    var p: NotificationPageView? = null
                    p = NotificationPageView(this, onCloseSidebar = { closeSidebar() }) { newHeight ->
                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }""", widget_handling)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)

