import re

with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "r") as f:
    content = f.read()

content = content.replace("FloatingReaderService.instance?.openSidebarPage(pageType)", 'FloatingReaderService.instance?.openSidebarPage("sidebar", pageType)')

with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "w") as f:
    f.write(content)

# For PageManagementSettingsScreen, it seems obsolete, but I'll fix it anyway to compile.
with open("app/src/main/java/com/example/PageManagementSettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("PageManager.getPages(prefs)", 'PageManager.getPages(prefs, "sidebar")')
content = content.replace("PageManager.getDefaultPageIndex(prefs)", 'PageManager.getDefaultPageIndex(prefs, "sidebar")')
content = content.replace("PageManager.savePages(prefs, pages)", 'PageManager.savePages(prefs, "sidebar", pages)')
content = content.replace("PageManager.savePages(prefs, newPages)", 'PageManager.savePages(prefs, "sidebar", newPages)')
content = content.replace("PageManager.saveDefaultPageIndex(prefs, defaultIndex)", 'PageManager.saveDefaultPageIndex(prefs, "sidebar", defaultIndex)')

with open("app/src/main/java/com/example/PageManagementSettingsScreen.kt", "w") as f:
    f.write(content)
