import re

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("                            com.example.service.FloatingReaderService.instance?.toggleReader()", """                            if (com.example.service.FloatingReaderService.instance != null) {
                                com.example.service.FloatingReaderService.instance?.toggleReader()
                            } else {
                                val intent = android.content.Intent(context, com.example.service.FloatingReaderService::class.java)
                                intent.putExtra("UNFOLD", true)
                                androidx.core.content.ContextCompat.startForegroundService(context, intent)
                            }""")

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)
