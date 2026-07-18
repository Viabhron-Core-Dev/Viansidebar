import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onDestroy() {
        super.onDestroy()
        tempImagePath?.let { path ->
            try {
                val file = File(path)
                if (file.exists()) {
                    file.delete()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

replacement = """    override fun onDestroy() {
        super.onDestroy()
        tempImagePath?.let { path ->
            try {
                val file = File(path)
                if (file.exists()) {
                    file.delete()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        
        try {
            val cacheFiles = cacheDir.listFiles { _, name -> name.startsWith("shared_crop_") }
            cacheFiles?.forEach { file ->
                if (file.lastModified() < System.currentTimeMillis() - 60 * 60 * 1000) { // 1 hour old
                    file.delete()
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
