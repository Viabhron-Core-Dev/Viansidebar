import re

with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("fun SidebarSettingsScreen(onBack: () -> Unit) {", "fun SidebarSettingsScreen(handleId: String, onBack: () -> Unit) {")

# We also need to fix default index to be per-handle?
# The user wants "different Sidebars not same". Default index should also be per handle!
# Let's see if we should update PageManager.getDefaultPageIndex to take handleId.
# We will do that next.

content = content.replace("PageManager.getPages(prefs)", "PageManager.getPages(prefs, handleId)")
content = content.replace("PageManager.savePages(prefs, pages)", "PageManager.savePages(prefs, handleId, pages)")
content = content.replace("PageManager.getDefaultPageIndex(prefs)", "PageManager.getDefaultPageIndex(prefs, handleId)")
content = content.replace("PageManager.setDefaultPageIndex(prefs, newIndex)", "PageManager.setDefaultPageIndex(prefs, handleId, newIndex)")

with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "w") as f:
    f.write(content)
