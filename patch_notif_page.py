with open("app/src/main/java/com/example/service/NotificationPageView.kt", "r") as f:
    content = f.read()

content = content.replace("AppNotificationListener.ACTION_NOTIFICATION_POSTED", "AppNotificationListener.Companion.ACTION_NOTIFICATION_POSTED")
content = content.replace("AppNotificationListener.ACTION_NOTIFICATION_REMOVED", "AppNotificationListener.Companion.ACTION_NOTIFICATION_REMOVED")
content = content.replace("AppNotificationListener.ACTION_CLEAR_ALL", "AppNotificationListener.Companion.ACTION_CLEAR_ALL")

with open("app/src/main/java/com/example/service/NotificationPageView.kt", "w") as f:
    f.write(content)
