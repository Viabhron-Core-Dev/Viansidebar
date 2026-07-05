import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

# Fix constructor
old_constructor = """class AppsPageView(
    context: Context,
    private val manager: SidebarAppsManager,
    private val serviceScope: CoroutineScope,"""
new_constructor = """class AppsPageView(
    context: Context,
    private val pageConfig: com.example.utils.SidebarPage?,
    private val manager: SidebarAppsManager,
    private val serviceScope: CoroutineScope,"""
content = content.replace(old_constructor, new_constructor)

# Fix columns
old_columns = """val columns = prefs.getInt("sidebar_columns", 4)"""
new_columns = """val columns = if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else prefs.getInt("sidebar_columns", 4)"""
content = content.replace(old_columns, new_columns)

# Fix maxCols
old_maxcols = """val maxCols = if (folder.popupColumns > 0) folder.popupColumns else prefs.getInt("sidebar_columns", 4)"""
new_maxcols = """val maxCols = if (folder.popupColumns > 0) folder.popupColumns else (if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else prefs.getInt("sidebar_columns", 4))"""
content = content.replace(old_maxcols, new_maxcols)

# Fix popupOpacity
old_popupopacity = """val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)"""
new_popupopacity = """val popupOpacity = if (pageConfig?.useCustomSettings == true) pageConfig.transparency else prefs.getFloat("sidebar_transparency", 0.9f)"""
content = content.replace(old_popupopacity, new_popupopacity)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
