import re

# Fix SidebarView.kt
with open('app/src/main/java/com/example/service/SidebarView.kt', 'r') as f:
    content = f.read()

old_styles = """        val wrapContent = if (pageConfig?.useCustomSettings == true) pageConfig.wrapContentHeight else prefs.getBoolean("sidebar_wrap_content", true)
        val prefHeight = if (pageConfig?.useCustomSettings == true) pageConfig.height else prefs.getInt("sidebar_height", 450)
        val prefWidth = if (pageConfig?.useCustomSettings == true) pageConfig.width else prefs.getInt("sidebar_width", 320)
        val opacity = if (pageConfig?.useCustomSettings == true) pageConfig.transparency else prefs.getFloat("sidebar_transparency", 0.9f)"""

new_styles = """        val globalWrap = prefs.getBoolean("sidebar_wrap_content", true)
        val globalHeight = prefs.getInt("sidebar_height", 450)
        val globalWidth = prefs.getInt("sidebar_width", 320)
        
        val wrapContent = if (pageConfig?.useCustomSettings == true) pageConfig.wrapContentHeight else {
            when (pageConfig?.type) {
                "calculator", "compass", "notification", "scheduler", "reader" -> false
                else -> globalWrap
            }
        }
        val prefHeight = if (pageConfig?.useCustomSettings == true) pageConfig.height else {
            when (pageConfig?.type) {
                "calculator" -> 450
                "compass" -> 400
                "notification", "scheduler", "reader" -> 500
                else -> globalHeight
            }
        }
        val prefWidth = if (pageConfig?.useCustomSettings == true) pageConfig.width else {
            when (pageConfig?.type) {
                "calculator", "compass", "notification", "scheduler", "reader" -> 320
                else -> globalWidth
            }
        }
        val opacity = if (pageConfig?.useCustomSettings == true) pageConfig.transparency else prefs.getFloat("sidebar_transparency", 0.9f)"""

content = content.replace(old_styles, new_styles)

with open('app/src/main/java/com/example/service/SidebarView.kt', 'w') as f:
    f.write(content)

# Fix PageManager.kt SidebarPage data class
with open('app/src/main/java/com/example/utils/PageManager.kt', 'r') as f:
    content = f.read()

old_companion = """    companion object {
        fun fromJson(obj: JSONObject): SidebarPage {"""

new_companion = """    companion object {
        fun createDefault(id: String, type: String, title: String): SidebarPage {
            val wrap = when(type) { "calculator", "compass", "notification", "scheduler", "reader" -> false else -> true }
            val h = when(type) { "calculator" -> 450; "compass" -> 400; "notification", "scheduler", "reader" -> 500; else -> 450 }
            return SidebarPage(
                id = id, type = type, title = title,
                wrapContentHeight = wrap, height = h, width = 320
            )
        }
        
        fun fromJson(obj: JSONObject): SidebarPage {"""

content = content.replace(old_companion, new_companion)

with open('app/src/main/java/com/example/utils/PageManager.kt', 'w') as f:
    f.write(content)

# Fix PageManagementSettingsScreen.kt
with open('app/src/main/java/com/example/PageManagementSettingsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('newPages.add(SidebarPage(id = UUID.randomUUID().toString(), type = type, title = title))', 
                          'newPages.add(SidebarPage.createDefault(id = UUID.randomUUID().toString(), type = type, title = title))')

with open('app/src/main/java/com/example/PageManagementSettingsScreen.kt', 'w') as f:
    f.write(content)

