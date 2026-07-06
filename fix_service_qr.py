import re

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'r') as f:
    content = f.read()

old_action = """        if (action == "screenshot") {
            handleScreenshotWithDelay()
            return true
        }"""

new_action = """        if (action == "screenshot") {
            handleScreenshotWithDelay()
            return true
        }
        if (action == "qr_scan") {
            handleQRScan()
            return true
        }"""
content = content.replace(old_action, new_action)

new_methods = """
    private fun handleQRScan() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Toast.makeText(this, "Scanning for QR Code...", Toast.LENGTH_SHORT).show()
            takeScreenshot(android.view.Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {
                override fun onSuccess(screenshotResult: ScreenshotResult) {
                    try {
                        val hwBuffer = screenshotResult.hardwareBuffer
                        val colorSpace = screenshotResult.colorSpace
                        val bitmap = Bitmap.wrapHardwareBuffer(hwBuffer, colorSpace)
                        if (bitmap != null) {
                            val softwareBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, false)
                            scanBitmapForQRCode(softwareBitmap)
                        } else {
                            Handler(Looper.getMainLooper()).post {
                                Toast.makeText(this@VianSideAccessibilityService, "Failed to get screenshot", Toast.LENGTH_SHORT).show()
                            }
                        }
                        hwBuffer.close()
                    } catch (e: Exception) {
                        e.printStackTrace()
                        Handler(Looper.getMainLooper()).post {
                            Toast.makeText(this@VianSideAccessibilityService, "Error reading screenshot", Toast.LENGTH_SHORT).show()
                        }
                    }
                }

                override fun onFailure(errorCode: Int) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(this@VianSideAccessibilityService, "Failed to take screenshot", Toast.LENGTH_SHORT).show()
                    }
                }
            })
        } else {
            Toast.makeText(this, "Screen QR Scanner requires Android 11+", Toast.LENGTH_LONG).show()
        }
    }

    private fun scanBitmapForQRCode(bitmap: Bitmap) {
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
            } catch (e: com.google.zxing.NotFoundException) {
                Handler(Looper.getMainLooper()).post {
                    Toast.makeText(this, "No QR Code found on screen", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                e.printStackTrace()
                Handler(Looper.getMainLooper()).post {
                    Toast.makeText(this, "Error scanning QR Code", Toast.LENGTH_SHORT).show()
                }
            }
        }.start()
    }
"""
content = content.replace('    companion object {', new_methods + '\n    companion object {')

with open('app/src/main/java/com/example/service/VianSideAccessibilityService.kt', 'w') as f:
    f.write(content)
