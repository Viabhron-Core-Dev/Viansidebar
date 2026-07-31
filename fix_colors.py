import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    replacement = """        val colorInt = try {
            val c = prefs.all["${prefix}color"]
            when (c) {
                is Int -> c
                is String -> android.graphics.Color.parseColor(c)
                else -> android.graphics.Color.GRAY
            }
        } catch(e: Exception) { android.graphics.Color.GRAY }"""

    content = re.sub(r'        val colorInt = prefs\.getInt\("\$\{prefix\}color", android\.graphics\.Color\.GRAY\)', replacement, content)
    with open(path, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/service/TriggerHandleView.kt')
fix_file('app/src/main/java/com/example/service/ReaderHandleView.kt')
