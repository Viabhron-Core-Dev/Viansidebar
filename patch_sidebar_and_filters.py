import re

# 1. SidebarView.kt
with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

content = content.replace('"calculator", "compass", "notification", "scheduler", "reader" -> false', '"calculator", "compass", "notifications", "scheduler", "reader" -> false')
content = content.replace('"notification", "scheduler", "reader" -> 500', '"notifications", "scheduler", "reader" -> 650')
content = content.replace('"calculator", "compass", "notification", "scheduler", "reader" -> 320', '"calculator", "compass", "notifications", "scheduler", "reader" -> 360')

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)

# 2. NotificationPageView.kt
with open("app/src/main/java/com/example/service/NotificationPageView.kt", "r") as f:
    content = f.read()

target_list = """                    val pm = context.packageManager
                    val appsInList = notifications.map { it.packageName to 
                        try { pm.getApplicationLabel(pm.getApplicationInfo(it.packageName, 0)).toString() } 
                        catch(e: Exception) { it.packageName }
                    }.distinctBy { it.first }"""

replacement_list = """                    val pm = context.packageManager
                    val appsInList = remember {
                        val intent = android.content.Intent(android.content.Intent.ACTION_MAIN, null).apply {
                            addCategory(android.content.Intent.CATEGORY_LAUNCHER)
                        }
                        pm.queryIntentActivities(intent, 0).map { 
                            it.activityInfo.packageName to it.loadLabel(pm).toString()
                        }.distinctBy { it.first }.sortedBy { it.second }
                    }"""

content = content.replace(target_list, replacement_list)

with open("app/src/main/java/com/example/service/NotificationPageView.kt", "w") as f:
    f.write(content)

# 3. NotificationHistoryActivity.kt
with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "r") as f:
    content = f.read()

target_history_list = """                        val pm = context.packageManager
                        val appsInHistory = history.map { it.packageName to it.appName }.distinctBy { it.first }"""

replacement_history_list = """                        val pm = context.packageManager
                        val appsInHistory = remember {
                            val intent = android.content.Intent(android.content.Intent.ACTION_MAIN, null).apply {
                                addCategory(android.content.Intent.CATEGORY_LAUNCHER)
                            }
                            pm.queryIntentActivities(intent, 0).map { 
                                it.activityInfo.packageName to it.loadLabel(pm).toString()
                            }.distinctBy { it.first }.sortedBy { it.second }
                        }"""

content = content.replace(target_history_list, replacement_history_list)

with open("app/src/main/java/com/example/NotificationHistoryActivity.kt", "w") as f:
    f.write(content)

