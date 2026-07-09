import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("fun NotificationScreen(context: Context) {", "fun NotificationScreen(context: Context, onCloseSidebar: () -> Unit) {")
content = content.replace("NotificationScreen(context)", "NotificationScreen(context, myCloseSidebar)")
content = content.replace("onCloseSidebar = myCloseSidebar", "onCloseSidebar = onCloseSidebar")
content = content.replace("val myCloseSidebar: () -> Unit,", "private val onCloseSidebar: () -> Unit,")
content = content.replace("NotificationScreen(context, myCloseSidebar)", "NotificationScreen(context, onCloseSidebar)")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)

