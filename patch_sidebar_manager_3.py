import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        } else if (id.startsWith("spacer:")) {
            try {
                val parts = id.split(":", limit = 3)
                val uuid = parts[1]
                val height = if (parts.size > 2) parts[2].toIntOrNull() ?: 50 else 50
                return SidebarItem.Spacer(uuid, height, id)"""

replacement = """        } else if (id.startsWith("spacer:")) {
            try {
                val parts = id.split(":", limit = 3)
                val uuid = parts[1]
                val spacerDataStr = if (parts.size > 2) parts[2] else "{}"
                var height = 50
                try {
                    val obj = org.json.JSONObject(spacerDataStr)
                    height = obj.optInt("heightDp", 50)
                } catch(e: Exception) {
                    height = spacerDataStr.toIntOrNull() ?: 50
                }
                return SidebarItem.Spacer(uuid, height, id)"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
