import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

content = content.replace(
"""    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    private val recyclerView: RecyclerView""",
"""    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    private var columns: Int = 3
    private val recyclerView: RecyclerView"""
)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
