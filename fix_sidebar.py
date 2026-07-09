import re

with open('app/src/main/java/com/example/service/SidebarView.kt', 'r') as f:
    content = f.read()

sidebar_check = """                    updatePageStyles(pageConfig, page.getCurrentHeightPx())
                } else if (page is NotificationPageView) {
                    updatePageStyles(pageConfig, page.getCurrentHeightPx())
                } else if (page is WidgetPageView) {
                    updatePageStyles(pageConfig, page.getCurrentHeightPx())
                } else if (page != null) {"""

content = content.replace("""                    updatePageStyles(pageConfig, page.getCurrentHeightPx())
                } else if (page is NotificationPageView) {
                    updatePageStyles(pageConfig, page.getCurrentHeightPx())
                } else if (page != null) {""", sidebar_check)

with open('app/src/main/java/com/example/service/SidebarView.kt', 'w') as f:
    f.write(content)

