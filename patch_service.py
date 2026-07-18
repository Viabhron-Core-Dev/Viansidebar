import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

target = """    private fun handleQRScan() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Toast.makeText(this, "Scanning for QR Code...", Toast.LENGTH_SHORT).show()
            Handler(Looper.getMainLooper()).postDelayed({
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
            }, 400) // Delay to let sidebar close
        } else {
            Toast.makeText(this, "Screen QR Scanner requires Android 11+", Toast.LENGTH_LONG).show()
        }
    }

    private fun scanBitmapForQRCode(bitmap: Bitmap) {"""

replacement = """    private fun handleQRScan() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Toast.makeText(this, "Preparing Screen Capture...", Toast.LENGTH_SHORT).show()
            Handler(Looper.getMainLooper()).postDelayed({
                takeScreenshot(android.view.Display.DEFAULT_DISPLAY, mainExecutor, object : TakeScreenshotCallback {
                override fun onSuccess(screenshotResult: ScreenshotResult) {
                    try {
                        val hwBuffer = screenshotResult.hardwareBuffer
                        val colorSpace = screenshotResult.colorSpace
                        val bitmap = Bitmap.wrapHardwareBuffer(hwBuffer, colorSpace)
                        if (bitmap != null) {
                            val softwareBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, false)
                            launchCropActivity(softwareBitmap)
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
            }, 400) // Delay to let sidebar close
        } else {
            Toast.makeText(this, "Screen QR Scanner requires Android 11+", Toast.LENGTH_LONG).show()
        }
    }

    private fun launchCropActivity(bitmap: Bitmap) {
        try {
            val cacheFile = java.io.File(cacheDir, "temp_qr_screenshot.png")
            java.io.FileOutputStream(cacheFile).use { out ->
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, out)
            }
            val intent = Intent(this, QRCropActivity::class.java).apply {
                putExtra("image_path", cacheFile.absolutePath)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            startActivity(intent)
        } catch (e: Exception) {
            e.printStackTrace()
            Handler(Looper.getMainLooper()).post {
                Toast.makeText(this, "Failed to prepare screenshot", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun scanBitmapForQRCode(bitmap: Bitmap) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
    f.write(content)
