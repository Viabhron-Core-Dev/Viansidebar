import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

pattern = """                IconButton\\(onClick = \\{ 
                    val intent = Intent\\(context, NotificationHistoryActivity::class\\.java\\)\\.apply \\{
                        flags = Intent\\.FLAG_ACTIVITY_NEW_TASK
                    \\}
                    context\\.startActivity\\(intent\\)
                \\}\\) \\{"""

replacement = """                IconButton(onClick = { 
                    val intent = Intent(context, NotificationHistoryActivity::class.java).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK
                    }
                    context.startActivity(intent)
                    onCloseSidebar()
                }) {"""

content = re.sub(pattern, replacement, content)

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)
