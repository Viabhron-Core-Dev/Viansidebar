with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target_oncreate = "    override fun onCreate(savedInstanceState: Bundle?) {"
replacement_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Cleanup old shared crop images
        Thread {
            try {
                cacheDir.listFiles()?.forEach { file ->
                    if (file.name.startsWith("shared_crop_") && file.name.endsWith(".jpg")) {
                        file.delete()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
"""
content = content.replace(target_oncreate, replacement_oncreate)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
