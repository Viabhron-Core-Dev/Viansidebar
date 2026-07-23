with open("app/src/main/java/com/example/service/ScreenRecordService.kt", "r") as f:
    content = f.read()

content = content.replace("e.printStackTrace()\\n            Toast.makeText(this, \\\"Failed to start recording\\\", Toast.LENGTH_SHORT).show()",
                          "e.printStackTrace()\\n            com.example.LogKeeper.writeLog(\\\"ScreenRecord\\\", \\\"Start failed: ${e.message}\\\")\\n            Toast.makeText(this, \\\"Failed to start recording\\\", Toast.LENGTH_SHORT).show()")

content = content.replace("e.printStackTrace()\\n            Handler(Looper.getMainLooper()).post {\\n                Toast.makeText(this, \\\"Failed to save recording\\\", Toast.LENGTH_SHORT).show()\\n            }",
                          "e.printStackTrace()\\n            com.example.LogKeeper.writeLog(\\\"ScreenRecord\\\", \\\"Save failed: ${e.message}\\\")\\n            Handler(Looper.getMainLooper()).post {\\n                Toast.makeText(this, \\\"Failed to save recording\\\", Toast.LENGTH_SHORT).show()\\n            }")

with open("app/src/main/java/com/example/service/ScreenRecordService.kt", "w") as f:
    f.write(content)
