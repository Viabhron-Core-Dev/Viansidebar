import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """class QRCropActivity : ComponentActivity() {"""

replacement = """class QRCropActivity : ComponentActivity() {
    private var tempImagePath: String? = null

    override fun onDestroy() {
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
    }
"""

content = content.replace(target, replacement)

target2 = """        val imagePath = intent.getStringExtra("IMAGE_PATH")"""
replacement2 = """        val imagePath = intent.getStringExtra("IMAGE_PATH")
        tempImagePath = imagePath"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
