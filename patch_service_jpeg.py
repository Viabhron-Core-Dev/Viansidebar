import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

target = """                val cacheFile = java.io.File(cacheDir, "temp_qr_screenshot.png")
                java.io.FileOutputStream(cacheFile).use { out ->
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
                }"""

replacement = """                val cacheFile = java.io.File(cacheDir, "temp_qr_screenshot.jpg")
                java.io.FileOutputStream(cacheFile).use { out ->
                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out)
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
    f.write(content)
