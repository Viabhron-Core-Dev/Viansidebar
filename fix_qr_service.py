import re

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'r') as f:
    content = f.read()

old_scan_func = """    private fun scanBitmapForQRCode(bitmap: Bitmap) {
        Thread {
            try {
                val width = bitmap.width
                val height = bitmap.height
                val pixels = IntArray(width * height)
                bitmap.getPixels(pixels, 0, width, 0, 0, width, height)
                
                val source = com.google.zxing.RGBLuminanceSource(width, height, pixels)
                val binaryBitmap = com.google.zxing.BinaryBitmap(com.google.zxing.common.HybridBinarizer(source))
                
                val reader = com.google.zxing.MultiFormatReader()
                val result = reader.decode(binaryBitmap)
                
                val text = result.text
                if (text.isNullOrEmpty()) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(this, "No QR Code found", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(this, "QR Code found!", Toast.LENGTH_SHORT).show()
                        val intent = Intent(Intent.ACTION_SEND).apply {
                            type = "text/plain"
                            putExtra(Intent.EXTRA_TEXT, text)
                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        }
                        val chooser = Intent.createChooser(intent, "QR Code Result")
                        chooser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        startActivity(chooser)
                    }
                }
            } catch (e: Exception) {
                Handler(Looper.getMainLooper()).post {
                    Toast.makeText(this, "No QR Code found", Toast.LENGTH_SHORT).show()
                }
            }
        }.start()
    }"""

new_scan_func = """    private fun scanBitmapForQRCode(bitmap: Bitmap) {
        try {
            val cacheFile = File(cacheDir, "qr_screenshot.png")
            java.io.FileOutputStream(cacheFile).use { out ->
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            val intent = Intent(this, com.example.service.QRCropActivity::class.java).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                putExtra("IMAGE_PATH", cacheFile.absolutePath)
            }
            startActivity(intent)
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Failed to prepare QR scan", Toast.LENGTH_SHORT).show()
        }
    }"""

content = content.replace(old_scan_func, new_scan_func)

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'w') as f:
    f.write(content)

