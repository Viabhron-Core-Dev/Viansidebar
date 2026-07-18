import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

target = """    private fun launchCropActivity(bitmap: Bitmap) {
        try {
            val cacheFile = java.io.File(cacheDir, "temp_qr_screenshot.png")
            java.io.FileOutputStream(cacheFile).use { out ->
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            val intent = Intent(this, QRCropActivity::class.java).apply {
                putExtra("IMAGE_PATH", cacheFile.absolutePath)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            startActivity(intent)
        } catch (e: Exception) {
            e.printStackTrace()
            Handler(Looper.getMainLooper()).post {
                Toast.makeText(this, "Failed to prepare screenshot", Toast.LENGTH_SHORT).show()
            }
        }
    }"""

replacement = """    private fun launchCropActivity(bitmap: Bitmap) {
        Thread {
            try {
                val cacheFile = java.io.File(cacheDir, "temp_qr_screenshot.png")
                java.io.FileOutputStream(cacheFile).use { out ->
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
                }
                val intent = Intent(this@VianSideAccessibilityService, QRCropActivity::class.java).apply {
                    putExtra("IMAGE_PATH", cacheFile.absolutePath)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(intent)
            } catch (e: Exception) {
                e.printStackTrace()
                Handler(Looper.getMainLooper()).post {
                    Toast.makeText(this@VianSideAccessibilityService, "Failed to prepare screenshot", Toast.LENGTH_SHORT).show()
                }
            }
        }.start()
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
    f.write(content)
