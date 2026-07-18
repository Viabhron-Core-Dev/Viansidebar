import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """                    QRCropScreen(
                        bitmap = bitmap,
                        onScan = { x, y, width, height ->
                            scanCroppedArea(bitmap, x, y, width, height)
                        },
                        onClose = { finish() }
                    )"""

replacement = """                    QRCropScreen(
                        bitmap = bitmap,
                        onAction = { action, x, y, width, height ->
                            if (action == "scan") {
                                scanCroppedArea(bitmap, x, y, width, height)
                            } else if (action == "share") {
                                shareCroppedArea(bitmap, x, y, width, height)
                            }
                        },
                        onClose = { finish() }
                    )"""
content = content.replace(target, replacement)

target_scan = """    private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {"""

replacement_scan = """    private fun shareCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {
        val cropX = maxOf(0, x.toInt())
        val cropY = maxOf(0, y.toInt())
        val cropW = minOf(bitmap.width - cropX, w.toInt())
        val cropH = minOf(bitmap.height - cropY, h.toInt())
        if (cropW <= 0 || cropH <= 0) {
            Toast.makeText(this, "Invalid crop area", Toast.LENGTH_SHORT).show()
            return
        }
        try {
            val croppedBitmap = Bitmap.createBitmap(bitmap, cropX, cropY, cropW, cropH)
            val cacheFile = java.io.File(cacheDir, "shared_crop_${System.currentTimeMillis()}.png")
            java.io.FileOutputStream(cacheFile).use { out ->
                croppedBitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            val uri = androidx.core.content.FileProvider.getUriForFile(this, "${packageName}.provider", cacheFile)
            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            startActivity(Intent.createChooser(shareIntent, "Share Image"))
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error sharing image", Toast.LENGTH_SHORT).show()
        }
    }

    private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {"""
content = content.replace(target_scan, replacement_scan)

target_screen = """fun QRCropScreen(bitmap: Bitmap, onScan: (Float, Float, Float, Float) -> Unit, onClose: () -> Unit) {"""
replacement_screen = """fun QRCropScreen(bitmap: Bitmap, onAction: (String, Float, Float, Float, Float) -> Unit, onClose: () -> Unit) {"""
content = content.replace(target_screen, replacement_screen)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
