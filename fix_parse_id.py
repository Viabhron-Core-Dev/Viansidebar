import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# I need to fix the first one (around line 403) to use return
parse_id_fix = """                    if (jsonStr != null && jsonStr.isNotEmpty()) {
                        val json = org.json.JSONObject(jsonStr)
                        label = json.optString("label", label)
                    }
                    return SidebarItem.Widget(widgetId, label)
                }
            } catch (e: Exception) {"""

content = re.sub(r'if \(jsonStr != null && jsonStr\.isNotEmpty\(\)\) \{\s*val json = org\.json\.JSONObject\(jsonStr\)\s*label = json\.optString\("label", label\)\s*\}\s*result\.add\(SidebarItem\.Widget\(widgetId, label\)\)\s*\}\s*\} catch \(e: Exception\) \{', parse_id_fix, content, count=1)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)

