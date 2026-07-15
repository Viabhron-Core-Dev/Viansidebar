import sys

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """                "notifications" -> {
                    var p: NotificationPageView? = null
                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }"""

replacement = """                "notifications" -> {
                    var p: NotificationPageView? = null
                    p = NotificationPageView(this) { newHeight ->
                        if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
