import os
import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace(
'''    fun showWidgetsGridEditOverlay(pageId: String) {
        lastWidgetsGridPageId = pageId
        val intent = android.content.Intent(this, com.example.WidgetsGridEditActivity::class.java).apply {
            putExtra("PAGE_ID", pageId)
            addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        startActivity(intent)
    }''',
'''    fun showWidgetsGridEditOverlay(pageId: String) {
        lastWidgetsGridPageId = pageId
        val intent = android.content.Intent(this, com.example.WidgetsGridEditActivity::class.java).apply {
            putExtra("PAGE_ID", pageId)
            addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        startActivity(intent)
    }

    fun showHybridGridEditOverlay(pageId: String) {
        val intent = android.content.Intent(this, com.example.HybridGridEditActivity::class.java).apply {
            putExtra("PAGE_ID", pageId)
            addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        startActivity(intent)
    }''')

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
