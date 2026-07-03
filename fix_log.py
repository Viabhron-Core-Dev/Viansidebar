import re
with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

new_catch = """} catch (e: Exception) { 
                    com.example.LogKeeper.writeLog("SidebarAppsManager", "Error parsing folder id: $id - ${e.message}")
                    e.printStackTrace() 
                }"""

content = content.replace('} catch (e: Exception) { e.printStackTrace() }', new_catch)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
